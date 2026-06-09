from typing import Dict, Optional, NamedTuple
from BaseClasses import ItemClassification
import BaseClasses


class TS2ItemData(NamedTuple):
    code: Optional[int]
    classification: ItemClassification


class ToyStory2Item(BaseClasses.Item):
    game = "Toy Story 2"


# ============================================================
# BASE ID
# ============================================================
BASE_ID = 0x75320000


# ============================================================
# ITEM TABLE
# ============================================================
# Classification shortcuts
prog  = ItemClassification.progression
use   = ItemClassification.useful
filler = ItemClassification.filler
trap  = ItemClassification.trap

ITEM_TABLE: Dict[str, TS2ItemData] = {

    # -- MOVES (Movesanity) --
    "Progressive Laser":        TS2ItemData(BASE_ID + 0,  prog),
    "Spin":                     TS2ItemData(BASE_ID + 1,  prog),
    "Stomp":                    TS2ItemData(BASE_ID + 2,  prog),
    "Double Jump":              TS2ItemData(BASE_ID + 3,  prog),
    "Pole Climb":               TS2ItemData(BASE_ID + 4,  prog),
    "Ledge Grab":               TS2ItemData(BASE_ID + 5,  prog),
    "Pole Vault":               TS2ItemData(BASE_ID + 6,  prog),
    "Push":                     TS2ItemData(BASE_ID + 7,  prog),
    "Rope Sliding":             TS2ItemData(BASE_ID + 8,  prog),
    "Visor":                    TS2ItemData(BASE_ID + 9,  prog),

    # -- GADGETS --
    "Cosmic Shield - Andy's House":         TS2ItemData(BASE_ID + 10, use),
    "Rocket Boots - Andy's Neighborhood":   TS2ItemData(BASE_ID + 11, prog),
    "Disc Launcher - Construction Yard":    TS2ItemData(BASE_ID + 12, prog),
    "Grappling Hook - Alleys and Gullies":  TS2ItemData(BASE_ID + 13, prog),
    "Disc Launcher - Alleys and Gullies":   TS2ItemData(BASE_ID + 14, prog),
    "Rocket Boots - Alleys and Gullies":    TS2ItemData(BASE_ID + 15, prog),
    "Rocket Boots - Al's Toy Barn":         TS2ItemData(BASE_ID + 16, prog),
    "Disc Launcher - Al's Toy Barn":        TS2ItemData(BASE_ID + 17, prog),
    "Hover Boots - Al's Toy Barn":          TS2ItemData(BASE_ID + 18, prog),
    "Cosmic Shield - Al's Space Land":      TS2ItemData(BASE_ID + 19, use),
    "Grappling Hook - Elevator Hop":        TS2ItemData(BASE_ID + 20, prog),
    "Cosmic Shield - Al's Penthouse":       TS2ItemData(BASE_ID + 21, prog),
    "Hover Boots - Airport Infiltration":   TS2ItemData(BASE_ID + 22, prog),
    "Rocket Boots - Tarmac Trouble":        TS2ItemData(BASE_ID + 23, use),

    # -- MISSING PARTS --
    "Missing Ear":              TS2ItemData(BASE_ID + 24, prog),
    "Missing Eye":              TS2ItemData(BASE_ID + 25, prog),
    "Missing Arm":              TS2ItemData(BASE_ID + 26, prog),
    "Missing Foot":             TS2ItemData(BASE_ID + 27, prog),
    "Missing Mouth":            TS2ItemData(BASE_ID + 28, prog),

    # -- FINAL SHOWDOWN TICKETS --
    "Final Showdown Ticket":    TS2ItemData(BASE_ID + 29, prog),

    # -- LEVEL UNLOCKS (Open Mode only) --
    "Andy's House Unlock":              TS2ItemData(BASE_ID + 30, prog),
    "Andy's Neighborhood Unlock":       TS2ItemData(BASE_ID + 31, prog),
    "Bombs Away! Unlock":               TS2ItemData(BASE_ID + 32, prog),
    "Construction Yard Unlock":         TS2ItemData(BASE_ID + 33, prog),
    "Alleys and Gullies Unlock":        TS2ItemData(BASE_ID + 34, prog),
    "Slime Time Unlock":                TS2ItemData(BASE_ID + 35, prog),
    "Al's Toy Barn Unlock":             TS2ItemData(BASE_ID + 36, prog),
    "Al's Space Land Unlock":           TS2ItemData(BASE_ID + 37, prog),
    "Toy Barn Encounter Unlock":        TS2ItemData(BASE_ID + 38, prog),
    "Elevator Hop Unlock":              TS2ItemData(BASE_ID + 39, prog),
    "Al's Penthouse Unlock":            TS2ItemData(BASE_ID + 40, prog),
    "The Evil Emperor Zurg Unlock":     TS2ItemData(BASE_ID + 41, prog),
    "Airport Infiltration Unlock":      TS2ItemData(BASE_ID + 42, prog),
    "Tarmac Trouble Unlock":            TS2ItemData(BASE_ID + 43, prog),
    "Final Showdown Unlock":            TS2ItemData(BASE_ID + 44, prog),

    # -- PIZZA PLANET TOKENS --
    "Pizza Planet Token":       TS2ItemData(BASE_ID + 45, prog),

    # -- COIN BUNDLES (Coinsanity) --
    "Coin Bundle - Andy's House":           TS2ItemData(BASE_ID + 46, prog),
    "Coin Bundle - Andy's Neighborhood":    TS2ItemData(BASE_ID + 47, prog),
    "Coin Bundle - Construction Yard":      TS2ItemData(BASE_ID + 48, prog),
    "Coin Bundle - Alleys and Gullies":     TS2ItemData(BASE_ID + 49, prog),
    "Coin Bundle - Al's Toy Barn":          TS2ItemData(BASE_ID + 50, prog),
    "Coin Bundle - Al's Space Land":        TS2ItemData(BASE_ID + 51, prog),
    "Coin Bundle - Elevator Hop":           TS2ItemData(BASE_ID + 52, prog),
    "Coin Bundle - Al's Penthouse":         TS2ItemData(BASE_ID + 53, prog),
    "Coin Bundle - Airport Infiltration":   TS2ItemData(BASE_ID + 54, prog),
    "Coin Bundle - Tarmac Trouble":         TS2ItemData(BASE_ID + 55, prog),

    # -- TRAPS --
    "Freeze Buzz Trap":             TS2ItemData(BASE_ID + 56, trap),
    "Damage Buzz Trap":             TS2ItemData(BASE_ID + 57, trap),
    "Cutscene Trap":                TS2ItemData(BASE_ID + 58, trap),
    "Invincible Enemies Trap":      TS2ItemData(BASE_ID + 59, trap),
    "Narrow Vision Trap":           TS2ItemData(BASE_ID + 60, trap),

    # -- FILLER --
    "1 Life":                   TS2ItemData(BASE_ID + 61, filler),
    "Extra Battery":            TS2ItemData(BASE_ID + 62, filler),

    # -- MISSING TOYS (per coin level; progression class) --
    "Sheep":            TS2ItemData(BASE_ID + 63, prog),
    "Soldier":          TS2ItemData(BASE_ID + 64, prog),
    "Worker Tike":      TS2ItemData(BASE_ID + 65, prog),
    "Duck":             TS2ItemData(BASE_ID + 66, prog),
    "Chick":            TS2ItemData(BASE_ID + 67, prog),
    "Alien":            TS2ItemData(BASE_ID + 68, prog),
    "Mouse":            TS2ItemData(BASE_ID + 69, prog),
    "Critter":          TS2ItemData(BASE_ID + 70, prog),
    "Passenger Tike":   TS2ItemData(BASE_ID + 71, prog),
    "Luggage":          TS2ItemData(BASE_ID + 72, prog),
}

# -- DYNAMIC CLASSIFICATION HELPERS --

def get_disc_launcher_alleys_classification(coinsanity: bool) -> ItemClassification:
    """Disc Launcher - Alleys and Gullies is Progressive in Coinsanity,
    Useful otherwise."""
    return prog if coinsanity else use


def get_cosmic_shield_penthouse_classification(lifesanity: bool) -> ItemClassification:
    """Cosmic Shield - Al's Penthouse is Progressive in Lifesanity,
    Useful otherwise."""
    return prog if lifesanity else use


# -- ITEM GROUPS --

MOVE_ITEMS = {
    "Progressive Laser", "Spin", "Stomp", "Double Jump", "Pole Climb",
    "Ledge Grab", "Pole Vault", "Push", "Rope Sliding", "Visor",
}

WEAPON_MOVE_ITEMS = {
    "Progressive Laser", "Spin", "Stomp", "Visor",
}

TRAVERSAL_MOVE_ITEMS = {
    "Double Jump", "Pole Climb", "Ledge Grab", "Pole Vault",
    "Push", "Rope Sliding",
}

GADGET_ITEMS = {
    "Cosmic Shield - Andy's House",
    "Rocket Boots - Andy's Neighborhood",
    "Disc Launcher - Construction Yard",
    "Grappling Hook - Alleys and Gullies",
    "Disc Launcher - Alleys and Gullies",
    "Rocket Boots - Alleys and Gullies",
    "Rocket Boots - Al's Toy Barn",
    "Disc Launcher - Al's Toy Barn",
    "Hover Boots - Al's Toy Barn",
    "Cosmic Shield - Al's Space Land",
    "Grappling Hook - Elevator Hop",
    "Cosmic Shield - Al's Penthouse",
    "Hover Boots - Airport Infiltration",
    "Rocket Boots - Tarmac Trouble",
}

MISSING_PART_ITEMS = {
    "Missing Ear", "Missing Eye", "Missing Arm",
    "Missing Foot", "Missing Mouth",
}

LEVEL_UNLOCK_ITEMS = {
    "Andy's House Unlock", "Andy's Neighborhood Unlock",
    "Bombs Away! Unlock", "Construction Yard Unlock",
    "Alleys and Gullies Unlock", "Slime Time Unlock",
    "Al's Toy Barn Unlock", "Al's Space Land Unlock",
    "Toy Barn Encounter Unlock", "Elevator Hop Unlock",
    "Al's Penthouse Unlock", "The Evil Emperor Zurg Unlock",
    "Airport Infiltration Unlock", "Tarmac Trouble Unlock",
    "Final Showdown Unlock",
}

COIN_LEVEL_UNLOCK_ITEMS = {
    "Andy's House Unlock", "Andy's Neighborhood Unlock",
    "Construction Yard Unlock", "Alleys and Gullies Unlock",
    "Al's Toy Barn Unlock", "Al's Space Land Unlock",
    "Elevator Hop Unlock", "Al's Penthouse Unlock",
    "Airport Infiltration Unlock", "Tarmac Trouble Unlock",
}

BOSS_UNLOCK_ITEMS = {
    "Bombs Away! Unlock", "Slime Time Unlock",
    "Toy Barn Encounter Unlock", "The Evil Emperor Zurg Unlock",
    "Final Showdown Unlock",
}

COIN_BUNDLE_ITEMS = {
    "Coin Bundle - Andy's House", "Coin Bundle - Andy's Neighborhood",
    "Coin Bundle - Construction Yard", "Coin Bundle - Alleys and Gullies",
    "Coin Bundle - Al's Toy Barn", "Coin Bundle - Al's Space Land",
    "Coin Bundle - Elevator Hop", "Coin Bundle - Al's Penthouse",
    "Coin Bundle - Airport Infiltration", "Coin Bundle - Tarmac Trouble",
}

TRAP_ITEMS = {
    "Freeze Buzz Trap", "Damage Buzz Trap", "Cutscene Trap",
    "Invincible Enemies Trap", "Narrow Vision Trap",
}

FILLER_ITEMS = {
    "1 Life", "Extra Battery",
}

# Missing toy items: item name -> level id. Each is Progressive with 5 copies in
# the pool (one per toy location in that level). The client counts how many of
# each toy item has been received and writes that count to SHARED_TOY_RECEIVED
# for the matching level. Present in both Open and Linear modes.
MISSING_TOY_ITEMS = {
    "Sheep":            1,
    "Soldier":          2,
    "Worker Tike":      4,
    "Duck":             5,
    "Chick":            7,
    "Alien":            8,
    "Mouse":            10,
    "Critter":          11,
    "Passenger Tike":   13,
    "Luggage":          14,
}