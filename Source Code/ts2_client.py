"""
Toy Story 2: Buzz Lightyear to the Rescue - Archipelago BizHawk Client

ARCHITECTURE — two directions of data flow:

  GAME -> AP  (detection):  We MUST read game RAM to learn the player collected
              something in-level (coin counter, pickup ==5 flags, token byte,
              part-collected flags, boss screens, Rex dialog). The Lua writes
              these into our shared scratch addresses; the client reads them and
              sends LocationChecks. This is the only thing RAM reads are for.

  AP -> GAME  (projection): The AP server is the SOURCE OF TRUTH for what the
              player HAS (items_received) and what they have CHECKED
              (checked_locations). The client DERIVES the full state from those
              two and writes it to RAM authoritatively every frame, starting
              from zero — it never reads a value back from RAM and accumulates
              onto it. This makes boot garbage, stale values, and address
              collisions harmless: whatever is there gets overwritten with the
              correct value before the game reads it.

  Exception — DELIVERY QUEUES (traps, 1 Life, Extra Battery): these are pushed
              by the client and CONSUMED (decremented) by the Lua, so they can't
              be a pure projection. We track how many we've delivered in
              self._delivered (never read from RAM) and push only the new delta.
"""
from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Optional

from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient
from worlds._bizhawk import read, write, guarded_write

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

logger = logging.getLogger("Client")

# ============================================================
# GAME IDENTITY
# ============================================================
# PS1 game header bytes at ROM address 0x9C50 - "SCUS-94     " etc
# We validate by checking a known memory signature instead
GAME_NAME_ADDR    = (0x0A16A4, 4, "MainRAM")   # Should be 0x54532032 ("TS2\x00") in our shared area
VALIDATE_ADDR     = (0x1FFFD0, 1, "MainRAM")    # We write 0xAB here on init to confirm shared mem
SHARED_CONN_GEN   = (0x1FF96A, 1, "MainRAM")    # bumped each connect; Lua clears session state on change

# ============================================================
# SHARED MEMORY MAP
# ============================================================
# All addresses in MainRAM domain

# Core settings (written by client on connect)
SHARED_GAME_MODE           = (0x1FFFD1, 1, "MainRAM")  # 0=Open, 1=Linear
SHARED_BUNDLE_SIZE         = (0x1FFFD3, 1, "MainRAM")  # coin CHECKS bundle size
SHARED_RECV_BUNDLE_SIZE    = (0x1FFFD4, 1, "MainRAM")  # coin RECEIVED bundle size
SHARED_TOKEN_POOL          = (0x1FFFD5, 1, "MainRAM")  # total tokens in pool
SHARED_TICKETS_REQUIRED    = (0x1FFFD7, 1, "MainRAM")  # Prospector ticket gate (Open)

# Gates (Linear mode token thresholds)
SHARED_GATE_BOMBS_AWAY     = (0x1FFFD9, 1, "MainRAM")
SHARED_GATE_SLIME_TIME     = (0x1FFFDB, 1, "MainRAM")
SHARED_GATE_TOY_BARN       = (0x1FFFDD, 1, "MainRAM")
SHARED_GATE_ZURG           = (0x1FFFDF, 1, "MainRAM")
SHARED_GATE_PROSPECTOR     = (0x1FFFE1, 1, "MainRAM")

# Player state (read by client to check progress / written by client for received items)
SHARED_TOKENS_RECEIVED     = (0x1FFFE3, 1, "MainRAM")
SHARED_LEVEL_UNLOCKS_LOW   = (0x1FFFE5, 1, "MainRAM")  # bitmask levels 7-14
SHARED_LEVEL_UNLOCKS_HIGH  = (0x1FFFE7, 1, "MainRAM")  # bitmask levels 15-21
SHARED_TICKETS_RECEIVED    = (0x1FFFE9, 1, "MainRAM")
SHARED_LASER_LEVEL         = (0x1FFFEB, 1, "MainRAM")  # 0-3
SHARED_MOVE_UNLOCKS_LOW    = (0x1FFFED, 1, "MainRAM")  # bitmask bits 0-7
SHARED_MOVE_UNLOCKS_HIGH   = (0x1FFFEF, 1, "MainRAM")  # bit 0 = rope
SHARED_BOSS_DEFEATS        = (0x1FFFF2, 1, "MainRAM")  # bitmask

# Coinsanity DETECTION (Lua writes how many bundles collected in-level; client reads)
# Relocated to our clean scratch area (0x1FF971-0x1FF97A); the old 0x1FFFxx
# addresses sat in the game's high stack/system RAM and read garbage, firing
# every bundle on level entry.
SHARED_COINS_ANDYS_HOUSE        = (0x1FF971, 1, "MainRAM")
SHARED_COINS_NEIGHBORHOOD       = (0x1FF972, 1, "MainRAM")
SHARED_COINS_CONSTRUCTION       = (0x1FF973, 1, "MainRAM")
SHARED_COINS_ALLEYS             = (0x1FF974, 1, "MainRAM")
SHARED_COINS_TOY_BARN           = (0x1FF975, 1, "MainRAM")
SHARED_COINS_SPACE_LAND         = (0x1FF976, 1, "MainRAM")
SHARED_COINS_ELEVATOR           = (0x1FF977, 1, "MainRAM")
SHARED_COINS_PENTHOUSE          = (0x1FF978, 1, "MainRAM")
SHARED_COINS_AIRPORT            = (0x1FF979, 1, "MainRAM")
SHARED_COINS_TARMAC             = (0x1FF97A, 1, "MainRAM")

# Coin bundle ITEMS received (client writes count; Lua reads to grant coins to
# spend). These are SEPARATE from the coinsanity detection counters above so the
# two never feed back into each other.
SHARED_COIN_ITEM_ANDYS_HOUSE    = (0x1FF9E6, 1, "MainRAM")
SHARED_COIN_ITEM_NEIGHBORHOOD   = (0x1FF9E7, 1, "MainRAM")
SHARED_COIN_ITEM_CONSTRUCTION   = (0x1FF9E8, 1, "MainRAM")
SHARED_COIN_ITEM_ALLEYS         = (0x1FF9E9, 1, "MainRAM")
SHARED_COIN_ITEM_TOY_BARN       = (0x1FF9EA, 1, "MainRAM")
SHARED_COIN_ITEM_SPACE_LAND     = (0x1FF9EB, 1, "MainRAM")
SHARED_COIN_ITEM_ELEVATOR       = (0x1FF9EC, 1, "MainRAM")
SHARED_COIN_ITEM_PENTHOUSE      = (0x1FF9ED, 1, "MainRAM")
SHARED_COIN_ITEM_AIRPORT        = (0x1FF9EE, 1, "MainRAM")
SHARED_COIN_ITEM_TARMAC         = (0x1FF9EF, 1, "MainRAM")

# Hamm "50 Coins" check DONE per coin level (client writes 1 when that level's
# "Hamm's 50 Coins Token" location is in checked_locations). The Lua reads this to
# suppress the in-game "give Hamm 50 coins" prompt on revisits. Authoritative from
# checked_locations, so it persists across reconnects. Keyed by IN-GAME level id
# (the value the Lua reads from A.LEVEL), one byte each in the free 0x1FF96x region.
SHARED_HAMM_DONE = {
    1:  (0x1FF960, 1, "MainRAM"),   # Andy's House
    2:  (0x1FF961, 1, "MainRAM"),   # Andy's Neighborhood
    4:  (0x1FF962, 1, "MainRAM"),   # Construction Yard
    5:  (0x1FF963, 1, "MainRAM"),   # Alleys and Gullies
    7:  (0x1FF964, 1, "MainRAM"),   # Al's Toy Barn
    8:  (0x1FF965, 1, "MainRAM"),   # Al's Space Land
    10: (0x1FF966, 1, "MainRAM"),   # Elevator Hop
    11: (0x1FF967, 1, "MainRAM"),   # Al's Penthouse
    13: (0x1FF968, 1, "MainRAM"),   # Airport Infiltration
    14: (0x1FF969, 1, "MainRAM"),   # Tarmac Trouble
}
# Map in-game level id -> that level's Hamm location name (for checked_locations).
HAMM_LOC_BY_LEVEL = {
    1:  "Andy's House - Hamm's 50 Coins Token",
    2:  "Andy's Neighborhood - Hamm's 50 Coins Token",
    4:  "Construction Yard - Hamm's 50 Coins Token",
    5:  "Alleys and Gullies - Hamm's 50 Coins Token",
    7:  "Al's Toy Barn - Hamm's 50 Coins Token",
    8:  "Al's Space Land - Hamm's 50 Coins Token",
    10: "Elevator Hop - Hamm's 50 Coins Token",
    11: "Al's Penthouse - Hamm's 50 Coins Token",
    13: "Airport Infiltration - Hamm's 50 Coins Token",
    14: "Tarmac Trouble - Hamm's 50 Coins Token",
}

# Token checks collected, one byte per hover_id (7-21). Bits: 1=Hamm's 50 Coins,
# 2=Missing Toys, 4=Race, 8=Hidden, 16=Boss. Lua writes, client reads.
SHARED_TOKENS_COLLECTED = {
    7:  (0x1FF9F0, 1, "MainRAM"),
    8:  (0x1FF9F1, 1, "MainRAM"),
    9:  (0x1FF9F2, 1, "MainRAM"),
    10: (0x1FF9F3, 1, "MainRAM"),
    11: (0x1FF9F4, 1, "MainRAM"),
    12: (0x1FF9F5, 1, "MainRAM"),
    13: (0x1FF9F6, 1, "MainRAM"),
    14: (0x1FF9F7, 1, "MainRAM"),
    15: (0x1FF9F8, 1, "MainRAM"),
    16: (0x1FF9F9, 1, "MainRAM"),
    17: (0x1FF9FA, 1, "MainRAM"),
    18: (0x1FF9FB, 1, "MainRAM"),
    19: (0x1FF9FC, 1, "MainRAM"),
    20: (0x1FF9FD, 1, "MainRAM"),
    21: (0x1FF9FE, 1, "MainRAM"),
}

# Rex checks
SHARED_REX_LOW                  = (0x1FF9C4, 1, "MainRAM")
SHARED_REX_HIGH                 = (0x1FF9C5, 1, "MainRAM")
SHARED_REX_SEED_LOW             = (0x1FF97B, 1, "MainRAM")
SHARED_REX_SEED_HIGH            = (0x1FF97C, 1, "MainRAM")
# On-screen item feed buffer (safe scratch region, not the game-used 0x1FFFxx top)
FEED_SEQ_ADDR                   = (0x1FFA00, 1, "MainRAM")
FEED_TEXT_BASE                  = 0x1FFA01
# Lua bumps this counter on each debounced Select press; the client advances the
# feed mode (Off->Sent->Received->Both->Off) whenever the value changes.
FEED_CYCLE_ADDR                 = (0x1FF970, 1, "MainRAM")

# Prospector open mode unlock
SHARED_PROSPECTOR_UNLOCK        = (0x1FF9C6, 1, "MainRAM")

# ── DESPAWN SEEDS (server -> Lua, one direction only) ─────────────────────────
# The AP server is the source of truth for what's collected. Each tick the client
# derives the CURRENT level's collected mask from checked_locations and writes it
# to these dedicated "despawn seed" bytes. The Lua only READS them (to hide
# already-collected objects); it never writes them, and the client never reads
# them back — so unlike the SHARED_BATTERY/LIFE/etc. masks (which carry Lua->client
# fresh-collection reports) a stray bit here can never become a phantom check.
# This is the same one-direction seed pattern Rex/Potato Head already use, which
# is why those survive resets. Only the current level needs publishing (the Lua
# only acts on the level it's in), so 1 byte per category suffices.
SHARED_DESPAWN_BATTERY          = (0x1FF97F, 1, "MainRAM")
SHARED_DESPAWN_LIFE             = (0x1FF980, 1, "MainRAM")
SHARED_DESPAWN_LASER            = (0x1FF9C7, 1, "MainRAM")
SHARED_DESPAWN_TOY              = (0x1FF9FF, 1, "MainRAM")
# Part-collected seed: one bit per Potato-Head level indicating the "Missing X"
# pickup check is done. The Lua uses it to decide whether to keep re-spawning the
# world pickup (by clearing the gadget-unlock bit) — once collected, it stops.
# Bit order: 0=Andy's House(Ear/Shield), 1=Construction(Eye/Disc),
# 2=Al's Toy Barn(Arm/Rocket), 3=Elevator Hop(Foot/Grapple),
# 4=Airport(Mouth/Hover).
SHARED_DESPAWN_PART             = (0x1FF9C0, 1, "MainRAM")
# Part-exchanged seed: one bit per Potato-Head level indicating "Give Potato Head
# His X" is done. Same bit order as SHARED_DESPAWN_PART. Lets the Lua keep Potato
# Head in his post-gift state across resets without trusting the garbage-prone
# exchanged_flag RAM byte.
SHARED_DESPAWN_PART_EXCH        = (0x1FF9C1, 1, "MainRAM")

# Traps queue
SHARED_TRAP_NARROW_VISION       = (0x1FF981, 1, "MainRAM")
SHARED_TRAP_INVINCIBLE_ENEMIES  = (0x1FF982, 1, "MainRAM")
SHARED_TRAP_FREEZE_BUZZ         = (0x1FF983, 1, "MainRAM")
SHARED_TRAP_CUTSCENE            = (0x1FF984, 1, "MainRAM")
SHARED_TRAP_DAMAGE_BUZZ         = (0x1FF985, 1, "MainRAM")
SHARED_DEATH_LINK_QUEUE         = (0x1FF986, 1, "MainRAM")

# Filler items
SHARED_FILLER_EXTRA_LIFE        = (0x1FF987, 1, "MainRAM")
SHARED_FILLER_HEALTH_UP         = (0x1FF988, 1, "MainRAM")

# Mr. Potato Head parts collected flags
SHARED_EAR_COLLECTED            = (0x1FF989, 1, "MainRAM")
SHARED_EYE_COLLECTED            = (0x1FF98A, 1, "MainRAM")
SHARED_ARM_COLLECTED            = (0x1FF98B, 1, "MainRAM")
SHARED_FOOT_COLLECTED           = (0x1FF98C, 1, "MainRAM")
SHARED_MOUTH_COLLECTED          = (0x1FF98D, 1, "MainRAM")

# Mr. Potato Head parts received flags
SHARED_EAR_RECEIVED             = (0x1FF98E, 1, "MainRAM")
SHARED_EYE_RECEIVED             = (0x1FF98F, 1, "MainRAM")
SHARED_ARM_RECEIVED             = (0x1FF990, 1, "MainRAM")
SHARED_FOOT_RECEIVED            = (0x1FF991, 1, "MainRAM")
SHARED_MOUTH_RECEIVED           = (0x1FF992, 1, "MainRAM")

# Mr. Potato Head parts exchanged (turned in) flags
SHARED_EAR_EXCHANGED            = (0x1FF9E1, 1, "MainRAM")
SHARED_EYE_EXCHANGED            = (0x1FF9E2, 1, "MainRAM")
SHARED_ARM_EXCHANGED            = (0x1FF9E3, 1, "MainRAM")
SHARED_FOOT_EXCHANGED           = (0x1FF9E4, 1, "MainRAM")
SHARED_MOUTH_EXCHANGED          = (0x1FF9E5, 1, "MainRAM")

# Gadget received flags
SHARED_GADGET_COSMIC_ANDYS      = (0x1FF993, 1, "MainRAM")
SHARED_GADGET_ROCKET_NEIGHBORHOOD=(0x1FF994, 1, "MainRAM")
SHARED_GADGET_DISC_CONSTRUCTION = (0x1FF995, 1, "MainRAM")
SHARED_GADGET_GRAPPLE_ALLEYS    = (0x1FF996, 1, "MainRAM")
SHARED_GADGET_DISC_ALLEYS       = (0x1FF997, 1, "MainRAM")
SHARED_GADGET_ROCKET_ALLEYS     = (0x1FF998, 1, "MainRAM")
SHARED_GADGET_ROCKET_TOYBARN    = (0x1FF999, 1, "MainRAM")
SHARED_GADGET_DISC_TOYBARN      = (0x1FF99A, 1, "MainRAM")
SHARED_GADGET_HOVER_TOYBARN     = (0x1FF99B, 1, "MainRAM")
SHARED_GADGET_COSMIC_SPACELAND  = (0x1FF99C, 1, "MainRAM")
SHARED_GADGET_GRAPPLE_ELEVATOR  = (0x1FF99D, 1, "MainRAM")
SHARED_GADGET_COSMIC_PENTHOUSE  = (0x1FF99E, 1, "MainRAM")
SHARED_GADGET_HOVER_AIRPORT     = (0x1FF99F, 1, "MainRAM")
SHARED_GADGET_ROCKET_TARMAC     = (0x1FF9A0, 1, "MainRAM")

# Missing toys collected/received counts per coin level
SHARED_TOY_COLLECTED = {
    1:  (0x1FF9A1, 1, "MainRAM"),
    2:  (0x1FF9A2, 1, "MainRAM"),
    4:  (0x1FF9A3, 1, "MainRAM"),
    5:  (0x1FF9A4, 1, "MainRAM"),
    7:  (0x1FF9A5, 1, "MainRAM"),
    8:  (0x1FF9A6, 1, "MainRAM"),
    10: (0x1FF9A7, 1, "MainRAM"),
    11: (0x1FF9A8, 1, "MainRAM"),
    13: (0x1FF9A9, 1, "MainRAM"),
    14: (0x1FF9AA, 1, "MainRAM"),
}
SHARED_TOY_RECEIVED = {
    1:  (0x1FF9AB, 1, "MainRAM"),
    2:  (0x1FF9AC, 1, "MainRAM"),
    4:  (0x1FF9AD, 1, "MainRAM"),
    5:  (0x1FF9AE, 1, "MainRAM"),
    7:  (0x1FF9AF, 1, "MainRAM"),
    8:  (0x1FF9B0, 1, "MainRAM"),
    10: (0x1FF9B1, 1, "MainRAM"),
    11: (0x1FF9B2, 1, "MainRAM"),
    13: (0x1FF9B3, 1, "MainRAM"),
    14: (0x1FF9B4, 1, "MainRAM"),
}

# Battery sanity bitmasks
SHARED_BATTERY = {
    1:  (0x1FF9B5, 1, "MainRAM"),
    2:  (0x1FF9B6, 1, "MainRAM"),
    6:  (0x1FF9B7, 1, "MainRAM"),
    4:  (0x1FF9B8, 1, "MainRAM"),
    5:  (0x1FF9B9, 1, "MainRAM"),
    7:  (0x1FF9BA, 1, "MainRAM"),
    8:  (0x1FF9BB, 1, "MainRAM"),
    9:  (0x1FF9BC, 1, "MainRAM"),
    11: (0x1FF9BD, 1, "MainRAM"),
    13: (0x1FF9BE, 1, "MainRAM"),
    14: (0x1FF9BF, 1, "MainRAM"),
}

# Life sanity bitmasks
SHARED_LIFE = {
    1:  (0x1FF9D9, 1, "MainRAM"),
    2:  (0x1FF9DA, 1, "MainRAM"),
    4:  (0x1FF9DB, 1, "MainRAM"),
    5:  (0x1FF9DC, 1, "MainRAM"),
    7:  (0x1FF9DD, 1, "MainRAM"),
    8:  (0x1FF9DE, 1, "MainRAM"),
    11: (0x1FF9DF, 1, "MainRAM"),
    14: (0x1FF9E0, 1, "MainRAM"),
}

# Green laser sanity bitmasks
SHARED_LASER_SANITY = {
    1:  (0x1FF9C8, 1, "MainRAM"),
    2:  (0x1FF9C9, 1, "MainRAM"),
    3:  (0x1FF9CA, 1, "MainRAM"),
    4:  (0x1FF9CB, 1, "MainRAM"),
    5:  (0x1FF9CC, 1, "MainRAM"),
    7:  (0x1FF9CD, 1, "MainRAM"),
    8:  (0x1FF9CE, 1, "MainRAM"),
    10: (0x1FF9CF, 1, "MainRAM"),
    11: (0x1FF9D0, 1, "MainRAM"),
    13: (0x1FF9D1, 1, "MainRAM"),
    14: (0x1FF9D2, 1, "MainRAM"),
}

# Death link
BUZZ_HEALTH_ADDR = (0x0B221E, 1, "MainRAM")
BUZZ_STATE_ADDR  = (0x0A155C, 1, "MainRAM")
BUZZ_DEATH_ADDR  = (0x0A136E, 1, "MainRAM")  # == 2 means Buzz has died (in-level)

# ============================================================
# ITEM NAME -> ACTION MAP
# ============================================================

# Bitmasks for move unlocks (SHARED_MOVE_UNLOCKS_LOW bits 0-7)
MOVE_BITS_LOW = {
    "Spin":        0,
    "Stomp":       1,
    "Double Jump": 2,
    "Visor":       3,
    "Ledge Grab":  4,
    "Pole Climb":  5,
    "Pole Vault":  6,
    "Push":        7,
}
# Bit 0 of HIGH byte
MOVE_BIT_ROPE = 0

# Level unlock bitmasks (hover IDs 7-14 = low byte, 15-21 = high byte)
LEVEL_UNLOCK_BITS = {
    "Andy's House Unlock":          (7,  False),  # hover 7
    "Andy's Neighborhood Unlock":   (8,  False),
    "Bombs Away! Unlock":           (9,  False),
    "Construction Yard Unlock":     (10, False),
    "Alleys and Gullies Unlock":    (11, False),
    "Slime Time Unlock":            (12, False),
    "Al's Toy Barn Unlock":         (13, False),
    "Al's Space Land Unlock":       (14, False),
    "Toy Barn Encounter Unlock":    (15, True),   # hover 15 = high byte bit 0
    "Elevator Hop Unlock":          (16, True),
    "Al's Penthouse Unlock":        (17, True),
    "The Evil Emperor Zurg Unlock": (18, True),
    "Airport Infiltration Unlock":  (19, True),
    "Tarmac Trouble Unlock":        (20, True),
    "Final Showdown Unlock":        (21, True),
}

# Gadget item -> shared address
GADGET_ITEM_TO_ADDR = {
    "Cosmic Shield - Andy's House":         SHARED_GADGET_COSMIC_ANDYS,
    "Rocket Boots - Andy's Neighborhood":   SHARED_GADGET_ROCKET_NEIGHBORHOOD,
    "Disc Launcher - Construction Yard":    SHARED_GADGET_DISC_CONSTRUCTION,
    "Grappling Hook - Alleys and Gullies":  SHARED_GADGET_GRAPPLE_ALLEYS,
    "Disc Launcher - Alleys and Gullies":   SHARED_GADGET_DISC_ALLEYS,
    "Rocket Boots - Alleys and Gullies":    SHARED_GADGET_ROCKET_ALLEYS,
    "Rocket Boots - Al's Toy Barn":         SHARED_GADGET_ROCKET_TOYBARN,
    "Disc Launcher - Al's Toy Barn":        SHARED_GADGET_DISC_TOYBARN,
    "Hover Boots - Al's Toy Barn":          SHARED_GADGET_HOVER_TOYBARN,
    "Cosmic Shield - Al's Space Land":      SHARED_GADGET_COSMIC_SPACELAND,
    "Grappling Hook - Elevator Hop":        SHARED_GADGET_GRAPPLE_ELEVATOR,
    "Cosmic Shield - Al's Penthouse":       SHARED_GADGET_COSMIC_PENTHOUSE,
    "Hover Boots - Airport Infiltration":   SHARED_GADGET_HOVER_AIRPORT,
    "Rocket Boots - Tarmac Trouble":        SHARED_GADGET_ROCKET_TARMAC,
}

# Missing part item -> shared address
PART_ITEM_TO_ADDR = {
    "Missing Ear":   SHARED_EAR_RECEIVED,
    "Missing Eye":   SHARED_EYE_RECEIVED,
    "Missing Arm":   SHARED_ARM_RECEIVED,
    "Missing Foot":  SHARED_FOOT_RECEIVED,
    "Missing Mouth": SHARED_MOUTH_RECEIVED,
}

# Trap item -> shared address
TRAP_ITEM_TO_ADDR = {
    "Narrow Vision Trap":       SHARED_TRAP_NARROW_VISION,
    "Invincible Enemies Trap":  SHARED_TRAP_INVINCIBLE_ENEMIES,
    "Freeze Buzz Trap":         SHARED_TRAP_FREEZE_BUZZ,
    "Cutscene Trap":            SHARED_TRAP_CUTSCENE,
    "Damage Buzz Trap":         SHARED_TRAP_DAMAGE_BUZZ,
}

# Coin bundle item -> shared address
COIN_BUNDLE_TO_ADDR = {
    "Coin Bundle - Andy's House":           SHARED_COIN_ITEM_ANDYS_HOUSE,
    "Coin Bundle - Andy's Neighborhood":    SHARED_COIN_ITEM_NEIGHBORHOOD,
    "Coin Bundle - Construction Yard":      SHARED_COIN_ITEM_CONSTRUCTION,
    "Coin Bundle - Alleys and Gullies":     SHARED_COIN_ITEM_ALLEYS,
    "Coin Bundle - Al's Toy Barn":          SHARED_COIN_ITEM_TOY_BARN,
    "Coin Bundle - Al's Space Land":        SHARED_COIN_ITEM_SPACE_LAND,
    "Coin Bundle - Elevator Hop":           SHARED_COIN_ITEM_ELEVATOR,
    "Coin Bundle - Al's Penthouse":         SHARED_COIN_ITEM_PENTHOUSE,
    "Coin Bundle - Airport Infiltration":   SHARED_COIN_ITEM_AIRPORT,
    "Coin Bundle - Tarmac Trouble":         SHARED_COIN_ITEM_TARMAC,
}

# Token detection: in-game level_id -> hover_id (for SHARED_TOKENS_COLLECTED),
# level_id -> level display name, and bit value -> token name.
TOKEN_HOVER_BY_LEVEL = {
    1: 7, 2: 8, 6: 9, 4: 10, 5: 11, 3: 12, 7: 13, 8: 14,
    9: 15, 10: 16, 11: 17, 12: 18, 13: 19, 14: 20, 15: 21,
}
TOKEN_LEVEL_NAME_BY_LEVEL = {
    1: "Andy's House", 2: "Andy's Neighborhood", 6: "Bombs Away!",
    4: "Construction Yard", 5: "Alleys and Gullies", 3: "Slime Time",
    7: "Al's Toy Barn", 8: "Al's Space Land", 9: "Toy Barn Encounter",
    10: "Elevator Hop", 11: "Al's Penthouse", 12: "The Evil Emperor Zurg",
    13: "Airport Infiltration", 14: "Tarmac Trouble", 15: "Prospector Showdown",
}
TOKEN_BIT_TO_NAME = {
    1:  "Hamm's 50 Coins Token",
    2:  "Missing Toys Token",
    4:  "Race Token",
    8:  "Hidden Token",
    16: "Boss Token",
}

# ============================================================
# LOCATION NAME -> CHECK DETECTION
# ============================================================

# Boss defeat locations
BOSS_DEFEAT_LOCATIONS = {
    "Bombs Away! - Defeat Reward 1":            35,
    "Bombs Away! - Defeat Reward 2":            35,
    "Slime Time - Defeat Reward 1":             38,
    "Slime Time - Defeat Reward 2":             38,
    "Toy Barn Encounter - Defeat Reward 1":     41,
    "Toy Barn Encounter - Defeat Reward 2":     41,
    "The Evil Emperor Zurg - Defeat Reward 1":  44,
    "The Evil Emperor Zurg - Defeat Reward 2":  44,
}

# Level ID -> game level ID mapping
LEVEL_ID_ADDR = (0x0A16A8, 1, "MainRAM")
CUTSCENE_ACTIVE_ADDR = (0x1FF97E, 1, "MainRAM")  # Lua sets 1 while a cutscene trap plays; pause checks

# Boss defeat screen IDs
BOSS_DEFEAT_SCREENS = {35, 38, 41, 44}

# Token location -> (level_id, token_bit)
# Token bitmasks: 0x0C1618-0x0C1625 (1 byte per level, hover 7-20)
TOKEN_ADDR_BASE = 0x0C1618
HOVER_TO_LEVEL_OFFSET = {
    7: 0, 8: 1, 9: 2, 10: 3, 11: 4, 12: 5,
    13: 6, 14: 7, 15: 8, 16: 9, 17: 10, 18: 11, 19: 12, 20: 13,
}

# Rex addresses per level
REX_ADDR_LOW_BITS = {
    1:  0,  # Andy's House
    2:  1,  # Andy's Neighborhood
    4:  2,  # Construction Yard (bit 2 of low byte)
    5:  3,
    7:  4,
    8:  5,
}
REX_ADDR_HIGH_BITS = {
    10: 0,
    11: 1,
    13: 2,
    14: 3,
}

# ── SHARED LOCATION MAPS (used by both check + restore) ──────

TOY_LEVEL_MAP = {
    1:  ("Sheep",          "Andy's House",         ["Basement","Living Room","Kitchen","Attic","Garage"]),
    2:  ("Soldier",        "Andy's Neighborhood",  ["Molehill","Clothes Line","Swing","Pool Plant","Tree"]),
    4:  ("Worker Tike",    "Construction Yard",    ["Wheelbarrow","Filing Cabinets","Bulldozer","Construction Floor 1","Boss Arena"]),
    5:  ("Duck",           "Alleys and Gullies",   ["Pool Behind Construction","Hidden Near Race","Incline Parasol","Window Sill","Rain Gutter"]),
    7:  ("Chick",          "Al's Toy Barn",        ["Complete Race","Gumball Machines","Shipping Boxes","Near Basketballs","End of Long Aisle"]),
    8:  ("Alien",          "Al's Space Land",      ["Ballpit","Planet Mobile","End of Race","Middle of Zurg Aisle","End of Zurg Aisle"]),
    10: ("Mouse",          "Elevator Hop",         ["Electrical Room","Next to Rex","Control Room","Side of Elevator Shaft","Top of Elevator"]),
    11: ("Critter",        "Al's Penthouse",       ["Living Room","Kitchen","Bathroom","Train Bed","Woody Room"]),
    13: ("Passenger Tike", "Airport Infiltration", ["Near Start","Top of Conveyor Belts","Near Boss Arena","Top of Jet","Scaffolding"]),
    14: ("Luggage",        "Tarmac Trouble",       ["Top of Plane","Zone 2 Cart","Zone 8","Zone 6 Conveyor Belt","Zone 4"]),
}

BATTERY_LOCATIONS = {
    1:  ["Andy's House - Battery (Andy's Room)", "Andy's House - Battery (Attic)",
         "Andy's House - Battery (Basement)", "Andy's House - Battery (Garage)",
         "Andy's House - Battery (Living Room)", "Andy's House - Battery (Handrail)"],
    2:  ["Andy's Neighborhood - Battery (Lawnmower Yard)", "Andy's Neighborhood - Battery (Washing Machine)",
         "Andy's Neighborhood - Battery (Pool Yard)", "Andy's Neighborhood - Battery (Swing)",
         "Andy's Neighborhood - Battery (Top of Tree)"],
    6:  ["Bombs Away! - Battery (Back Right)", "Bombs Away! - Battery (Back Left)",
         "Bombs Away! - Battery (Front Left)", "Bombs Away! - Battery (Front Right)"],
    4:  ["Construction Yard - Battery (Bulldozer)", "Construction Yard - Battery (Boss Arena Front Left)",
         "Construction Yard - Battery (Boss Arena Back Left)", "Construction Yard - Battery (Boss Arena Back Right)"],
    5:  ["Alleys and Gullies - Battery (Behind Construction)", "Alleys and Gullies - Battery (Balcony Fence)",
         "Alleys and Gullies - Battery (Boss Arena)"],
    7:  ["Al's Toy Barn - Battery (Gumball Machine)", "Al's Toy Barn - Battery (Ventilation Shaft)",
         "Al's Toy Barn - Battery (Between Bicycles)", "Al's Toy Barn - Battery (Cardboard Boxes)",
         "Al's Toy Barn - Battery (Boss Arena)"],
    8:  ["Al's Space Land - Battery (Boss Arena)", "Al's Space Land - Battery (Arcade Cabinet)",
         "Al's Space Land - Battery (Blue Shelves)", "Al's Space Land - Battery (Red Shelf)",
         "Al's Space Land - Battery (Race Blue Shelf)"],
    9:  ["Toy Barn Encounter - Battery (South)", "Toy Barn Encounter - Battery (North)",
         "Toy Barn Encounter - Battery (East)", "Toy Barn Encounter - Battery (West)"],
    11: ["Al's Penthouse - Battery (Under Table)", "Al's Penthouse - Battery (Bathroom)",
         "Al's Penthouse - Battery (Kitchen)", "Al's Penthouse - Battery (Train Bed)",
         "Al's Penthouse - Battery (Television)"],
    13: ["Airport Infiltration - Battery (Luggage Pile)", "Airport Infiltration - Battery (Near Hidden Token)",
         "Airport Infiltration - Battery (Boss Arena)"],
    14: ["Tarmac Trouble - Battery (Road Opposite Zone 8)", "Tarmac Trouble - Battery (Helicopter Pad)",
         "Tarmac Trouble - Battery (Zone 3)", "Tarmac Trouble - Battery (Green Slime Maze)",
         "Tarmac Trouble - Battery (Boss Arena)"],
}

LIFE_LOCATIONS = {
    1:  ["Andy's House - Life (Crib)", "Andy's House - Life (Living Room)", "Andy's House - Life (Garage)"],
    2:  ["Andy's Neighborhood - Life (Top of Swing)"],
    4:  ["Construction Yard - Life (Top of Bulldozer)", "Construction Yard - Life (Roof of Green Building)"],
    5:  ["Alleys and Gullies - Life (Pool Behind Construction)", "Alleys and Gullies - Life (Lily Pad Behind Race)", "Alleys and Gullies - Life (Window Sill)"],
    7:  ["Al's Toy Barn - Life (Tennis Ball Isle)"],
    8:  ["Al's Space Land - Life (Planet Mobile)"],
    11: ["Al's Penthouse - Life (Fireplace)"],
    14: ["Tarmac Trouble - Life (Zone 6)"],
}

LASER_LOCATIONS = {
    1:  "Andy's House - Green Laser",
    2:  "Andy's Neighborhood - Green Laser",
    3:  "Slime Time - Green Laser",
    4:  "Construction Yard - Green Laser",
    5:  "Alleys and Gullies - Green Laser",
    7:  "Al's Toy Barn - Green Laser",
    8:  "Al's Space Land - Green Laser",
    10: "Elevator Hop - Green Laser",
    11: "Al's Penthouse - Green Laser",
    13: "Airport Infiltration - Green Laser",
    14: "Tarmac Trouble - Green Laser",
}

REX_LOCATIONS = {
    ("low", 0): "Andy's House - Talk to Rex",
    ("low", 1): "Andy's Neighborhood - Talk to Rex",
    ("low", 2): "Construction Yard - Talk to Rex",
    ("low", 3): "Alleys and Gullies - Talk to Rex",
    ("low", 4): "Al's Toy Barn - Talk to Rex",
    ("low", 5): "Al's Space Land - Talk to Rex",
    ("high", 0): "Elevator Hop - Talk to Rex",
    ("high", 1): "Al's Penthouse - Talk to Rex",
    ("high", 2): "Airport Infiltration - Talk to Rex",
    ("high", 3): "Tarmac Trouble - Talk to Rex",
}

# Hint Block Sanity. Current-level scoped 16-bit mask/seed (matches the Lua).
# Mask is in the safe Lua-managed 0x1FF9xx region (an address above the feed
# buffer held game garbage on load and fired phantom checks). 16-bit because
# Andy's House has 9 blocks. The seed is read-only -> Lua and only affects dialog,
# so its location above the feed buffer is fine (a stale read can't cause a send).
SHARED_HINT_MASK = (0x1FF9C2, 2, "MainRAM")
SHARED_HINT_SEED = (0x1FFA83, 2, "MainRAM")
# Per-level ORDERED hint location names. The order MUST match the Lua HINT_BLOCKS
# table exactly (bit i-1 = entry i).
HINT_LOCATIONS = {
    1: [
        "Andy's House - Hint Block (Andy's Room Bookshelf)",
        "Andy's House - Hint Block (Andy's Room Bed)",
        "Andy's House - Hint Block (Andy's Room Dresser Shelf)",
        "Andy's House - Hint Block (Andy's Room Crib)",
        "Andy's House - Hint Block (Top of Stairs)",
        "Andy's House - Hint Block (Attic)",
        "Andy's House - Hint Block (Bottom of Stairs)",
        "Andy's House - Hint Block (Top of Garage)",
        "Andy's House - Hint Block (Living Room Recliner)",
    ],
    2: [
        "Andy's Neighborhood - Hint Block (Lawnmower Yard)",
    ],
    4: [
        "Construction Yard - Hint Block (Paint Can Room)",
    ],
    7: [
        "Al's Toy Barn - Hint Block (Hay Bale Ride)",
    ],
    10: [
        "Elevator Hop - Hint Block (East Shortcut Fan)",
        "Elevator Hop - Hint Block (West Shortcut Fan)",
        "Elevator Hop - Hint Block (Control Room)",
    ],
    11: [
        "Al's Penthouse - Hint Block (Bathtub)",
        "Al's Penthouse - Hint Block (Train Bed)",
    ],
    14: [
        "Tarmac Trouble - Hint Block (Light Puzzle)",
    ],
}

COIN_LEVEL_ADDR_MAP = {
    "Andy's House":         SHARED_COINS_ANDYS_HOUSE,
    "Andy's Neighborhood":  SHARED_COINS_NEIGHBORHOOD,
    "Construction Yard":    SHARED_COINS_CONSTRUCTION,
    "Alleys and Gullies":   SHARED_COINS_ALLEYS,
    "Al's Toy Barn":        SHARED_COINS_TOY_BARN,
    "Al's Space Land":      SHARED_COINS_SPACE_LAND,
    "Elevator Hop":         SHARED_COINS_ELEVATOR,
    "Al's Penthouse":       SHARED_COINS_PENTHOUSE,
    "Airport Infiltration": SHARED_COINS_AIRPORT,
    "Tarmac Trouble":       SHARED_COINS_TARMAC,
}

PARTS_RESTORE = [
    (SHARED_EAR_COLLECTED,   SHARED_EAR_EXCHANGED,   "Andy's House - Missing Ear",          "Andy's House - Give Potato Head His Ear"),
    (SHARED_EYE_COLLECTED,   SHARED_EYE_EXCHANGED,   "Construction Yard - Missing Eye",     "Construction Yard - Give Potato Head His Eye"),
    (SHARED_ARM_COLLECTED,   SHARED_ARM_EXCHANGED,   "Al's Toy Barn - Missing Arm",         "Al's Toy Barn - Give Potato Head His Arm"),
    (SHARED_FOOT_COLLECTED,  SHARED_FOOT_EXCHANGED,  "Elevator Hop - Missing Foot",         "Elevator Hop - Give Potato Head His Foot"),
    (SHARED_MOUTH_COLLECTED, SHARED_MOUTH_EXCHANGED, "Airport Infiltration - Missing Mouth","Airport Infiltration - Give Potato Head His Mouth"),
]

# ============================================================
# CLIENT
# ============================================================

class ToyStory2Client(BizHawkClient):
    system = "PSX"
    game   = "Toy Story 2"
    patch_suffix = None  # No patch file needed — uses shared memory

    def __init__(self):
        super().__init__()
        self.slot_data: Optional[dict] = None
        self.last_item_index: int = 0
        self.checked_locations: set = set()
        self._rex_baseline_low = None
        self._rex_baseline_high = None
        self._bump_conn_gen = False
        self._conn_gen_value = 0
        self.death_link_sent: bool = False
        self._pending_deaths: int = 0
        self._death_from_link: bool = False
        self._deathlink_hooked: bool = False
        self.prev_boss_level: int = -1
        self.boss_reward_sent: set = set()
        self.restored_from_server: bool = False
        self._loc_name_to_id: Optional[dict] = None
        self._gameplay_started: bool = False
        self._last_seen_level: int = -1
        self._level_stable_ticks: int = 0
        # Delivered-count trackers for queue items (traps/filler). We track how
        # many of each we have pushed into the game's delivery queue so we never
        # rely on reading the RAM counter back (the Lua consumes/decrements it).
        # Keyed by RAM address (int). Reset on connect; rebuilt from items.
        self._delivered: dict = {}

    def _location_map(self, ctx: "BizHawkClientContext") -> dict:
        """Build (and cache) a location name -> id map. We derive it from our own
        world's location table plus the dynamic coin-bundle ID scheme, since the
        BizHawk context does not expose location_name_to_id directly."""
        if self._loc_name_to_id is not None:
            return self._loc_name_to_id

        name_to_id: dict = {}

        # Static (non-coin) locations from our own locations table.
        try:
            from .locations import LOCATION_TABLE, LOC_BASE
            for name, data in LOCATION_TABLE.items():
                if data.code is not None:
                    name_to_id[name] = data.code
        except Exception as e:
            logger.error(f"[TS2] failed to load location table: {e}")

        # Dynamic coin-bundle locations — must match __init__.py's scheme exactly:
        #   offset = LOC_BASE + 2000
        #   id = offset + (level_idx * 110) + bundle_num
        try:
            from .locations import LOC_BASE
            from .coin_data import COIN_DATA
            coin_levels = [
                "Andy's House", "Andy's Neighborhood", "Construction Yard",
                "Alleys and Gullies", "Al's Toy Barn", "Al's Space Land",
                "Elevator Hop", "Al's Penthouse", "Airport Infiltration",
                "Tarmac Trouble",
            ]
            offset = LOC_BASE + 2000
            per_level = 110
            for li, level in enumerate(coin_levels):
                coins = COIN_DATA.get(level, [])
                for bn in range(1, len(coins) + 1):
                    loc_name = f"{level} - Coin Bundle {bn}"
                    name_to_id[loc_name] = offset + (li * per_level) + bn
        except Exception as e:
            logger.error(f"[TS2] failed to build coin bundle map: {e}")

        self._loc_name_to_id = name_to_id
        return self._loc_name_to_id

    # ── ROM VALIDATION ────────────────────────────────────────

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        """Check for Toy Story 2. We confirm via the shared-memory sentinel that
        our Lua writes (0xAB at 0x1FFFD0). The Lua sets this on its first frame,
        so the player must have both Lua scripts running."""
        try:
            sentinel = await read(ctx.bizhawk_ctx, [VALIDATE_ADDR])
            if sentinel[0][0] == 0xAB:
                ctx.game = self.game
                ctx.items_handling = 0b111  # receive all items
                ctx.want_slot_data = True
                return True
        except Exception:
            pass
        return False

    # ── SLOT DATA ─────────────────────────────────────────────

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        if cmd == "Connected":
            self.slot_data = args.get("slot_data", {})
            self.restored_from_server = False
            self.last_item_index = 0
            self._gameplay_started = False
            # Request a one-time connection-generation bump (consumed in
            # _write_settings) so the Lua clears session-only rex state for this
            # (possibly different) seed.
            self._bump_conn_gen = True
            # Capture a rex baseline on the first scan after connect: rex bits
            # already set in RAM at connect time are stale (a previous seed's talks
            # still in shared RAM, or save-state leftovers) and must NOT be sent to
            # this seed. Only bits that turn on AFTER connect are genuine talks.
            self._rex_baseline_low = None
            self._rex_baseline_high = None
            self._last_seen_level = -1
            self._level_stable_ticks = 0
            self._delivered = {}
            # On-screen item feed tracking
            self._feed_item_index = 0
            self._feed_checked = set()
            self._feed_seq = 0
            self._feed_inited = False
            # Live feed mode (0=off,1=sent,2=received,3=both). Owned by the client
            # so the Select button can cycle it at runtime; starts at the YAML value.
            self.feed_mode = self.slot_data.get("on_screen_item_feed", 2)
            # Last-seen Select cycle counter (from the Lua); None = read baseline.
            self._feed_cycle_seen = None
            # Whether we've issued the one-time LocationScouts for the sent feed.
            self._scouts_sent = False
            # Our own pending-received-death counter. The standard AP DeathLink
            # mixin does NOT keep a queue — it just calls ctx.on_deathlink(data).
            # We override that to count incoming deaths so the game_watcher can
            # apply them to the Lua. (Relying on ctx.death_link_queue silently did
            # nothing — that attribute doesn't exist, so received deaths never
            # killed the player's Buzz.)
            self._pending_deaths = 0
            self._death_from_link = False
            if self.slot_data.get("death_link", 0):
                import asyncio as _asyncio
                _asyncio.create_task(ctx.update_death_link(True))

                # Wrap ctx.on_deathlink ONCE. on_package/connect can fire multiple
                # times (reconnects, repeated slot_data), and naively re-wrapping
                # each time stacks the handlers: one received death then increments
                # _pending_deaths once PER layer, which killed Buzz 3x after a
                # couple of reconnects. The guard flag ensures a single wrapper.
                if not getattr(self, "_deathlink_hooked", False):
                    self._deathlink_hooked = True
                    _orig_on_deathlink = getattr(ctx, "on_deathlink", None)

                    def _on_deathlink(data, _client=self, _orig=_orig_on_deathlink):
                        _client._pending_deaths += 1
                        if _orig is not None:
                            try:
                                return _orig(data)
                            except Exception:
                                pass
                    ctx.on_deathlink = _on_deathlink
            logger.info("[TS2] Connected! Slot data received.")
            # Note: the LocationScouts that populates ctx.locations_info for the
            # "sent" feed is issued from game_watcher (see _scout_locations), once
            # the server has sent us the set of locations that actually exist in
            # this seed. Scouting the apworld's full location list here crashed the
            # server with a KeyError, because IDs not placed in this generation
            # aren't valid to scout.

    # ── GAME WATCHER ──────────────────────────────────────────

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if not ctx.server or not ctx.slot:
            return
        if not self.slot_data:
            return

        try:
            # Write settings to shared memory
            await self._write_settings(ctx)

            # One-time scout of this seed's real locations so the "sent" feed can
            # show the item that was at a location. Done here (not in on_package)
            # because the valid location set arrives after the Connected packet.
            await self._scout_locations(ctx)

            # Restore progress from server on first tick after connect
            if not self.restored_from_server:
                await self._restore_from_server(ctx)
                self.restored_from_server = True

            # Process received items
            await self._process_items(ctx)

            # Publish the current level's despawn masks (derived from the server's
            # checked_locations) to the one-direction despawn-seed bytes. Done every
            # tick so it survives a BizHawk reset without needing a reconnect.
            await self._publish_despawn_seeds(ctx)

            # Check for completed locations
            await self._check_locations(ctx)

            # Handle death link (only during active gameplay, so health reading 0
            # during a level load/transition can't be mistaken for a death).
            if self.slot_data.get("death_link", 0) and getattr(self, "_gameplay_started", False):
                await self._handle_death_link(ctx)

            # Check goal completion
            await self._check_goal(ctx)

            # On-screen item feed
            await self._update_item_feed(ctx)

        except Exception as e:
            logger.error(f"[TS2] game_watcher error: {e}")

    # ── WRITE SETTINGS ────────────────────────────────────────

    async def _write_settings(self, ctx: "BizHawkClientContext") -> None:
        sd = self.slot_data

        # Bump the connection-generation byte ONCE per connection (flag set by the
        # Connected handler in on_package), so the Lua can detect a fresh connection
        # / seed swap and clear session-only state such as the rex talk mask. This
        # function runs every tick, so the bump MUST be gated — bumping every tick
        # made the Lua wipe rex every frame (Rex never sent).
        if getattr(self, "_bump_conn_gen", False):
            self._bump_conn_gen = False
            try:
                cur_gen = (await read(ctx.bizhawk_ctx, [SHARED_CONN_GEN]))[0][0]
            except Exception:
                cur_gen = 0
            self._conn_gen_value = (cur_gen + 1) & 0xFF
        new_gen = getattr(self, "_conn_gen_value", 0)

        # Build settings byte: bit0=coinsanity, bit1=lifesanity, bit2=batterysanity,
        #                      bit3=laser_sanity, bit4=rexsanity, bit5=movesanity
        settings_byte = (
            (1 if sd.get("coinsanity", 0)          else 0) << 0 |
            (1 if sd.get("lifesanity", 0)           else 0) << 1 |
            (1 if sd.get("batterysanity", 0)        else 0) << 2 |
            (1 if sd.get("green_laser_sanity", 0)   else 0) << 3 |
            (1 if sd.get("rexsanity", 0)            else 0) << 4 |
            (1 if sd.get("movesanity", 0)           else 0) << 5 |
            (1 if sd.get("hint_block_sanity", 0)    else 0) << 6
        )

        # Build QOL byte: bit0=autosave, bit1=disc-fill, bit2=fallAnim, bit3=skipCutscenes, bit4=autocoins
        qol_byte = (
            (1 if sd.get("auto_save", 1)                         else 0) << 0 |
            (1 if sd.get("disc_launcher_fill_pockets", 1)        else 0) << 1 |
            (1 if sd.get("disable_falling_animation", 0)         else 0) << 2 |
            (1 if sd.get("skip_cutscenes", 1)                    else 0) << 3 |
            (1 if sd.get("collect_enemy_coins_automatically", 1) else 0) << 4
        )

        writes = [
            # Core settings
            (SHARED_GAME_MODE[0],        [sd.get("game_mode", 0)],               "MainRAM"),
            # Mirror game mode to a SAFE scratch address (0x1FF97D), tagged with a
            # magic high nibble (0xA0=open, 0xA1=linear) so the Lua only latches a
            # value the client actually wrote — random RAM garbage almost never
            # equals 0xA0/0xA1, whereas a bare 0/1/2 could match game corruption
            # and wrongly latch the mode (which broke linear after the 1st level).
            (0x1FF97D,                   [0xA0 + sd.get("game_mode", 0)],        "MainRAM"),
            (SHARED_BUNDLE_SIZE[0],      [sd.get("coinsanity_checks_bundle_size", 5)],  "MainRAM"),
            (SHARED_RECV_BUNDLE_SIZE[0], [sd.get("coinsanity_received_bundle_size", 5)], "MainRAM"),
            (SHARED_TOKEN_POOL[0],       [sd.get("pizza_planet_token_pool", 50)], "MainRAM"),
            (SHARED_TICKETS_REQUIRED[0], [sd.get("final_showdown_token_gate", 50)], "MainRAM"),
            # Gates
            (SHARED_GATE_BOMBS_AWAY[0],  [sd.get("bombs_away_token_gate", 10)],  "MainRAM"),
            (SHARED_GATE_SLIME_TIME[0],  [sd.get("slime_time_token_gate", 20)],  "MainRAM"),
            (SHARED_GATE_TOY_BARN[0],    [sd.get("toy_barn_encounter_token_gate", 30)], "MainRAM"),
            (SHARED_GATE_ZURG[0],        [sd.get("evil_emperor_zurg_token_gate", 40)], "MainRAM"),
            (SHARED_GATE_PROSPECTOR[0],  [sd.get("linear_final_showdown_token_gate", 50)], "MainRAM"),
            # Sanity + movesanity flags
            (0x1FF9D3, [settings_byte],  "MainRAM"),
            # Music
            (0x1FF9D4, [sd.get("music_randomizer_mode", 0)],    "MainRAM"),
            (0x1FF9D5, [sd.get("oops_all_bangers_song", 19)],   "MainRAM"),
            (0x1FF9D6, [1 if sd.get("skip_song", 1) else 0],    "MainRAM"),
            # QOL
            (0x1FF9D7, [qol_byte],       "MainRAM"),
            # Death link
            (0x1FF9D8, [1 if sd.get("death_link", 0) else 0],   "MainRAM"),
            # Sentinel
            (VALIDATE_ADDR[0],           [0xAB],                 "MainRAM"),
            # Connection generation (stable; bumped once per connect in on_package)
            (SHARED_CONN_GEN[0],         [new_gen],              "MainRAM"),
        ]
        await write(ctx.bizhawk_ctx, writes)

    # ── PROCESS RECEIVED ITEMS ────────────────────────────────

    async def _process_items(self, ctx: "BizHawkClientContext") -> None:
        if not ctx.items_received:
            return

        # Authoritative rebuild: compute token/laser/move/unlock/ticket state from
        # the FULL received-items list every pass, starting from zero. We do NOT
        # read these back from RAM and OR onto them, because (a) boot garbage could
        # set spurious bits and (b) the Lua zeroes these on init, which would race
        # with an incremental approach and drop the starting-level unlock.
        token_count  = 0
        laser_level  = 0
        moves_low    = 0
        moves_high   = 0
        unlocks_low  = 0
        unlocks_high = 0
        tickets      = 0

        writes = []
        coin_counts = {}  # addr -> count to write

        for item in ctx.items_received:
            item_name = ctx.item_names.lookup_in_game(item.item)
            if item_name is None:
                continue

            if item_name == "Pizza Planet Token":
                token_count = min(token_count + 1, 99)
            elif item_name == "Progressive Laser":
                laser_level = min(laser_level + 1, 3)
            elif item_name in MOVE_BITS_LOW:
                moves_low |= (1 << MOVE_BITS_LOW[item_name])
            elif item_name == "Rope Sliding":
                moves_high |= (1 << MOVE_BIT_ROPE)
            elif item_name in LEVEL_UNLOCK_BITS:
                hover_id, is_high = LEVEL_UNLOCK_BITS[item_name]
                if is_high:
                    unlocks_high |= (1 << (hover_id - 15))
                else:
                    unlocks_low |= (1 << (hover_id - 7))
            elif item_name == "Final Showdown Ticket":
                tickets = min(tickets + 1, 4)
            elif item_name in COIN_BUNDLE_TO_ADDR:
                addr = COIN_BUNDLE_TO_ADDR[item_name]
                coin_counts[addr] = coin_counts.get(addr, 0) + 1

        # Gadgets and parts are simple "set to 1" flags — safe to (re)assert from
        # the full list each pass (idempotent).
        for item in ctx.items_received:
            item_name = ctx.item_names.lookup_in_game(item.item)
            if item_name is None:
                continue
            if item_name in GADGET_ITEM_TO_ADDR:
                addr = GADGET_ITEM_TO_ADDR[item_name]
                writes.append((addr[0], [1], "MainRAM"))
            elif item_name in PART_ITEM_TO_ADDR:
                addr = PART_ITEM_TO_ADDR[item_name]
                writes.append((addr[0], [1], "MainRAM"))

        # Re-assert Mr. Potato Head collected/exchanged flags EVERY pass (not just
        # once on connect). These live in a RAM region the game can clobber on a
        # level load; if we only restored them on connect, a later load would clear
        # the exchanged flag and the "give me my part" UI would pop back up even
        # though the part was already turned in (the recurring potato glitch).
        # Driven authoritatively by checked_locations.
        try:
            loc_map = self._location_map(ctx)
            id_to_name = {v: k for k, v in loc_map.items()}
            checked_names = {id_to_name.get(i) for i in ctx.checked_locations
                             if i in id_to_name}
            for collected_addr, exchanged_addr, found_loc, given_loc in PARTS_RESTORE:
                if found_loc in checked_names:
                    writes.append((collected_addr[0], [1], "MainRAM"))
                if given_loc in checked_names:
                    writes.append((exchanged_addr[0], [1], "MainRAM"))
            # Hamm "50 coins" UI suppression: per coin level, tell the Lua whether
            # that level's Hamm token location has been checked. Authoritative from
            # checked_locations (persists across reconnects).
            for lvl_id, addr in SHARED_HAMM_DONE.items():
                loc = HAMM_LOC_BY_LEVEL.get(lvl_id)
                done = 1 if (loc in checked_names) else 0
                writes.append((addr[0], [done], "MainRAM"))
        except Exception:
            pass

        # Traps and filler are DELIVERY QUEUES: the client pushes items in, the
        # Lua consumes (applies the trap / grants the life) and decrements. We
        # track how many of each we've delivered in self._delivered (NOT by
        # reading RAM, which the Lua mutates). Each pass we compute the target
        # total from the full item list and push only the new delta into the
        # queue, adding to whatever the Lua hasn't consumed yet.
        queue_targets: dict = {}  # addr(int) -> total count that should be delivered
        for item in ctx.items_received:
            item_name = ctx.item_names.lookup_in_game(item.item)
            if item_name is None:
                continue
            if item_name in TRAP_ITEM_TO_ADDR:
                a = TRAP_ITEM_TO_ADDR[item_name][0]
                queue_targets[a] = queue_targets.get(a, 0) + 1
            elif item_name == "1 Life":
                a = SHARED_FILLER_EXTRA_LIFE[0]
                queue_targets[a] = queue_targets.get(a, 0) + 1
            elif item_name == "Extra Battery":
                a = SHARED_FILLER_HEALTH_UP[0]
                queue_targets[a] = queue_targets.get(a, 0) + 1

        for a, target in queue_targets.items():
            delivered = self._delivered.get(a, 0)
            delta = target - delivered
            if delta > 0:
                # Add the new deliveries to whatever is still queued (unconsumed).
                cur = (await read(ctx.bizhawk_ctx, [(a, 1, "MainRAM")]))[0][0]
                writes.append((a, [min(cur + delta, 255)], "MainRAM"))
                self._delivered[a] = target

        # Write accumulated authoritative state
        writes += [
            (SHARED_TOKENS_RECEIVED[0],   [token_count],  "MainRAM"),
            (SHARED_LASER_LEVEL[0],       [laser_level],  "MainRAM"),
            (SHARED_MOVE_UNLOCKS_LOW[0],  [moves_low],    "MainRAM"),
            (SHARED_MOVE_UNLOCKS_HIGH[0], [moves_high],   "MainRAM"),
            (SHARED_TICKETS_RECEIVED[0],  [tickets],      "MainRAM"),
        ]

        # Level unlock bitmask: ONLY write it in OPEN mode, where unlocks come from
        # received Level Unlock items. In LINEAR mode the Lua owns this same
        # address (0x1FFFE5/E7) via apply_linear_area (unlocks are driven by
        # tickets), so writing our item-derived value here — which is 0 in linear,
        # since you don't receive unlock items — was zeroing the Lua's linear
        # unlocks every frame and locking every level after the first one.
        if self.slot_data.get("game_mode", 0) == 0:
            writes += [
                (SHARED_LEVEL_UNLOCKS_LOW[0], [unlocks_low],  "MainRAM"),
                (SHARED_LEVEL_UNLOCKS_HIGH[0],[unlocks_high], "MainRAM"),
            ]

        # ── OPEN-MODE FINAL SHOWDOWN (Prospector) UNLOCK ──────
        # The Prospector unlocks when the player's chosen GOAL CONDITIONS are met.
        # The Lua previously hard-required tokens AND bosses regardless of the
        # selected goal, so a non-token (or non-boss) goal never unlocked it. We
        # compute it here from slot_data + received items and write a single
        # unlock flag the Lua reads.
        if self.slot_data.get("game_mode", 0) == 0:  # open mode only
            goal = self.slot_data.get("goal_conditions", 0)
            tok_gate = self.slot_data.get("final_showdown_token_gate", 50)
            boss_req = self.slot_data.get("defeated_bosses_required", 4)
            tokens_ok = token_count >= tok_gate
            bosses_ok = tickets >= boss_req
            # "Level unlock" goal: matches the generator's rule (rules.py), which
            # defines this condition as owning the FINAL SHOWDOWN UNLOCK item — the
            # dedicated unlock for the final level — NOT owning every level unlock.
            # (The earlier client logic required all 14 unlocks, which both
            # disagreed with generation AND was impossible since starting-level
            # unlocks are pre-collected and never received.)
            owned_unlocks = {
                ctx.item_names.lookup_in_game(it.item)
                for it in ctx.items_received
            }
            levels_ok = "Final Showdown Unlock" in owned_unlocks
            goal_met = {
                0: tokens_ok,
                1: bosses_ok,
                2: levels_ok,
                3: tokens_ok and bosses_ok,
                4: tokens_ok and levels_ok,
                5: bosses_ok and levels_ok,
                6: tokens_ok and bosses_ok and levels_ok,
            }.get(goal, tokens_ok)
            writes.append((SHARED_PROSPECTOR_UNLOCK[0], [1 if goal_met else 0], "MainRAM"))

        # Coin bundle item counts are absolute. Write ALL coin-item addresses
        # authoritatively (0 for levels with no received bundles) so that game
        # RAM garbage at these addresses can never leak through as phantom
        # spendable coins. coin_counts holds only the non-zero ones.
        for addr in (
            SHARED_COIN_ITEM_ANDYS_HOUSE, SHARED_COIN_ITEM_NEIGHBORHOOD,
            SHARED_COIN_ITEM_CONSTRUCTION, SHARED_COIN_ITEM_ALLEYS,
            SHARED_COIN_ITEM_TOY_BARN, SHARED_COIN_ITEM_SPACE_LAND,
            SHARED_COIN_ITEM_ELEVATOR, SHARED_COIN_ITEM_PENTHOUSE,
            SHARED_COIN_ITEM_AIRPORT, SHARED_COIN_ITEM_TARMAC,
        ):
            count = coin_counts.get(addr, 0)
            writes.append((addr[0], [min(count, 255)], "MainRAM"))

        # ── MISSING TOYS (received-item count) ────────────────
        # Count "Sheep"/"Soldier"/etc. ITEMS received and write the per-level
        # total to SHARED_TOY_RECEIVED every frame, so the level UI reflects toys
        # received AFTER connect. (This used to live in _restore_from_server,
        # which runs only once on connect, so later toys never updated.) The Lua
        # owns SHARED_TOY_COLLECTED; we only touch SHARED_TOY_RECEIVED here.
        toy_item_to_level = {
            "Sheep": 1, "Soldier": 2,
            "Worker Tike": 4, "Duck": 5,
            "Chick": 7, "Alien": 8,
            "Mouse": 10, "Critter": 11,
            "Passenger Tike": 13, "Luggage": 14,
        }
        toy_recv_counts = {lvl: 0 for lvl in TOY_LEVEL_MAP}
        for item in ctx.items_received:
            iname = ctx.item_names.lookup_in_game(item.item)
            lvl = toy_item_to_level.get(iname)
            if lvl is not None:
                toy_recv_counts[lvl] = min(toy_recv_counts[lvl] + 1, 5)
        for level_id, count in toy_recv_counts.items():
            recv_addr = SHARED_TOY_RECEIVED.get(level_id)
            if recv_addr:
                writes.append((recv_addr[0], [count], "MainRAM"))

        if writes:
            await write(ctx.bizhawk_ctx, writes)

        self.last_item_index = len(ctx.items_received)

    # ── RESTORE FROM SERVER ───────────────────────────────────

    async def _restore_from_server(self, ctx: "BizHawkClientContext") -> None:
        """On connect, rebuild all shared-memory progress from the server's
        checked_locations so the game reflects everything already done."""
        checked = ctx.checked_locations
        if not checked:
            return

        # Build id -> name lookup
        loc_map = self._location_map(ctx)
        id_to_name = {v: k for k, v in loc_map.items()}
        checked_names = {id_to_name.get(i) for i in checked if i in id_to_name}
        self.checked_locations |= set(checked)

        writes = []

        # ── BOSS DEFEATS ──────────────────────────────────────
        boss_bits = {
            "Bombs Away! - Defeat Reward 1":           0,
            "Slime Time - Defeat Reward 1":            1,
            "Toy Barn Encounter - Defeat Reward 1":    2,
            "The Evil Emperor Zurg - Defeat Reward 1": 3,
        }
        boss_mask = 0
        for loc_name, bit in boss_bits.items():
            if loc_name in checked_names:
                boss_mask |= (1 << bit)
        # Authoritative: write the full mask derived from checked_locations.
        writes.append((SHARED_BOSS_DEFEATS[0], [boss_mask], "MainRAM"))

        # ── MISSING PARTS ─────────────────────────────────────
        # Restore the two flags independently: "Missing X" -> collected,
        # "Give Potato Head His X" -> exchanged.
        for collected_addr, exchanged_addr, found_loc, given_loc in PARTS_RESTORE:
            if found_loc in checked_names:
                writes.append((collected_addr[0], [1], "MainRAM"))
            if given_loc in checked_names:
                writes.append((exchanged_addr[0], [1], "MainRAM"))

        # ── REX ───────────────────────────────────────────────
        # Write server-confirmed rex bits to the SEED addresses (always, even 0).
        # The Lua merges these into its own mask and writes the real rex bytes
        # authoritatively, so game RAM garbage at 0x1FF9C4/C5 can't fire phantom
        # checks while previously-confirmed talks still persist.
        rex_low = 0
        rex_high = 0
        for (byte_key, bit), loc_name in REX_LOCATIONS.items():
            if loc_name in checked_names:
                if byte_key == "low":
                    rex_low |= (1 << bit)
                else:
                    rex_high |= (1 << bit)
        writes.append((SHARED_REX_SEED_LOW[0], [rex_low], "MainRAM"))
        writes.append((SHARED_REX_SEED_HIGH[0], [rex_high], "MainRAM"))

        # ── MISSING TOYS ──────────────────────────────────────
        # Restore the per-level COLLECTED mask from checked toy locations so toys
        # we've already picked up stay despawned across a reset/reconnect. The
        # received-COUNT (SHARED_TOY_RECEIVED) is separate and handled every frame
        # in _process_items. Bit order must match the check-send mapping exactly
        # (bit i = locations[i]); we reuse the same table here.
        toy_restore_map = {
            1:  ("Sheep",           "Andy's House",         ["Basement","Living Room","Kitchen","Attic","Garage"]),
            2:  ("Soldier",         "Andy's Neighborhood",  ["Molehill","Clothes Line","Swing","Pool Plant","Tree"]),
            4:  ("Worker Tike",     "Construction Yard",    ["Wheelbarrow","Filing Cabinets","Bulldozer","Construction Floor 1","Boss Arena"]),
            5:  ("Duck",            "Alleys and Gullies",   ["Pool Behind Construction","Hidden Near Race","Incline Parasol","Window Sill","Rain Gutter"]),
            7:  ("Chick",           "Al's Toy Barn",        ["Complete Race","Gumball Machines","Shipping Boxes","Near Basketballs","End of Long Aisle"]),
            8:  ("Alien",           "Al's Space Land",      ["Ballpit","Planet Mobile","End of Race","Middle of Zurg Aisle","End of Zurg Aisle"]),
            10: ("Mouse",           "Elevator Hop",         ["Electrical Room","Next to Rex","Control Room","Side of Elevator Shaft","Top of Elevator"]),
            11: ("Critter",         "Al's Penthouse",       ["Living Room","Kitchen","Bathroom","Train Bed","Woody Room"]),
            13: ("Passenger Tike",  "Airport Infiltration", ["Near Start","Top of Conveyor Belts","Near Boss Arena","Top of Jet","Scaffolding"]),
            14: ("Luggage",         "Tarmac Trouble",       ["Top of Plane","Zone 2 Cart","Zone 8","Zone 6 Conveyor Belt","Zone 4"]),
        }
        for level_id, (toy_type, level_name, suffixes) in toy_restore_map.items():
            mask = 0
            for i, suffix in enumerate(suffixes):
                if f"{level_name} - {toy_type} ({suffix})" in checked_names:
                    mask |= (1 << i)
            if mask:
                addr = SHARED_TOY_COLLECTED.get(level_id)
                if addr:
                    writes.append((addr[0], [mask], "MainRAM"))

        # ── BATTERIES ─────────────────────────────────────────
        for level_id, locs in BATTERY_LOCATIONS.items():
            mask = 0
            for i, loc_name in enumerate(locs):
                if loc_name in checked_names:
                    mask |= (1 << i)
            if mask:
                addr = SHARED_BATTERY.get(level_id)
                if addr:
                    writes.append((addr[0], [mask], "MainRAM"))

        # ── LIVES ─────────────────────────────────────────────
        for level_id, locs in LIFE_LOCATIONS.items():
            mask = 0
            for i, loc_name in enumerate(locs):
                if loc_name in checked_names:
                    mask |= (1 << i)
            if mask:
                addr = SHARED_LIFE.get(level_id)
                if addr:
                    writes.append((addr[0], [mask], "MainRAM"))

        # ── GREEN LASERS ──────────────────────────────────────
        for level_id, loc_name in LASER_LOCATIONS.items():
            if loc_name in checked_names:
                addr = SHARED_LASER_SANITY.get(level_id)
                if addr:
                    writes.append((addr[0], [1], "MainRAM"))

        # ── COIN BUNDLES (highest bundle number collected) ────
        for level_name, addr in COIN_LEVEL_ADDR_MAP.items():
            highest = 0
            for name in checked_names:
                if name and name.startswith(f"{level_name} - Coin Bundle "):
                    try:
                        bn = int(name.split("Coin Bundle ")[1])
                        highest = max(highest, bn)
                    except (IndexError, ValueError):
                        pass
            if highest > 0:
                writes.append((addr[0], [min(highest, 255)], "MainRAM"))

        if writes:
            await write(ctx.bizhawk_ctx, writes)
            logger.info(f"[TS2] Restored {len(writes)} progress values from server.")

    # ── DESPAWN SEEDS (server -> Lua, one direction) ──────────
    # Bit-ordering maps. These MUST match the Lua's per-level object order and the
    # check-send mapping exactly (bit i = entry i). Battery/Life are ordered lists;
    # Laser is a single object per level (bit 0); Toy uses the same table as the
    # check-send / restore paths.
    _TOY_DESPAWN_MAP = {
        1:  ("Sheep",           "Andy's House",         ["Basement","Living Room","Kitchen","Attic","Garage"]),
        2:  ("Soldier",         "Andy's Neighborhood",  ["Molehill","Clothes Line","Swing","Pool Plant","Tree"]),
        4:  ("Worker Tike",     "Construction Yard",    ["Wheelbarrow","Filing Cabinets","Bulldozer","Construction Floor 1","Boss Arena"]),
        5:  ("Duck",            "Alleys and Gullies",   ["Pool Behind Construction","Hidden Near Race","Incline Parasol","Window Sill","Rain Gutter"]),
        7:  ("Chick",           "Al's Toy Barn",        ["Complete Race","Gumball Machines","Shipping Boxes","Near Basketballs","End of Long Aisle"]),
        8:  ("Alien",           "Al's Space Land",      ["Ballpit","Planet Mobile","End of Race","Middle of Zurg Aisle","End of Zurg Aisle"]),
        10: ("Mouse",           "Elevator Hop",         ["Electrical Room","Next to Rex","Control Room","Side of Elevator Shaft","Top of Elevator"]),
        11: ("Critter",         "Al's Penthouse",       ["Living Room","Kitchen","Bathroom","Train Bed","Woody Room"]),
        13: ("Passenger Tike",  "Airport Infiltration", ["Near Start","Top of Conveyor Belts","Near Boss Arena","Top of Jet","Scaffolding"]),
        14: ("Luggage",         "Tarmac Trouble",       ["Top of Plane","Zone 2 Cart","Zone 8","Zone 6 Conveyor Belt","Zone 4"]),
    }

    async def _publish_despawn_seeds(self, ctx: "BizHawkClientContext") -> None:
        """Each tick, derive the CURRENT level's collected masks from the server's
        checked_locations and write them to the one-direction despawn-seed bytes.
        The Lua only reads these (to hide already-collected objects). Because the
        client never reads them back and re-derives them from checked_locations
        every tick, this survives a BizHawk reset automatically and can never feed
        a phantom check back to the server."""
        # Build the set of checked location NAMES once.
        loc_map = self._location_map(ctx)
        id_to_name = {v: k for k, v in loc_map.items()}
        checked_names = {id_to_name.get(i) for i in ctx.checked_locations
                         if i in id_to_name}
        if not checked_names:
            return

        # Read the current level id.
        try:
            data = await read(ctx.bizhawk_ctx, [LEVEL_ID_ADDR])
        except Exception:
            return
        level_id = data[0][0]

        def mask_from_list(locs):
            m = 0
            for i, name in enumerate(locs):
                if name in checked_names:
                    m |= (1 << i)
            return m

        writes = []
        # Batteries
        locs = BATTERY_LOCATIONS.get(level_id)
        writes.append((SHARED_DESPAWN_BATTERY[0],
                       [mask_from_list(locs) if locs else 0], "MainRAM"))
        # Lives
        locs = LIFE_LOCATIONS.get(level_id)
        writes.append((SHARED_DESPAWN_LIFE[0],
                       [mask_from_list(locs) if locs else 0], "MainRAM"))
        # Green laser (single object -> bit 0)
        laser_name = LASER_LOCATIONS.get(level_id)
        writes.append((SHARED_DESPAWN_LASER[0],
                       [1 if (laser_name and laser_name in checked_names) else 0],
                       "MainRAM"))
        # Toys
        toy = self._TOY_DESPAWN_MAP.get(level_id)
        toy_mask = 0
        if toy:
            toy_type, level_name, suffixes = toy
            for i, suffix in enumerate(suffixes):
                if f"{level_name} - {toy_type} ({suffix})" in checked_names:
                    toy_mask |= (1 << i)
        writes.append((SHARED_DESPAWN_TOY[0], [toy_mask], "MainRAM"))

        # ── PART-COLLECTED SEED (Missing X pickups) ───────────
        # One bit per Potato-Head level: set when the "Missing X" pickup check is
        # done. The Lua reads this to stop re-spawning that level's part pickup.
        part_collected_bits = [
            (0, "Andy's House - Missing Ear"),
            (1, "Construction Yard - Missing Eye"),
            (2, "Al's Toy Barn - Missing Arm"),
            (3, "Elevator Hop - Missing Foot"),
            (4, "Airport Infiltration - Missing Mouth"),
        ]
        part_mask = 0
        for bit, name in part_collected_bits:
            if name in checked_names:
                part_mask |= (1 << bit)
        writes.append((SHARED_DESPAWN_PART[0], [part_mask], "MainRAM"))

        # Part-exchanged seed (Give Potato Head His X)
        part_exch_bits = [
            (0, "Andy's House - Give Potato Head His Ear"),
            (1, "Construction Yard - Give Potato Head His Eye"),
            (2, "Al's Toy Barn - Give Potato Head His Arm"),
            (3, "Elevator Hop - Give Potato Head His Foot"),
            (4, "Airport Infiltration - Give Potato Head His Mouth"),
        ]
        part_exch_mask = 0
        for bit, name in part_exch_bits:
            if name in checked_names:
                part_exch_mask |= (1 << bit)
        writes.append((SHARED_DESPAWN_PART_EXCH[0], [part_exch_mask], "MainRAM"))

        # ── HINT BLOCK SEED (current level) ───────────────────
        # Bit i = block i of the current level is already checked. The Lua reads
        # this to show the "already found" dialog and to never resend after a
        # reset. Re-derived from checked_locations every tick.
        hint_locs = HINT_LOCATIONS.get(level_id)
        hint_seed = 0
        if hint_locs:
            for i, name in enumerate(hint_locs):
                if name in checked_names:
                    hint_seed |= (1 << i)
        writes.append((SHARED_HINT_SEED[0], [hint_seed & 0xFF, (hint_seed >> 8) & 0xFF], "MainRAM"))

        # ── REX SEED (re-assert every tick) ───────────────────
        # The Lua merges these one-direction seed bytes into its rex mask. They
        # were previously only written once on connect, so a mid-level reset wiped
        # Rex's "already talked" state. Re-derive from checked_locations every tick.
        rex_low = 0
        rex_high = 0
        for (byte_key, bit), loc_name in REX_LOCATIONS.items():
            if loc_name in checked_names:
                if byte_key == "low":
                    rex_low |= (1 << bit)
                else:
                    rex_high |= (1 << bit)
        writes.append((SHARED_REX_SEED_LOW[0], [rex_low], "MainRAM"))
        writes.append((SHARED_REX_SEED_HIGH[0], [rex_high], "MainRAM"))

        # ── BOSS DEFEAT MASK (re-assert every tick) ───────────
        # The Lua WRITES this same byte the instant a boss's HP hits 0 (outward
        # detection). We must NOT overwrite it with a server-only mask, or we'd
        # wipe a freshly-set defeat bit before its check has sent — which is
        # exactly what made Slime Time (single-frame 99->0) never send while
        # Bombs Away (won the tick-ordering race) happened to work. Instead we OR
        # the server-confirmed bits onto whatever the Lua currently has set: we
        # only ever ADD confirmed defeats, never CLEAR a just-detected one. The
        # check-send path dedups against the server, so re-asserting is safe.
        boss_bits = {
            "Bombs Away! - Defeat Reward 1":           0,
            "Slime Time - Defeat Reward 1":            1,
            "Toy Barn Encounter - Defeat Reward 1":    2,
            "The Evil Emperor Zurg - Defeat Reward 1": 3,
        }
        server_boss_mask = 0
        for loc_name, bit in boss_bits.items():
            if loc_name in checked_names:
                server_boss_mask |= (1 << bit)
        try:
            cur_boss_mask = (await read(ctx.bizhawk_ctx, [SHARED_BOSS_DEFEATS]))[0][0]
        except Exception:
            cur_boss_mask = 0
        writes.append((SHARED_BOSS_DEFEATS[0], [cur_boss_mask | server_boss_mask], "MainRAM"))

        # ── MISSING PARTS (re-assert every tick) ──────────────
        # Keep Potato Head's collected/exchanged state in sync with the server so
        # his dialog persists through a mid-level reset (previously only restored
        # once on connect). Re-asserting already-checked locations is safe: the
        # check-send path dedups against checked_locations.
        for collected_addr, exchanged_addr, found_loc, given_loc in PARTS_RESTORE:
            if found_loc in checked_names:
                writes.append((collected_addr[0], [1], "MainRAM"))
            if given_loc in checked_names:
                writes.append((exchanged_addr[0], [1], "MainRAM"))

        await write(ctx.bizhawk_ctx, writes)

    # ── CHECK LOCATIONS ───────────────────────────────────────

    async def _scout_locations(self, ctx: "BizHawkClientContext") -> None:
        """Scout the locations that ACTUALLY EXIST in this seed so
        ctx.locations_info gets filled with {location_id: NetworkItem}. The
        on-screen 'sent' feed reads that to show the item at a checked location.

        Only the server-known set is valid: ctx.missing_locations together with
        ctx.checked_locations. Scouting IDs that weren't placed in this generation
        crashes the server with a KeyError, so we never scout the apworld's full
        list. Runs once per connection."""
        if getattr(self, "_scouts_sent", False):
            return
        valid = set(getattr(ctx, "missing_locations", set())) \
            | set(getattr(ctx, "checked_locations", set()))
        if not valid:
            # Server hasn't sent the location sets yet; try again next tick.
            return
        self._scouts_sent = True
        try:
            await ctx.send_msgs([{
                "cmd": "LocationScouts",
                "locations": list(valid),
                "create_as_hint": 0,
            }])
        except Exception:
            # If the send fails, allow a retry on a later tick.
            self._scouts_sent = False

    async def _check_locations(self, ctx: "BizHawkClientContext") -> None:
        new_checks = set()

        reads = await read(ctx.bizhawk_ctx, [
            LEVEL_ID_ADDR,
            SHARED_EAR_COLLECTED,
            SHARED_EYE_COLLECTED,
            SHARED_ARM_COLLECTED,
            SHARED_FOOT_COLLECTED,
            SHARED_MOUTH_COLLECTED,
            SHARED_REX_LOW,
            SHARED_REX_HIGH,
            SHARED_EAR_EXCHANGED,
            SHARED_EYE_EXCHANGED,
            SHARED_ARM_EXCHANGED,
            SHARED_FOOT_EXCHANGED,
            SHARED_MOUTH_EXCHANGED,
            SHARED_BOSS_DEFEATS,
            CUTSCENE_ACTIVE_ADDR,
            SHARED_HINT_MASK,
        ])

        level_id    = reads[0][0]

        # Pause ALL location-check scanning while a cutscene is ACTUALLY on screen
        # (the Lua gates this flag on the game's real cutscene-state byte): the
        # cutscene corrupts collectible/token memory, which fired phantom checks.
        if reads[14][0] == 1:
            return

        # Guard: only scan for checks during real gameplay. On the title screen,
        # BIOS boot, or loading screens the RAM holds uninitialised/garbage values
        # that can look like collected items. We require having seen the map (16)
        # or a real level (1-15) at least once this session before trusting reads.
        if 1 <= level_id <= 16:
            self._gameplay_started = True

        if not getattr(self, "_gameplay_started", False):
            return

        valid_state = (1 <= level_id <= 16) or (level_id in BOSS_DEFEAT_SCREENS)
        if not valid_state:
            self._last_seen_level = level_id
            self._level_stable_ticks = 0
            return

        # Level-load settling guard: when the level ID changes, the game is still
        # loading and collectible memory is transient. Wait for the level ID to be
        # stable across several consecutive watcher ticks before trusting reads.
        if level_id != self._last_seen_level:
            self._last_seen_level = level_id
            self._level_stable_ticks = 0
            return
        self._level_stable_ticks += 1
        if self._level_stable_ticks < 15:
            return

        ear_coll    = reads[1][0]
        eye_coll    = reads[2][0]
        arm_coll    = reads[3][0]
        foot_coll   = reads[4][0]
        mouth_coll  = reads[5][0]
        rex_low     = reads[6][0]
        rex_high    = reads[7][0]
        ear_exch    = reads[8][0]
        eye_exch    = reads[9][0]
        arm_exch    = reads[10][0]
        foot_exch   = reads[11][0]
        mouth_exch  = reads[12][0]

        # ── BOSS DEFEATS ──────────────────────────────────────
        # Use the bitmask the Lua sets when the boss's HP actually reaches 0
        # DURING the fight (not the boss-defeated screen, which fired regardless
        # of HP and mismatched the reward). Lua bit assignments:
        #   bit0 = Bombs Away (level 6)
        #   bit1 = Slime Time (level 3)
        #   bit2 = Toy Barn Encounter (level 9)
        #   bit3 = Evil Emperor Zurg (level 12)
        boss_defeat_mask = reads[13][0]
        boss_bit_rewards = {
            0: ["Bombs Away! - Defeat Reward 1", "Bombs Away! - Defeat Reward 2"],
            1: ["Slime Time - Defeat Reward 1", "Slime Time - Defeat Reward 2"],
            2: ["Toy Barn Encounter - Defeat Reward 1", "Toy Barn Encounter - Defeat Reward 2"],
            3: ["The Evil Emperor Zurg - Defeat Reward 1", "The Evil Emperor Zurg - Defeat Reward 2"],
        }
        for bit, loc_names in boss_bit_rewards.items():
            if (boss_defeat_mask >> bit) & 1:
                for loc_name in loc_names:
                    loc_id = self._location_map(ctx).get(loc_name)
                    if loc_id is not None:
                        new_checks.add(loc_id)

        # ── PROSPECTOR GOAL ───────────────────────────────────
        if level_id == 15:
            # Prospector level — check for defeat (we rely on Lua boss script)
            pass

        # ── MISSING PARTS ─────────────────────────────────────
        # Two separate checks per part:
        #   "Missing X"            -> sent when Buzz picks up the part (collected)
        #   "Give Potato Head His X"-> sent when Buzz turns it in (exchanged)
        part_checks = [
            (ear_coll,   ear_exch,   "Andy's House - Missing Ear",            "Andy's House - Give Potato Head His Ear"),
            (eye_coll,   eye_exch,   "Construction Yard - Missing Eye",       "Construction Yard - Give Potato Head His Eye"),
            (arm_coll,   arm_exch,   "Al's Toy Barn - Missing Arm",           "Al's Toy Barn - Give Potato Head His Arm"),
            (foot_coll,  foot_exch,  "Elevator Hop - Missing Foot",           "Elevator Hop - Give Potato Head His Foot"),
            (mouth_coll, mouth_exch, "Airport Infiltration - Missing Mouth",  "Airport Infiltration - Give Potato Head His Mouth"),
        ]
        for collected, exchanged, found_loc, given_loc in part_checks:
            if collected == 1:
                loc_id = self._location_map(ctx).get(found_loc)
                if loc_id is not None:
                    new_checks.add(loc_id)
            if exchanged == 1:
                loc_id = self._location_map(ctx).get(given_loc)
                if loc_id is not None:
                    new_checks.add(loc_id)

        # ── REX SANITY ────────────────────────────────────────
        # Only scan rex when actually IN a rex level. During the map-load hitch
        # the game corrupts the rex bytes (0x1FF9C4/C5) and the client could read
        # that garbage between the game's write and the Lua's clean re-write,
        # firing phantom rex checks (this bug recurred on map loading). Rex levels
        # are the toy/coin levels: 1,2,4,5,7,8,10,11,13,14.
        # Capture the connect-time rex baseline on the first scan after connect
        # (before the player could reach a Rex), so stale leftover bits from a
        # previous seed / save state are masked out of sends below.
        if self.slot_data.get("rexsanity", 0) and self._rex_baseline_low is None:
            self._rex_baseline_low = rex_low
            self._rex_baseline_high = rex_high

        REX_LEVELS = {1, 2, 4, 5, 7, 8, 10, 11, 13, 14}
        if self.slot_data.get("rexsanity", 0) and level_id in REX_LEVELS:
            # Only consider bits that turned on AFTER connect (genuine new talks).
            eff_low  = rex_low  & ~(self._rex_baseline_low or 0)
            eff_high = rex_high & ~(self._rex_baseline_high or 0)
            rex_level_map_low = {
                "Andy's House - Talk to Rex":       (eff_low, 0),
                "Andy's Neighborhood - Talk to Rex":(eff_low, 1),
                "Construction Yard - Talk to Rex":  (eff_low, 2),
                "Alleys and Gullies - Talk to Rex": (eff_low, 3),
                "Al's Toy Barn - Talk to Rex":      (eff_low, 4),
                "Al's Space Land - Talk to Rex":    (eff_low, 5),
            }
            rex_level_map_high = {
                "Elevator Hop - Talk to Rex":       (eff_high, 0),
                "Al's Penthouse - Talk to Rex":     (eff_high, 1),
                "Airport Infiltration - Talk to Rex":(eff_high, 2),
                "Tarmac Trouble - Talk to Rex":     (eff_high, 3),
            }
            for loc_name, (byte_val, bit) in {**rex_level_map_low, **rex_level_map_high}.items():
                if (byte_val >> bit) & 1:
                    loc_id = self._location_map(ctx).get(loc_name)
                    if loc_id is not None:
                        new_checks.add(loc_id)

        # ── HINT BLOCK SANITY ─────────────────────────────────
        # The Lua publishes the CURRENT level's touched-block mask (bit i = block i
        # of this level was touched). Map each set bit to that level's hint location
        # and send it. One-direction (Lua only sets bits from genuine detection), so
        # no phantom risk; already-sent checks are deduped against checked_locations.
        if self.slot_data.get("hint_block_sanity", 0):
            hint_raw = reads[15]
            hint_mask = hint_raw[0] | (hint_raw[1] << 8)
            hint_locs = HINT_LOCATIONS.get(level_id)
            if hint_locs and hint_mask:
                for i, loc_name in enumerate(hint_locs):
                    if (hint_mask >> i) & 1:
                        loc_id = self._location_map(ctx).get(loc_name)
                        if loc_id is not None:
                            new_checks.add(loc_id)
        toy_level_map = {
            1:  ("Sheep",           "Andy's House",         ["Basement","Living Room","Kitchen","Attic","Garage"]),
            2:  ("Soldier",         "Andy's Neighborhood",  ["Molehill","Clothes Line","Swing","Pool Plant","Tree"]),
            4:  ("Worker Tike",     "Construction Yard",    ["Wheelbarrow","Filing Cabinets","Bulldozer","Construction Floor 1","Boss Arena"]),
            5:  ("Duck",            "Alleys and Gullies",   ["Pool Behind Construction","Hidden Near Race","Incline Parasol","Window Sill","Rain Gutter"]),
            7:  ("Chick",           "Al's Toy Barn",        ["Complete Race","Gumball Machines","Shipping Boxes","Near Basketballs","End of Long Aisle"]),
            8:  ("Alien",           "Al's Space Land",      ["Ballpit","Planet Mobile","End of Race","Middle of Zurg Aisle","End of Zurg Aisle"]),
            10: ("Mouse",           "Elevator Hop",         ["Electrical Room","Next to Rex","Control Room","Side of Elevator Shaft","Top of Elevator"]),
            11: ("Critter",         "Al's Penthouse",       ["Living Room","Kitchen","Bathroom","Train Bed","Woody Room"]),
            13: ("Passenger Tike",  "Airport Infiltration", ["Near Start","Top of Conveyor Belts","Near Boss Arena","Top of Jet","Scaffolding"]),
            14: ("Luggage",         "Tarmac Trouble",       ["Top of Plane","Zone 2 Cart","Zone 8","Zone 6 Conveyor Belt","Zone 4"]),
        }

        # ── MISSING TOYS ──────────────────────────────────────
        # Only scan the toys for the level we are currently in. On the map and
        # other levels the shared masks are not meaningful for this level.
        for level_id_key, (toy_type, level_name, locations) in toy_level_map.items():
            if level_id != level_id_key:
                continue
            addr = SHARED_TOY_COLLECTED.get(level_id_key)
            if addr is None:
                continue
            toy_data = await read(ctx.bizhawk_ctx, [addr])
            collected_mask = toy_data[0][0]
            for i, loc_suffix in enumerate(locations):
                if (collected_mask >> i) & 1:
                    loc_name = f"{level_name} - {toy_type} ({loc_suffix})"
                    loc_id = self._location_map(ctx).get(loc_name)
                    if loc_id is not None:
                        new_checks.add(loc_id)

        # ── BATTERY SANITY ────────────────────────────────────
        if self.slot_data.get("batterysanity", 0):
            battery_locations = {
                1:  [
                    "Andy's House - Battery (Andy's Room)",
                    "Andy's House - Battery (Attic)",
                    "Andy's House - Battery (Basement)",
                    "Andy's House - Battery (Garage)",
                    "Andy's House - Battery (Living Room)",
                    "Andy's House - Battery (Handrail)",
                ],
                2:  [
                    "Andy's Neighborhood - Battery (Lawnmower Yard)",
                    "Andy's Neighborhood - Battery (Washing Machine)",
                    "Andy's Neighborhood - Battery (Pool Yard)",
                    "Andy's Neighborhood - Battery (Swing)",
                    "Andy's Neighborhood - Battery (Top of Tree)",
                ],
                6:  [
                    "Bombs Away! - Battery (Back Right)",
                    "Bombs Away! - Battery (Back Left)",
                    "Bombs Away! - Battery (Front Left)",
                    "Bombs Away! - Battery (Front Right)",
                ],
                4:  [
                    "Construction Yard - Battery (Bulldozer)",
                    "Construction Yard - Battery (Boss Arena Front Left)",
                    "Construction Yard - Battery (Boss Arena Back Left)",
                    "Construction Yard - Battery (Boss Arena Back Right)",
                ],
                5:  [
                    "Alleys and Gullies - Battery (Behind Construction)",
                    "Alleys and Gullies - Battery (Balcony Fence)",
                    "Alleys and Gullies - Battery (Boss Arena)",
                ],
                7:  [
                    "Al's Toy Barn - Battery (Gumball Machine)",
                    "Al's Toy Barn - Battery (Ventilation Shaft)",
                    "Al's Toy Barn - Battery (Between Bicycles)",
                    "Al's Toy Barn - Battery (Cardboard Boxes)",
                    "Al's Toy Barn - Battery (Boss Arena)",
                ],
                8:  [
                    "Al's Space Land - Battery (Boss Arena)",
                    "Al's Space Land - Battery (Arcade Cabinet)",
                    "Al's Space Land - Battery (Blue Shelves)",
                    "Al's Space Land - Battery (Red Shelf)",
                    "Al's Space Land - Battery (Race Blue Shelf)",
                ],
                9:  [
                    "Toy Barn Encounter - Battery (South)",
                    "Toy Barn Encounter - Battery (North)",
                    "Toy Barn Encounter - Battery (East)",
                    "Toy Barn Encounter - Battery (West)",
                ],
                11: [
                    "Al's Penthouse - Battery (Under Table)",
                    "Al's Penthouse - Battery (Bathroom)",
                    "Al's Penthouse - Battery (Kitchen)",
                    "Al's Penthouse - Battery (Train Bed)",
                    "Al's Penthouse - Battery (Television)",
                ],
                13: [
                    "Airport Infiltration - Battery (Luggage Pile)",
                    "Airport Infiltration - Battery (Near Hidden Token)",
                    "Airport Infiltration - Battery (Boss Arena)",
                ],
                14: [
                    "Tarmac Trouble - Battery (Road Opposite Zone 8)",
                    "Tarmac Trouble - Battery (Helicopter Pad)",
                    "Tarmac Trouble - Battery (Zone 3)",
                    "Tarmac Trouble - Battery (Green Slime Maze)",
                    "Tarmac Trouble - Battery (Boss Arena)",
                ],
            }
            for level_key, locs in battery_locations.items():
                if level_id != level_key:
                    continue
                addr = SHARED_BATTERY.get(level_key)
                if addr is None:
                    continue
                batt_data = await read(ctx.bizhawk_ctx, [addr])
                mask = batt_data[0][0]
                for i, loc_name in enumerate(locs):
                    if (mask >> i) & 1:
                        loc_id = self._location_map(ctx).get(loc_name)
                        if loc_id is not None:
                            new_checks.add(loc_id)

        # ── LIFE SANITY ───────────────────────────────────────
        if self.slot_data.get("lifesanity", 0):
            life_locations = {
                1:  ["Andy's House - Life (Crib)", "Andy's House - Life (Living Room)", "Andy's House - Life (Garage)"],
                2:  ["Andy's Neighborhood - Life (Top of Swing)"],
                4:  ["Construction Yard - Life (Top of Bulldozer)", "Construction Yard - Life (Roof of Green Building)"],
                5:  ["Alleys and Gullies - Life (Pool Behind Construction)", "Alleys and Gullies - Life (Lily Pad Behind Race)", "Alleys and Gullies - Life (Window Sill)"],
                7:  ["Al's Toy Barn - Life (Tennis Ball Isle)"],
                8:  ["Al's Space Land - Life (Planet Mobile)"],
                11: ["Al's Penthouse - Life (Fireplace)"],
                14: ["Tarmac Trouble - Life (Zone 6)"],
            }
            for level_key, locs in life_locations.items():
                if level_id != level_key:
                    continue
                addr = SHARED_LIFE.get(level_key)
                if addr is None:
                    continue
                life_data = await read(ctx.bizhawk_ctx, [addr])
                mask = life_data[0][0]
                for i, loc_name in enumerate(locs):
                    if (mask >> i) & 1:
                        loc_id = self._location_map(ctx).get(loc_name)
                        if loc_id is not None:
                            new_checks.add(loc_id)

        # ── GREEN LASER SANITY ────────────────────────────────
        if self.slot_data.get("green_laser_sanity", 0):
            laser_locations = {
                1:  "Andy's House - Green Laser",
                2:  "Andy's Neighborhood - Green Laser",
                3:  "Slime Time - Green Laser",
                4:  "Construction Yard - Green Laser",
                5:  "Alleys and Gullies - Green Laser",
                7:  "Al's Toy Barn - Green Laser",
                8:  "Al's Space Land - Green Laser",
                10: "Elevator Hop - Green Laser",
                11: "Al's Penthouse - Green Laser",
                13: "Airport Infiltration - Green Laser",
                14: "Tarmac Trouble - Green Laser",
            }
            for level_key, loc_name in laser_locations.items():
                if level_id != level_key:
                    continue
                addr = SHARED_LASER_SANITY.get(level_key)
                if addr is None:
                    continue
                laser_data = await read(ctx.bizhawk_ctx, [addr])
                if laser_data[0][0] & 1:
                    loc_id = self._location_map(ctx).get(loc_name)
                    if loc_id is not None:
                        new_checks.add(loc_id)

        # ── COIN BUNDLES ──────────────────────────────────────
        if self.slot_data.get("coinsanity", 0):
            # Map the current level_id to its coin level name + address. Only the
            # level we are actually in has a meaningful coin counter; reading the
            # others returns stale/garbage values (this caused mass phantom sends
            # on the map screen).
            coin_level_by_id = {
                1:  ("Andy's House",         SHARED_COINS_ANDYS_HOUSE),
                2:  ("Andy's Neighborhood",  SHARED_COINS_NEIGHBORHOOD),
                4:  ("Construction Yard",    SHARED_COINS_CONSTRUCTION),
                5:  ("Alleys and Gullies",   SHARED_COINS_ALLEYS),
                7:  ("Al's Toy Barn",        SHARED_COINS_TOY_BARN),
                8:  ("Al's Space Land",      SHARED_COINS_SPACE_LAND),
                10: ("Elevator Hop",         SHARED_COINS_ELEVATOR),
                11: ("Al's Penthouse",       SHARED_COINS_PENTHOUSE),
                13: ("Airport Infiltration", SHARED_COINS_AIRPORT),
                14: ("Tarmac Trouble",       SHARED_COINS_TARMAC),
            }
            entry = coin_level_by_id.get(level_id)
            if entry is not None:
                level_name, addr = entry
                coin_data = await read(ctx.bizhawk_ctx, [addr])
                bundles_collected = coin_data[0][0]
                for bn in range(1, bundles_collected + 1):
                    loc_name = f"{level_name} - Coin Bundle {bn}"
                    loc_id = self._location_map(ctx).get(loc_name)
                    if loc_id is not None:
                        new_checks.add(loc_id)

        # ── PIZZA PLANET TOKENS (Hamm's/Missing Toys/Race/Hidden/Boss) ─────
        # The Lua publishes collected token bits per hover_id. Only the current
        # level's hover is meaningful, so map level_id -> hover_id and read that.
        token_hover = TOKEN_HOVER_BY_LEVEL.get(level_id)
        if token_hover is not None:
            t_addr = SHARED_TOKENS_COLLECTED.get(token_hover)
            level_name = TOKEN_LEVEL_NAME_BY_LEVEL.get(level_id)
            if t_addr is not None and level_name is not None:
                tok_data = await read(ctx.bizhawk_ctx, [t_addr])
                tok_bits = tok_data[0][0]
                for bit_val, token_name in TOKEN_BIT_TO_NAME.items():
                    if tok_bits & bit_val:
                        loc_name = f"{level_name} - {token_name}"
                        loc_id = self._location_map(ctx).get(loc_name)
                        if loc_id is not None:
                            new_checks.add(loc_id)

        # Send new checks.
        #
        # IMPORTANT: dedup against the SERVER-AUTHORITATIVE ctx.checked_locations,
        # never an optimistic local set. The old code marked checks done in
        # self.checked_locations *before* the send was confirmed; if that send was
        # ever dropped (a transient stall, or a race during a level transition),
        # the location was buried forever — it could never re-fire, because the
        # local set said "already done." That silently lost checks (batteries that
        # never sent) and, for session-only state like the boss-defeat bitmask,
        # soft-locked the seed (after a reset the boss isn't re-fought, so the bit
        # never returns and the reward is unrecoverable).
        #
        # Fix: re-send every detected-but-unconfirmed check each tick. AP's
        # LocationChecks is idempotent, so resending costs nothing once the server
        # has recorded them (they fall out of this diff the moment ctx.checked_locations
        # updates). A dropped send simply retries on the next tick — self-healing.
        unconfirmed = new_checks - set(ctx.checked_locations)
        if unconfirmed:
            await ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": list(unconfirmed)
            }])

    # ── DEATH LINK ────────────────────────────────────────────

    async def _handle_death_link(self, ctx: "BizHawkClientContext") -> None:
        data = await read(ctx.bizhawk_ctx, [BUZZ_DEATH_ADDR, SHARED_DEATH_LINK_QUEUE,
                                            LEVEL_ID_ADDR])
        death        = data[0][0]   # 0x0A136E == 2 means Buzz has died (in-level)
        pending_recv = data[1][0]   # deaths still queued for the Lua to apply
        level_id     = data[2][0]
        in_level     = 1 <= level_id <= 15

        is_dead = (death == 2)

        # SEND our own death. Do NOT send if this death was caused by a death link
        # we applied (self._death_from_link) or one still queued/just applied
        # (pending_recv) — that would bounce the death back to the sender.
        if is_dead:
            if (not self.death_link_sent and not self._death_from_link
                    and pending_recv == 0):
                self.death_link_sent = True
                try:
                    await ctx.send_death("Buzz Lightyear has fallen!")
                except Exception:
                    await ctx.send_msgs([{
                        "cmd": "Bounce",
                        "tags": ["DeathLink"],
                        "data": {
                            "time": asyncio.get_event_loop().time(),
                            "cause": "Buzz Lightyear has fallen!",
                            "source": ctx.slot_info[ctx.slot].name,
                        }
                    }])
        else:
            # Buzz is alive again — reset the per-death latches.
            self.death_link_sent = False
            self._death_from_link = False

        # RECEIVE deaths. Only apply them while IN A LEVEL (1-15); otherwise leave
        # them queued in self._pending_deaths until the player loads into a level
        # (killing Buzz on the map / loading screen does nothing useful).
        # RECEIVE deaths. Only apply them while IN A LEVEL (1-15), Buzz is alive,
        # and the level has been STABLE for a while (the same settling guard the
        # check-scanner uses). Without the stability gate, a death could be applied
        # on the level's loading screen — Buzz "dies" before you have control, the
        # death byte sticks, and you can't press Start/X to continue past the load.
        stable = getattr(self, "_level_stable_ticks", 0) >= 15
        if (getattr(self, "_pending_deaths", 0) > 0 and in_level
                and not is_dead and stable):
            self._pending_deaths -= 1
            cur = (await read(ctx.bizhawk_ctx, [SHARED_DEATH_LINK_QUEUE]))[0][0]
            await write(ctx.bizhawk_ctx, [
                (SHARED_DEATH_LINK_QUEUE[0], [min(cur + 1, 255)], "MainRAM")
            ])
            # Mark that the death now about to occur came from a link, so the send
            # logic above won't bounce it back.
            self._death_from_link = True

    # ── CHECK GOAL ────────────────────────────────────────────

    async def _check_goal(self, ctx: "BizHawkClientContext") -> None:
        if ctx.finished_game:
            return
        if not getattr(self, "_gameplay_started", False):
            return
        data = await read(ctx.bizhawk_ctx, [LEVEL_ID_ADDR])
        level_id = data[0][0]
        # Prospector defeat screen is level 47
        if level_id == 47:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

    # ── ON-SCREEN ITEM FEED ───────────────────────────────────

    def _player_name(self, ctx, slot) -> str:
        """Best-effort player name for a slot number."""
        try:
            names = getattr(ctx, "player_names", None)
            if names and slot in names:
                return names[slot]
        except Exception:
            pass
        return f"Player {slot}"

    async def _push_feed(self, ctx, message: str) -> None:
        """Write a message to the on-screen feed buffer and bump the sequence
        byte so the Lua picks it up and shows it top-right. The message is encoded
        as alternating text|color|text|color... segments; color codes are single
        letters (w=white, g=green item, c=cyan player, y=yellow location)."""
        msg = message[:120]
        self._feed_seq = (self._feed_seq + 1) % 256
        data = list(msg.encode("ascii", "replace")) + [0]  # null-terminated
        await write(ctx.bizhawk_ctx,
                    [(FEED_TEXT_BASE, data, "MainRAM"),
                     (FEED_SEQ_ADDR[0], [self._feed_seq], "MainRAM")])

    async def _update_item_feed(self, ctx: "BizHawkClientContext") -> None:
        # ── Select-button mode cycle ──────────────────────────
        # The Lua bumps FEED_CYCLE_ADDR on each debounced Select press. Read it and
        # advance the mode (Off->Sent->Received->Both->Off) whenever it changes,
        # announcing the new mode on screen. This runs even when the feed is Off so
        # the player can cycle it back on.
        MODE_NAMES = {0: "Off", 1: "Sent", 2: "Received", 3: "Both"}
        try:
            cyc = (await read(ctx.bizhawk_ctx, [FEED_CYCLE_ADDR]))[0][0]
        except Exception:
            cyc = None
        if cyc is not None:
            if self._feed_cycle_seen is None:
                # First read: establish baseline without cycling.
                self._feed_cycle_seen = cyc
            elif cyc != self._feed_cycle_seen:
                # One or more presses since last tick: advance one step per press.
                steps = (cyc - self._feed_cycle_seen) % 256
                self._feed_cycle_seen = cyc
                self.feed_mode = (self.feed_mode + steps) % 4
                # Keep baselines current so the mode we land on doesn't immediately
                # dump a backlog of activity that happened under the previous mode.
                self._feed_item_index = len(ctx.items_received)
                self._feed_checked = set(ctx.checked_locations)
                # Announce the new mode and RETURN this tick. Returning is what makes
                # the announcement appear INSTANTLY: if we fell through, a pending
                # received-item / sent-check message would overwrite the feed buffer
                # in the same tick (only the last write per tick survives for the Lua
                # to read), so the mode text would only show when nothing else was
                # queued. The pending event surfaces on the next tick instead.
                await self._push_feed(
                    ctx, f"Item Feed: |w|{MODE_NAMES.get(self.feed_mode, '?')}|g|")
                return

        mode = getattr(self, "feed_mode", self.slot_data.get("on_screen_item_feed", 2))

        # First pass after connect: sync baselines WITHOUT announcing the backlog
        # of already-received items / already-checked locations. (Done regardless
        # of mode so toggling on later doesn't dump the whole history.)
        if not getattr(self, "_feed_inited", False):
            self._feed_item_index = len(ctx.items_received)
            self._feed_checked = set(ctx.checked_locations)
            self._feed_inited = True
            return

        if mode == 0:
            # Off: keep baselines current so cycling back on doesn't dump a backlog.
            self._feed_item_index = len(ctx.items_received)
            self._feed_checked = set(ctx.checked_locations)
            return

        # Show only ONE message per tick (the most recent new event), so messages
        # don't stomp each other; the rest will surface on following ticks.

        # RECEIVED items (mode 2 = received, 3 = both)
        if mode in (2, 3) and len(ctx.items_received) > self._feed_item_index:
            item = ctx.items_received[self._feed_item_index]
            self._feed_item_index += 1
            iname = ctx.item_names.lookup_in_game(item.item) or "Unknown"
            sender = self._player_name(ctx, getattr(item, "player", 0))
            # Color the item by category (AP NetworkItem.flags bitfield):
            #   trap (0b100) -> red, progression (0b001) -> green,
            #   filler (flags == 0) -> light blue, anything else -> purple.
            flags = getattr(item, "flags", 0)
            if flags & 0b100:
                icol = "r"   # trap
            elif flags & 0b001:
                icol = "g"   # progression
            elif flags == 0:
                icol = "b"   # filler (light blue)
            else:
                icol = "p"   # useful / other -> purple
            await self._push_feed(ctx, f"Got |w|{iname}|{icol}| from |w|{sender}|c|")
            return

        # SENT checks (mode 1 = sent, 3 = both)
        if mode in (1, 3):
            new_checked = set(ctx.checked_locations) - self._feed_checked
            if new_checked:
                loc_id = sorted(new_checked)[0]
                self._feed_checked.add(loc_id)
                # Prefer showing WHAT ITEM was at this location (and who it went to)
                # rather than the location's own name. ctx.locations_info is filled
                # by the LocationScouts we send on connect.
                info = None
                try:
                    info = getattr(ctx, "locations_info", {}).get(loc_id)
                except Exception:
                    info = None
                if info is not None:
                    recipient_slot = getattr(info, "player", 0)
                    # Skip self->self sends: when an item we placed is for ourselves,
                    # the "Got ... from [you]" received line already covers it, so the
                    # "Sent ... to [you]" line is redundant. Sends to OTHER players
                    # still show.
                    if ctx.slot_concerns_self(recipient_slot):
                        return
                    # Look the item up in the RECIPIENT'S game (lookup_in_slot), not
                    # our own — an item sent to another player belongs to their
                    # game's item table, so lookup_in_game would return "Unknown".
                    iname = None
                    try:
                        iname = ctx.item_names.lookup_in_slot(info.item, recipient_slot)
                    except Exception:
                        iname = None
                    if not iname:
                        iname = ctx.item_names.lookup_in_game(info.item) or "Unknown"
                    recipient = self._player_name(ctx, recipient_slot)
                    flags = getattr(info, "flags", 0)
                    if flags & 0b100:
                        icol = "r"   # trap
                    elif flags & 0b001:
                        icol = "g"   # progression
                    elif flags == 0:
                        icol = "b"   # filler
                    else:
                        icol = "p"   # useful / other
                    # "Sent <item> to <recipient>"
                    await self._push_feed(ctx, f"Sent |w|{iname}|{icol}| to |w|{recipient}|c|")
                else:
                    # Fallback: location not scouted yet — show the location name.
                    loc_name = ctx.location_names.lookup_in_game(loc_id) \
                        if hasattr(ctx, "location_names") else str(loc_id)
                    await self._push_feed(ctx, f"Sent |w|{loc_name}|y|")
                return