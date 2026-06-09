from dataclasses import dataclass
from Options import (
    Choice, Toggle, DefaultOnToggle, Range, PerGameCommonOptions, OptionGroup
)


# ============================================================
# GAME
# ============================================================

class GameMode(Choice):
    """How would you like to experience Toy Story 2?
    Open Mode has all of the levels at your disposal at the very start.
    Find the level unlocks to gain access to them!
    Linear Mode has you playing the game in order. Each area is fully
    unlocked after defeating a boss to allow you more options and to keep
    you from getting stuck. In this mode you have to fight every boss."""
    display_name = "Game Mode"
    option_open = 0
    option_linear = 1
    default = 0


class Skips(Choice):
    """Determines the logic for certain checks.
    Easy is incredibly easy skips that anyone can do.
    Hard is for the glitch hunters and rule breakers out there."""
    display_name = "Skips"
    option_off = 0
    option_easy = 1
    option_hard = 2
    default = 0


# ============================================================
# PIZZA PLANET TOKENS
# ============================================================

class PizzaPlanetTokenPool(Range):
    """Determines how many Pizza Planet Tokens are in the item pool.
    Highly recommend adding more sanities the more tokens you add."""
    display_name = "Pizza Planet Token Pool"
    range_start = 30
    range_end = 99
    default = 50


# ============================================================
# OPEN MODE
# ============================================================

class StartingLevels(Range):
    """NOTE: This does nothing if you didn't select Open Mode.
    How many levels would you like to start your game with?"""
    display_name = "Starting Levels"
    range_start = 1
    range_end = 5
    default = 1


class OmitAirportInfiltration(Toggle):
    """NOTE: This does nothing if you didn't select Open Mode.
    Airport Infiltration has nothing going for it if you don't have Stomp.
    This makes it so you won't get it as a starting level."""
    display_name = "Omit Airport Infiltration From Pool"


class OmitElevatorHop(Toggle):
    """NOTE: This does nothing if you didn't select Open Mode.
    Elevator Hop has nothing going for it if you don't have Visor.
    This makes it so you won't get it as a starting level."""
    display_name = "Omit Elevator Hop From Pool"


class GoalConditions(Choice):
    """NOTE: This does nothing if you didn't select Open Mode.
    Determines what you need to save Woody. Options:
    Pizza Planet Tokens; Defeated Bosses; Level Unlock;
    Pizza Planet Tokens & Defeated Bosses;
    Pizza Planet Tokens & Level Unlock;
    Defeated Bosses & Level Unlock;
    Pizza Planet Tokens, Defeated Bosses, & Level Unlock."""
    display_name = "Goal Conditions"
    option_pizza_planet_tokens = 0
    option_defeated_bosses = 1
    option_level_unlock = 2
    option_pizza_planet_tokens_and_defeated_bosses = 3
    option_pizza_planet_tokens_and_level_unlock = 4
    option_defeated_bosses_and_level_unlock = 5
    option_pizza_planet_tokens_and_defeated_bosses_and_level_unlock = 6
    default = 0


class FinalShowdownTokenGate(Range):
    """NOTE: This does nothing if you didn't select it as your game mode
    or goal condition.
    Determines how many Pizza Planet Tokens are needed for your goal.
    Selecting a higher number than your total pool will force the pool to a
    higher number."""
    display_name = "Final Showdown Token Gate"
    range_start = 10
    range_end = 99
    default = 50


class DefeatedBossesRequired(Range):
    """NOTE: This does nothing if you didn't select it as your game mode
    or goal condition.
    Determines how many bosses you have to defeat to reach your goal."""
    display_name = "Defeated Bosses Required"
    range_start = 1
    range_end = 4
    default = 4


# ============================================================
# LINEAR MODE
# ============================================================

class BombsAwayTokenGate(Range):
    """NOTE: This does nothing if you didn't select Linear Mode.
    Determines how many Pizza Planet Tokens are needed to fight Bombs Away!
    Selecting a higher number than your total pool will force the pool to a
    higher number."""
    display_name = "Bombs Away! Token Gate"
    range_start = 1
    range_end = 20
    default = 10


class SlimeTimeTokenGate(Range):
    """NOTE: This does nothing if you didn't select Linear Mode.
    Determines how many Pizza Planet Tokens are needed to fight Slime Time.
    Selecting a higher number than your total pool will force the pool to a
    higher number."""
    display_name = "Slime Time Token Gate"
    range_start = 5
    range_end = 40
    default = 20


class ToyBarnEncounterTokenGate(Range):
    """NOTE: This does nothing if you didn't select Linear Mode.
    Determines how many Pizza Planet Tokens are needed to fight Toy Barn
    Encounter.
    Selecting a higher number than your total pool will force the pool to a
    higher number."""
    display_name = "Toy Barn Encounter Token Gate"
    range_start = 10
    range_end = 60
    default = 30


class EvilEmperorZurgTokenGate(Range):
    """NOTE: This does nothing if you didn't select Linear Mode.
    Determines how many Pizza Planet Tokens are needed to fight The Evil
    Emperor Zurg.
    Selecting a higher number than your total pool will force the pool to a
    higher number."""
    display_name = "The Evil Emperor Zurg Token Gate"
    range_start = 15
    range_end = 80
    default = 40


class LinearFinalShowdownTokenGate(Range):
    """NOTE: This does nothing if you didn't select Linear Mode.
    Determines how many Pizza Planet Tokens are needed for your goal.
    Selecting a higher number than your total pool will force the pool to a
    higher number."""
    display_name = "Final Showdown Token Gate"
    range_start = 20
    range_end = 99
    default = 50


# ============================================================
# SANITY
# ============================================================

class Movesanity(Choice):
    """Movesanity will shuffle every single thing Buzz can do. If you choose
    this setting, I highly recommend pairing it with other sanities.
    Movesanity LITE (Weapons) only shuffles Buzz's attack abilities:
    Laser, Spin, Stomp, and Visor.
    Movesanity LITE (Traversal) only shuffles Buzz's movement abilities:
    Double Jump, Pole Climb, Ledge Grab, Pole Vault, Push, and Rope Sliding."""
    display_name = "Movesanity"
    option_off = 0
    option_on = 1
    option_lite_weapons = 2
    option_lite_traversal = 3
    default = 0


class Coinsanity(Toggle):
    """Coins send checks! They aren't individually id'd, it's based on the
    amount you gather in one go through a level. Keep that in mind when
    selecting your bundle amounts. You'll be gathering the same coins a lot.
    Your coins are also items that are sent to you based on your Coinsanity
    Received Bundle Size as well. Make Hamm proud and get him some coins!"""
    display_name = "Coinsanity"


class CoinsanityChecksBundleSize(Choice):
    """If Coinsanity is not turned on, this does nothing.

    Choose the amount coins needed per level to send checks."""
    display_name = "Coinsanity Checks Bundle Size"
    option_1 = 1
    option_5 = 5
    option_10 = 10
    option_15 = 15
    option_20 = 20
    option_25 = 25
    option_all = 0
    default = 5


class CoinsanityReceivedBundleSize(Choice):
    """If Coinsanity is not turned on, this does nothing.

    Choose the amount coins received."""
    display_name = "Coinsanity Received Bundle Size"
    option_1 = 1
    option_5 = 5
    option_10 = 10
    option_15 = 15
    option_20 = 20
    option_25 = 25
    option_50 = 50
    default = 5


class Lifesanity(Toggle):
    """All lives are checks now! That means lives will no longer grant you a
    life, but a check instead! They also don't respawn so play carefully!"""
    display_name = "Lifesanity"


class Batterysanity(Toggle):
    """All batteries are checks now! Batteries will still give health, but
    they won't respawn."""
    display_name = "Batterysanity"


class GreenLaserSanity(Toggle):
    """Green Lasers are checks now! But just like the other sanities, these
    won't respawn. Use them wisely!"""
    display_name = "Green Laser Sanity"


class Rexsanity(Toggle):
    """Hey Buzz! Need a hint? Talking to Rex now gives checks!"""
    display_name = "Rexsanity"


class HintBlockSanity(Toggle):
    """Hints? Who needs them? I'd rather get a useful item! This turns all hint blocks into checks!"""
    display_name = "Hint Block Sanity"


# ============================================================
# TRAPS AND FILLER
# ============================================================

class FillerReplacedWithTraps(Range):
    """Determines the percentage of filler items that will be replaced
    with traps."""
    display_name = "Filler Replaced With Traps"
    range_start = 0
    range_end = 100
    default = 0


class TrapWeight(Choice):
    """Base class for trap weights."""
    option_off = 0
    option_low = 1
    option_medium = 2
    option_high = 3
    default = 1


class CutsceneTrapWeight(TrapWeight):
    """Hope you like Toy Story 2, because you're gonna be watching it a lot!"""
    display_name = "Cutscene Trap Weight"


class NarrowVisionTrapWeight(TrapWeight):
    """I can't see! I can't see!"""
    display_name = "Narrow Vision Trap Weight"


class DamageBuzzTrapWeight(TrapWeight):
    """Ouch!"""
    display_name = "Damage Buzz Trap Weight"


class FreezeBuzzTrapWeight(TrapWeight):
    """Buzz must have run out of batteries!"""
    display_name = "Freeze Buzz Trap Weight"


class InvincibleEnemiesTrapWeight(TrapWeight):
    """I swear I hit him!"""
    display_name = "Invincible Enemies Trap Weight"


class FillerWeight(Choice):
    """Base class for filler weights. (No 'off' — Archipelago must always have
    filler items available to fill empty locations.)"""
    option_low = 1
    option_medium = 2
    option_high = 3
    default = 1


class OneLifeFillerWeight(FillerWeight):
    """How often 1 Life appears among the filler items."""
    display_name = "1 Life Filler Weight"
    default = 1  # Low


class ExtraBatteryFillerWeight(FillerWeight):
    """How often Extra Battery appears among the filler items."""
    display_name = "Extra Battery Filler Weight"
    default = 3  # High


# ============================================================
# QOL
# ============================================================

class CollectEnemyCoinsAutomatically(DefaultOnToggle):
    """Does exactly as it says. Highly recommended if you're playing
    Coinsanity."""
    display_name = "Collect Enemy Coins Automatically"


class SkipCutscenes(DefaultOnToggle):
    """Sets all the cutscene flags to 'watched' when starting the game.
    This does not bypass the Cutscene Trap."""
    display_name = "Skip Cutscenes"


class DisableFallingAnimation(Toggle):
    """Makes it so Buzz always lands on his feet!"""
    display_name = "Disable Falling Animation"


class AutoSave(DefaultOnToggle):
    """Auto saves your game to slot 10 every time you go to the map.
    Highly recommend turning this on if you're worried about game overs.
    They'll send you back to the title screen..."""
    display_name = "Auto Save"


class DiscLauncherFillPockets(DefaultOnToggle):
    """When you pick up Disc Launchers they will
    now go to the maximum you can hold!"""
    display_name = "Disc Launcher Pick Ups Fill Pockets"


class OnScreenItemFeed(Choice):
    """Show Archipelago item activity on-screen (top-left) in BizHawk.
    Off shows nothing. Sent shows checks you send out. Received shows items you
    get. Both shows everything. Pressing Select will cycle this feature's modes."""
    display_name = "On-Screen Item Feed"
    option_off = 0
    option_sent = 1
    option_received = 2
    option_both = 3
    default = 2


# ============================================================
# MUSIC RANDOMIZER
# ============================================================

class MusicRandomizerMode(Choice):
    """Normal: Randomizes the game's music one to one! Note, minigame,
    miniboss, title screen, and map aren't randomized.
    Chaos: You never know what you're going to get! You could be listening
    to the Game Over music on loop for all I know!
    Oops All Bangers: What's your favorite song? What if you heard that for
    every single level in the game?"""
    display_name = "Music Randomizer Mode"
    option_off = 0
    option_normal = 1
    option_chaos = 2
    option_oops_all_bangers = 3
    default = 0


class OopsAllBangersSong(Choice):
    """Better choose wisely, you're gonna be hearing this for a while."""
    display_name = "Oops All Bangers Song"
    option_andys_house = 0
    option_andys_neighborhood = 1
    option_bombs_away = 2
    option_construction_yard = 3
    option_alleys_and_gullies = 4
    option_slime_time = 5
    option_als_toy_barn = 6
    option_als_space_land = 7
    option_toy_barn_encounter = 8
    option_elevator_hop = 9
    option_als_penthouse = 10
    option_the_evil_emperor_zurg = 11
    option_airport_infiltration = 12
    option_tarmac_trouble = 13
    option_prospector_showdown = 14
    option_miniboss_theme = 15
    option_minigame_theme = 16
    option_game_over = 17
    option_credits = 18
    option_youve_got_a_friend_in_me = 19
    option_title_screen = 20
    option_level_complete = 21
    default = 19


class SkipSong(DefaultOnToggle):
    """Man this song sucks. Wouldn't it be nice if you could skip it?
    Well now you can! If you're in a level, you can hold Triangle and press
    L2 and R2 to change the song! Unless you're in Oops All Bangers Mode.
    You dug your grave and now you have to lay in it."""
    display_name = "Skip Song"


# ============================================================
# DEATH LINK
# ============================================================

class DeathLink(Toggle):
    """If Buzz dies you kill everyone else that has Death Link on and vice
    versa. Highly recommended to turn on Auto Save if you play with
    Death Link."""
    display_name = "Death Link"


# ============================================================
# PER GAME OPTIONS
# ============================================================

@dataclass
class ToyStory2Options(PerGameCommonOptions):
    # Game
    game_mode:                          GameMode
    skips:                              Skips
    # Pizza Planet Tokens
    pizza_planet_token_pool:            PizzaPlanetTokenPool
    # Open Mode
    starting_levels:                    StartingLevels
    omit_airport_infiltration:          OmitAirportInfiltration
    omit_elevator_hop:                  OmitElevatorHop
    goal_conditions:                    GoalConditions
    final_showdown_token_gate:          FinalShowdownTokenGate
    defeated_bosses_required:           DefeatedBossesRequired
    # Linear Mode
    bombs_away_token_gate:              BombsAwayTokenGate
    slime_time_token_gate:              SlimeTimeTokenGate
    toy_barn_encounter_token_gate:      ToyBarnEncounterTokenGate
    evil_emperor_zurg_token_gate:       EvilEmperorZurgTokenGate
    linear_final_showdown_token_gate:   LinearFinalShowdownTokenGate
    # Sanity
    movesanity:                         Movesanity
    coinsanity:                         Coinsanity
    coinsanity_checks_bundle_size:      CoinsanityChecksBundleSize
    coinsanity_received_bundle_size:    CoinsanityReceivedBundleSize
    lifesanity:                         Lifesanity
    batterysanity:                      Batterysanity
    green_laser_sanity:                 GreenLaserSanity
    rexsanity:                          Rexsanity
    hint_block_sanity:                  HintBlockSanity
    # Traps and Filler
    filler_replaced_with_traps:         FillerReplacedWithTraps
    cutscene_trap_weight:               CutsceneTrapWeight
    narrow_vision_trap_weight:          NarrowVisionTrapWeight
    damage_buzz_trap_weight:            DamageBuzzTrapWeight
    freeze_buzz_trap_weight:            FreezeBuzzTrapWeight
    invincible_enemies_trap_weight:     InvincibleEnemiesTrapWeight
    one_life_filler_weight:             OneLifeFillerWeight
    extra_battery_filler_weight:        ExtraBatteryFillerWeight
    # QOL
    collect_enemy_coins_automatically:  CollectEnemyCoinsAutomatically
    skip_cutscenes:                     SkipCutscenes
    disc_launcher_fill_pockets:         DiscLauncherFillPockets
    on_screen_item_feed:                OnScreenItemFeed
    disable_falling_animation:          DisableFallingAnimation
    auto_save:                          AutoSave
    # Music Randomizer
    music_randomizer_mode:              MusicRandomizerMode
    oops_all_bangers_song:              OopsAllBangersSong
    skip_song:                          SkipSong
    # Death Link
    death_link:                         DeathLink


# ============================================================
# OPTION GROUPS (launcher GUI categories)
# ============================================================

ts2_option_groups = [
    OptionGroup("Game", [
        GameMode,
        Skips,
    ]),
    OptionGroup("Pizza Planet Tokens", [
        PizzaPlanetTokenPool,
    ]),
    OptionGroup("Open Mode", [
        StartingLevels,
        OmitAirportInfiltration,
        OmitElevatorHop,
        GoalConditions,
        FinalShowdownTokenGate,
        DefeatedBossesRequired,
    ]),
    OptionGroup("Linear Mode", [
        BombsAwayTokenGate,
        SlimeTimeTokenGate,
        ToyBarnEncounterTokenGate,
        EvilEmperorZurgTokenGate,
        LinearFinalShowdownTokenGate,
    ]),
    OptionGroup("Sanity", [
        Movesanity,
        Coinsanity,
        CoinsanityChecksBundleSize,
        CoinsanityReceivedBundleSize,
        Lifesanity,
        Batterysanity,
        GreenLaserSanity,
        Rexsanity,
        HintBlockSanity,
    ]),
    OptionGroup("Traps and Filler", [
        FillerReplacedWithTraps,
        CutsceneTrapWeight,
        NarrowVisionTrapWeight,
        DamageBuzzTrapWeight,
        FreezeBuzzTrapWeight,
        InvincibleEnemiesTrapWeight,
        OneLifeFillerWeight,
        ExtraBatteryFillerWeight,
    ]),
    OptionGroup("QOL", [
        CollectEnemyCoinsAutomatically,
        SkipCutscenes,
        DisableFallingAnimation,
        AutoSave,
        DiscLauncherFillPockets,
        OnScreenItemFeed,
    ]),
    OptionGroup("Music Randomizer", [
        MusicRandomizerMode,
        OopsAllBangersSong,
        SkipSong,
    ]),
    OptionGroup("Death Link", [
        DeathLink,
    ]),
]