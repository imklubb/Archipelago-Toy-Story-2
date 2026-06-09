# coin_data.py
# Per-coin logic data for all 10 coin levels.
# Each entry is a tuple:
#   (moves_and, moves_or, gadgets_and, gadgets_or,
#    glitch_tier, g_moves_and, g_moves_or, g_gadgets_and, g_gadgets_or)
# glitch_tier: None | "Easy" | "Hard" | "Easy, Hard"

from typing import List, Optional, Tuple

CoinEntry = Tuple[
    List[str], List[str], List[str], List[str],
    Optional[str],
    List[str], List[str], List[str], List[str]
]

ANDYS_HOUSE_COINS: List[CoinEntry] = [
    # Coin 1
    ([], [], [], [], None, [], [], [], []),
    # Coin 2
    ([], [], [], [], None, [], [], [], []),
    # Coin 3
    ([], [], [], [], None, [], [], [], []),
    # Coin 4
    ([], [], [], [], None, [], [], [], []),
    # Coin 5
    ([], [], [], [], None, [], [], [], []),
    # Coin 6
    ([], [], [], [], None, [], [], [], []),
    # Coin 7
    ([], [], [], [], None, [], [], [], []),
    # Coin 8
    ([], [], [], [], None, [], [], [], []),
    # Coin 9
    ([], [], [], [], None, [], [], [], []),
    # Coin 10
    ([], [], [], [], None, [], [], [], []),
    # Coin 11
    ([], [], [], [], None, [], [], [], []),
    # Coin 12
    ([], [], [], [], None, [], [], [], []),
    # Coin 13
    ([], [], [], [], None, [], [], [], []),
    # Coin 14
    ([], [], [], [], None, [], [], [], []),
    # Coin 15
    ([], [], [], [], None, [], [], [], []),
    # Coin 16
    ([], ['Double Jump', 'Ledge Grab'], [], [], 'Easy', [], [], [], []),
    # Coin 17
    ([], ['Double Jump', 'Ledge Grab'], [], [], 'Easy', [], [], [], []),
    # Coin 18
    ([], ['Double Jump', 'Ledge Grab'], [], [], 'Easy', [], [], [], []),
    # Coin 19
    ([], ['Double Jump', 'Ledge Grab'], [], [], 'Easy', [], [], [], []),
    # Coin 20
    (['Ledge Grab', 'Double Jump'], [], [], [], 'Easy', [], [], [], []),
    # Coin 21
    ([], ['Spin', 'Laser'], [], [], None, [], [], [], []),
    # Coin 22
    ([], ['Spin', 'Laser'], [], [], None, [], [], [], []),
    # Coin 23
    ([], ['Spin', 'Laser'], [], [], None, [], [], [], []),
    # Coin 24
    ([], ['Spin', 'Laser'], [], [], None, [], [], [], []),
    # Coin 25
    ([], ['Spin', 'Laser'], [], [], None, [], [], [], []),
    # Coin 26
    ([], ['Stomp', 'Spin', 'Laser'], [], [], None, [], [], [], []),
    # Coin 27
    ([], ['Stomp', 'Spin', 'Laser'], [], [], None, [], [], [], []),
    # Coin 28
    ([], ['Stomp', 'Spin', 'Laser'], [], [], None, [], [], [], []),
    # Coin 29
    ([], ['Stomp', 'Spin', 'Laser'], [], [], None, [], [], [], []),
    # Coin 30
    ([], ['Stomp', 'Spin', 'Laser'], [], [], None, [], [], [], []),
    # Coin 31
    ([], ['Stomp', 'Spin', 'Laser'], [], [], None, [], [], [], []),
    # Coin 32
    ([], ['Stomp', 'Spin', 'Laser'], [], [], None, [], [], [], []),
    # Coin 33
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 34
    (['Double Jump', 'Ledge Grab', 'Push'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 35
    (['Double Jump', 'Ledge Grab', 'Push'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 36
    (['Double Jump', 'Ledge Grab', 'Push', 'Pole Climb', 'Rope Sliding', 'Visor'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 37
    (['Double Jump', 'Ledge Grab', 'Push', 'Pole Climb', 'Rope Sliding', 'Visor'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 38
    ([], ['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], None, [], [], [], []),
    # Coin 39
    ([], ['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], None, [], [], [], []),
    # Coin 40
    (['Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 41
    (['Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 42
    (['Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 43
    (['Double Jump', 'Pole Climb', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 44
    (['Double Jump', 'Pole Climb', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 45
    (['Double Jump', 'Pole Climb', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 46
    (['Double Jump', 'Pole Climb', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 47
    (['Push', 'Pole Climb', 'Pole Vault', 'Ledge Grab', 'Double Jump'], [], [], [], 'Easy', ['Pole Climb', 'Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 48
    (['Push', 'Pole Climb', 'Pole Vault', 'Ledge Grab', 'Double Jump'], [], [], [], 'Easy', ['Pole Climb', 'Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 49
    (['Push', 'Pole Climb', 'Pole Vault', 'Ledge Grab', 'Double Jump'], [], [], [], 'Easy', ['Pole Climb', 'Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 50
    (['Push', 'Pole Climb', 'Pole Vault', 'Ledge Grab', 'Double Jump'], ['Laser', 'Spin', 'Stomp'], [], [], 'Easy', ['Pole Climb', 'Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 51
    ([], ['Double Jump', 'Pole Climb'], [], [], 'Easy', ['Ledge Grab'], [], [], []),
    # Coin 52
    ([], ['Double Jump', 'Ledge Grab', 'Pole Climb', 'Stomp'], [], [], 'Hard', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 53
    ([], ['Double Jump', 'Ledge Grab', 'Pole Climb', 'Laser', 'Spin', 'Stomp'], [], [], 'Hard', ['Double Jump', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], []),
    # Coin 54
    (['Stomp'], ['Ledge Grab', 'Pole Climb', 'Double Jump'], [], [], 'Hard', ['Double Jump', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], []),
    # Coin 55
    (['Stomp', 'Double Jump', 'Ledge Grab'], [], [], [], 'Hard', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 56
    (['Stomp', 'Double Jump', 'Ledge Grab'], [], [], [], 'Hard', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 57
    (['Stomp', 'Double Jump', 'Ledge Grab'], [], [], [], 'Hard', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 58
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 59
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 60
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 61
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 62
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 63
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 64
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 65
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 66
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 67
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 68
    (['Double Jump', 'Ledge Grab', 'Pole Climb', 'Pole Vault'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 69
    (['Double Jump', 'Ledge Grab', 'Pole Climb', 'Pole Vault'], ['Laser', 'Spin', 'Stomp'], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], []),
    # Coin 70
    (['Double Jump', 'Ledge Grab', 'Pole Climb', 'Pole Vault'], ['Laser', 'Spin', 'Stomp'], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], []),
    # Coin 71
    (['Double Jump', 'Ledge Grab', 'Pole Climb', 'Pole Vault'], ['Laser', 'Spin'], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], ['Laser', 'Spin'], [], []),
    # Coin 72
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], ['Laser', 'Spin'], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], ['Laser', 'Spin'], [], []),
    # Coin 73
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], ['Pole Climb', 'Ledge Grab'], [], []),
    # Coin 74
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], ['Pole Climb', 'Ledge Grab'], [], []),
    # Coin 75
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], ['Pole Climb', 'Ledge Grab'], [], []),
    # Coin 76
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], ['Pole Climb', 'Ledge Grab'], [], []),
    # Coin 77
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], ['Pole Climb', 'Ledge Grab'], [], []),
    # Coin 78
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], ['Pole Climb', 'Ledge Grab'], [], []),
    # Coin 79
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], ['Pole Climb', 'Ledge Grab'], [], []),
    # Coin 80
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], ['Pole Climb', 'Ledge Grab'], [], []),
    # Coin 81
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], ['Pole Climb', 'Ledge Grab'], [], []),
    # Coin 82
    (['Push', 'Double Jump', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], [], 'Easy', ['Double Jump'], ['Pole Climb', 'Ledge Grab', 'Laser', 'Spin'], [], []),
    # Coin 83
    (['Push', 'Double Jump', 'Ledge Grab'], ['Laser', 'Spin'], [], [], 'Easy', ['Double Jump'], ['Pole Climb', 'Ledge Grab', 'Laser', 'Spin', 'Stomp'], [], []),
    # Coin 84
    (['Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], [], [], []),
    # Coin 85
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 86
    (['Double Jump', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 87
    (['Double Jump', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 88
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 89
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 90
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 91
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 92
    (['Double Jump', 'Ledge Grab', 'Pole Climb', 'Push'], [], [], [], 'Easy, Hard', ['Double Jump', 'Ledge Grab', 'Push'], [], [], []),
    # Coin 93
    (['Double Jump', 'Ledge Grab', 'Pole Climb', 'Push'], [], [], [], 'Easy, Hard', ['Double Jump', 'Ledge Grab', 'Push'], [], [], []),
]

ANDYS_NEIGHBORHOOD_COINS: List[CoinEntry] = [
    # Coin 1
    ([], [], [], [], None, [], [], [], []),
    # Coin 2
    ([], [], [], [], None, [], [], [], []),
    # Coin 3
    ([], [], [], [], None, [], [], [], []),
    # Coin 4
    ([], [], [], [], None, [], [], [], []),
    # Coin 5
    ([], [], [], [], None, [], [], [], []),
    # Coin 6
    ([], [], [], [], None, [], [], [], []),
    # Coin 7
    ([], [], [], [], None, [], [], [], []),
    # Coin 8
    ([], [], [], [], None, [], [], [], []),
    # Coin 9
    ([], [], [], [], None, [], [], [], []),
    # Coin 10
    ([], [], [], [], None, [], [], [], []),
    # Coin 11
    ([], [], [], [], None, [], [], [], []),
    # Coin 12
    ([], [], [], [], None, [], [], [], []),
    # Coin 13
    ([], [], [], [], None, [], [], [], []),
    # Coin 14
    ([], [], [], [], None, [], [], [], []),
    # Coin 15
    ([], [], [], [], None, [], [], [], []),
    # Coin 16
    ([], [], [], [], None, [], [], [], []),
    # Coin 17
    ([], [], [], [], None, [], [], [], []),
    # Coin 18
    ([], [], [], [], None, [], [], [], []),
    # Coin 19
    ([], [], [], [], None, [], [], [], []),
    # Coin 20
    ([], [], [], [], None, [], [], [], []),
    # Coin 21
    ([], [], [], [], None, [], [], [], []),
    # Coin 22
    ([], [], [], [], None, [], [], [], []),
    # Coin 23
    ([], [], [], [], None, [], [], [], []),
    # Coin 24
    ([], [], [], [], None, [], [], [], []),
    # Coin 25
    ([], [], [], [], None, [], [], [], []),
    # Coin 26
    ([], [], [], [], None, [], [], [], []),
    # Coin 27
    ([], [], [], [], None, [], [], [], []),
    # Coin 28
    ([], [], [], [], None, [], [], [], []),
    # Coin 29
    ([], [], [], [], None, [], [], [], []),
    # Coin 30
    ([], [], [], [], None, [], [], [], []),
    # Coin 31
    ([], [], [], [], None, [], [], [], []),
    # Coin 32
    ([], [], [], [], None, [], [], [], []),
    # Coin 33
    ([], [], [], [], None, [], [], [], []),
    # Coin 34
    ([], ['Laser', 'Spin'], [], [], None, [], [], [], []),
    # Coin 35
    ([], ['Laser', 'Spin'], [], [], None, [], [], [], []),
    # Coin 36
    ([], ['Laser', 'Spin'], [], [], None, [], [], [], []),
    # Coin 37
    ([], ['Laser', 'Spin'], [], [], None, [], [], [], []),
    # Coin 38
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 39
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 40
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 41
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 42
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 43
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 44
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 45
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 46
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 47
    (['Stomp', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 48
    (['Stomp', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 49
    (['Stomp', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 50
    (['Stomp', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 51
    (['Stomp', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 52
    (['Stomp', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 53
    (['Stomp', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 54
    (['Stomp', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 55
    (['Stomp', 'Ledge Grab', 'Push'], [], [], [], 'Easy, Hard', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 56
    (['Stomp', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Ledge Grab'], [], [], []),
    # Coin 57
    (['Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 58
    (['Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 59
    (['Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 60
    (['Double Jump', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 61
    (['Double Jump', 'Pole Climb'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 62
    (['Double Jump', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 63
    (['Double Jump', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 64
    (['Double Jump', 'Pole Climb'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 65
    (['Double Jump', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 66
    (['Double Jump', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 67
    (['Double Jump', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 68
    (['Double Jump', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 69
    (['Double Jump', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 70
    (['Double Jump', 'Pole Climb', 'Pole Vault'], [], [], [], None, [], [], [], []),
    # Coin 71
    (['Double Jump', 'Pole Climb', 'Pole Vault'], [], [], [], 'Easy', ['Double Jump', 'Pole Climb', 'Ledge Grab'], [], [], []),
    # Coin 72
    (['Double Jump', 'Pole Climb', 'Pole Vault'], [], [], [], 'Easy', ['Double Jump', 'Pole Climb', 'Ledge Grab'], [], [], []),
    # Coin 73
    (['Double Jump', 'Pole Climb', 'Pole Vault'], [], [], [], 'Easy', ['Double Jump', 'Pole Climb', 'Ledge Grab'], [], [], []),
    # Coin 74
    (['Double Jump', 'Pole Climb', 'Pole Vault'], [], [], [], 'Easy', ['Double Jump', 'Pole Climb', 'Ledge Grab'], [], [], []),
    # Coin 75
    ([], ['Double Jump'], [], ['Rocket Boots'], None, [], [], [], []),
    # Coin 76
    ([], ['Double Jump'], [], ['Rocket Boots'], None, [], [], [], []),
    # Coin 77
    (['Ledge Grab', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 78
    (['Ledge Grab', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 79
    (['Ledge Grab', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 80
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 81
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 82
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 83
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 84
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 85
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 86
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 87
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 88
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 89
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 90
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 91
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 92
    (['Double Jump', 'Pole Climb', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 93
    (['Double Jump', 'Pole Climb', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 94
    (['Double Jump', 'Pole Climb', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 95
    (['Double Jump', 'Ledge Grab', 'Pole Climb', 'Pole Vault'], [], [], [], None, [], [], [], []),
    # Coin 96
    (['Double Jump', 'Ledge Grab', 'Pole Climb', 'Pole Vault'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 97
    (['Double Jump', 'Ledge Grab', 'Pole Climb', 'Pole Vault'], [], [], [], None, [], [], [], []),
    # Coin 98
    (['Double Jump', 'Ledge Grab', 'Pole Climb', 'Pole Vault'], [], [], [], None, [], [], [], []),
    # Coin 99
    (['Double Jump', 'Ledge Grab', 'Pole Climb', 'Pole Vault'], [], [], [], None, [], [], [], []),
]

CONSTRUCTION_YARD_COINS: List[CoinEntry] = [
    # Coin 1
    ([], [], [], [], None, [], [], [], []),
    # Coin 2
    ([], [], [], [], None, [], [], [], []),
    # Coin 3
    ([], [], [], [], None, [], [], [], []),
    # Coin 4
    ([], [], [], [], None, [], [], [], []),
    # Coin 5
    ([], [], [], [], None, [], [], [], []),
    # Coin 6
    ([], [], [], [], None, [], [], [], []),
    # Coin 7
    ([], [], [], [], None, [], [], [], []),
    # Coin 8
    ([], [], [], [], None, [], [], [], []),
    # Coin 9
    ([], [], [], [], None, [], [], [], []),
    # Coin 10
    ([], [], [], [], None, [], [], [], []),
    # Coin 11
    ([], [], [], [], None, [], [], [], []),
    # Coin 12
    ([], [], [], [], None, [], [], [], []),
    # Coin 13
    ([], [], [], [], None, [], [], [], []),
    # Coin 14
    ([], [], [], [], None, [], [], [], []),
    # Coin 15
    ([], [], [], [], None, [], [], [], []),
    # Coin 16
    ([], [], [], [], None, [], [], [], []),
    # Coin 17
    ([], [], [], [], None, [], [], [], []),
    # Coin 18
    ([], [], [], [], None, [], [], [], []),
    # Coin 19
    ([], [], [], [], None, [], [], [], []),
    # Coin 20
    ([], [], [], [], None, [], [], [], []),
    # Coin 21
    ([], [], [], [], None, [], [], [], []),
    # Coin 22
    ([], [], [], [], None, [], [], [], []),
    # Coin 23
    ([], [], [], [], None, [], [], [], []),
    # Coin 24
    ([], [], [], [], None, [], [], [], []),
    # Coin 25
    ([], [], [], [], None, [], [], [], []),
    # Coin 26
    ([], [], [], [], None, [], [], [], []),
    # Coin 27
    ([], [], [], [], None, [], [], [], []),
    # Coin 28
    ([], [], [], [], None, [], [], [], []),
    # Coin 29
    ([], ['Laser', 'Spin'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 30
    ([], [], [], [], None, [], [], [], []),
    # Coin 31
    ([], ['Laser', 'Spin'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 32
    ([], [], [], [], None, [], [], [], []),
    # Coin 33
    ([], ['Laser', 'Spin'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 34
    ([], ['Laser', 'Spin', 'Stomp'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 35
    ([], ['Laser', 'Spin', 'Stomp'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 36
    ([], ['Laser', 'Spin', 'Stomp'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 37
    ([], ['Laser', 'Spin', 'Stomp'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 38
    ([], ['Laser', 'Spin', 'Stomp'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 39
    ([], ['Laser', 'Spin', 'Stomp'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 40
    ([], ['Laser', 'Spin', 'Stomp'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 41
    ([], ['Laser', 'Spin', 'Stomp'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 42
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 43
    (['Double Jump', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 44
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 45
    (['Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 46
    (['Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 47
    (['Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 48
    (['Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 49
    (['Double Jump', 'Ledge Grab', 'Laser'], [], [], [], 'Easy', ['Double Jump', 'Laser'], [], [], []),
    # Coin 50
    (['Double Jump', 'Ledge Grab', 'Laser'], [], [], [], 'Easy', ['Double Jump', 'Laser'], [], [], []),
    # Coin 51
    (['Stomp', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], [], [], []),
    # Coin 52
    (['Stomp', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], [], [], []),
    # Coin 53
    (['Stomp', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], [], [], []),
    # Coin 54
    (['Stomp', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], [], [], []),
    # Coin 55
    (['Stomp', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], [], [], []),
    # Coin 56
    (['Stomp', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], [], [], []),
    # Coin 57
    (['Stomp', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], [], [], []),
    # Coin 58
    (['Stomp', 'Double Jump', 'Ledge Grab'], ['Laser', 'Spin'], [], ['Disc Launcher'], 'Easy', ['Double Jump'], ['Laser', 'Spin'], [], ['Disc Launcher']),
    # Coin 59
    (['Stomp', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], [], [], []),
    # Coin 60
    (['Stomp', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], [], [], []),
    # Coin 61
    (['Stomp', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], [], [], []),
    # Coin 62
    (['Stomp', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump'], [], [], []),
    # Coin 63
    (['Stomp', 'Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 64
    (['Stomp', 'Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump'], [], [], []),
    # Coin 65
    (['Stomp', 'Double Jump', 'Ledge Grab', 'Pole Climb'], ['Laser', 'Spin'], [], ['Disc Launcher'], 'Easy', ['Double Jump'], ['Laser', 'Spin'], [], ['Disc Launcher']),
    # Coin 66
    (['Stomp', 'Double Jump', 'Ledge Grab', 'Pole Climb'], ['Laser', 'Visor'], [], ['Disc Launcher'], 'Easy', ['Double Jump'], ['Laser', 'Visor'], [], ['Disc Launcher']),
    # Coin 67
    (['Stomp', 'Double Jump', 'Ledge Grab', 'Pole Climb'], ['Laser', 'Visor'], [], ['Disc Launcher'], 'Easy', ['Double Jump'], ['Laser', 'Visor'], [], ['Disc Launcher']),
    # Coin 68
    (['Stomp', 'Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump'], [], [], []),
    # Coin 69
    (['Stomp', 'Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump'], [], [], []),
    # Coin 70
    (['Stomp', 'Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump'], [], [], []),
    # Coin 71
    (['Stomp', 'Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump'], [], [], []),
    # Coin 72
    (['Stomp', 'Double Jump', 'Ledge Grab', 'Pole Climb'], [], ['Disc Launcher'], [], 'Easy', ['Double Jump', 'Laser'], [], ['Disc Launcher'], []),
]

ALLEYS_AND_GULLIES_COINS: List[CoinEntry] = [
    # Coin 1
    ([], [], [], [], None, [], [], [], []),
    # Coin 2
    ([], [], [], [], None, [], [], [], []),
    # Coin 3
    ([], [], [], [], None, [], [], [], []),
    # Coin 4
    ([], [], [], [], None, [], [], [], []),
    # Coin 5
    ([], [], [], [], None, [], [], [], []),
    # Coin 6
    ([], [], [], [], None, [], [], [], []),
    # Coin 7
    ([], [], [], [], None, [], [], [], []),
    # Coin 8
    ([], [], [], [], None, [], [], [], []),
    # Coin 9
    ([], [], [], [], None, [], [], [], []),
    # Coin 10
    ([], [], [], [], None, [], [], [], []),
    # Coin 11
    ([], [], [], [], None, [], [], [], []),
    # Coin 12
    ([], [], [], [], None, [], [], [], []),
    # Coin 13
    ([], [], [], [], None, [], [], [], []),
    # Coin 14
    ([], [], [], [], None, [], [], [], []),
    # Coin 15
    ([], [], [], [], None, [], [], [], []),
    # Coin 16
    ([], [], [], [], None, [], [], [], []),
    # Coin 17
    ([], [], [], [], None, [], [], [], []),
    # Coin 18
    ([], [], [], [], None, [], [], [], []),
    # Coin 19
    ([], [], [], [], None, [], [], [], []),
    # Coin 20
    ([], [], [], [], None, [], [], [], []),
    # Coin 21
    ([], [], [], [], None, [], [], [], []),
    # Coin 22
    ([], ['Laser', 'Spin', 'Stomp'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 23
    ([], ['Laser', 'Spin', 'Stomp'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 24
    ([], ['Laser', 'Spin', 'Stomp'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 25
    ([], ['Laser', 'Spin', 'Stomp'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 26
    ([], ['Laser', 'Spin', 'Stomp'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 27
    ([], ['Laser', 'Spin', 'Stomp'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 28
    ([], ['Laser', 'Spin', 'Stomp'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 29
    ([], ['Laser', 'Spin', 'Stomp'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 30
    (['Push', 'Ledge Grab', 'Double Jump'], ['Laser', 'Spin'], [], ['Disc Launcher'], 'Hard', ['Push', 'Ledge Grab', 'Double Jump', 'Stomp'], [], [], []),
    # Coin 31
    (['Push', 'Ledge Grab', 'Double Jump'], ['Laser', 'Spin'], [], ['Disc Launcher'], 'Hard', ['Push', 'Ledge Grab', 'Double Jump', 'Stomp'], [], [], []),
    # Coin 32
    (['Push', 'Ledge Grab', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 33
    (['Push', 'Ledge Grab', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 34
    ([], ['Ledge Grab', 'Double Jump'], [], [], None, [], [], [], []),
    # Coin 35
    ([], ['Ledge Grab', 'Double Jump'], [], [], None, [], [], [], []),
    # Coin 36
    (['Rope Sliding'], ['Ledge Grab', 'Double Jump'], [], [], None, [], [], [], []),
    # Coin 37
    (['Rope Sliding'], ['Ledge Grab', 'Double Jump'], [], [], None, [], [], [], []),
    # Coin 38
    (['Rope Sliding'], ['Ledge Grab', 'Double Jump'], [], [], None, [], [], [], []),
    # Coin 39
    (['Rope Sliding'], ['Ledge Grab', 'Double Jump'], [], [], None, [], [], [], []),
    # Coin 40
    (['Rope Sliding'], ['Ledge Grab', 'Double Jump', 'Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 41
    (['Rope Sliding'], ['Ledge Grab', 'Double Jump', 'Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 42
    (['Rope Sliding'], ['Ledge Grab', 'Double Jump', 'Laser', 'Spin'], [], [], None, [], [], [], []),
    # Coin 43
    (['Ledge Grab', 'Double Jump', 'Rope Sliding', 'Pole Vault'], ['Spin', 'Stomp'], [], ['Disc Launcher'], 'Easy', ['Ledge Grab', 'Double Jump', 'Rope Sliding'], ['Spin', 'Stomp'], [], ['Disc Launcher']),
    # Coin 44
    (['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Laser'], [], [], [], None, [], [], [], []),
    # Coin 45
    (['Double Jump', 'Rope Sliding', 'Ledge Grab'], ['Laser', 'Visor'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 46
    (['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy', ['Double Jump', 'Rope Sliding', 'Ledge Grab'], [], [], []),
    # Coin 47
    (['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy', ['Double Jump', 'Rope Sliding', 'Ledge Grab'], [], [], []),
    # Coin 48
    (['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy', ['Double Jump', 'Rope Sliding', 'Ledge Grab'], [], [], []),
    # Coin 49
    (['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy', ['Double Jump', 'Rope Sliding', 'Ledge Grab'], [], [], []),
    # Coin 50
    (['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy', ['Double Jump', 'Rope Sliding', 'Ledge Grab'], [], [], []),
    # Coin 51
    (['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy', ['Double Jump', 'Rope Sliding', 'Ledge Grab'], [], [], []),
    # Coin 52
    (['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy', ['Double Jump', 'Rope Sliding', 'Ledge Grab'], [], [], []),
    # Coin 53
    (['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy', ['Double Jump', 'Rope Sliding', 'Ledge Grab'], [], [], []),
    # Coin 54
    (['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp', 'Pole Vault'], [], [], [], 'Easy, Hard', ['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp'], [], [], []),
    # Coin 55
    (['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp', 'Pole Vault'], [], [], [], 'Easy, Hard', ['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp'], [], [], []),
    # Coin 56
    (['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp', 'Pole Vault'], [], [], [], 'Easy, Hard', ['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp'], [], [], []),
    # Coin 57
    (['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp', 'Pole Vault'], [], [], [], 'Easy, Hard', ['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp'], [], [], []),
    # Coin 58
    (['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp', 'Pole Vault'], [], [], [], 'Easy, Hard', ['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp'], [], [], []),
    # Coin 59
    (['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp', 'Pole Vault'], [], [], [], 'Easy, Hard', ['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp'], [], [], []),
    # Coin 60
    (['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp', 'Pole Vault'], [], [], [], 'Easy, Hard', ['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp'], [], [], []),
    # Coin 61
    (['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp', 'Pole Vault'], [], [], [], 'Easy, Hard', ['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp'], [], [], []),
    # Coin 62
    (['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp', 'Pole Vault'], [], [], [], 'Easy, Hard', ['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp'], [], [], []),
    # Coin 63
    (['Double Jump', 'Rope Sliding', 'Ledge Grab', 'Stomp', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy', ['Double Jump', 'Rope Sliding', 'Ledge Grab'], [], [], []),
    # Coin 64
    (['Visor'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 65
    (['Visor', 'Pole Climb'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 66
    (['Visor', 'Pole Climb'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 67
    (['Visor', 'Pole Climb'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 68
    (['Visor', 'Pole Climb'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 69
    (['Visor', 'Pole Climb', 'Rope Sliding'], [], ['Grappling Hook'], [], 'Easy', ['Visor', 'Pole Climb', 'Double Jump'], [], ['Grappling Hook'], []),
    # Coin 70
    (['Visor', 'Pole Climb', 'Rope Sliding'], [], ['Grappling Hook'], [], 'Easy', ['Visor', 'Pole Climb', 'Double Jump'], [], ['Grappling Hook'], []),
    # Coin 71
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Laser', 'Spin', 'Stomp'], ['Grappling Hook'], ['Disc Launcher'], 'Easy', ['Visor', 'Pole Climb', 'Double Jump'], ['Laser', 'Spin', 'Stomp'], ['Grappling Hook'], ['Disc Launcher']),
    # Coin 72
    (['Visor', 'Pole Climb', 'Rope Sliding'], [], ['Grappling Hook'], [], 'Easy', ['Visor', 'Pole Climb', 'Double Jump'], [], ['Grappling Hook'], []),
    # Coin 73
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 74
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], 'Hard', ['Visor', 'Pole Climb', 'Double Jump'], [], ['Grappling Hook'], []),
    # Coin 75
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 76
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 77
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 78
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 79
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump', 'Laser', 'Spin'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 80
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 81
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 82
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 83
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump', 'Laser', 'Spin'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 84
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 85
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 86
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 87
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 88
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 89
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 90
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 91
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 92
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 93
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 94
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 95
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 96
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 97
    (['Visor', 'Pole Climb', 'Rope Sliding'], ['Ledge Grab', 'Double Jump'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 98
    (['Visor', 'Pole Climb', 'Rope Sliding', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 99
    (['Visor', 'Pole Climb', 'Rope Sliding', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 100
    (['Visor', 'Pole Climb', 'Rope Sliding', 'Double Jump'], ['Laser', 'Spin', 'Stomp'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 101
    (['Visor', 'Pole Climb', 'Rope Sliding', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 102
    (['Push', 'Ledge Grab', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 103
    (['Push', 'Ledge Grab', 'Double Jump'], [], [], [], None, [], [], [], []),
]

ALS_TOY_BARN_COINS: List[CoinEntry] = [
    # Coin 1
    ([], [], [], [], None, [], [], [], []),
    # Coin 2
    ([], [], [], [], None, [], [], [], []),
    # Coin 3
    ([], [], [], [], None, [], [], [], []),
    # Coin 4
    ([], [], [], [], None, [], [], [], []),
    # Coin 5
    ([], [], [], [], None, [], [], [], []),
    # Coin 6
    ([], [], [], [], None, [], [], [], []),
    # Coin 7
    ([], [], [], [], None, [], [], [], []),
    # Coin 8
    ([], ['Laser', 'Spin', 'Stomp'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 9
    ([], ['Laser', 'Spin', 'Stomp'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 10
    ([], ['Laser', 'Spin'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 11
    ([], ['Laser', 'Spin'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 12
    ([], ['Laser', 'Spin'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 13
    ([], ['Laser', 'Spin'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 14
    ([], ['Laser', 'Spin'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 15
    ([], ['Laser', 'Spin'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 16
    ([], ['Laser', 'Spin'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 17
    ([], ['Laser', 'Spin'], [], ['Disc Launcher'], None, [], [], [], []),
    # Coin 18
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 19
    (['Double Jump', 'Ledge Grab', 'Push'], [], [], [], 'Hard', ['Double Jump'], [], ['Rocket Boots'], []),
    # Coin 20
    (['Double Jump', 'Ledge Grab', 'Push'], ['Laser', 'Spin'], [], ['Disc Launcher'], 'Hard', ['Double Jump'], ['Laser', 'Spin'], ['Rocket Boots'], ['Disc Launcher']),
    # Coin 21
    (['Pole Climb'], ['Ledge Grab', 'Double Jump'], [], [], None, [], [], [], []),
    # Coin 22
    (['Pole Climb'], ['Ledge Grab', 'Double Jump'], [], [], None, [], [], [], []),
    # Coin 23
    (['Pole Climb'], ['Ledge Grab', 'Double Jump'], [], [], None, [], [], [], []),
    # Coin 24
    ([], ['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], None, [], [], [], []),
    # Coin 25
    ([], ['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], None, [], [], [], []),
    # Coin 26
    ([], ['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], None, [], [], [], []),
    # Coin 27
    ([], ['Double Jump', 'Ledge Grab', 'Pole Climb'], ['Disc Launcher'], [], None, [], [], [], []),
    # Coin 28
    ([], ['Double Jump', 'Ledge Grab', 'Pole Climb'], ['Disc Launcher'], [], None, [], [], [], []),
    # Coin 29
    ([], ['Double Jump', 'Ledge Grab', 'Pole Climb'], ['Disc Launcher'], [], None, [], [], [], []),
    # Coin 30
    ([], [], ['Hover Boots'], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 31
    ([], [], ['Hover Boots'], [], None, [], [], [], []),
    # Coin 32
    ([], [], ['Hover Boots'], [], None, [], [], [], []),
    # Coin 33
    ([], [], ['Hover Boots'], [], None, [], [], [], []),
    # Coin 34
    (['Double Jump'], [], ['Hover Boots'], [], None, [], [], [], []),
    # Coin 35
    (['Double Jump'], [], ['Hover Boots'], [], None, [], [], [], []),
    # Coin 36
    (['Double Jump'], [], ['Hover Boots'], [], None, [], [], [], []),
    # Coin 37
    (['Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 38
    (['Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 39
    (['Double Jump'], ['Ledge Grab'], [], ['Hover Boots'], None, [], [], [], []),
    # Coin 40
    (['Double Jump'], ['Ledge Grab'], [], ['Hover Boots'], None, [], [], [], []),
    # Coin 41
    (['Double Jump', 'Pole Climb'], ['Ledge Grab'], [], ['Hover Boots'], 'Easy', ['Double Jump'], ['Ledge Grab'], [], ['Hover Boots']),
    # Coin 42
    (['Double Jump', 'Pole Climb'], ['Ledge Grab'], [], ['Hover Boots'], 'Easy', ['Double Jump'], ['Ledge Grab'], [], ['Hover Boots']),
    # Coin 43
    (['Double Jump', 'Pole Climb'], ['Ledge Grab'], [], ['Hover Boots'], 'Easy', ['Double Jump'], ['Ledge Grab'], [], ['Hover Boots']),
    # Coin 44
    ([], ['Double Jump', 'Ledge Grab'], [], [], None, [], [], [], []),
    # Coin 45
    ([], ['Double Jump', 'Ledge Grab'], [], [], None, [], [], [], []),
    # Coin 46
    ([], ['Double Jump', 'Ledge Grab'], [], [], None, [], [], [], []),
    # Coin 47
    ([], ['Double Jump', 'Ledge Grab'], [], [], None, [], [], [], []),
    # Coin 48
    ([], ['Double Jump', 'Ledge Grab'], [], [], None, [], [], [], []),
    # Coin 49
    (['Pole Vault', 'Double Jump'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 50
    (['Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 51
    (['Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 52
    (['Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 53
    (['Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 54
    (['Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 55
    (['Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 56
    (['Double Jump', 'Ledge Grab', 'Rope Sliding', 'Pole Vault'], [], [], [], 'Easy, Hard', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 57
    (['Double Jump', 'Ledge Grab', 'Rope Sliding', 'Pole Vault'], [], [], [], 'Easy, Hard', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 58
    (['Double Jump', 'Ledge Grab', 'Rope Sliding', 'Pole Vault'], ['Laser', 'Spin'], [], [], 'Easy, Hard', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 59
    (['Double Jump', 'Rope Sliding', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy, Hard', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 60
    (['Double Jump', 'Rope Sliding', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy, Hard', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 61
    (['Stomp', 'Double Jump', 'Rope Sliding', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy', ['Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], []),
    # Coin 62
    (['Stomp', 'Double Jump', 'Rope Sliding', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy', ['Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], []),
    # Coin 63
    (['Stomp', 'Double Jump', 'Rope Sliding', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy', ['Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], []),
    # Coin 64
    (['Stomp', 'Double Jump', 'Rope Sliding', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 65
    (['Stomp', 'Double Jump', 'Rope Sliding', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 66
    (['Stomp', 'Double Jump', 'Rope Sliding', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 67
    (['Stomp', 'Double Jump', 'Rope Sliding', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 68
    (['Stomp', 'Double Jump', 'Rope Sliding', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 69
    (['Double Jump', 'Stomp', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], ['Rocket Boots'], []),
    # Coin 70
    (['Double Jump', 'Stomp', 'Pole Vault'], [], ['Rocket Boots'], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], ['Rocket Boots'], []),
    # Coin 71
    (['Double Jump'], ['Ledge Grab'], [], ['Hover Boots'], None, [], [], [], []),
]

ALS_SPACE_LAND_COINS: List[CoinEntry] = [
    # Coin 1
    ([], [], [], [], None, [], [], [], []),
    # Coin 2
    ([], [], [], [], None, [], [], [], []),
    # Coin 3
    ([], ['Laser', 'Spin'], [], [], None, [], [], [], []),
    # Coin 4
    ([], ['Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 5
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 6
    ([], ['Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 7
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 8
    ([], ['Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 9
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 10
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 11
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 12
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 13
    ([], ['Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 14
    ([], ['Spin', 'Laser'], [], [], None, [], [], [], []),
    # Coin 15
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 16
    ([], ['Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 17
    ([], ['Laser', 'Spin'], [], [], None, [], [], [], []),
    # Coin 18
    (['Push', 'Ledge Grab', 'Double Jump'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 19
    (['Push', 'Ledge Grab', 'Double Jump'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 20
    (['Push', 'Ledge Grab', 'Double Jump', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], []),
    # Coin 21
    (['Push', 'Ledge Grab', 'Double Jump', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], []),
    # Coin 22
    (['Push', 'Ledge Grab', 'Double Jump', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], []),
    # Coin 23
    (['Push', 'Ledge Grab', 'Double Jump', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], []),
    # Coin 24
    (['Push', 'Ledge Grab', 'Double Jump', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], []),
    # Coin 25
    (['Push', 'Ledge Grab', 'Double Jump', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], []),
    # Coin 26
    (['Push', 'Ledge Grab', 'Double Jump', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], []),
    # Coin 27
    (['Push', 'Ledge Grab', 'Double Jump', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], []),
    # Coin 28
    (['Push', 'Ledge Grab', 'Double Jump', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], []),
    # Coin 29
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 30
    (['Double Jump', 'Ledge Grab'], ['Laser', 'Spin'], [], [], None, [], [], [], []),
    # Coin 31
    (['Double Jump', 'Ledge Grab'], ['Laser', 'Spin'], [], [], None, [], [], [], []),
    # Coin 32
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 33
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 34
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 35
    (['Double Jump', 'Ledge Grab'], ['Laser', 'Spin'], [], [], None, [], [], [], []),
    # Coin 36
    (['Double Jump', 'Ledge Grab'], ['Laser', 'Spin'], [], [], None, [], [], [], []),
    # Coin 37
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 38
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 39
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 40
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], ['Laser', 'Spin'], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], ['Laser', 'Spin'], [], []),
    # Coin 41
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 42
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 43
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 44
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 45
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 46
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 47
    (['Double Jump', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 48
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 49
    (['Double Jump', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 50
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 51
    (['Double Jump', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 52
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 53
    (['Double Jump', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 54
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 55
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 56
    (['Double Jump', 'Ledge Grab', 'Rope Sliding'], [], [], [], None, [], [], [], []),
    # Coin 57
    (['Double Jump', 'Ledge Grab', 'Rope Sliding'], [], [], [], None, [], [], [], []),
    # Coin 58
    (['Double Jump', 'Ledge Grab', 'Rope Sliding'], [], [], [], None, [], [], [], []),
    # Coin 59
    (['Double Jump', 'Ledge Grab', 'Rope Sliding'], [], [], [], None, [], [], [], []),
    # Coin 60
    (['Double Jump', 'Ledge Grab', 'Rope Sliding'], [], [], [], None, [], [], [], []),
    # Coin 61
    (['Double Jump', 'Ledge Grab', 'Rope Sliding'], [], [], [], None, [], [], [], []),
    # Coin 62
    (['Double Jump', 'Ledge Grab', 'Rope Sliding'], [], [], [], None, [], [], [], []),
    # Coin 63
    (['Double Jump', 'Ledge Grab', 'Rope Sliding'], [], [], [], None, [], [], [], []),
    # Coin 64
    (['Double Jump', 'Ledge Grab', 'Rope Sliding'], [], [], [], None, [], [], [], []),
    # Coin 65
    (['Double Jump', 'Ledge Grab', 'Rope Sliding'], [], [], [], None, [], [], [], []),
    # Coin 66
    (['Double Jump', 'Ledge Grab', 'Rope Sliding'], [], [], [], None, [], [], [], []),
    # Coin 67
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 68
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 69
    (['Double Jump', 'Pole Vault', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 70
    (['Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 71
    (['Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 72
    (['Double Jump', 'Pole Vault', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 73
    (['Double Jump', 'Pole Vault', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 74
    (['Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 75
    (['Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 76
    (['Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 77
    (['Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 78
    (['Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 79
    (['Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 80
    (['Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 81
    (['Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 82
    (['Double Jump', 'Pole Vault', 'Ledge Grab', 'Rope Sliding'], [], [], [], 'Easy', ['Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], []),
    # Coin 83
    (['Double Jump', 'Pole Vault', 'Ledge Grab', 'Rope Sliding'], ['Laser', 'Spin'], [], [], 'Easy', ['Double Jump', 'Pole Vault', 'Ledge Grab'], ['Laser', 'Spin'], [], []),
    # Coin 84
    (['Double Jump', 'Pole Vault', 'Ledge Grab', 'Rope Sliding'], ['Laser', 'Spin'], [], [], 'Easy', ['Double Jump', 'Pole Vault', 'Ledge Grab'], ['Laser', 'Spin'], [], []),
    # Coin 85
    (['Double Jump', 'Pole Vault', 'Ledge Grab', 'Rope Sliding'], ['Laser', 'Spin', 'Stomp'], [], [], 'Easy', ['Double Jump', 'Pole Vault', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], []),
    # Coin 86
    (['Double Jump', 'Pole Vault', 'Ledge Grab', 'Rope Sliding'], [], [], [], 'Easy', ['Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], []),
    # Coin 87
    (['Double Jump', 'Pole Vault', 'Ledge Grab', 'Rope Sliding'], ['Laser', 'Spin'], [], [], 'Easy', ['Double Jump', 'Pole Vault', 'Ledge Grab'], ['Laser', 'Spin'], [], []),
    # Coin 88
    (['Double Jump', 'Pole Vault', 'Ledge Grab'], ['Laser', 'Spin'], [], [], None, [], [], [], []),
    # Coin 89
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
]

ELEVATOR_HOP_COINS: List[CoinEntry] = [
    # Coin 1
    ([], ['Spin', 'Laser'], [], [], None, [], [], [], []),
    # Coin 2
    ([], [], [], [], None, [], [], [], []),
    # Coin 3
    ([], [], [], [], None, [], [], [], []),
    # Coin 4
    ([], [], [], [], None, [], [], [], []),
    # Coin 5
    ([], [], [], [], None, [], [], [], []),
    # Coin 6
    ([], [], [], [], None, [], [], [], []),
    # Coin 7
    (['Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 8
    (['Pole Vault', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 9
    (['Pole Vault', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 10
    (['Pole Vault', 'Double Jump', 'Rope Sliding', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 11
    (['Visor'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 12
    (['Visor'], ['Spin', 'Laser'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 13
    (['Visor'], ['Laser', 'Spin', 'Stomp'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 14
    (['Visor'], ['Laser', 'Spin', 'Stomp'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 15
    (['Visor'], ['Laser', 'Spin', 'Stomp'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 16
    (['Visor'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 17
    (['Visor'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 18
    (['Visor'], ['Laser', 'Spin', 'Stomp'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 19
    (['Visor'], ['Laser', 'Spin', 'Stomp'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 20
    (['Visor'], ['Laser', 'Spin', 'Stomp'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 21
    (['Visor'], ['Spin', 'Laser'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 22
    (['Visor'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 23
    (['Visor'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 24
    (['Visor'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 25
    (['Visor'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 26
    (['Visor'], ['Spin', 'Laser'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 27
    (['Visor'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 28
    (['Visor'], ['Stomp', 'Spin'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 29
    (['Visor'], ['Laser', 'Spin', 'Stomp'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 30
    (['Visor'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 31
    (['Visor'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 32
    (['Visor'], ['Stomp', 'Spin'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 33
    (['Visor'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 34
    (['Visor'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 35
    (['Visor'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 36
    (['Visor'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 37
    (['Visor'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 38
    (['Visor', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 39
    (['Visor', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 40
    (['Visor', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 41
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 42
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 43
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 44
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 45
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 46
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 47
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 48
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 49
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 50
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 51
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 52
    (['Visor', 'Double Jump', 'Stomp'], ['Laser', 'Spin'], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 53
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 54
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 55
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 56
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 57
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 58
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 59
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 60
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 61
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 62
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
    # Coin 63
    (['Visor', 'Stomp', 'Double Jump'], [], ['Grappling Hook'], [], None, [], [], [], []),
]

ALS_PENTHOUSE_COINS: List[CoinEntry] = [
    # Coin 1
    ([], [], [], [], None, [], [], [], []),
    # Coin 2
    ([], [], [], [], None, [], [], [], []),
    # Coin 3
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 4
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 5
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 6
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 7
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 8
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 9
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 10
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 11
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 12
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 13
    (['Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 14
    (['Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 15
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 16
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 17
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 18
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 19
    (['Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 20
    (['Double Jump', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 21
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 22
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 23
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 24
    (['Double Jump', 'Ledge Grab', 'Pole Climb'], [], [], [], None, [], [], [], []),
    # Coin 25
    (['Double Jump', 'Ledge Grab', 'Pole Climb', 'Pole Vault'], [], [], [], None, [], [], [], []),
    # Coin 26
    (['Laser', 'Visor'], [], [], [], None, [], [], [], []),
    # Coin 27
    (['Laser', 'Visor', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 28
    (['Laser', 'Visor', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 29
    (['Laser', 'Visor', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 30
    (['Laser', 'Stomp', 'Visor', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 31
    (['Laser', 'Stomp', 'Visor', 'Pole Climb', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 32
    (['Laser', 'Stomp', 'Visor', 'Pole Climb', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 33
    (['Laser', 'Stomp', 'Visor', 'Pole Climb', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 34
    (['Laser', 'Stomp', 'Visor', 'Pole Climb', 'Double Jump'], [], [], [], 'Easy', ['Laser', 'Visor', 'Double Jump'], [], [], []),
    # Coin 35
    (['Laser', 'Visor', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 36
    (['Laser', 'Visor', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 37
    (['Laser', 'Visor', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 38
    (['Laser', 'Visor', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 39
    (['Laser', 'Visor', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 40
    (['Laser'], ['Double Jump', 'Visor'], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], ['Spin', 'Stomp'], [], []),
    # Coin 41
    (['Laser'], ['Double Jump', 'Visor'], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], ['Spin', 'Stomp'], [], []),
    # Coin 42
    (['Laser'], ['Double Jump', 'Visor'], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], ['Spin', 'Stomp'], [], []),
    # Coin 43
    (['Laser'], ['Double Jump', 'Visor'], [], [], 'Easy', ['Double Jump', 'Ledge Grab'], ['Spin', 'Stomp'], [], []),
    # Coin 44
    (['Laser', 'Stomp'], ['Double Jump', 'Visor', 'Ledge Grab'], [], [], 'Easy', ['Double Jump', 'Ledge Grab', 'Stomp'], [], [], []),
    # Coin 45
    (['Laser', 'Stomp'], ['Double Jump', 'Visor', 'Ledge Grab'], [], [], 'Easy', ['Double Jump', 'Ledge Grab', 'Stomp'], [], [], []),
    # Coin 46
    (['Laser', 'Stomp', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab', 'Stomp'], [], [], []),
    # Coin 47
    (['Laser', 'Stomp', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab', 'Stomp'], [], [], []),
    # Coin 48
    (['Laser', 'Stomp', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab', 'Stomp'], [], [], []),
    # Coin 49
    (['Laser', 'Stomp', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab', 'Stomp'], [], [], []),
    # Coin 50
    (['Laser', 'Stomp', 'Double Jump', 'Ledge Grab'], [], [], [], 'Easy', ['Double Jump', 'Ledge Grab', 'Stomp'], [], [], []),
    # Coin 51
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 52
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 53
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 54
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 55
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 56
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 57
    (['Push', 'Double Jump', 'Ledge Grab', 'Stomp'], [], [], [], 'Easy', ['Push', 'Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 58
    (['Push', 'Double Jump', 'Ledge Grab', 'Stomp'], [], [], [], 'Easy', ['Push', 'Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 59
    (['Push', 'Double Jump', 'Ledge Grab', 'Stomp'], [], [], [], 'Easy', ['Push', 'Double Jump', 'Ledge Grab'], [], [], []),
    # Coin 60
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 61
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 62
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 63
    (['Push', 'Double Jump', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 64
    (['Push', 'Double Jump', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 65
    (['Push', 'Double Jump', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 66
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 67
    (['Push', 'Double Jump', 'Ledge Grab'], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 68
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 69
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 70
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 71
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 72
    (['Push', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
]

AIRPORT_INFILTRATION_COINS: List[CoinEntry] = [
    # Coin 1
    ([], [], [], [], None, [], [], [], []),
    # Coin 2
    ([], [], [], [], None, [], [], [], []),
    # Coin 3
    ([], [], [], [], None, [], [], [], []),
    # Coin 4
    ([], [], [], [], None, [], [], [], []),
    # Coin 5
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 6
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 7
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 8
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 9
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 10
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 11
    (['Stomp'], [], [], [], None, [], [], [], []),
    # Coin 12
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 13
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 14
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 15
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 16
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 17
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 18
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 19
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 20
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 21
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 22
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 23
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 24
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 25
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 26
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 27
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 28
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 29
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 30
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 31
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 32
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 33
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 34
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 35
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 36
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 37
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 38
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 39
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 40
    (['Stomp', 'Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Ledge Grab'], [], [], []),
    # Coin 41
    (['Stomp', 'Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Ledge Grab'], [], [], []),
    # Coin 42
    (['Stomp', 'Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Ledge Grab'], [], [], []),
    # Coin 43
    (['Stomp', 'Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Ledge Grab'], [], [], []),
    # Coin 44
    (['Stomp', 'Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Ledge Grab'], [], [], []),
    # Coin 45
    (['Stomp', 'Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Ledge Grab'], [], [], []),
    # Coin 46
    (['Stomp', 'Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Ledge Grab'], [], [], []),
    # Coin 47
    (['Stomp', 'Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Ledge Grab'], [], [], []),
    # Coin 48
    (['Stomp', 'Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Ledge Grab'], [], [], []),
    # Coin 49
    (['Stomp', 'Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Ledge Grab'], [], [], []),
    # Coin 50
    (['Stomp', 'Double Jump', 'Pole Vault', 'Ledge Grab'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Ledge Grab'], [], [], []),
    # Coin 51
    (['Stomp', 'Double Jump', 'Pole Vault', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Ledge Grab', 'Pole Climb'], [], [], []),
    # Coin 52
    (['Stomp', 'Double Jump', 'Pole Vault', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Ledge Grab', 'Pole Climb'], [], [], []),
    # Coin 53
    (['Stomp', 'Double Jump', 'Pole Vault', 'Ledge Grab', 'Pole Climb'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Ledge Grab', 'Pole Climb'], [], [], []),
    # Coin 54
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 55
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 56
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 57
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 58
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 59
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 60
    (['Stomp', 'Double Jump', 'Pole Vault'], [], [], [], 'Hard', ['Double Jump', 'Stomp'], [], [], []),
    # Coin 61
    (['Stomp', 'Double Jump', 'Pole Vault', 'Pole Climb'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Pole Climb'], [], [], []),
    # Coin 62
    (['Stomp', 'Double Jump', 'Pole Vault', 'Pole Climb'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Pole Climb'], [], [], []),
    # Coin 63
    (['Stomp', 'Double Jump', 'Pole Vault', 'Pole Climb'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Pole Climb'], [], [], []),
    # Coin 64
    (['Stomp', 'Double Jump', 'Pole Vault', 'Pole Climb'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Pole Climb'], [], [], []),
    # Coin 65
    (['Stomp', 'Double Jump', 'Pole Vault', 'Pole Climb'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Pole Climb'], [], [], []),
    # Coin 66
    (['Stomp', 'Double Jump', 'Pole Vault', 'Pole Climb'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Pole Climb'], [], [], []),
    # Coin 67
    (['Stomp', 'Double Jump', 'Pole Vault', 'Pole Climb'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Pole Climb'], [], [], []),
    # Coin 68
    (['Stomp', 'Double Jump', 'Pole Vault', 'Pole Climb'], [], [], [], 'Hard', ['Double Jump', 'Stomp', 'Pole Climb'], [], [], []),
    # Coin 69
    (['Stomp', 'Double Jump', 'Pole Vault', 'Pole Climb'], ['Rope Sliding', 'Ledge Grab'], [], [], 'Hard', ['Double Jump', 'Stomp', 'Ledge Grab', 'Pole Climb'], [], [], []),
    # Coin 70
    (['Stomp', 'Double Jump', 'Pole Vault', 'Pole Climb'], ['Rope Sliding', 'Ledge Grab'], [], [], 'Hard', ['Double Jump', 'Stomp', 'Ledge Grab', 'Pole Climb'], [], [], []),
    # Coin 71
    (['Stomp', 'Double Jump', 'Pole Vault', 'Pole Climb'], ['Rope Sliding', 'Ledge Grab'], [], [], 'Hard', ['Double Jump', 'Stomp', 'Ledge Grab', 'Pole Climb'], [], [], []),
    # Coin 72
    (['Stomp', 'Double Jump', 'Pole Vault'], [], ['Hover Boots'], [], 'Hard', ['Double Jump', 'Stomp'], [], ['Hover Boots'], []),
]

TARMAC_TROUBLE_COINS: List[CoinEntry] = [
    # Coin 1
    (['Double Jump', 'Ledge Grab'], [], [], [], 'Easy', [], [], [], []),
    # Coin 2
    (['Double Jump', 'Ledge Grab'], [], [], [], 'Easy', [], [], [], []),
    # Coin 3
    ([], [], [], [], None, [], [], [], []),
    # Coin 4
    ([], [], [], [], None, [], [], [], []),
    # Coin 5
    ([], [], [], [], None, [], [], [], []),
    # Coin 6
    ([], [], [], [], None, [], [], [], []),
    # Coin 7
    ([], [], [], [], None, [], [], [], []),
    # Coin 8
    ([], [], [], [], None, [], [], [], []),
    # Coin 9
    ([], [], [], [], None, [], [], [], []),
    # Coin 10
    ([], [], [], [], None, [], [], [], []),
    # Coin 11
    ([], [], [], [], None, [], [], [], []),
    # Coin 12
    ([], [], [], [], None, [], [], [], []),
    # Coin 13
    ([], [], [], [], None, [], [], [], []),
    # Coin 14
    ([], [], [], [], None, [], [], [], []),
    # Coin 15
    ([], [], [], [], None, [], [], [], []),
    # Coin 16
    ([], [], [], [], None, [], [], [], []),
    # Coin 17
    ([], [], [], [], None, [], [], [], []),
    # Coin 18
    ([], [], [], [], None, [], [], [], []),
    # Coin 19
    ([], [], [], [], None, [], [], [], []),
    # Coin 20
    ([], [], [], [], None, [], [], [], []),
    # Coin 21
    ([], [], [], [], None, [], [], [], []),
    # Coin 22
    ([], [], [], [], None, [], [], [], []),
    # Coin 23
    ([], [], [], [], None, [], [], [], []),
    # Coin 24
    ([], [], [], [], None, [], [], [], []),
    # Coin 25
    ([], [], [], [], None, [], [], [], []),
    # Coin 26
    ([], [], [], [], None, [], [], [], []),
    # Coin 27
    ([], [], [], [], None, [], [], [], []),
    # Coin 28
    ([], [], [], [], None, [], [], [], []),
    # Coin 29
    ([], [], [], [], None, [], [], [], []),
    # Coin 30
    ([], [], [], [], None, [], [], [], []),
    # Coin 31
    ([], [], [], [], None, [], [], [], []),
    # Coin 32
    ([], [], [], [], None, [], [], [], []),
    # Coin 33
    ([], [], [], [], None, [], [], [], []),
    # Coin 34
    ([], [], [], [], None, [], [], [], []),
    # Coin 35
    ([], [], [], [], None, [], [], [], []),
    # Coin 36
    ([], [], [], [], None, [], [], [], []),
    # Coin 37
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 38
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 39
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 40
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 41
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 42
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 43
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 44
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 45
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 46
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 47
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 48
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 49
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 50
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 51
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 52
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 53
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 54
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 55
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 56
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 57
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 58
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 59
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 60
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 61
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 62
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 63
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 64
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 65
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 66
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 67
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 68
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 69
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 70
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 71
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 72
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 73
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 74
    ([], ['Laser', 'Spin', 'Stomp'], [], [], None, [], [], [], []),
    # Coin 75
    (['Pole Climb', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 76
    (['Pole Climb', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 77
    (['Pole Climb', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 78
    (['Pole Climb', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 79
    (['Pole Climb', 'Double Jump'], [], [], [], None, [], [], [], []),
    # Coin 80
    (['Pole Climb', 'Double Jump'], ['Rope Sliding', 'Ledge Grab'], [], [], None, [], [], [], []),
    # Coin 81
    (['Pole Climb', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 82
    (['Pole Climb', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 83
    (['Pole Climb', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 84
    (['Pole Climb', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 85
    (['Pole Climb', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 86
    (['Pole Climb', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 87
    (['Pole Climb', 'Double Jump', 'Ledge Grab'], [], [], [], None, [], [], [], []),
    # Coin 88
    ([], [], [], [], None, [], [], [], []),
]

# Map level name -> coin list
COIN_DATA = {
    "Andy's House":          ANDYS_HOUSE_COINS,
    "Andy's Neighborhood":   ANDYS_NEIGHBORHOOD_COINS,
    "Construction Yard":      CONSTRUCTION_YARD_COINS,
    "Alleys and Gullies":     ALLEYS_AND_GULLIES_COINS,
    "Al's Toy Barn":         ALS_TOY_BARN_COINS,
    "Al's Space Land":       ALS_SPACE_LAND_COINS,
    "Elevator Hop":           ELEVATOR_HOP_COINS,
    "Al's Penthouse":        ALS_PENTHOUSE_COINS,
    "Airport Infiltration":   AIRPORT_INFILTRATION_COINS,
    "Tarmac Trouble":         TARMAC_TROUBLE_COINS,
}