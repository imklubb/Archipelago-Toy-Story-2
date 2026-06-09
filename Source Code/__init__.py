import math
import random
import logging
from typing import ClassVar, Dict, List, Optional, Tuple

from BaseClasses import Item, ItemClassification, MultiWorld, Region, Location, Tutorial
from worlds.AutoWorld import WebWorld, World
from .options import ToyStory2Options, ts2_option_groups
from .items import (
    ITEM_TABLE, ToyStory2Item, BASE_ID,
    MOVE_ITEMS, WEAPON_MOVE_ITEMS, TRAVERSAL_MOVE_ITEMS,
    GADGET_ITEMS, MISSING_PART_ITEMS, LEVEL_UNLOCK_ITEMS,
    COIN_LEVEL_UNLOCK_ITEMS, BOSS_UNLOCK_ITEMS,
    COIN_BUNDLE_ITEMS, TRAP_ITEMS, FILLER_ITEMS, MISSING_TOY_ITEMS,
)
from .locations import LOCATION_TABLE, ToyStory2Location, LOC_BASE
from .coin_data import COIN_DATA
from .rules import set_rules, can_access_level

# ── LAUNCHER COMPONENT (custom client) ────────────────────────
# Register a "Toy Story 2 Client" button in the Archipelago Launcher with the TS2
# icon. It launches the same BizHawk integration as the generic client, plus a
# filter that hides your own self->self "Sent" messages. Guarded so that any
# Launcher-API difference across Archipelago versions can't break world loading.
try:
    from worlds.LauncherComponents import (
        Component, components, Type, icon_paths,
    )
    try:
        from worlds.LauncherComponents import launch as _lc_launch  # newer API
    except Exception:
        _lc_launch = None

    # NOTE: the client launch + message filter are defined HERE, in __init__.py,
    # rather than in a separate client.py submodule. AP's frozen/zipped apworld
    # loader loads this __init__ but does NOT make sibling submodules importable
    # via importlib ("No module named 'worlds.toystory2.client'"), so any attempt
    # to import a submodule — eager or lazy — fails. Inlining avoids that entirely.
    # The heavy worlds._bizhawk imports stay inside the functions so they run at
    # click time (in the launcher process, where they ARE importable) and don't
    # cause a circular import at world-load time.

    def _ts2_make_gui_factory(orig_make_gui):
        """Wrap a context's make_gui() so the returned GameManager sets our window
        title."""
        def make_gui(self):
            ui = orig_make_gui(self)  # the stock GameManager class for this context

            class TS2Manager(ui):
                base_title = "Archipelago Toy Story 2 Client"

            return TS2Manager
        return make_gui

    def _ts2_launch(*args):
        """Defer to the stock BizHawk client's public launch entry (identical
        connect/watcher behaviour), only swapping the window title via make_gui."""
        from worlds._bizhawk.context import BizHawkClientContext
        if (hasattr(BizHawkClientContext, "make_gui")
                and not getattr(BizHawkClientContext, "_ts2_gui_wrapped", False)):
            BizHawkClientContext.make_gui = _ts2_make_gui_factory(
                BizHawkClientContext.make_gui)
            BizHawkClientContext._ts2_gui_wrapped = True
        from worlds._bizhawk.context import launch as bizhawk_launch
        bizhawk_launch(*args)

    def _launch_ts2_client(*args):
        import logging
        try:
            if _lc_launch is not None:
                _lc_launch(_ts2_launch, name="Toy Story 2 Client", args=args)
            else:
                _ts2_launch(*args)
        except Exception:
            logging.getLogger("Client").exception("[TS2] Failed to launch client")
            raise

    # Register the icon shipped inside this apworld. Derive the path from THIS
    # package's module name so it resolves regardless of where the apworld is
    # installed. The "ap:" prefix tells the launcher to resolve inside the package.
    icon_paths["ts2_logo"] = f"ap:{__name__}/TS2_Client_Logo.png"

    components.append(Component(
        "Toy Story 2 Client",
        func=_launch_ts2_client,
        component_type=Type.CLIENT,
        icon="ts2_logo",
        description="Connect to a Toy Story 2 (PS1) Archipelago game via BizHawk.",
    ))
    import logging as _logging
    _logging.getLogger("Client").info(
        "[TS2] Registered Toy Story 2 Client launcher component (pkg=%s)", __name__)
except Exception:
    # Launcher integration is optional; never let it block the world from loading,
    # but DO log why it failed so we can diagnose (otherwise the button silently
    # never appears).
    import logging as _logging
    _logging.getLogger("Client").exception(
        "[TS2] Failed to register Toy Story 2 Client launcher component")

# ── COIN LEVEL INFO ───────────────────────────────────────────

COIN_LEVELS = [
    "Andy's House",
    "Andy's Neighborhood",
    "Construction Yard",
    "Alleys and Gullies",
    "Al's Toy Barn",
    "Al's Space Land",
    "Elevator Hop",
    "Al's Penthouse",
    "Airport Infiltration",
    "Tarmac Trouble",
]

ALL_LEVELS = [
    "Andy's House", "Andy's Neighborhood", "Bombs Away!",
    "Construction Yard", "Alleys and Gullies", "Slime Time",
    "Al's Toy Barn", "Al's Space Land", "Toy Barn Encounter",
    "Elevator Hop", "Al's Penthouse", "The Evil Emperor Zurg",
    "Airport Infiltration", "Tarmac Trouble", "Prospector Showdown",
]

BOSS_LEVELS = [
    "Bombs Away!", "Slime Time", "Toy Barn Encounter",
    "The Evil Emperor Zurg", "Prospector Showdown",
]

# Gadgets always in the pool regardless of movesanity
ALL_GADGET_ITEMS = list(GADGET_ITEMS)

# ── TRAP WEIGHTS ──────────────────────────────────────────────

TRAP_WEIGHT_VALUES = {0: 0, 1: 1, 2: 3, 3: 6}  # Off/Low/Medium/High


class ToyStory2Web(WebWorld):
    theme = "ocean"
    option_groups = ts2_option_groups
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Toy Story 2 for Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["You!"]
    )]


class ToyStory2World(World):
    """
    Buzz Lightyear is on a mission to rescue Woody from the evil Al McWhiggin!
    Explore 15 levels, collect Pizza Planet Tokens, and defeat the Prospector
    to save Woody and infinity and beyond!
    """
    game: ClassVar[str] = "Toy Story 2"
    web: ClassVar[WebWorld] = ToyStory2Web()
    options_dataclass = ToyStory2Options
    options: ToyStory2Options

    # Built at class level — includes ALL possible locations and items
    # Dynamic ones (coin bundles) are added in create_regions
    item_name_to_id: ClassVar[Dict[str, int]] = {
        name: data.code for name, data in ITEM_TABLE.items() if data.code is not None
    }

    # Base location table — coin bundle locations are added dynamically
    location_name_to_id: ClassVar[Dict[str, int]] = {
        name: data.code for name, data in LOCATION_TABLE.items() if data.code is not None
    }

    # ── COIN BUNDLE LOCATION IDS ──────────────────────────────
    # Pre-register all possible coin bundle locations
    # Max bundles per level: ceil(103/1) = 103 (Alleys, largest level)
    # We register up to 110 per level to be safe, offset per level
    _COIN_BUNDLE_OFFSET = LOC_BASE + 2000
    _COIN_BUNDLE_PER_LEVEL = 110

    @classmethod
    def _coin_bundle_id(cls, level_idx: int, bundle_num: int) -> int:
        return cls._COIN_BUNDLE_OFFSET + (level_idx * cls._COIN_BUNDLE_PER_LEVEL) + bundle_num

    # Add coin bundle IDs to location_name_to_id at class level
    for _li, _level in enumerate(COIN_LEVELS):
        _coins = COIN_DATA.get(_level, [])
        # Register max possible bundles (bundle size 1 = 1 location per coin)
        for _bn in range(1, len(_coins) + 1):
            _loc_name = f"{_level} - Coin Bundle {_bn}"
            location_name_to_id[_loc_name] = _COIN_BUNDLE_OFFSET + (_li * _COIN_BUNDLE_PER_LEVEL) + _bn

    required_client_version: Tuple[int, int, int] = (0, 5, 0)

    item_name_groups = {
        "Moves":            frozenset(MOVE_ITEMS),
        "Weapon Moves":     frozenset(WEAPON_MOVE_ITEMS),
        "Traversal Moves":  frozenset(TRAVERSAL_MOVE_ITEMS),
        "Gadgets":          frozenset(GADGET_ITEMS),
        "Missing Parts":    frozenset(MISSING_PART_ITEMS),
        "Missing Toys":     frozenset(MISSING_TOY_ITEMS),
        "Level Unlocks":    frozenset(LEVEL_UNLOCK_ITEMS),
        "Coin Bundles":     frozenset(COIN_BUNDLE_ITEMS),
        "Traps":            frozenset(TRAP_ITEMS),
        "Filler":           frozenset(FILLER_ITEMS),
    }

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.coin_bundle_locations: List[str] = []  # populated in create_regions

    # ── STANDARD ITEM CREATION (required by AP core + Universal Tracker) ──
    def create_item(self, name: str) -> ToyStory2Item:
        """Create an item by name. AP core and Universal Tracker call this, so it
        must resolve every item name in item_name_to_id (previously only the
        internal _make_item existed, which UT can't see — hence the 'not able to
        be created' errors)."""
        data = ITEM_TABLE[name]
        return ToyStory2Item(name, data.classification, data.code, self.player)

    def create_event(self, name: str) -> ToyStory2Item:
        """Create a non-networked event item (no code)."""
        return ToyStory2Item(name, ItemClassification.progression, None, self.player)

    # ── HELPERS ───────────────────────────────────────────────

    def _make_item(self, name: str, override_class: Optional[ItemClassification] = None) -> ToyStory2Item:
        if override_class is None:
            return self.create_item(name)
        data = ITEM_TABLE[name]
        return ToyStory2Item(name, override_class, data.code, self.player)

    def _is_coinsanity(self) -> bool:
        return bool(self.options.coinsanity.value)

    def _is_movesanity(self) -> bool:
        return self.options.movesanity.value != 0

    def _checks_bundle_size(self) -> int:
        return self.options.coinsanity_checks_bundle_size.value  # 0 = ALL

    def _received_bundle_size(self) -> int:
        return self.options.coinsanity_received_bundle_size.value

    def _num_check_bundles(self, level: str) -> int:
        """How many coin-bundle CHECK locations a level has = level coin total
        divided by the checks bundle size."""
        coins = COIN_DATA.get(level, [])
        total = len(coins)
        if total == 0:
            return 0
        size = self._checks_bundle_size()
        if size == 0:  # ALL -> one check for the whole level
            return 1
        return math.ceil(total / size)

    def _num_received_bundles(self, level: str) -> int:
        """How many coin-bundle ITEMS a level contributes = level coin total
        divided by the received bundle size (which is never 'all'). Splitting
        these from the check count frees pool slots for Pizza Planet Tokens."""
        coins = COIN_DATA.get(level, [])
        total = len(coins)
        if total == 0:
            return 0
        size = self._received_bundle_size()
        if size <= 0:
            return 1
        return math.ceil(total / size)

    def _is_open_mode(self) -> bool:
        return self.options.game_mode.value == 0

    def _trap_pool(self) -> List[str]:
        """Build weighted trap list based on settings."""
        traps = []
        weights = {
            "Cutscene Trap":            self.options.cutscene_trap_weight.value,
            "Narrow Vision Trap":       self.options.narrow_vision_trap_weight.value,
            "Damage Buzz Trap":         self.options.damage_buzz_trap_weight.value,
            "Freeze Buzz Trap":         self.options.freeze_buzz_trap_weight.value,
            "Invincible Enemies Trap":  self.options.invincible_enemies_trap_weight.value,
        }
        for trap_name, weight in weights.items():
            traps.extend([trap_name] * TRAP_WEIGHT_VALUES[weight])
        return traps

    def _filler_pool(self) -> List[str]:
        """Build a weighted filler list based on settings, mirroring traps."""
        filler = []
        weights = {
            "1 Life":        self.options.one_life_filler_weight.value,
            "Extra Battery": self.options.extra_battery_filler_weight.value,
        }
        for name, weight in weights.items():
            filler.extend([name] * TRAP_WEIGHT_VALUES[weight])
        # If both are Off, fall back to an even split so we always have filler.
        if not filler:
            filler = ["1 Life", "Extra Battery"]
        return filler

    def _get_filler_or_trap(self) -> str:
        trap_pct = self.options.filler_replaced_with_traps.value
        trap_pool = self._trap_pool()
        if trap_pool and self.multiworld.random.randint(1, 100) <= trap_pct:
            return self.multiworld.random.choice(trap_pool)
        return self.multiworld.random.choice(self._filler_pool())

    # ── GENERATE EARLY ────────────────────────────────────────

    def generate_early(self) -> None:
        options = self.options

        # In open mode, validate starting levels vs pool size
        if self._is_open_mode():
            pool = list(COIN_LEVELS)
            if options.omit_airport_infiltration.value:
                pool = [l for l in pool if l != "Airport Infiltration"]
            if options.omit_elevator_hop.value:
                pool = [l for l in pool if l != "Elevator Hop"]
            starting = min(options.starting_levels.value, len(pool))

            # Universal Tracker re-generates the world to derive logic, but it
            # can't reproduce our random starting-level pick. When UT hands the
            # real seed's slot_data back through re_gen_passthrough, use the
            # ACTUAL starting levels from it so the tracker's reachability matches
            # the real game (otherwise it re-rolls different starting levels and
            # thinks unrelated levels are free).
            passthrough = getattr(self.multiworld, "re_gen_passthrough", None)
            chosen = None
            if isinstance(passthrough, dict):
                sd = passthrough.get("Toy Story 2")
                if isinstance(sd, dict) and sd.get("starting_levels"):
                    chosen = [lv for lv in sd["starting_levels"] if lv in pool]
            if chosen:
                self._starting_levels = chosen
            else:
                self._starting_levels = self.multiworld.random.sample(pool, starting)
        else:
            self._starting_levels = ["Andy's House", "Andy's Neighborhood"]

    # ── CREATE REGIONS ────────────────────────────────────────

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        options = self.options
        skips = options.skips.value

        for level_name in ALL_LEVELS:
            region = Region(level_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

            # Connect menu to level (access rules applied in set_rules)
            menu.connect(region, f"To {level_name}")

            # Add non-coin locations
            for loc_name, loc_data in LOCATION_TABLE.items():
                if loc_data.region != level_name:
                    continue
                # Filter by option
                if loc_data.option == "coinsanity" and not self._is_coinsanity():
                    continue
                if loc_data.option == "lifesanity" and not options.lifesanity.value:
                    continue
                if loc_data.option == "batterysanity" and not options.batterysanity.value:
                    continue
                if loc_data.option == "green_laser_sanity" and not options.green_laser_sanity.value:
                    continue
                if loc_data.option == "rexsanity" and not options.rexsanity.value:
                    continue
                if loc_data.option == "hint_block_sanity" and not options.hint_block_sanity.value:
                    continue

                loc = ToyStory2Location(self.player, loc_name, loc_data.code, region)
                region.locations.append(loc)

            # Add coin bundle CHECK locations (count uses the checks bundle size)
            if self._is_coinsanity() and level_name in COIN_LEVELS:
                level_idx = COIN_LEVELS.index(level_name)
                num_bundles = self._num_check_bundles(level_name)
                for bn in range(1, num_bundles + 1):
                    loc_name = f"{level_name} - Coin Bundle {bn}"
                    loc_id = self._coin_bundle_id(level_idx, bn)
                    loc = ToyStory2Location(self.player, loc_name, loc_id, region)
                    region.locations.append(loc)
                    self.coin_bundle_locations.append(loc_name)

        # Place goal event
        prospector = self.multiworld.get_region("Prospector Showdown", self.player)
        goal_loc = ToyStory2Location(
            self.player, "Prospector Showdown - Defeat GOAL", None, prospector
        )
        goal_loc.place_locked_item(
            ToyStory2Item("Victory", ItemClassification.progression, None, self.player)
        )
        prospector.locations.append(goal_loc)
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has("Victory", self.player)

        # ── FINAL SHOWDOWN TICKETS (hard-coded boss rewards) ──
        # Reward 1 of every non-final boss is ALWAYS a Final Showdown Ticket —
        # these are NOT randomized. Defeating a boss hands the player a ticket,
        # and the client counts received Final Showdown Ticket items to know how
        # many bosses have been beaten. Both modes need this: open mode gates the
        # final showdown on ticket count, and linear mode uses tickets to know
        # which areas are unlocked.
        for boss_reward1 in (
            "Bombs Away! - Defeat Reward 1",
            "Slime Time - Defeat Reward 1",
            "Toy Barn Encounter - Defeat Reward 1",
            "The Evil Emperor Zurg - Defeat Reward 1",
        ):
            loc = self.multiworld.get_location(boss_reward1, self.player)
            loc.place_locked_item(self._make_item("Final Showdown Ticket"))

    # ── CREATE ITEMS ──────────────────────────────────────────

    def create_items(self) -> None:
        options = self.options
        items_to_add: List[ToyStory2Item] = []

        # ── MOVES ─────────────────────────────────────────────
        movesanity = options.movesanity.value
        if movesanity == 0:
            # No movesanity — all moves pre-collected (handled via start_inventory)
            pass
        elif movesanity == 1:
            # Full movesanity — all moves in pool
            for move in MOVE_ITEMS:
                if move == "Progressive Laser":
                    for _ in range(3):
                        items_to_add.append(self._make_item("Progressive Laser"))
                else:
                    items_to_add.append(self._make_item(move))
        elif movesanity == 2:
            # LITE Weapons
            for move in WEAPON_MOVE_ITEMS:
                if move == "Progressive Laser":
                    for _ in range(3):
                        items_to_add.append(self._make_item("Progressive Laser"))
                else:
                    items_to_add.append(self._make_item(move))
        elif movesanity == 3:
            # LITE Traversal
            for move in TRAVERSAL_MOVE_ITEMS:
                items_to_add.append(self._make_item(move))

        # ── GADGETS ───────────────────────────────────────────
        for gadget in ALL_GADGET_ITEMS:
            items_to_add.append(self._make_item(gadget))

        # ── MISSING PARTS ─────────────────────────────────────
        for part in MISSING_PART_ITEMS:
            items_to_add.append(self._make_item(part))

        # ── MISSING TOYS (5 progressive of each, both modes) ──
        # The 50 toy locations are always in the pool, so always add the matching
        # 50 toy items (5 per type). The client counts received toy items and
        # writes the count to SHARED_TOY_RECEIVED for that level.
        for toy_item in MISSING_TOY_ITEMS:
            for _ in range(5):
                items_to_add.append(self._make_item(toy_item))

        # ── PIZZA PLANET TOKENS ───────────────────────────────
        # Deferred to the balance step: the requested pool size is capped to the
        # number of locations that actually remain after every other required
        # item is placed, so a high token request with low (few-location) settings
        # can't overflow the pool (which previously silently truncated the count).
        token_count_requested = options.pizza_planet_token_pool.value

        # ── FINAL SHOWDOWN TICKETS ────────────────────────────
        # Not added to the randomized pool: in open mode they are hard-coded as
        # locked items on each non-final boss's Reward 1 (placed in
        # create_regions). In linear mode tickets aren't items — gates are
        # token-based.

        # ── LEVEL UNLOCKS (Open Mode only) ───────────────────
        if self._is_open_mode():
            starting = set(self._starting_levels)
            for level_unlock in LEVEL_UNLOCK_ITEMS:
                if level_unlock == "Final Showdown Unlock":
                    level_name = "Prospector Showdown"
                else:
                    level_name = level_unlock.replace(" Unlock", "")
                if level_name in starting:
                    # Starting levels are pre-collected
                    self.multiworld.push_precollected(self._make_item(level_unlock))
                else:
                    items_to_add.append(self._make_item(level_unlock))

        # ── COIN BUNDLES (items: count uses the received bundle size) ──
        if self._is_coinsanity():
            for level_name in COIN_LEVELS:
                num_bundles = self._num_received_bundles(level_name)
                bundle_item_name = f"Coin Bundle - {level_name}"
                for _ in range(num_bundles):
                    items_to_add.append(self._make_item(bundle_item_name))

        # ── PRE-COLLECT MOVES IF NO MOVESANITY ───────────────
        if movesanity == 0:
            for move in MOVE_ITEMS:
                if move == "Progressive Laser":
                    # Laser is NOT randomized in this mode, so grant only the
                    # first laser. Progressive Laser 2 and 3 are upgrades meant to
                    # be found through Movesanity / LITE Weapons; granting all 3
                    # here would rob those modes of their progression.
                    self.multiworld.push_precollected(self._make_item("Progressive Laser"))
                else:
                    self.multiworld.push_precollected(self._make_item(move))
        elif movesanity == 2:
            # LITE Weapons — pre-collect traversal moves
            for move in TRAVERSAL_MOVE_ITEMS:
                self.multiworld.push_precollected(self._make_item(move))
        elif movesanity == 3:
            # LITE Traversal — pre-collect weapon moves. Laser isn't randomized in
            # this mode either, so grant only the first Progressive Laser.
            for move in WEAPON_MOVE_ITEMS:
                if move == "Progressive Laser":
                    self.multiworld.push_precollected(self._make_item("Progressive Laser"))
                else:
                    self.multiworld.push_precollected(self._make_item(move))

        # ── BALANCE: TOKENS (capped) then FILLER/TRAPS ────────
        # Count available (unfilled, non-event) locations. Locations that already
        # hold a locked item (e.g. the hard-coded Final Showdown Tickets on boss
        # Reward 1 slots, and the Victory goal) must be excluded.
        loc_count = len([l for l in self.multiworld.get_locations(self.player)
                         if not l.is_event and l.item is None])
        item_count = len(items_to_add)
        free_slots = loc_count - item_count

        # GUARD: the required items (coin-bundle items, level unlocks, moves,
        # missing parts, etc.) must fit in the available check locations. The
        # classic way to violate this is a lopsided Coinsanity config — e.g.
        # CHECKS bundle size = ALL (one check per level) but RECEIVED bundle size
        # = 1 (one coin ITEM per coin): that produces hundreds of coin-bundle
        # items but only ~10 coin-bundle check locations to hold them, so the
        # required items can't fit and Fill would die with an opaque error. Fail
        # early here with an actionable message instead.
        if free_slots < 0:
            over = -free_slots
            hint = ""
            if self._is_coinsanity():
                cb = self._checks_bundle_size()
                rb = self._received_bundle_size()
                total_check_bundles = sum(self._num_check_bundles(l) for l in COIN_LEVELS)
                total_recv_bundles = sum(self._num_received_bundles(l) for l in COIN_LEVELS)
                if total_recv_bundles > total_check_bundles:
                    hint = (
                        f" This looks like a lopsided Coinsanity setup: your "
                        f"'received' bundle size ({'1 coin' if rb<=0 else rb}) produces "
                        f"{total_recv_bundles} coin-bundle ITEMS, but your 'checks' "
                        f"bundle size ({'ALL' if cb==0 else cb}) only creates "
                        f"{total_check_bundles} coin-bundle CHECK location(s) to hold "
                        f"them. Make the checks bundle size smaller (more check "
                        f"locations) and/or the received bundle size larger (fewer "
                        f"items), or enable more sanities to add locations."
                    )
            raise Exception(
                f"[Toy Story 2] Player {self.player} "
                f"('{self.multiworld.get_player_name(self.player)}'): the selected "
                f"settings require {item_count} item(s) but only {loc_count} check "
                f"location(s) exist — {over} too many to place.{hint}"
            )

        # Ensure the token pool can actually satisfy whatever token gates are
        # active: if the player set a pool lower than a gate they need, force the
        # pool UP to the highest required gate (otherwise the goal/area would be
        # unreachable). Gates depend on mode and goal.
        required_tokens = 0
        if self._is_open_mode():
            goal = options.goal_conditions.value
            # Goals 0,3,4,6 involve Pizza Planet Tokens for the final showdown.
            if goal in (0, 3, 4, 6):
                required_tokens = max(required_tokens,
                                      options.final_showdown_token_gate.value)
        else:
            # Linear mode gates each area behind a token count.
            required_tokens = max(
                options.bombs_away_token_gate.value,
                options.slime_time_token_gate.value,
                options.toy_barn_encounter_token_gate.value,
                options.evil_emperor_zurg_token_gate.value,
                options.linear_final_showdown_token_gate.value,
            )
        token_count_requested = max(token_count_requested, required_tokens)

        # If the gates REQUIRE more tokens than can possibly fit (leaving room for
        # at least one filler item), the seed would be unwinnable — the player
        # could never reach the token gate. Fail generation with a clear, helpful
        # message instead of silently producing a stuck seed. This is the
        # "linear + few/no sanities + default gates" trap: too few check locations
        # to hold the tokens the gates demand.
        if required_tokens > free_slots - 1:
            raise Exception(
                f"[Toy Story 2] Player {self.player} "
                f"('{self.multiworld.get_player_name(self.player)}'): the "
                f"selected token gates require {required_tokens} Pizza Planet "
                f"Tokens, but only {max(0, free_slots - 1)} check location(s) are "
                f"available to hold them (need 1 spare for filler). Enable more "
                f"sanities (coinsanity/lifesanity/batterysanity/etc.) to add check "
                f"locations, lower your token gates, or both."
            )

        # Place as many Pizza Planet Tokens as requested, but never more than the
        # free slots remaining (so high token requests with few-location settings
        # don't overflow). Tokens take priority over filler.
        token_count = max(0, min(token_count_requested, free_slots - 1))
        if token_count < token_count_requested:
            logging.warning(
                f"[Toy Story 2] Player {self.player}: requested "
                f"{token_count_requested} Pizza Planet Tokens but only "
                f"{token_count} fit the available locations; capped to fit."
            )
        for _ in range(token_count):
            items_to_add.append(self._make_item("Pizza Planet Token"))

        # Fill any remaining slots with filler/traps.
        item_count = len(items_to_add)
        filler_needed = loc_count - item_count
        for _ in range(max(0, filler_needed)):
            items_to_add.append(self._make_item(self._get_filler_or_trap()))

        # Submit all items
        self.multiworld.itempool += items_to_add

    # ── SET RULES ─────────────────────────────────────────────

    def set_rules(self) -> None:
        set_rules(self)

        # Apply level access rules to region entrances
        for level_name in ALL_LEVELS:
            entrance = self.multiworld.get_entrance(f"To {level_name}", self.player)
            entrance.access_rule = lambda state, lv=level_name: \
                can_access_level(state, self.player, lv, self)

    # ── FILLER ────────────────────────────────────────────────

    def get_filler_item_name(self) -> str:
        return self._get_filler_or_trap()

    # ── SLOT DATA ─────────────────────────────────────────────

    def fill_slot_data(self) -> dict:
        options = self.options
        return {
            # Game
            "game_mode":                        options.game_mode.value,
            "skips":                            options.skips.value,
            # Pizza Planet Tokens
            "pizza_planet_token_pool":          options.pizza_planet_token_pool.value,
            # Open Mode
            "starting_levels":                  getattr(self, "_starting_levels", []),
            "omit_airport_infiltration":        options.omit_airport_infiltration.value,
            "omit_elevator_hop":                options.omit_elevator_hop.value,
            "goal_conditions":                  options.goal_conditions.value,
            "final_showdown_token_gate":        options.final_showdown_token_gate.value,
            "defeated_bosses_required":         options.defeated_bosses_required.value,
            # Linear Mode
            "bombs_away_token_gate":            options.bombs_away_token_gate.value,
            "slime_time_token_gate":            options.slime_time_token_gate.value,
            "toy_barn_encounter_token_gate":    options.toy_barn_encounter_token_gate.value,
            "evil_emperor_zurg_token_gate":     options.evil_emperor_zurg_token_gate.value,
            "linear_final_showdown_token_gate": options.linear_final_showdown_token_gate.value,
            # Sanity
            "movesanity":                       options.movesanity.value,
            "coinsanity":                       options.coinsanity.value,
            "coinsanity_checks_bundle_size":    options.coinsanity_checks_bundle_size.value,
            "coinsanity_received_bundle_size":  options.coinsanity_received_bundle_size.value,
            "lifesanity":                       options.lifesanity.value,
            "batterysanity":                    options.batterysanity.value,
            "green_laser_sanity":               options.green_laser_sanity.value,
            "rexsanity":                        options.rexsanity.value,
            "hint_block_sanity":                options.hint_block_sanity.value,
            # QOL
            "collect_enemy_coins_automatically": options.collect_enemy_coins_automatically.value,
            "skip_cutscenes":                   options.skip_cutscenes.value,
            "disc_launcher_fill_pockets":       options.disc_launcher_fill_pockets.value,
            "on_screen_item_feed":              options.on_screen_item_feed.value,
            "disable_falling_animation":        options.disable_falling_animation.value,
            "auto_save":                        options.auto_save.value,
            # Music
            "music_randomizer_mode":            options.music_randomizer_mode.value,
            "oops_all_bangers_song":            options.oops_all_bangers_song.value,
            "skip_song":                        options.skip_song.value,
            # Death Link
            "death_link":                       options.death_link.value,
            # Traps
            "filler_replaced_with_traps":       options.filler_replaced_with_traps.value,
            "cutscene_trap_weight":             options.cutscene_trap_weight.value,
            "narrow_vision_trap_weight":        options.narrow_vision_trap_weight.value,
            "damage_buzz_trap_weight":          options.damage_buzz_trap_weight.value,
            "freeze_buzz_trap_weight":          options.freeze_buzz_trap_weight.value,
            "invincible_enemies_trap_weight":   options.invincible_enemies_trap_weight.value,
        }

    # ── UNIVERSAL TRACKER SUPPORT ─────────────────────────────
    @staticmethod
    def interpret_slot_data(slot_data: dict) -> dict:
        """Universal Tracker hook. Returning the slot_data (truthy) tells UT to
        re-generate this world and hands the data back via re_gen_passthrough, so
        generate_early can restore the ACTUAL starting levels / options from the
        real seed instead of re-rolling them. Without this, UT re-rolls random
        starting levels and mis-reports which levels are accessible."""
        return slot_data


# Register the BizHawk client handler. This import must happen so the
# ToyStory2Client subclass of BizHawkClient is loaded and discoverable.
from . import ts2_client  # noqa: E402, F401