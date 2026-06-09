from typing import TYPE_CHECKING, Callable, List, Optional
from BaseClasses import CollectionState
from .coin_data import COIN_DATA, CoinEntry

if TYPE_CHECKING:
    from . import ToyStory2World

# ============================================================
# CONSTANTS
# ============================================================
SKIPS_OFF  = 0
SKIPS_EASY = 1
SKIPS_HARD = 2

GAME_MODE_OPEN   = 0
GAME_MODE_LINEAR = 1

GOAL_TOKENS   = 0
GOAL_BOSSES   = 1
GOAL_UNLOCK   = 2
GOAL_T_AND_B  = 3
GOAL_T_AND_U  = 4
GOAL_B_AND_U  = 5
GOAL_T_B_U    = 6

# ============================================================
# MOVE / GADGET HELPERS
# ============================================================

def has_laser(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Laser", player)

def has_spin(state: CollectionState, player: int) -> bool:
    return state.has("Spin", player)

def has_stomp(state: CollectionState, player: int) -> bool:
    return state.has("Stomp", player)

def has_double_jump(state: CollectionState, player: int) -> bool:
    return state.has("Double Jump", player)

def has_pole_climb(state: CollectionState, player: int) -> bool:
    return state.has("Pole Climb", player)

def has_ledge_grab(state: CollectionState, player: int) -> bool:
    return state.has("Ledge Grab", player)

def has_pole_vault(state: CollectionState, player: int) -> bool:
    return state.has("Pole Vault", player)

def has_push(state: CollectionState, player: int) -> bool:
    return state.has("Push", player)

def has_rope_sliding(state: CollectionState, player: int) -> bool:
    return state.has("Rope Sliding", player)

def has_visor(state: CollectionState, player: int) -> bool:
    return state.has("Visor", player)

def has_any_attack(state: CollectionState, player: int) -> bool:
    return has_laser(state, player) or has_spin(state, player) or has_stomp(state, player)

def has_laser_or_spin(state: CollectionState, player: int) -> bool:
    return has_laser(state, player) or has_spin(state, player)

# Gadget helpers
def has_gadget(state: CollectionState, player: int, gadget_name: str) -> bool:
    return state.has(gadget_name, player)

def has_cosmic_shield_andys(state: CollectionState, player: int) -> bool:
    return state.has("Cosmic Shield - Andy's House", player)

def has_rocket_boots_neighborhood(state: CollectionState, player: int) -> bool:
    return state.has("Rocket Boots - Andy's Neighborhood", player)

def has_disc_launcher_construction(state: CollectionState, player: int) -> bool:
    return state.has("Disc Launcher - Construction Yard", player)

def has_grappling_hook_alleys(state: CollectionState, player: int) -> bool:
    return state.has("Grappling Hook - Alleys and Gullies", player)

def has_disc_launcher_alleys(state: CollectionState, player: int) -> bool:
    # The Disc Launcher in Alleys and Gullies spawns deep in the level: reaching
    # it needs Double Jump + Rope Sliding + Ledge Grab in addition to the item.
    return (state.has("Disc Launcher - Alleys and Gullies", player)
            and has_double_jump(state, player)
            and has_rope_sliding(state, player)
            and has_ledge_grab(state, player))

def has_rocket_boots_alleys(state: CollectionState, player: int) -> bool:
    return state.has("Rocket Boots - Alleys and Gullies", player)

def has_rocket_boots_toybarn(state: CollectionState, player: int) -> bool:
    return state.has("Rocket Boots - Al's Toy Barn", player)

def has_disc_launcher_toybarn(state: CollectionState, player: int) -> bool:
    # The Disc Launcher in Al's Toy Barn spawns past an obstacle: reaching it
    # needs Double Jump plus EITHER Ledge Grab OR Pole Climb, plus the item.
    return (state.has("Disc Launcher - Al's Toy Barn", player)
            and has_double_jump(state, player)
            and (has_ledge_grab(state, player) or has_pole_climb(state, player)))

def has_hover_boots_toybarn(state: CollectionState, player: int) -> bool:
    return state.has("Hover Boots - Al's Toy Barn", player)

def has_cosmic_shield_spaceland(state: CollectionState, player: int) -> bool:
    return state.has("Cosmic Shield - Al's Space Land", player)

def has_grappling_hook_elevator(state: CollectionState, player: int) -> bool:
    return state.has("Grappling Hook - Elevator Hop", player)

def has_cosmic_shield_penthouse(state: CollectionState, player: int) -> bool:
    return state.has("Cosmic Shield - Al's Penthouse", player)

def has_hover_boots_airport(state: CollectionState, player: int) -> bool:
    # The Hover Boots in Airport Infiltration spawn past a movement gate. Reaching
    # them needs Stomp + Double Jump + Pole Vault normally, or just Stomp + Double
    # Jump when Hard Skips are enabled — plus the item itself.
    if not state.has("Hover Boots - Airport Infiltration", player):
        return False
    if not (has_stomp(state, player) and has_double_jump(state, player)):
        return False
    try:
        skips = state.multiworld.worlds[player].options.skips.value
    except Exception:
        skips = SKIPS_OFF
    if skips == SKIPS_HARD:
        return True
    return has_pole_vault(state, player)

def has_rocket_boots_tarmac(state: CollectionState, player: int) -> bool:
    return state.has("Rocket Boots - Tarmac Trouble", player)

# ── GADGET LOOKUP BY NAME ─────────────────────────────────────

GADGET_CHECKERS = {
    "Cosmic Shield":        has_cosmic_shield_andys,
    "Rocket Boots":         has_rocket_boots_neighborhood,
    "Disc Launcher":        has_disc_launcher_construction,
    "Grappling Hook":       has_grappling_hook_alleys,
    "Hover Boots":          has_hover_boots_toybarn,
    "Cosmic Shield - Andy's House":        has_cosmic_shield_andys,
    "Rocket Boots - Andy's Neighborhood":  has_rocket_boots_neighborhood,
    "Disc Launcher - Construction Yard":   has_disc_launcher_construction,
    "Grappling Hook - Alleys and Gullies": has_grappling_hook_alleys,
    "Disc Launcher - Alleys and Gullies":  has_disc_launcher_alleys,
    "Rocket Boots - Alleys and Gullies":   has_rocket_boots_alleys,
    "Rocket Boots - Al's Toy Barn":        has_rocket_boots_toybarn,
    "Disc Launcher - Al's Toy Barn":       has_disc_launcher_toybarn,
    "Hover Boots - Al's Toy Barn":         has_hover_boots_toybarn,
    "Cosmic Shield - Al's Space Land":     has_cosmic_shield_spaceland,
    "Grappling Hook - Elevator Hop":       has_grappling_hook_elevator,
    "Cosmic Shield - Al's Penthouse":      has_cosmic_shield_penthouse,
    "Hover Boots - Airport Infiltration":  has_hover_boots_airport,
    "Rocket Boots - Tarmac Trouble":       has_rocket_boots_tarmac,
}

MOVE_CHECKERS = {
    "Laser":        has_laser,
    "Spin":         has_spin,
    "Stomp":        has_stomp,
    "Double Jump":  has_double_jump,
    "Pole Climb":   has_pole_climb,
    "Ledge Grab":   has_ledge_grab,
    "Pole Vault":   has_pole_vault,
    "Push":         has_push,
    "Rope Sliding": has_rope_sliding,
    "Visor":        has_visor,
}

# ── GENERIC MOVE/GADGET CHECKERS ─────────────────────────────

def has_move(state: CollectionState, player: int, move: str) -> bool:
    checker = MOVE_CHECKERS.get(move)
    if checker:
        return checker(state, player)
    return False

def has_all_moves(state: CollectionState, player: int, moves: List[str]) -> bool:
    return all(has_move(state, player, m) for m in moves)

def has_any_move(state: CollectionState, player: int, moves: List[str]) -> bool:
    return any(has_move(state, player, m) for m in moves)

def has_gadget_by_name(state: CollectionState, player: int, gadget: str, level: str = "") -> bool:
    # Try level-specific first
    if level:
        level_specific = {
            "Rocket Boots": {
                "Andy's Neighborhood":  has_rocket_boots_neighborhood,
                "Alleys and Gullies":   has_rocket_boots_alleys,
                "Al's Toy Barn":        has_rocket_boots_toybarn,
                "Tarmac Trouble":       has_rocket_boots_tarmac,
            },
            "Disc Launcher": {
                "Construction Yard":    has_disc_launcher_construction,
                "Alleys and Gullies":   has_disc_launcher_alleys,
                "Al's Toy Barn":        has_disc_launcher_toybarn,
            },
            "Grappling Hook": {
                "Alleys and Gullies":   has_grappling_hook_alleys,
                "Elevator Hop":         has_grappling_hook_elevator,
            },
            "Hover Boots": {
                "Al's Toy Barn":        has_hover_boots_toybarn,
                "Airport Infiltration": has_hover_boots_airport,
            },
            "Cosmic Shield": {
                "Andy's House":         has_cosmic_shield_andys,
                "Al's Space Land":      has_cosmic_shield_spaceland,
                "Al's Penthouse":       has_cosmic_shield_penthouse,
            },
        }
        if gadget in level_specific and level in level_specific[gadget]:
            return level_specific[gadget][level](state, player)
    checker = GADGET_CHECKERS.get(gadget)
    if checker:
        return checker(state, player)
    return False

def has_all_gadgets(state: CollectionState, player: int, gadgets: List[str], level: str = "") -> bool:
    return all(has_gadget_by_name(state, player, g, level) for g in gadgets)

def has_any_gadget(state: CollectionState, player: int, gadgets: List[str], level: str = "") -> bool:
    return any(has_gadget_by_name(state, player, g, level) for g in gadgets)

# ── TOKEN / TICKET HELPERS ────────────────────────────────────

def token_count(state: CollectionState, player: int) -> int:
    return state.count("Pizza Planet Token", player)

def ticket_count(state: CollectionState, player: int) -> int:
    return state.count("Final Showdown Ticket", player)

def boss_defeats(state: CollectionState, player: int) -> int:
    count = 0
    for boss_loc in ["Bombs Away! - Defeat Reward 1", "Slime Time - Defeat Reward 1",
                     "Toy Barn Encounter - Defeat Reward 1",
                     "The Evil Emperor Zurg - Defeat Reward 1"]:
        if state.can_reach(boss_loc, "Location", player):
            count += 1
    return count

# ============================================================
# LEVEL ACCESS RULES
# ============================================================

def can_access_level(state: CollectionState, player: int, level: str, world: "ToyStory2World") -> bool:
    options = world.options
    mode = options.game_mode.value

    if mode == GAME_MODE_OPEN:
        # Only the randomly-chosen starting levels are free; everything else
        # needs its unlock item. The Prospector Showdown level's unlock item is
        # named "Final Showdown Unlock" (the only level whose unlock item name
        # doesn't follow the "{level} Unlock" pattern).
        starting = getattr(world, "_starting_levels", [])
        if level in starting:
            return True
        unlock_item = ("Final Showdown Unlock" if level == "Prospector Showdown"
                       else f"{level} Unlock")
        return state.has(unlock_item, player)

    else:  # Linear
        # Mirror the Lua's apply_linear_area exactly:
        #  - Area is reached by defeating the previous area's boss (the ticket).
        #  - REGULAR levels in an area are free once you're in that area (no token
        #    requirement) — the Lua unlocks AREA_UNLOCKED[area] with no token check.
        #  - The BOSS of an area needs tokens >= ITS OWN gate (gate 1..5), AND the
        #    previous boss defeated.
        #
        # IMPORTANT: a boss is "defeated" when you can ACCESS its level AND have the
        # attack to beat it. We compute this by recursing on can_access_level for
        # the (earlier) boss level — NOT via state.can_reach on the reward location.
        # Using can_reach here caused infinite recursion: reaching the reward
        # location re-evaluates its region's access rule, which re-enters
        # can_access_level, and the location-access wrapper closed the loop. Because
        # each area's gate only references strictly EARLIER areas, direct recursion
        # on can_access_level terminates.
        toks = token_count(state, player)

        def boss_defeated(boss_level: str, attack) -> bool:
            return can_access_level(state, player, boss_level, world) and attack()

        bombs_def = lambda: boss_defeated(
            "Bombs Away!", lambda: has_any_attack(state, player))
        slime_def = lambda: boss_defeated(
            "Slime Time", lambda: has_laser(state, player))
        tbe_def = lambda: boss_defeated(
            "Toy Barn Encounter",
            lambda: has_laser(state, player) and
                    has_any_move(state, player, ["Spin", "Stomp"]))
        zurg_def = lambda: boss_defeated(
            "The Evil Emperor Zurg", lambda: has_spin(state, player))

        # Area 0 starting levels
        if level in ("Andy's House", "Andy's Neighborhood"):
            return True
        # Area 0 boss
        elif level == "Bombs Away!":
            return toks >= options.bombs_away_token_gate.value
        # Area 1 regular (reached by beating Bombs Away)
        elif level in ("Construction Yard", "Alleys and Gullies"):
            return bombs_def()
        # Area 1 boss
        elif level == "Slime Time":
            return bombs_def() and toks >= options.slime_time_token_gate.value
        # Area 2 regular (reached by beating Slime Time)
        elif level in ("Al's Toy Barn", "Al's Space Land"):
            return slime_def()
        # Area 2 boss
        elif level == "Toy Barn Encounter":
            return slime_def() and toks >= options.toy_barn_encounter_token_gate.value
        # Area 3 regular (reached by beating Toy Barn Encounter)
        elif level in ("Elevator Hop", "Al's Penthouse"):
            return tbe_def()
        # Area 3 boss
        elif level == "The Evil Emperor Zurg":
            return tbe_def() and toks >= options.evil_emperor_zurg_token_gate.value
        # Area 4 regular (reached by beating Zurg)
        elif level in ("Airport Infiltration", "Tarmac Trouble"):
            return zurg_def()
        # Area 4 boss / final
        elif level == "Prospector Showdown":
            return zurg_def() and toks >= options.linear_final_showdown_token_gate.value
    return False

# ============================================================
# STANDARD RULE EVALUATOR
# ============================================================

def standard_rule(
    state: CollectionState,
    player: int,
    skips: int,
    moves_and: List[str],
    moves_or: List[str],
    gadgets_and: List[str],
    gadgets_or: List[str],
    glitch_tier: Optional[str],
    g_moves_and: List[str],
    g_moves_or: List[str],
    g_gadgets_and: List[str],
    g_gadgets_or: List[str],
    level: str = "",
) -> bool:
    # Check glitch shortcut first
    if glitch_tier and skips != SKIPS_OFF:
        tiers = [t.strip() for t in glitch_tier.split(",")]
        glitch_applies = (
            (skips == SKIPS_EASY and "Easy" in tiers) or
            (skips == SKIPS_HARD and ("Hard" in tiers or "Easy" in tiers))
        )
        if glitch_applies:
            gma_ok = has_all_moves(state, player, g_moves_and) if g_moves_and else True
            gga_ok = has_all_gadgets(state, player, g_gadgets_and, level) if g_gadgets_and else True
            if g_moves_or and g_gadgets_or:
                gor_ok = (has_any_move(state, player, g_moves_or)
                          or has_any_gadget(state, player, g_gadgets_or, level))
                if gma_ok and gga_ok and gor_ok:
                    return True
            else:
                gmo_ok = has_any_move(state, player, g_moves_or) if g_moves_or else True
                ggo_ok = has_any_gadget(state, player, g_gadgets_or, level) if g_gadgets_or else True
                if gma_ok and gmo_ok and gga_ok and ggo_ok:
                    return True

    # Normal requirements
    ma_ok = has_all_moves(state, player, moves_and) if moves_and else True
    ga_ok = has_all_gadgets(state, player, gadgets_and, level) if gadgets_and else True
    # OR-moves and OR-gadgets form ONE combined "any 1 of" pool when both are
    # present (per the "Any 1 of OR Movement & Gadgets" logic note): satisfying
    # EITHER an OR-move OR an OR-gadget is enough. (Previously these were ANDed,
    # which wrongly required both an attack AND the gadget — e.g. Laser AND Disc
    # Launcher instead of Laser OR Disc Launcher.) has_any_gadget still enforces the
    # per-level gadget-accessibility gates.
    if moves_or and gadgets_or:
        or_ok = (has_any_move(state, player, moves_or)
                 or has_any_gadget(state, player, gadgets_or, level))
        return ma_ok and ga_ok and or_ok
    mo_ok = has_any_move(state, player, moves_or) if moves_or else True
    go_ok = has_any_gadget(state, player, gadgets_or, level) if gadgets_or else True
    return ma_ok and mo_ok and ga_ok and go_ok

# ============================================================
# COIN BUNDLE RULES
# ============================================================

# ── COMPLEX COIN OVERRIDES ───────────────────────────────────
# These handle coins whose logic can't be expressed by simple AND/OR

def _alleys_coins_40_42(state: CollectionState, player: int, skips: int) -> bool:
    # (Ledge Grab OR Double Jump) AND (Laser OR Spin OR Stomp)
    return (
        has_any_move(state, player, ["Ledge Grab", "Double Jump"]) and
        has_any_attack(state, player) and
        has_rope_sliding(state, player)
    )

def _alleys_coins_79_83(state: CollectionState, player: int, skips: int) -> bool:
    # (Laser OR Spin) AND (Ledge Grab OR Double Jump) + Visor + Pole Climb + Rope Sliding + Grappling Hook
    return (
        has_laser_or_spin(state, player) and
        has_any_move(state, player, ["Ledge Grab", "Double Jump"]) and
        has_visor(state, player) and
        has_pole_climb(state, player) and
        has_rope_sliding(state, player) and
        has_grappling_hook_alleys(state, player)
    )

def _als_penthouse_coins_44_45(state: CollectionState, player: int, skips: int) -> bool:
    # Laser + Double Jump + Stomp OR Laser + Visor + Ledge Grab
    normal = (
        (has_laser(state, player) and has_double_jump(state, player) and has_stomp(state, player)) or
        (has_laser(state, player) and has_visor(state, player) and has_ledge_grab(state, player))
    )
    if normal:
        return True
    if skips in (SKIPS_EASY, SKIPS_HARD):
        return (has_double_jump(state, player) and has_ledge_grab(state, player) and
                has_stomp(state, player))
    return False

def _als_toybarn_coins_59_60(state: CollectionState, player: int, skips: int) -> bool:
    # Double Jump + Rocket Boots OR Double Jump + Ledge Grab + Pole Vault + Rope Sliding
    normal = (
        (has_double_jump(state, player) and has_rocket_boots_toybarn(state, player)) or
        (has_double_jump(state, player) and has_ledge_grab(state, player) and
         has_pole_vault(state, player) and has_rope_sliding(state, player))
    )
    if normal:
        return True
    if skips in (SKIPS_EASY, SKIPS_HARD):
        return has_double_jump(state, player) and has_ledge_grab(state, player)
    if skips == SKIPS_HARD:
        return has_double_jump(state, player)
    return False

def _als_toybarn_coins_61_68(state: CollectionState, player: int, skips: int) -> bool:
    # Stomp + Double Jump + Rocket Boots OR Double Jump + Pole Vault + Rope Sliding
    # OR Ledge Grab + Pole Vault + Rope Sliding
    normal = (
        (has_stomp(state, player) and has_double_jump(state, player) and
         has_rocket_boots_toybarn(state, player)) or
        (has_double_jump(state, player) and has_pole_vault(state, player) and
         has_rope_sliding(state, player)) or
        (has_ledge_grab(state, player) and has_pole_vault(state, player) and
         has_rope_sliding(state, player))
    )
    if normal:
        return True
    if skips in (SKIPS_EASY, SKIPS_HARD):
        return has_double_jump(state, player) and has_ledge_grab(state, player)
    return False

def _construction_coins_66_67(state: CollectionState, player: int, skips: int, level: str) -> bool:
    # (Laser + Visor) OR Disc Launcher, plus Stomp + Double Jump + Ledge Grab + Pole Climb
    base = (has_stomp(state, player) and has_double_jump(state, player) and
            has_ledge_grab(state, player) and has_pole_climb(state, player))
    attack = (
        (has_laser(state, player) and has_visor(state, player)) or
        has_disc_launcher_construction(state, player)
    )
    normal = base and attack
    if normal:
        return True
    if skips in (SKIPS_EASY, SKIPS_HARD):
        g_base = has_double_jump(state, player)
        g_attack = (
            (has_laser(state, player) and has_visor(state, player)) or
            has_disc_launcher_construction(state, player)
        )
        return g_base and g_attack
    return False

# ── COIN OVERRIDE MAP ─────────────────────────────────────────
# Maps (level, coin_index_0based) -> override function or None

def _get_coin_override(level: str, idx: int):
    overrides = {
        ("Alleys and Gullies", 39): _alleys_coins_40_42,
        ("Alleys and Gullies", 40): _alleys_coins_40_42,
        ("Alleys and Gullies", 41): _alleys_coins_40_42,
        ("Alleys and Gullies", 78): _alleys_coins_79_83,
        ("Alleys and Gullies", 82): _alleys_coins_79_83,
        ("Construction Yard", 65): lambda s, p, sk: _construction_coins_66_67(s, p, sk, "Construction Yard"),
        ("Construction Yard", 66): lambda s, p, sk: _construction_coins_66_67(s, p, sk, "Construction Yard"),
        ("Al's Toy Barn", 58): _als_toybarn_coins_59_60,
        ("Al's Toy Barn", 59): _als_toybarn_coins_59_60,
        ("Al's Toy Barn", 60): _als_toybarn_coins_61_68,
        ("Al's Toy Barn", 61): _als_toybarn_coins_61_68,
        ("Al's Toy Barn", 62): _als_toybarn_coins_61_68,
        ("Al's Toy Barn", 63): _als_toybarn_coins_61_68,
        ("Al's Toy Barn", 64): _als_toybarn_coins_61_68,
        ("Al's Toy Barn", 65): _als_toybarn_coins_61_68,
        ("Al's Toy Barn", 66): _als_toybarn_coins_61_68,
        ("Al's Toy Barn", 67): _als_toybarn_coins_61_68,
        ("Al's Penthouse", 43): _als_penthouse_coins_44_45,
        ("Al's Penthouse", 44): _als_penthouse_coins_44_45,
    }
    return overrides.get((level, idx))


def can_reach_coin(
    state: CollectionState,
    player: int,
    level: str,
    coin_idx: int,  # 0-based
    skips: int,
) -> bool:
    coins = COIN_DATA.get(level, [])
    if coin_idx >= len(coins):
        return True  # out of range, allow
    coin = coins[coin_idx]
    ma, mo, ga, go, glitch, gma, gmo, gga, ggo = coin

    # Check for override
    override = _get_coin_override(level, coin_idx)
    if override:
        return override(state, player, skips)

    # Handle disc launcher as attack alternative for Construction Yard / Alleys
    if level == "Construction Yard":
        if go and any(g in ("Disc Launcher",) for g in go):
            # gadgets_or includes Disc Launcher — treat as attack OR disc
            other_gadgets = [g for g in go if g != "Disc Launcher"]
            disc_ok = has_disc_launcher_construction(state, player)
            mo_ok = has_any_move(state, player, mo) if mo else True
            combined_ok = disc_ok or mo_ok or has_any_gadget(state, player, other_gadgets, level)
            ma_ok = has_all_moves(state, player, ma) if ma else True
            ga_ok = has_all_gadgets(state, player, ga, level) if ga else True
            normal = ma_ok and combined_ok and ga_ok
            if normal:
                return True
            # glitch
            if glitch and skips != SKIPS_OFF:
                tiers = [t.strip() for t in glitch.split(",")]
                if (skips == SKIPS_EASY and "Easy" in tiers) or \
                   (skips == SKIPS_HARD and ("Hard" in tiers or "Easy" in tiers)):
                    gma_ok = has_all_moves(state, player, gma) if gma else True
                    gmo_ok = has_any_move(state, player, gmo) if gmo else True
                    g_disc_ok = has_disc_launcher_construction(state, player)
                    g_other = [g for g in ggo if g != "Disc Launcher"] if ggo else []
                    g_combined = g_disc_ok or gmo_ok or has_any_gadget(state, player, g_other, level)
                    gga_ok = has_all_gadgets(state, player, gga, level) if gga else True
                    if gma_ok and g_combined and gga_ok:
                        return True
            return False

    if level == "Alleys and Gullies":
        disc_in_go = go and "Disc Launcher" in go
        disc_in_ggo = ggo and "Disc Launcher" in ggo
        if disc_in_go:
            other_go = [g for g in go if g != "Disc Launcher"]
            disc_ok = has_disc_launcher_alleys(state, player)
            mo_ok = has_any_move(state, player, mo) if mo else True
            combined_ok = disc_ok or mo_ok or has_any_gadget(state, player, other_go, level)
            ma_ok = has_all_moves(state, player, ma) if ma else True
            ga_ok = has_all_gadgets(state, player, ga, level) if ga else True
            normal = ma_ok and combined_ok and ga_ok
            if normal:
                return True
            if glitch and skips != SKIPS_OFF:
                tiers = [t.strip() for t in glitch.split(",")]
                if (skips == SKIPS_EASY and "Easy" in tiers) or \
                   (skips == SKIPS_HARD and ("Hard" in tiers or "Easy" in tiers)):
                    gma_ok = has_all_moves(state, player, gma) if gma else True
                    gmo_ok = has_any_move(state, player, gmo) if gmo else True
                    g_disc = has_disc_launcher_alleys(state, player) if disc_in_ggo else False
                    g_other = [g for g in ggo if g != "Disc Launcher"] if ggo else []
                    g_combined = g_disc or gmo_ok or has_any_gadget(state, player, g_other, level)
                    gga_ok = has_all_gadgets(state, player, gga, level) if gga else True
                    if gma_ok and g_combined and gga_ok:
                        return True
            return False

    return standard_rule(state, player, skips, ma, mo, ga, go, glitch, gma, gmo, gga, ggo, level)


def coin_bundle_rule(
    state: CollectionState,
    player: int,
    level: str,
    bundle_num: int,   # 1-based
    bundle_size: int,  # 0 = ALL
    skips: int,
    world: "ToyStory2World",
) -> bool:
    coins = COIN_DATA.get(level, [])
    total = len(coins)
    if total == 0:
        return True

    if bundle_size == 0:
        # ALL — must reach every coin
        return all(can_reach_coin(state, player, level, i, skips) for i in range(total))

    # Player needs ANY (bundle_num * bundle_size) coins total in this level.
    # The last bundle may be a partial (e.g. 103 coins, size 5 -> bundle 21 needs all 103).
    coins_needed = min(bundle_num * bundle_size, total)

    # Count how many coins are reachable with current state.
    # Short-circuit as soon as we have enough.
    reachable = 0
    for i in range(total):
        if can_reach_coin(state, player, level, i, skips):
            reachable += 1
            if reachable >= coins_needed:
                return True
    return False


# ============================================================
# HAMM'S 50 COINS TOKEN RULE
# ============================================================

def hamms_50_coins_rule(
    state: CollectionState,
    player: int,
    level: str,
    skips: int,
    moves_and: List[str],
    moves_or: List[str],
    world: "ToyStory2World",
    move_check=None,
) -> bool:
    """Player needs 50 coins in this level AND the move requirements to reach
    Hamm. How "50 coins" is satisfied depends on Coinsanity:
      - Coinsanity ON: coins come from received Coin Bundle items. Need enough
        bundles for this level that bundles * received_bundle_size >= 50.
      - Coinsanity OFF: coins are collected in-level, so need 50 of the level's
        coins to be physically reachable.
    move_check, if given, is a callable(state, player) -> bool used INSTEAD of
    moves_and/moves_or, for movement logic the flat lists can't express (e.g.
    "Pole Climb OR (Double Jump AND Ledge Grab)")."""
    options = world.options
    coins = COIN_DATA.get(level, [])
    level_max = len(coins)
    # A level with fewer than 50 coins can never satisfy Hamm either way.
    if level_max < 50:
        return False

    if options.coinsanity.value:
        # Need enough received bundles for THIS level to total >= 50 coins.
        recv_size = options.coinsanity_received_bundle_size.value or 5
        import math as _math
        bundles_needed = _math.ceil(50 / recv_size)
        if not state.has(f"Coin Bundle - {level}", player, bundles_needed):
            return False
    else:
        reachable = sum(1 for i in range(level_max)
                        if can_reach_coin(state, player, level, i, skips))
        if reachable < 50:
            return False

    if move_check is not None:
        return move_check(state, player)
    ma_ok = has_all_moves(state, player, moves_and) if moves_and else True
    mo_ok = has_any_move(state, player, moves_or) if moves_or else True
    return ma_ok and mo_ok

# ============================================================
# MISSING TOYS TOKEN RULE
# ============================================================

# Level -> the toy item name whose 5 copies gate that level's Missing Toys Token
MISSING_TOYS_TOKEN_ITEM = {
    "Andy's House":          "Sheep",
    "Andy's Neighborhood":   "Soldier",
    "Construction Yard":     "Worker Tike",
    "Alleys and Gullies":    "Duck",
    "Al's Toy Barn":         "Chick",
    "Al's Space Land":       "Alien",
    "Elevator Hop":          "Mouse",
    "Al's Penthouse":        "Critter",
    "Airport Infiltration":  "Passenger Tike",
    "Tarmac Trouble":        "Luggage",
}

def missing_toys_token_rule(
    state: CollectionState,
    player: int,
    level: str,
    moves_and: List[str],
    moves_or: List[str],
    gadgets_and: List[str],
) -> bool:
    """Player needs all 5 of the level's missing toys (the toy ITEMS) AND the
    movement/gadgets to reach the token. The 5-toy requirement is real AP logic
    now that toys are received items — previously this only checked movement, so
    the tracker thought the token was reachable with zero toys."""
    toy_item = MISSING_TOYS_TOKEN_ITEM.get(level)
    if toy_item and not state.has(toy_item, player, 5):
        return False
    ma_ok = has_all_moves(state, player, moves_and) if moves_and else True
    mo_ok = has_any_move(state, player, moves_or) if moves_or else True
    ga_ok = has_all_gadgets(state, player, gadgets_and, level) if gadgets_and else True
    return ma_ok and mo_ok and ga_ok

# ============================================================
# GIVE POTATO HEAD RULE
# ============================================================

def give_potato_head_rule(
    state: CollectionState,
    player: int,
    part_item: str,
    moves_and: List[str] = None,
) -> bool:
    """Player must have the missing part AP item, plus any move requirements."""
    if not state.has(part_item, player):
        return False
    if moves_and:
        return has_all_moves(state, player, moves_and)
    return True

# ============================================================
# GOAL RULE
# ============================================================

def goal_rule(state: CollectionState, player: int, world: "ToyStory2World") -> bool:
    options = world.options
    mode = options.game_mode.value
    skips = options.skips.value

    # Goal always requires Stomp OR Spin at Prospector
    if not (has_stomp(state, player) or has_spin(state, player)):
        return False

    # Must be able to access Prospector Showdown
    if not can_access_level(state, player, "Prospector Showdown", world):
        return False

    if mode == GAME_MODE_LINEAR:
        return True

    # Open mode — check goal conditions
    goal = options.goal_conditions.value
    token_gate = options.final_showdown_token_gate.value
    boss_req   = options.defeated_bosses_required.value

    needs_tokens = goal in (GOAL_TOKENS, GOAL_T_AND_B, GOAL_T_AND_U, GOAL_T_B_U)
    needs_bosses = goal in (GOAL_BOSSES, GOAL_T_AND_B, GOAL_B_AND_U, GOAL_T_B_U)
    needs_unlock = goal in (GOAL_UNLOCK, GOAL_T_AND_U, GOAL_B_AND_U, GOAL_T_B_U)

    if needs_tokens and token_count(state, player) < token_gate:
        return False
    if needs_bosses and boss_defeats(state, player) < boss_req:
        return False
    if needs_unlock and not state.has("Final Showdown Unlock", player):
        return False

    return True

# ============================================================
# SET RULES
# ============================================================

def set_rules(world: "ToyStory2World") -> None:
    from worlds.AutoWorld import World
    multiworld = world.multiworld
    player     = world.player
    options    = world.options
    skips      = options.skips.value
    mode       = options.game_mode.value
    bundle_size = options.coinsanity_checks_bundle_size.value

    def rule(loc_name: str, fn: Callable[[CollectionState], bool]) -> None:
        # A location may not exist if the sanity that creates it is disabled
        # (e.g. lifesanity off -> no "Life (...)" locations). get_location raises
        # KeyError in that case, so swallow it and skip applying the rule.
        try:
            loc = multiworld.get_location(loc_name, player)
        except KeyError:
            return
        if loc:
            loc.access_rule = fn

    def s(fn): return lambda state: fn(state)

    # ── ANDY'S HOUSE ─────────────────────────────────────────

    # Coin bundles
    for loc in multiworld.get_locations(player):
        if "Coin Bundle" in loc.name and "Andy's House" in loc.name:
            bundle_num = int(loc.name.split("Coin Bundle ")[1])
            loc.access_rule = lambda state, bn=bundle_num: coin_bundle_rule(
                state, player, "Andy's House", bn, bundle_size, skips, world)

    rule("Andy's House - Hamm's 50 Coins Token",
         lambda state: hamms_50_coins_rule(state, player, "Andy's House", skips,
                                            [], ["Double Jump", "Ledge Grab", "Pole Climb"], world))

    rule("Andy's House - Missing Toys Token",
         lambda state: missing_toys_token_rule(state, player, "Andy's House",
                                                [], ["Pole Climb", "Double Jump", "Ledge Grab"], []))

    # Race Token - no requirements
    # Hidden Token
    rule("Andy's House - Hidden Token",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Pole Climb", "Push"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Push"])) or
             (skips == SKIPS_HARD and
              has_all_moves(state, player, ["Double Jump", "Ledge Grab"]))
         ))

    rule("Andy's House - Boss Token",
         lambda state: (
             (has_pole_climb(state, player) and has_laser_or_spin(state, player)) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Pole Climb", "Stomp"]))
         ))

    rule("Andy's House - Sheep (Basement)",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Rope Sliding"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Ledge Grab"]))
         ))

    rule("Andy's House - Sheep (Living Room)",
         lambda state: (
             has_all_moves(state, player, ["Stomp", "Double Jump", "Ledge Grab"]) or
             (skips == SKIPS_HARD and
              has_double_jump(state, player) and
              has_any_move(state, player, ["Ledge Grab", "Pole Climb"]))
         ))

    rule("Andy's House - Sheep (Kitchen)",
         lambda state: (
             has_all_moves(state, player, ["Push", "Double Jump", "Ledge Grab"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Push"]))
         ))

    rule("Andy's House - Sheep (Attic)",
         lambda state: (
             has_all_moves(state, player, ["Push", "Pole Climb", "Pole Vault"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Pole Climb", "Pole Vault", "Double Jump"]))
         ))

    rule("Andy's House - Sheep (Garage)",
         lambda state: (
             has_all_moves(state, player, ["Ledge Grab", "Double Jump", "Pole Climb", "Pole Vault"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Ledge Grab"]))
         ))

    rule("Andy's House - Missing Ear",
         lambda state: (
             (has_stomp(state, player) and
              has_any_move(state, player, ["Double Jump", "Ledge Grab", "Pole Climb"])) or
             (skips == SKIPS_HARD and
              has_double_jump(state, player) and
              has_any_move(state, player, ["Ledge Grab", "Pole Climb"]))
         ))

    rule("Andy's House - Give Potato Head His Ear",
         lambda state: give_potato_head_rule(state, player, "Missing Ear"))

    rule("Andy's House - Life (Crib)",
         lambda state: (
             (has_all_moves(state, player, ['Push', 'Pole Climb', 'Visor', 'Rope Sliding']) and has_any_move(state, player, ['Double Jump', 'Ledge Grab'])) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_all_moves(state, player, ['Pole Climb']) and has_any_move(state, player, ['Ledge Grab', 'Double Jump']))
         ))

    rule("Andy's House - Life (Living Room)",
         lambda state: (
             has_all_moves(state, player, ["Stomp", "Double Jump", "Ledge Grab"]) or
             (skips == SKIPS_HARD and
              has_double_jump(state, player) and
              has_any_move(state, player, ["Ledge Grab", "Pole Climb"]))
         ))

    rule("Andy's House - Life (Garage)",
         lambda state: has_all_moves(state, player, ["Ledge Grab", "Double Jump", "Pole Climb"]))

    rule("Andy's House - Green Laser",
         lambda state: has_all_moves(state, player, ["Ledge Grab", "Double Jump", "Pole Climb"]))

    rule("Andy's House - Battery (Andy's Room)",
         lambda state: (
             (has_all_moves(state, player, ['Push', 'Pole Climb', 'Visor']) and has_any_move(state, player, ['Double Jump', 'Ledge Grab'])) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_all_moves(state, player, ['Pole Climb']) and has_any_move(state, player, ['Ledge Grab', 'Double Jump']))
         ))

    rule("Andy's House - Battery (Attic)",
         lambda state: (
             has_all_moves(state, player, ["Push", "Pole Climb", "Pole Vault"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Pole Climb", "Pole Vault", "Double Jump"]))
         ))

    rule("Andy's House - Battery (Basement)",
         lambda state: has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Pole Climb"]))

    rule("Andy's House - Battery (Garage)",
         lambda state: (
             has_all_moves(state, player, ["Ledge Grab", "Double Jump", "Pole Climb"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Ledge Grab"]))
         ))

    rule("Andy's House - Battery (Living Room)",
         lambda state: (
             (has_stomp(state, player) and
              has_any_move(state, player, ["Double Jump", "Ledge Grab", "Pole Climb"])) or
             (skips == SKIPS_HARD and
              has_double_jump(state, player) and
              has_any_move(state, player, ["Ledge Grab", "Pole Climb"]))
         ))

    rule("Andy's House - Battery (Handrail)",
         lambda state: (
             has_any_move(state, player, ['Double Jump', 'Ledge Grab', 'Pole Climb'])
         ))

    # Talk to Rex - no requirements

    # ── ANDY'S NEIGHBORHOOD ───────────────────────────────────

    for loc in multiworld.get_locations(player):
        if "Coin Bundle" in loc.name and "Andy's Neighborhood" in loc.name:
            bundle_num = int(loc.name.split("Coin Bundle ")[1])
            loc.access_rule = lambda state, bn=bundle_num: coin_bundle_rule(
                state, player, "Andy's Neighborhood", bn, bundle_size, skips, world)

    rule("Andy's Neighborhood - Hamm's 50 Coins Token",
         lambda state: hamms_50_coins_rule(state, player, "Andy's Neighborhood", skips,
                                            ["Double Jump", "Ledge Grab", "Pole Climb"], [], world))

    # Missing Toys Token - no requirements (already has 5 toys condition handled by misc)

    rule("Andy's Neighborhood - Race Token",
         lambda state: (
             has_rocket_boots_neighborhood(state, player) or
             (skips == SKIPS_HARD)
         ))

    rule("Andy's Neighborhood - Hidden Token",
         lambda state: (
             (has_all_moves(state, player, ['Stomp']) and has_any_move(state, player, ['Double Jump', 'Ledge Grab'])) or
             (skips == SKIPS_HARD and has_all_moves(state, player, ['Double Jump', 'Pole Climb']))
         ))

    rule("Andy's Neighborhood - Boss Token",
         lambda state: (
             has_all_moves(state, player, ['Double Jump', 'Ledge Grab', 'Pole Climb', 'Pole Vault', 'Laser'])
         ))

    rule("Andy's Neighborhood - Soldier (Molehill)",
         lambda state: has_stomp(state, player))

    rule("Andy's Neighborhood - Soldier (Clothes Line)",
         lambda state: (
             (has_all_moves(state, player, ['Stomp', 'Ledge Grab', 'Push', 'Rope Sliding'])) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_all_moves(state, player, ['Rope Sliding', 'Double Jump', 'Ledge Grab']))
         ))

    rule("Andy's Neighborhood - Soldier (Swing)",
         lambda state: has_all_moves(state, player, ["Double Jump", "Ledge Grab"]))

    rule("Andy's Neighborhood - Soldier (Pool Plant)",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Pole Climb", "Pole Vault"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Pole Climb", "Ledge Grab"]))
         ))

    rule("Andy's Neighborhood - Soldier (Tree)",
         lambda state: has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Pole Climb"]))

    rule("Andy's Neighborhood - Life (Top of Swing)",
         lambda state: has_all_moves(state, player, ["Double Jump", "Ledge Grab"]))

    # Green Laser - no requirements

    # Battery (Lawnmower Yard) - no requirements

    rule("Andy's Neighborhood - Battery (Washing Machine)",
         lambda state: (
             has_all_moves(state, player, ["Stomp", "Double Jump", "Ledge Grab"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Ledge Grab"]))
         ))

    rule("Andy's Neighborhood - Battery (Pool Yard)",
         lambda state: has_all_moves(state, player, ["Double Jump", "Pole Climb"]))

    rule("Andy's Neighborhood - Battery (Swing)",
         lambda state: has_all_moves(state, player, ["Double Jump", "Ledge Grab"]))

    rule("Andy's Neighborhood - Battery (Top of Tree)",
         lambda state: has_all_moves(state, player,
                                      ["Double Jump", "Ledge Grab", "Pole Climb", "Pole Vault"]))

    # Talk to Rex - no requirements

    # ── BOMBS AWAY! ───────────────────────────────────────────

    rule("Bombs Away! - Defeat Reward 1",
         lambda state: has_any_attack(state, player))
    rule("Bombs Away! - Defeat Reward 2",
         lambda state: has_any_attack(state, player))
    # Batteries - no requirements

    # ── CONSTRUCTION YARD ─────────────────────────────────────

    for loc in multiworld.get_locations(player):
        if "Coin Bundle" in loc.name and "Construction Yard" in loc.name:
            bundle_num = int(loc.name.split("Coin Bundle ")[1])
            loc.access_rule = lambda state, bn=bundle_num: coin_bundle_rule(
                state, player, "Construction Yard", bn, bundle_size, skips, world)

    rule("Construction Yard - Hamm's 50 Coins Token",
         lambda state: (
             hamms_50_coins_rule(state, player, "Construction Yard", skips,
                                  ["Push", "Double Jump", "Ledge Grab"], [], world) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              hamms_50_coins_rule(state, player, "Construction Yard", skips,
                                   ["Double Jump"], [], world))
         ))

    rule("Construction Yard - Missing Toys Token",
         lambda state: missing_toys_token_rule(state, player, "Construction Yard",
                                                ["Double Jump"], [], []))

    rule("Construction Yard - Race Token",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Ledge Grab"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_double_jump(state, player))
         ))

    rule("Construction Yard - Hidden Token",
         lambda state: (
             has_all_moves(state, player,
                            ["Double Jump", "Ledge Grab", "Pole Climb", "Stomp", "Push"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Stomp", "Double Jump", "Ledge Grab", "Push"]))
         ))

    rule("Construction Yard - Boss Token",
         lambda state: (
             (has_all_moves(state, player, ['Double Jump', 'Ledge Grab', 'Stomp', 'Pole Climb', 'Laser']) and has_all_gadgets(state, player, ['Disc Launcher'], "Construction Yard")) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_all_moves(state, player, ['Double Jump', 'Laser']) and has_all_gadgets(state, player, ['Disc Launcher'], "Construction Yard"))
         ))

    rule("Construction Yard - Worker Tike (Wheelbarrow)",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Push", "Ledge Grab"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_double_jump(state, player))
         ))

    rule("Construction Yard - Worker Tike (Filing Cabinets)",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Pole Climb"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Ledge Grab"]))
         ))

    rule("Construction Yard - Worker Tike (Bulldozer)",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Ledge Grab"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_double_jump(state, player))
         ))

    rule("Construction Yard - Worker Tike (Construction Floor 1)",
         lambda state: (
             has_all_moves(state, player, ["Stomp", "Double Jump", "Ledge Grab"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_double_jump(state, player))
         ))

    rule("Construction Yard - Worker Tike (Boss Arena)",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Stomp", "Pole Climb"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_double_jump(state, player))
         ))

    rule("Construction Yard - Missing Eye",
         lambda state: (
             has_all_moves(state, player, ["Stomp", "Double Jump", "Ledge Grab", "Pole Climb"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_double_jump(state, player))
         ))

    rule("Construction Yard - Give Potato Head His Eye",
         lambda state: give_potato_head_rule(state, player, "Missing Eye"))

    rule("Construction Yard - Life (Top of Bulldozer)",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Stomp", "Pole Climb"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_double_jump(state, player))
         ))

    rule("Construction Yard - Life (Roof of Green Building)",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Stomp", "Pole Climb"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_double_jump(state, player))
         ))

    # Green Laser - no requirements

    rule("Construction Yard - Battery (Bulldozer)",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Ledge Grab"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_double_jump(state, player))
         ))

    for battery in ["Battery (Boss Arena Front Left)", "Battery (Boss Arena Back Left)",
                    "Battery (Boss Arena Back Right)"]:
        rule(f"Construction Yard - {battery}",
             lambda state: (
                 has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Stomp", "Pole Climb"]) or
                 (skips in (SKIPS_EASY, SKIPS_HARD) and has_double_jump(state, player))
             ))

    # Talk to Rex - no requirements

    # ── ALLEYS AND GULLIES ────────────────────────────────────

    for loc in multiworld.get_locations(player):
        if "Coin Bundle" in loc.name and "Alleys and Gullies" in loc.name:
            bundle_num = int(loc.name.split("Coin Bundle ")[1])
            loc.access_rule = lambda state, bn=bundle_num: coin_bundle_rule(
                state, player, "Alleys and Gullies", bn, bundle_size, skips, world)

    rule("Alleys and Gullies - Hamm's 50 Coins Token",
         lambda state: hamms_50_coins_rule(state, player, "Alleys and Gullies", skips,
                                            ["Rope Sliding"],
                                            ["Ledge Grab", "Double Jump"], world))

    # Missing Toys Token - no requirements beyond toys

    rule("Alleys and Gullies - Race Token",
         lambda state: has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Push"]))

    rule("Alleys and Gullies - Hidden Token",
         lambda state: (
             (has_all_moves(state, player, ['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Pole Vault', 'Stomp', 'Pole Climb'])) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_all_moves(state, player, ['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp']))
         ))

    rule("Alleys and Gullies - Boss Token",
         lambda state: (
             has_all_moves(state, player,
                            ["Visor", "Pole Climb", "Rope Sliding", "Double Jump"]) and
             has_any_attack(state, player) and
             has_grappling_hook_alleys(state, player)
         ))

    rule("Alleys and Gullies - Duck (Pool Behind Construction)",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Rope Sliding", "Ledge Grab"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_rope_sliding(state, player) and
              has_any_move(state, player, ["Ledge Grab", "Double Jump"]))
         ))

    rule("Alleys and Gullies - Duck (Hidden Near Race)",
         lambda state: has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Push"]))

    rule("Alleys and Gullies - Duck (Incline Parasol)",
         lambda state: (
             (has_all_moves(state, player, ['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp', 'Pole Vault']) and has_all_gadgets(state, player, ['Rocket Boots'], "Alleys and Gullies")) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_all_moves(state, player, ['Double Jump', 'Rope Sliding', 'Ledge Grab']))
         ))

    rule("Alleys and Gullies - Duck (Window Sill)",
         lambda state: (
             has_all_moves(state, player, ["Visor", "Pole Climb", "Rope Sliding"]) and
             has_any_move(state, player, ["Double Jump", "Ledge Grab"]) and
             has_grappling_hook_alleys(state, player)
         ))

    rule("Alleys and Gullies - Duck (Rain Gutter)",
         lambda state: (
             has_all_moves(state, player, ["Visor", "Pole Climb", "Rope Sliding"]) and
             has_any_move(state, player, ["Double Jump", "Ledge Grab"]) and
             has_grappling_hook_alleys(state, player)
         ))

    # Missing Part - Arm is in Al's Toy Barn

    rule("Alleys and Gullies - Life (Pool Behind Construction)",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Rope Sliding", "Ledge Grab"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_rope_sliding(state, player) and
              has_any_move(state, player, ["Ledge Grab", "Double Jump"]))
         ))

    rule("Alleys and Gullies - Life (Lily Pad Behind Race)",
         lambda state: has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Push"]))

    rule("Alleys and Gullies - Life (Window Sill)",
         lambda state: (
             has_all_moves(state, player, ["Visor", "Pole Climb", "Rope Sliding"]) and
             has_any_move(state, player, ["Double Jump", "Ledge Grab"]) and
             has_grappling_hook_alleys(state, player)
         ))

    # Green Laser - no requirements

    rule("Alleys and Gullies - Battery (Behind Construction)",
         lambda state: (
             has_rope_sliding(state, player) and
             has_any_move(state, player, ["Ledge Grab", "Double Jump"])
         ))

    rule("Alleys and Gullies - Battery (Balcony Fence)",
         lambda state: (
             has_all_moves(state, player, ["Visor", "Pole Climb", "Rope Sliding"]) and
             has_any_move(state, player, ["Ledge Grab", "Double Jump"]) and
             has_grappling_hook_alleys(state, player)
         ))

    rule("Alleys and Gullies - Battery (Boss Arena)",
         lambda state: (
             has_all_moves(state, player,
                            ["Visor", "Pole Climb", "Rope Sliding", "Double Jump"]) and
             has_grappling_hook_alleys(state, player)
         ))

    # Talk to Rex - no requirements

    # ── SLIME TIME ────────────────────────────────────────────

    rule("Slime Time - Defeat Reward 1", lambda state: has_laser(state, player))
    rule("Slime Time - Defeat Reward 2", lambda state: has_laser(state, player))
    rule("Slime Time - Green Laser",
         lambda state: (
             has_all_moves(state, player, ['Laser'])
         ))

    # ── AL'S TOY BARN ─────────────────────────────────────────

    for loc in multiworld.get_locations(player):
        if "Coin Bundle" in loc.name and "Al's Toy Barn" in loc.name:
            bundle_num = int(loc.name.split("Coin Bundle ")[1])
            loc.access_rule = lambda state, bn=bundle_num: coin_bundle_rule(
                state, player, "Al's Toy Barn", bn, bundle_size, skips, world)

    rule("Al's Toy Barn - Hamm's 50 Coins Token",
         lambda state: hamms_50_coins_rule(state, player, "Al's Toy Barn", skips,
                                            [], [], world,
                                            move_check=lambda s, p: (
                                                has_pole_climb(s, p) or
                                                (has_double_jump(s, p) and has_ledge_grab(s, p))
                                            )))

    # Missing Toys Token - no requirements beyond toys

    rule("Al's Toy Barn - Race Token",
         lambda state: (
             has_all_moves(state, player, ["Pole Vault", "Rope Sliding"]) and
             has_any_move(state, player, ["Double Jump", "Ledge Grab"])
         ))

    rule("Al's Toy Barn - Hidden Token",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Ledge Grab"]) and
             has_disc_launcher_toybarn(state, player)
         ))

    rule("Al's Toy Barn - Boss Token",
         lambda state: (
             (has_all_moves(state, player, ['Double Jump', 'Pole Climb']) and has_any_move(state, player, ['Laser', 'Spin', 'Stomp', 'Ledge Grab']) and has_any_gadget(state, player, ['Disc Launcher', 'Hover Boots'], "Al's Toy Barn")) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_all_moves(state, player, ['Double Jump', 'Ledge Grab']) and has_any_move(state, player, ['Laser', 'Spin', 'Stomp']) and has_any_gadget(state, player, ['Disc Launcher'], "Al's Toy Barn"))
         ))

    rule("Al's Toy Barn - Chick (Complete Race)",
         lambda state: (
             has_all_moves(state, player, ["Pole Vault", "Rope Sliding"]) and
             has_any_move(state, player, ["Double Jump", "Ledge Grab"])
         ))

    rule("Al's Toy Barn - Chick (Gumball Machines)",
         lambda state: (
             (has_all_moves(state, player, ['Double Jump', 'Stomp', 'Pole Vault']) and has_all_gadgets(state, player, ['Rocket Boots'], "Al's Toy Barn")) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_all_moves(state, player, ['Double Jump', 'Ledge Grab']) and has_all_gadgets(state, player, ['Rocket Boots'], "Al's Toy Barn"))
         ))

    rule("Al's Toy Barn - Chick (Shipping Boxes)",
         lambda state: (
             has_double_jump(state, player) and has_hover_boots_toybarn(state, player)
         ))

    rule("Al's Toy Barn - Chick (Near Basketballs)",
         lambda state: (
             has_pole_climb(state, player) and
             has_any_move(state, player, ["Double Jump", "Ledge Grab"])
         ))

    rule("Al's Toy Barn - Chick (End of Long Aisle)",
         lambda state: (
             (has_all_moves(state, player, ['Push', 'Double Jump', 'Ledge Grab'])) or
             (skips == SKIPS_HARD and has_all_moves(state, player, ['Double Jump']) and has_all_gadgets(state, player, ['Rocket Boots'], "Al's Toy Barn"))
         ))

    rule("Al's Toy Barn - Missing Arm",
         lambda state: (
             has_all_moves(state, player,
                            ["Double Jump", "Ledge Grab", "Rope Sliding", "Pole Vault"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Ledge Grab"])) or
             (skips == SKIPS_HARD and has_double_jump(state, player))
         ))

    rule("Al's Toy Barn - Give Potato Head His Arm",
         lambda state: give_potato_head_rule(state, player, "Missing Arm",
                                              moves_and=["Double Jump"]))

    # Life (Tennis Ball Isle) - no requirements
    # Green Laser - no requirements

    rule("Al's Toy Barn - Battery (Gumball Machine)",
         lambda state: (
             (has_all_moves(state, player, ["Stomp", "Double Jump", "Rope Sliding", "Pole Vault"]) and
              has_rocket_boots_toybarn(state, player)) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Pole Vault", "Ledge Grab"]) and
              has_any_move(state, player, ["Stomp", "Rope Sliding"]))
         ))

    rule("Al's Toy Barn - Battery (Ventilation Shaft)",
         lambda state: (
             (has_all_moves(state, player, ['Push', 'Double Jump', 'Ledge Grab'])) or
             (skips == SKIPS_HARD and has_all_moves(state, player, ['Double Jump']) and has_all_gadgets(state, player, ['Rocket Boots'], "Al's Toy Barn"))
         ))

    rule("Al's Toy Barn - Battery (Between Bicycles)",
         lambda state: (
             has_pole_climb(state, player) and
             has_any_move(state, player, ["Double Jump", "Ledge Grab"])
         ))

    rule("Al's Toy Barn - Battery (Cardboard Boxes)",
         lambda state: (
             has_all_moves(state, player, ['Double Jump']) and has_any_move(state, player, ['Ledge Grab']) and has_any_gadget(state, player, ['Hover Boots'], "Al's Toy Barn")
         ))

    rule("Al's Toy Barn - Battery (Boss Arena)",
         lambda state: (
             has_all_moves(state, player, ['Double Jump', 'Pole Climb']) and has_any_move(state, player, ['Ledge Grab']) and has_any_gadget(state, player, ['Hover Boots'], "Al's Toy Barn")
         ))

    rule("Al's Toy Barn - Talk to Rex",
         lambda state: (
             has_all_moves(state, player, ['Double Jump']) and has_any_move(state, player, ['Ledge Grab']) and has_any_gadget(state, player, ['Hover Boots'], "Al's Toy Barn")
         ))

    # ── AL'S SPACE LAND ───────────────────────────────────────

    for loc in multiworld.get_locations(player):
        if "Coin Bundle" in loc.name and "Al's Space Land" in loc.name:
            bundle_num = int(loc.name.split("Coin Bundle ")[1])
            loc.access_rule = lambda state, bn=bundle_num: coin_bundle_rule(
                state, player, "Al's Space Land", bn, bundle_size, skips, world)

    rule("Al's Space Land - Hamm's 50 Coins Token",
         lambda state: (
             hamms_50_coins_rule(state, player, "Al's Space Land", skips,
                                  ["Double Jump", "Ledge Grab", "Pole Vault", "Rope Sliding"],
                                  [], world) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              hamms_50_coins_rule(state, player, "Al's Space Land", skips,
                                   ["Double Jump", "Pole Vault", "Ledge Grab"], [], world))
         ))

    # Missing Toys Token - no requirements beyond toys

    rule("Al's Space Land - Race Token",
         lambda state: has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Rope Sliding"]))

    rule("Al's Space Land - Hidden Token",
         lambda state: has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Stomp"]))

    rule("Al's Space Land - Boss Token",
         lambda state: (
             (has_all_moves(state, player, ['Push', 'Double Jump', 'Ledge Grab', 'Pole Climb']) and has_any_move(state, player, ['Laser', 'Spin', 'Stomp'])) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_all_moves(state, player, ['Double Jump', 'Ledge Grab', 'Pole Climb']) and has_any_move(state, player, ['Laser', 'Spin', 'Stomp']))
         ))

    rule("Al's Space Land - Alien (Ballpit)",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Pole Climb"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Ledge Grab"]))
         ))

    rule("Al's Space Land - Alien (Planet Mobile)",
         lambda state: has_all_moves(state, player,
                                      ["Push", "Double Jump", "Ledge Grab", "Pole Climb"]))

    rule("Al's Space Land - Alien (End of Race)",
         lambda state: has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Rope Sliding"]))

    rule("Al's Space Land - Alien (Middle of Zurg Aisle)",
         lambda state: (
             has_all_moves(state, player,
                            ["Double Jump", "Ledge Grab", "Pole Vault", "Rope Sliding"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Pole Vault", "Ledge Grab"]))
         ))

    rule("Al's Space Land - Alien (End of Zurg Aisle)",
         lambda state: (
             has_all_moves(state, player,
                            ["Double Jump", "Ledge Grab", "Pole Vault", "Rope Sliding"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Pole Vault", "Ledge Grab"]))
         ))

    rule("Al's Space Land - Life (Planet Mobile)",
         lambda state: (
             has_all_moves(state, player,
                            ["Push", "Double Jump", "Ledge Grab", "Pole Climb"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Pole Climb"]))
         ))

    # Green Laser - no requirements

    rule("Al's Space Land - Battery (Boss Arena)",
         lambda state: (
             has_all_moves(state, player,
                            ["Push", "Double Jump", "Ledge Grab", "Pole Climb"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Pole Climb"]))
         ))

    rule("Al's Space Land - Battery (Arcade Cabinet)",
         lambda state: has_all_moves(state, player, ["Double Jump", "Ledge Grab"]))

    rule("Al's Space Land - Battery (Blue Shelves)",
         lambda state: has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Pole Vault"]))

    rule("Al's Space Land - Battery (Red Shelf)",
         lambda state: (
             has_all_moves(state, player,
                            ["Double Jump", "Ledge Grab", "Pole Vault", "Rope Sliding"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Pole Vault", "Ledge Grab"]))
         ))

    rule("Al's Space Land - Battery (Race Blue Shelf)",
         lambda state: has_all_moves(state, player,
                                      ["Double Jump", "Ledge Grab", "Rope Sliding"]))

    # Talk to Rex - no requirements

    # ── TOY BARN ENCOUNTER ────────────────────────────────────

    rule("Toy Barn Encounter - Defeat Reward 1",
         lambda state: has_laser(state, player) and has_any_move(state, player, ["Spin", "Stomp"]))
    rule("Toy Barn Encounter - Defeat Reward 2",
         lambda state: has_laser(state, player) and has_any_move(state, player, ["Spin", "Stomp"]))
    # All batteries - no requirements

    # ── ELEVATOR HOP ──────────────────────────────────────────

    for loc in multiworld.get_locations(player):
        if "Coin Bundle" in loc.name and "Elevator Hop" in loc.name:
            bundle_num = int(loc.name.split("Coin Bundle ")[1])
            loc.access_rule = lambda state, bn=bundle_num: coin_bundle_rule(
                state, player, "Elevator Hop", bn, bundle_size, skips, world)

    rule("Elevator Hop - Hamm's 50 Coins Token",
         lambda state: hamms_50_coins_rule(state, player, "Elevator Hop", skips,
                                            ["Double Jump", "Pole Vault", "Ledge Grab"], [],
                                            world))

    rule("Elevator Hop - Missing Toys Token",
         lambda state: (
             missing_toys_token_rule(state, player, "Elevator Hop",
                                      ["Visor"], [], ["Grappling Hook - Elevator Hop"])
         ))

    rule("Elevator Hop - Race Token",
         lambda state: (
             has_all_moves(state, player, ["Visor", "Double Jump", "Stomp"]) and
             has_grappling_hook_elevator(state, player)
         ))

    rule("Elevator Hop - Hidden Token",
         lambda state: (
             has_all_moves(state, player, ["Visor", "Double Jump", "Stomp"]) and
             has_grappling_hook_elevator(state, player)
         ))

    rule("Elevator Hop - Boss Token",
         lambda state: (
             has_all_moves(state, player, ['Visor', 'Double Jump', 'Stomp']) and has_any_move(state, player, ['Laser', 'Spin']) and has_all_gadgets(state, player, ['Grappling Hook'], "Elevator Hop")
         ))

    rule("Elevator Hop - Mouse (Electrical Room)",
         lambda state: has_all_moves(state, player,
                                      ["Pole Vault", "Double Jump", "Rope Sliding", "Ledge Grab"]))

    rule("Elevator Hop - Mouse (Next to Rex)",
         lambda state: (
             has_visor(state, player) and has_grappling_hook_elevator(state, player)
         ))

    rule("Elevator Hop - Mouse (Control Room)",
         lambda state: (
             has_all_moves(state, player, ["Visor", "Double Jump"]) and
             has_grappling_hook_elevator(state, player)
         ))

    rule("Elevator Hop - Mouse (Side of Elevator Shaft)",
         lambda state: (
             has_all_moves(state, player, ["Visor", "Stomp", "Double Jump"]) and
             has_grappling_hook_elevator(state, player)
         ))

    rule("Elevator Hop - Mouse (Top of Elevator)",
         lambda state: (
             has_all_moves(state, player, ["Visor", "Double Jump", "Stomp"]) and
             has_grappling_hook_elevator(state, player)
         ))

    rule("Elevator Hop - Missing Foot",
         lambda state: has_all_moves(state, player,
                                      ["Pole Vault", "Double Jump", "Rope Sliding", "Ledge Grab"]))

    rule("Elevator Hop - Give Potato Head His Foot",
         lambda state: give_potato_head_rule(state, player, "Missing Foot"))

    rule("Elevator Hop - Green Laser",
         lambda state: has_visor(state, player) and has_grappling_hook_elevator(state, player))

    rule("Elevator Hop - Talk to Rex",
         lambda state: has_visor(state, player) and has_grappling_hook_elevator(state, player))

    # ── AL'S PENTHOUSE ────────────────────────────────────────

    for loc in multiworld.get_locations(player):
        if "Coin Bundle" in loc.name and "Al's Penthouse" in loc.name:
            bundle_num = int(loc.name.split("Coin Bundle ")[1])
            loc.access_rule = lambda state, bn=bundle_num: coin_bundle_rule(
                state, player, "Al's Penthouse", bn, bundle_size, skips, world)

    rule("Al's Penthouse - Hamm's 50 Coins Token",
         lambda state: (
             hamms_50_coins_rule(state, player, "Al's Penthouse", skips,
                                  ["Laser"], ["Double Jump", "Visor"], world) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              hamms_50_coins_rule(state, player, "Al's Penthouse", skips,
                                   ["Double Jump", "Ledge Grab"],
                                   ["Spin", "Stomp"], world))
         ))

    rule("Al's Penthouse - Missing Toys Token",
         lambda state: missing_toys_token_rule(state, player, "Al's Penthouse",
                                                ["Visor", "Laser", "Double Jump"], [], []))

    rule("Al's Penthouse - Race Token",
         lambda state: has_ledge_grab(state, player))

    rule("Al's Penthouse - Hidden Token",
         lambda state: (
             has_all_moves(state, player, ["Push", "Double Jump", "Ledge Grab", "Stomp"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Push", "Double Jump", "Ledge Grab"]))
         ))

    rule("Al's Penthouse - Boss Token",
         lambda state: (
             has_all_moves(state, player, ['Push', 'Double Jump', 'Ledge Grab']) and has_any_move(state, player, ['Laser', 'Spin', 'Stomp'])
         ))

    rule("Al's Penthouse - Critter (Living Room)",
         lambda state: has_all_moves(state, player,
                                      ["Double Jump", "Ledge Grab", "Pole Climb", "Pole Vault"]))

    rule("Al's Penthouse - Critter (Kitchen)",
         lambda state: (
             (has_all_moves(state, player, ['Laser', 'Stomp', 'Visor', 'Pole Climb', 'Double Jump'])) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_all_moves(state, player, ['Laser', 'Visor', 'Double Jump']))
         ))

    rule("Al's Penthouse - Critter (Bathroom)",
         lambda state: (
             has_all_moves(state, player, ["Laser", "Stomp", "Double Jump", "Ledge Grab"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Stomp"]))
         ))

    rule("Al's Penthouse - Critter (Train Bed)",
         lambda state: (
             has_all_moves(state, player, ["Push", "Double Jump", "Ledge Grab", "Stomp"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Push", "Double Jump", "Ledge Grab"]))
         ))

    rule("Al's Penthouse - Critter (Woody Room)",
         lambda state: has_all_moves(state, player, ["Push", "Double Jump", "Ledge Grab"]))

    rule("Al's Penthouse - Life (Fireplace)",
         lambda state: has_cosmic_shield_penthouse(state, player))

    rule("Al's Penthouse - Green Laser",
         lambda state: has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Pole Climb"]))

    # Battery (Under Table) - no requirements

    rule("Al's Penthouse - Battery (Bathroom)",
         lambda state: (
             (has_all_moves(state, player, ['Laser', 'Stomp', 'Double Jump', 'Ledge Grab'])) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_all_moves(state, player, ['Double Jump', 'Ledge Grab', 'Stomp']))
         ))

    # Battery (Kitchen) - no requirements

    rule("Al's Penthouse - Battery (Train Bed)",
         lambda state: has_all_moves(state, player,
                                      ["Push", "Double Jump", "Ledge Grab", "Stomp"]))

    rule("Al's Penthouse - Battery (Television)",
         lambda state: has_all_moves(state, player, ["Push", "Double Jump", "Ledge Grab"]))

    # Talk to Rex - no requirements

    # ── THE EVIL EMPEROR ZURG ─────────────────────────────────

    rule("The Evil Emperor Zurg - Defeat Reward 1",
         lambda state: has_spin(state, player))
    rule("The Evil Emperor Zurg - Defeat Reward 2",
         lambda state: has_spin(state, player))

    # ── AIRPORT INFILTRATION ──────────────────────────────────

    for loc in multiworld.get_locations(player):
        if "Coin Bundle" in loc.name and "Airport Infiltration" in loc.name:
            bundle_num = int(loc.name.split("Coin Bundle ")[1])
            loc.access_rule = lambda state, bn=bundle_num: coin_bundle_rule(
                state, player, "Airport Infiltration", bn, bundle_size, skips, world)

    def airport_base(state): return has_all_moves(state, player, ["Stomp", "Double Jump", "Pole Vault"])
    def airport_hard(state): return has_all_moves(state, player, ["Double Jump", "Stomp"])

    rule("Airport Infiltration - Hamm's 50 Coins Token",
         lambda state: (
             (hamms_50_coins_rule(state, player, "Airport Infiltration", skips,
                                   ["Stomp", "Double Jump", "Pole Vault", "Pole Climb"],
                                   [], world)) or
             (skips == SKIPS_HARD and
              hamms_50_coins_rule(state, player, "Airport Infiltration", skips,
                                   ["Double Jump", "Stomp", "Pole Vault"], [], world))
         ))

    rule("Airport Infiltration - Missing Toys Token",
         lambda state: (
             airport_base(state) or
             (skips == SKIPS_HARD and airport_hard(state))
         ))

    rule("Airport Infiltration - Race Token",
         lambda state: (
             has_all_moves(state, player, ["Stomp", "Double Jump", "Pole Vault", "Ledge Grab"]) or
             (skips == SKIPS_HARD and
              has_all_moves(state, player, ["Double Jump", "Stomp", "Ledge Grab"]))
         ))

    rule("Airport Infiltration - Hidden Token",
         lambda state: (
             (has_all_moves(state, player, ['Stomp', 'Double Jump', 'Pole Vault', 'Ledge Grab']) and has_all_gadgets(state, player, ['Hover Boots'], "Airport Infiltration")) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_all_moves(state, player, ['Stomp', 'Double Jump', 'Pole Vault', 'Ledge Grab', 'Pole Climb']))
         ))

    rule("Airport Infiltration - Boss Token",
         lambda state: (
             (has_all_moves(state, player, ['Stomp', 'Double Jump', 'Pole Vault']) and has_all_gadgets(state, player, ['Hover Boots'], "Airport Infiltration")) or
             (skips == SKIPS_HARD and has_all_moves(state, player, ['Double Jump', 'Stomp']) and has_all_gadgets(state, player, ['Hover Boots'], "Airport Infiltration"))
         ))

    rule("Airport Infiltration - Passenger Tike (Near Start)",
         lambda state: (
             has_all_moves(state, player,
                            ["Stomp", "Double Jump", "Pole Vault", "Pole Climb"]) or
             (skips == SKIPS_HARD and
              has_all_moves(state, player, ["Double Jump", "Stomp", "Pole Vault"]))
         ))

    rule("Airport Infiltration - Passenger Tike (Top of Conveyor Belts)",
         lambda state: (
             (has_all_moves(state, player,
                             ["Stomp", "Double Jump", "Pole Vault", "Pole Climb"]) and
              has_any_move(state, player, ["Rope Sliding", "Ledge Grab"])) or
             (skips == SKIPS_HARD and
              has_all_moves(state, player,
                             ["Double Jump", "Stomp", "Pole Climb", "Ledge Grab"]))
         ))

    rule("Airport Infiltration - Passenger Tike (Near Boss Arena)",
         lambda state: (
             (has_all_moves(state, player, ['Stomp', 'Double Jump', 'Pole Vault', 'Pole Climb', 'Rope Sliding']) and has_all_gadgets(state, player, ['Hover Boots'], "Airport Infiltration")) or
             (skips == SKIPS_HARD and has_all_moves(state, player, ['Double Jump', 'Stomp', 'Pole Climb', 'Rope Sliding']) and has_all_gadgets(state, player, ['Hover Boots'], "Airport Infiltration"))
         ))

    rule("Airport Infiltration - Passenger Tike (Top of Jet)",
         lambda state: (
             has_all_moves(state, player,
                            ["Stomp", "Double Jump", "Pole Vault",
                             "Ledge Grab", "Pole Climb"]) or
             (skips == SKIPS_HARD and
              has_all_moves(state, player,
                             ["Double Jump", "Stomp", "Pole Climb", "Ledge Grab"]))
         ))

    rule("Airport Infiltration - Passenger Tike (Scaffolding)",
         lambda state: (
             (has_all_moves(state, player, ['Stomp', 'Double Jump', 'Pole Vault', 'Ledge Grab', 'Pole Climb'])) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_all_moves(state, player, ['Double Jump', 'Stomp', 'Ledge Grab', 'Pole Vault']))
         ))

    rule("Airport Infiltration - Missing Mouth",
         lambda state: (
             has_all_moves(state, player,
                            ["Stomp", "Double Jump", "Pole Vault", "Push", "Ledge Grab"]) or
             (skips == SKIPS_HARD and
              has_all_moves(state, player, ["Double Jump", "Stomp", "Ledge Grab"]))
         ))

    rule("Airport Infiltration - Give Potato Head His Mouth",
         lambda state: (
             give_potato_head_rule(state, player, "Missing Mouth",
                                   moves_and=["Stomp", "Double Jump", "Pole Vault"]) or
             (skips == SKIPS_HARD and
              give_potato_head_rule(state, player, "Missing Mouth",
                                    moves_and=["Double Jump", "Stomp"]))
         ))

    rule("Airport Infiltration - Green Laser",
         lambda state: (
             airport_base(state) or
             (skips == SKIPS_HARD and airport_hard(state))
         ))

    rule("Airport Infiltration - Battery (Luggage Pile)",
         lambda state: (
             airport_base(state) or
             (skips == SKIPS_HARD and
              has_all_moves(state, player, ["Double Jump", "Stomp", "Pole Climb"]))
         ))

    rule("Airport Infiltration - Battery (Near Hidden Token)",
         lambda state: (
             (has_all_moves(state, player,
                             ["Stomp", "Double Jump", "Pole Vault",
                              "Ledge Grab", "Pole Climb"]) and
              has_hover_boots_airport(state, player)) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player,
                             ["Stomp", "Double Jump", "Pole Vault",
                              "Ledge Grab", "Pole Climb"]))
         ))

    rule("Airport Infiltration - Battery (Boss Arena)",
         lambda state: (
             (has_all_moves(state, player, ['Stomp', 'Double Jump', 'Pole Vault']) and has_all_gadgets(state, player, ['Hover Boots'], "Airport Infiltration")) or
             (skips == SKIPS_HARD and has_all_moves(state, player, ['Double Jump', 'Stomp']) and has_all_gadgets(state, player, ['Hover Boots'], "Airport Infiltration"))
         ))

    rule("Airport Infiltration - Talk to Rex",
         lambda state: (
             airport_base(state) or
             (skips == SKIPS_HARD and airport_hard(state))
         ))

    # ── TARMAC TROUBLE ────────────────────────────────────────

    for loc in multiworld.get_locations(player):
        if "Coin Bundle" in loc.name and "Tarmac Trouble" in loc.name:
            bundle_num = int(loc.name.split("Coin Bundle ")[1])
            loc.access_rule = lambda state, bn=bundle_num: coin_bundle_rule(
                state, player, "Tarmac Trouble", bn, bundle_size, skips, world)

    # Hamm's 50 Coins - no move requirements beyond coins
    rule("Tarmac Trouble - Hamm's 50 Coins Token",
         lambda state: hamms_50_coins_rule(state, player, "Tarmac Trouble", skips,
                                            [], [], world))

    # Missing Toys Token - no requirements beyond toys

    # Race Token - no requirements

    rule("Tarmac Trouble - Hidden Token",
         lambda state: has_all_moves(state, player,
                                      ["Double Jump", "Ledge Grab", "Pole Climb", "Stomp"]))

    rule("Tarmac Trouble - Boss Token",
         lambda state: (
             has_all_moves(state, player, ["Pole Climb", "Double Jump"]) and
             has_any_move(state, player, ["Spin", "Stomp"])
         ))

    rule("Tarmac Trouble - Luggage (Top of Plane)",
         lambda state: has_pole_climb(state, player))

    rule("Tarmac Trouble - Luggage (Zone 2 Cart)",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Pole Climb"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and has_double_jump(state, player))
         ))

    rule("Tarmac Trouble - Luggage (Zone 8)",
         lambda state: has_pole_climb(state, player))

    rule("Tarmac Trouble - Luggage (Zone 6 Conveyor Belt)",
         lambda state: has_pole_climb(state, player))

    # Luggage (Zone 4) - no requirements

    rule("Tarmac Trouble - Life (Zone 6)",
         lambda state: has_pole_climb(state, player))

    # Green Laser - no requirements
    # Battery (Road Opposite Zone 8) - no requirements

    rule("Tarmac Trouble - Battery (Helicopter Pad)",
         lambda state: has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Pole Climb"]))

    # Battery (Zone 3) - no requirements
    # Battery (Green Slime Maze) - no requirements

    rule("Tarmac Trouble - Battery (Boss Arena)",
         lambda state: has_all_moves(state, player, ["Pole Climb", "Double Jump"]))

    rule("Tarmac Trouble - Talk to Rex",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Ledge Grab"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD))
         ))

    # ── PROSPECTOR SHOWDOWN ───────────────────────────────────

    rule("Prospector Showdown - Defeat GOAL",
         lambda state: goal_rule(state, player, world))

    # ── MISSING TOYS TOKEN: require 5 toys (blanket safety pass) ──
    # Several per-level Missing Toys Tokens were left without an access rule
    # (just a comment), so they defaulted to always-reachable — the tracker then
    # thought you could claim them with zero toys. Ensure EVERY Missing Toys
    # Token requires all 5 of its level's toy item, wrapping any existing rule.
    for level_name, toy_item in MISSING_TOYS_TOKEN_ITEM.items():
        loc_name = f"{level_name} - Missing Toys Token"
        try:
            loc = multiworld.get_location(loc_name, player)
        except KeyError:
            continue
        if loc is None:
            continue
        prev = loc.access_rule
        loc.access_rule = lambda state, ti=toy_item, er=prev: (
            state.has(ti, player, 5) and er(state)
        )

    # ── LEVEL ACCESS RULES ────────────────────────────────────
    # NOTE: Level access is enforced by each region's ENTRANCE rule (set in
    # create_regions: the "To <level>" entrance uses can_access_level). A location
    # is only reachable if its region is reachable AND its own access_rule passes,
    # so we do NOT also wrap every location's access_rule with can_access_level.
    # The old wrapper here did that redundantly and, after locations were renamed
    # to "<Level> - <Thing>", its suffix/substring region detection mis-assigned
    # regions and created an infinite recursion through the boss-defeat checks.

    # ── HINT BLOCK SANITY ─────────────────────────────────────
    # Rules translated from the per-level logic sheets. Hard branch is the
    # default required move set; the Easy/Hard skip branches relax it. "No
    # requirements" locations get no rule (reachable once the region is).
    rule("Andy's House - Hint Block (Andy's Room Bookshelf)",
         lambda state: has_all_moves(state, player, ["Double Jump", "Ledge Grab"]))
    rule("Andy's House - Hint Block (Andy's Room Bed)",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Push"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Ledge Grab"]))
         ))
    rule("Andy's House - Hint Block (Andy's Room Dresser Shelf)",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Push", "Pole Climb"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Pole Climb"]))
         ))
    rule("Andy's House - Hint Block (Andy's Room Crib)",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Push", "Pole Climb", "Rope Sliding"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Ledge Grab"]))
         ))
    # Top of Stairs - No requirements
    rule("Andy's House - Hint Block (Attic)",
         lambda state: has_pole_climb(state, player))
    # Bottom of Stairs - No requirements
    rule("Andy's House - Hint Block (Top of Garage)",
         lambda state: (
             has_all_moves(state, player, ["Ledge Grab", "Double Jump", "Pole Climb"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Ledge Grab"]))
         ))
    rule("Andy's House - Hint Block (Living Room Recliner)",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Pole Climb"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD))  # Easy branch: No requirements
         ))

    # Andy's Neighborhood - No requirements
    # (Lawnmower Yard)

    rule("Construction Yard - Hint Block (Paint Can Room)",
         lambda state: (
             has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Pole Climb"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and
              has_all_moves(state, player, ["Double Jump", "Ledge Grab"]))
         ))

    # Al's Toy Barn - No requirements
    # (Hay Bale Ride)

    # Elevator Hop - East/West Shortcut Fan - No requirements
    rule("Elevator Hop - Hint Block (Control Room)",
         lambda state: (
             has_all_moves(state, player, ["Visor", "Double Jump"]) and
             has_grappling_hook_elevator(state, player)
         ))

    rule("Al's Penthouse - Hint Block (Bathtub)",
         lambda state: (
             has_laser(state, player) or
             has_all_moves(state, player, ["Double Jump", "Visor"]) or
             (skips in (SKIPS_EASY, SKIPS_HARD) and (
                 has_spin(state, player) or
                 has_all_moves(state, player, ["Double Jump", "Ledge Grab", "Stomp"])
             ))
         ))
    rule("Al's Penthouse - Hint Block (Train Bed)",
         lambda state: has_all_moves(state, player, ["Push", "Double Jump", "Ledge Grab"]))

    rule("Tarmac Trouble - Hint Block (Light Puzzle)",
         lambda state: has_all_moves(state, player, ["Pole Climb", "Double Jump"]))