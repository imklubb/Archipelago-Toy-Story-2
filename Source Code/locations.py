from typing import Dict, Optional, NamedTuple, Set
from BaseClasses import Location
from .items import BASE_ID


class TS2LocationData(NamedTuple):
    region: str
    code: Optional[int]
    # Option availability — which setting must be on for this location to exist
    # None = always available (Base AP)
    option: Optional[str]  # "coinsanity" | "lifesanity" | "batterysanity" | "green_laser_sanity" | "rexsanity" | "hint_block_sanity" | None


class ToyStory2Location(Location):
    game = "Toy Story 2"


# ============================================================
# LOCATION ID OFFSET
# ============================================================
# Locations start after items (items use 0-62)
LOC_BASE = BASE_ID + 1000


# ============================================================
# LOCATION TABLE
# ============================================================

LOCATION_TABLE: Dict[str, TS2LocationData] = {

    # ══════════════════════════════════════════════════════
    # ANDY'S HOUSE
    # ══════════════════════════════════════════════════════

    # Coins

    # Tokens
    "Andy's House - Hamm's 50 Coins Token":     TS2LocationData("Andy's House", LOC_BASE + 93,  None),
    "Andy's House - Missing Toys Token":         TS2LocationData("Andy's House", LOC_BASE + 94,  None),
    "Andy's House - Race Token":                 TS2LocationData("Andy's House", LOC_BASE + 95,  None),
    "Andy's House - Hidden Token":               TS2LocationData("Andy's House", LOC_BASE + 96,  None),
    "Andy's House - Boss Token":                 TS2LocationData("Andy's House", LOC_BASE + 97,  None),

    # Missing Toys
    "Andy's House - Sheep (Basement)":           TS2LocationData("Andy's House", LOC_BASE + 98,  None),
    "Andy's House - Sheep (Living Room)":        TS2LocationData("Andy's House", LOC_BASE + 99,  None),
    "Andy's House - Sheep (Kitchen)":            TS2LocationData("Andy's House", LOC_BASE + 100, None),
    "Andy's House - Sheep (Attic)":              TS2LocationData("Andy's House", LOC_BASE + 101, None),
    "Andy's House - Sheep (Garage)":             TS2LocationData("Andy's House", LOC_BASE + 102, None),

    # Missing Part
    "Andy's House - Missing Ear":                TS2LocationData("Andy's House", LOC_BASE + 103, None),
    "Andy's House - Give Potato Head His Ear":   TS2LocationData("Andy's House", LOC_BASE + 104, None),

    # Sanity
    "Andy's House - Life (Crib)":                TS2LocationData("Andy's House", LOC_BASE + 105, "lifesanity"),
    "Andy's House - Life (Living Room)":         TS2LocationData("Andy's House", LOC_BASE + 106, "lifesanity"),
    "Andy's House - Life (Garage)":              TS2LocationData("Andy's House", LOC_BASE + 107, "lifesanity"),
    "Andy's House - Green Laser":                TS2LocationData("Andy's House", LOC_BASE + 108, "green_laser_sanity"),
    "Andy's House - Battery (Andy's Room)":      TS2LocationData("Andy's House", LOC_BASE + 109, "batterysanity"),
    "Andy's House - Battery (Attic)":            TS2LocationData("Andy's House", LOC_BASE + 110, "batterysanity"),
    "Andy's House - Battery (Basement)":         TS2LocationData("Andy's House", LOC_BASE + 111, "batterysanity"),
    "Andy's House - Battery (Garage)":           TS2LocationData("Andy's House", LOC_BASE + 112, "batterysanity"),
    "Andy's House - Battery (Living Room)":      TS2LocationData("Andy's House", LOC_BASE + 113, "batterysanity"),
    "Andy's House - Battery (Handrail)":         TS2LocationData("Andy's House", LOC_BASE + 114, "batterysanity"),
    "Andy's House - Talk to Rex":                TS2LocationData("Andy's House", LOC_BASE + 115, "rexsanity"),

    # ══════════════════════════════════════════════════════
    # ANDY'S NEIGHBORHOOD
    # ══════════════════════════════════════════════════════

    # Coins

    # Tokens
    "Andy's Neighborhood - Hamm's 50 Coins Token":  TS2LocationData("Andy's Neighborhood", LOC_BASE + 215, None),
    "Andy's Neighborhood - Missing Toys Token":      TS2LocationData("Andy's Neighborhood", LOC_BASE + 216, None),
    "Andy's Neighborhood - Race Token":              TS2LocationData("Andy's Neighborhood", LOC_BASE + 217, None),
    "Andy's Neighborhood - Hidden Token":            TS2LocationData("Andy's Neighborhood", LOC_BASE + 218, None),
    "Andy's Neighborhood - Boss Token":              TS2LocationData("Andy's Neighborhood", LOC_BASE + 219, None),

    # Missing Toys
    "Andy's Neighborhood - Soldier (Molehill)":      TS2LocationData("Andy's Neighborhood", LOC_BASE + 220, None),
    "Andy's Neighborhood - Soldier (Clothes Line)":  TS2LocationData("Andy's Neighborhood", LOC_BASE + 221, None),
    "Andy's Neighborhood - Soldier (Swing)":         TS2LocationData("Andy's Neighborhood", LOC_BASE + 222, None),
    "Andy's Neighborhood - Soldier (Pool Plant)":    TS2LocationData("Andy's Neighborhood", LOC_BASE + 223, None),
    "Andy's Neighborhood - Soldier (Tree)":          TS2LocationData("Andy's Neighborhood", LOC_BASE + 224, None),

    # Sanity
    "Andy's Neighborhood - Life (Top of Swing)":         TS2LocationData("Andy's Neighborhood", LOC_BASE + 225, "lifesanity"),
    "Andy's Neighborhood - Green Laser":                 TS2LocationData("Andy's Neighborhood", LOC_BASE + 226, "green_laser_sanity"),
    "Andy's Neighborhood - Battery (Lawnmower Yard)":    TS2LocationData("Andy's Neighborhood", LOC_BASE + 227, "batterysanity"),
    "Andy's Neighborhood - Battery (Washing Machine)":   TS2LocationData("Andy's Neighborhood", LOC_BASE + 228, "batterysanity"),
    "Andy's Neighborhood - Battery (Pool Yard)":         TS2LocationData("Andy's Neighborhood", LOC_BASE + 229, "batterysanity"),
    "Andy's Neighborhood - Battery (Swing)":             TS2LocationData("Andy's Neighborhood", LOC_BASE + 230, "batterysanity"),
    "Andy's Neighborhood - Battery (Top of Tree)":       TS2LocationData("Andy's Neighborhood", LOC_BASE + 231, "batterysanity"),
    "Andy's Neighborhood - Talk to Rex":                 TS2LocationData("Andy's Neighborhood", LOC_BASE + 232, "rexsanity"),

    # ══════════════════════════════════════════════════════
    # BOMBS AWAY!
    # ══════════════════════════════════════════════════════

    "Bombs Away! - Defeat Reward 1":            TS2LocationData("Bombs Away!", LOC_BASE + 233, None),
    "Bombs Away! - Defeat Reward 2":            TS2LocationData("Bombs Away!", LOC_BASE + 234, None),
    "Bombs Away! - Battery (Back Right)":       TS2LocationData("Bombs Away!", LOC_BASE + 235, "batterysanity"),
    "Bombs Away! - Battery (Back Left)":        TS2LocationData("Bombs Away!", LOC_BASE + 236, "batterysanity"),
    "Bombs Away! - Battery (Front Left)":       TS2LocationData("Bombs Away!", LOC_BASE + 237, "batterysanity"),
    "Bombs Away! - Battery (Front Right)":      TS2LocationData("Bombs Away!", LOC_BASE + 238, "batterysanity"),

    # ══════════════════════════════════════════════════════
    # CONSTRUCTION YARD
    # ══════════════════════════════════════════════════════

    # Coins

    # Tokens
    "Construction Yard - Hamm's 50 Coins Token":    TS2LocationData("Construction Yard", LOC_BASE + 311, None),
    "Construction Yard - Missing Toys Token":        TS2LocationData("Construction Yard", LOC_BASE + 312, None),
    "Construction Yard - Race Token":                TS2LocationData("Construction Yard", LOC_BASE + 313, None),
    "Construction Yard - Hidden Token":              TS2LocationData("Construction Yard", LOC_BASE + 314, None),
    "Construction Yard - Boss Token":                TS2LocationData("Construction Yard", LOC_BASE + 315, None),

    # Missing Toys
    "Construction Yard - Worker Tike (Wheelbarrow)":        TS2LocationData("Construction Yard", LOC_BASE + 316, None),
    "Construction Yard - Worker Tike (Filing Cabinets)":    TS2LocationData("Construction Yard", LOC_BASE + 317, None),
    "Construction Yard - Worker Tike (Bulldozer)":          TS2LocationData("Construction Yard", LOC_BASE + 318, None),
    "Construction Yard - Worker Tike (Construction Floor 1)": TS2LocationData("Construction Yard", LOC_BASE + 319, None),
    "Construction Yard - Worker Tike (Boss Arena)":         TS2LocationData("Construction Yard", LOC_BASE + 320, None),

    # Missing Part
    "Construction Yard - Missing Eye":               TS2LocationData("Construction Yard", LOC_BASE + 321, None),
    "Construction Yard - Give Potato Head His Eye":  TS2LocationData("Construction Yard", LOC_BASE + 322, None),

    # Sanity
    "Construction Yard - Life (Top of Bulldozer)":       TS2LocationData("Construction Yard", LOC_BASE + 323, "lifesanity"),
    "Construction Yard - Life (Roof of Green Building)": TS2LocationData("Construction Yard", LOC_BASE + 324, "lifesanity"),
    "Construction Yard - Green Laser":                   TS2LocationData("Construction Yard", LOC_BASE + 325, "green_laser_sanity"),
    "Construction Yard - Battery (Bulldozer)":           TS2LocationData("Construction Yard", LOC_BASE + 326, "batterysanity"),
    "Construction Yard - Battery (Boss Arena Front Left)": TS2LocationData("Construction Yard", LOC_BASE + 327, "batterysanity"),
    "Construction Yard - Battery (Boss Arena Back Left)":  TS2LocationData("Construction Yard", LOC_BASE + 328, "batterysanity"),
    "Construction Yard - Battery (Boss Arena Back Right)": TS2LocationData("Construction Yard", LOC_BASE + 329, "batterysanity"),
    "Construction Yard - Talk to Rex":                   TS2LocationData("Construction Yard", LOC_BASE + 330, "rexsanity"),

    # ══════════════════════════════════════════════════════
    # ALLEYS AND GULLIES
    # ══════════════════════════════════════════════════════

    # Coins

    # Tokens
    "Alleys and Gullies - Hamm's 50 Coins Token":   TS2LocationData("Alleys and Gullies", LOC_BASE + 434, None),
    "Alleys and Gullies - Missing Toys Token":       TS2LocationData("Alleys and Gullies", LOC_BASE + 435, None),
    "Alleys and Gullies - Race Token":               TS2LocationData("Alleys and Gullies", LOC_BASE + 436, None),
    "Alleys and Gullies - Hidden Token":             TS2LocationData("Alleys and Gullies", LOC_BASE + 437, None),
    "Alleys and Gullies - Boss Token":               TS2LocationData("Alleys and Gullies", LOC_BASE + 438, None),

    # Missing Toys
    "Alleys and Gullies - Duck (Pool Behind Construction)": TS2LocationData("Alleys and Gullies", LOC_BASE + 439, None),
    "Alleys and Gullies - Duck (Hidden Near Race)":         TS2LocationData("Alleys and Gullies", LOC_BASE + 440, None),
    "Alleys and Gullies - Duck (Incline Parasol)":          TS2LocationData("Alleys and Gullies", LOC_BASE + 441, None),
    "Alleys and Gullies - Duck (Window Sill)":              TS2LocationData("Alleys and Gullies", LOC_BASE + 442, None),
    "Alleys and Gullies - Duck (Rain Gutter)":              TS2LocationData("Alleys and Gullies", LOC_BASE + 443, None),

    # Sanity
    "Alleys and Gullies - Life (Pool Behind Construction)": TS2LocationData("Alleys and Gullies", LOC_BASE + 446, "lifesanity"),
    "Alleys and Gullies - Life (Lily Pad Behind Race)":     TS2LocationData("Alleys and Gullies", LOC_BASE + 447, "lifesanity"),
    "Alleys and Gullies - Life (Window Sill)":              TS2LocationData("Alleys and Gullies", LOC_BASE + 448, "lifesanity"),
    "Alleys and Gullies - Green Laser":                     TS2LocationData("Alleys and Gullies", LOC_BASE + 449, "green_laser_sanity"),
    "Alleys and Gullies - Battery (Behind Construction)":   TS2LocationData("Alleys and Gullies", LOC_BASE + 450, "batterysanity"),
    "Alleys and Gullies - Battery (Balcony Fence)":         TS2LocationData("Alleys and Gullies", LOC_BASE + 451, "batterysanity"),
    "Alleys and Gullies - Battery (Boss Arena)":            TS2LocationData("Alleys and Gullies", LOC_BASE + 452, "batterysanity"),
    "Alleys and Gullies - Talk to Rex":                     TS2LocationData("Alleys and Gullies", LOC_BASE + 453, "rexsanity"),

    # ══════════════════════════════════════════════════════
    # SLIME TIME
    # ══════════════════════════════════════════════════════

    "Slime Time - Defeat Reward 1":     TS2LocationData("Slime Time", LOC_BASE + 454, None),
    "Slime Time - Defeat Reward 2":     TS2LocationData("Slime Time", LOC_BASE + 455, None),
    "Slime Time - Green Laser":         TS2LocationData("Slime Time", LOC_BASE + 456, "green_laser_sanity"),

    # ══════════════════════════════════════════════════════
    # AL'S TOY BARN
    # ══════════════════════════════════════════════════════

    # Coins

    # Tokens
    "Al's Toy Barn - Hamm's 50 Coins Token":    TS2LocationData("Al's Toy Barn", LOC_BASE + 528, None),
    "Al's Toy Barn - Missing Toys Token":        TS2LocationData("Al's Toy Barn", LOC_BASE + 529, None),
    "Al's Toy Barn - Race Token":                TS2LocationData("Al's Toy Barn", LOC_BASE + 530, None),
    "Al's Toy Barn - Hidden Token":              TS2LocationData("Al's Toy Barn", LOC_BASE + 531, None),
    "Al's Toy Barn - Boss Token":                TS2LocationData("Al's Toy Barn", LOC_BASE + 532, None),

    # Missing Toys
    "Al's Toy Barn - Chick (Complete Race)":     TS2LocationData("Al's Toy Barn", LOC_BASE + 533, None),
    "Al's Toy Barn - Chick (Gumball Machines)":  TS2LocationData("Al's Toy Barn", LOC_BASE + 534, None),
    "Al's Toy Barn - Chick (Shipping Boxes)":    TS2LocationData("Al's Toy Barn", LOC_BASE + 535, None),
    "Al's Toy Barn - Chick (Near Basketballs)":  TS2LocationData("Al's Toy Barn", LOC_BASE + 536, None),
    "Al's Toy Barn - Chick (End of Long Aisle)": TS2LocationData("Al's Toy Barn", LOC_BASE + 537, None),

    # Missing Part
    "Al's Toy Barn - Missing Arm":               TS2LocationData("Al's Toy Barn", LOC_BASE + 538, None),
    "Al's Toy Barn - Give Potato Head His Arm":  TS2LocationData("Al's Toy Barn", LOC_BASE + 539, None),

    # Sanity
    "Al's Toy Barn - Life (Tennis Ball Isle)":   TS2LocationData("Al's Toy Barn", LOC_BASE + 540, "lifesanity"),
    "Al's Toy Barn - Green Laser":               TS2LocationData("Al's Toy Barn", LOC_BASE + 541, "green_laser_sanity"),
    "Al's Toy Barn - Battery (Gumball Machine)": TS2LocationData("Al's Toy Barn", LOC_BASE + 542, "batterysanity"),
    "Al's Toy Barn - Battery (Ventilation Shaft)": TS2LocationData("Al's Toy Barn", LOC_BASE + 543, "batterysanity"),
    "Al's Toy Barn - Battery (Between Bicycles)":  TS2LocationData("Al's Toy Barn", LOC_BASE + 544, "batterysanity"),
    "Al's Toy Barn - Battery (Cardboard Boxes)":   TS2LocationData("Al's Toy Barn", LOC_BASE + 545, "batterysanity"),
    "Al's Toy Barn - Battery (Boss Arena)":         TS2LocationData("Al's Toy Barn", LOC_BASE + 546, "batterysanity"),
    "Al's Toy Barn - Talk to Rex":                  TS2LocationData("Al's Toy Barn", LOC_BASE + 547, "rexsanity"),

    # ══════════════════════════════════════════════════════
    # AL'S SPACE LAND
    # ══════════════════════════════════════════════════════

    # Coins

    # Tokens
    "Al's Space Land - Hamm's 50 Coins Token":  TS2LocationData("Al's Space Land", LOC_BASE + 637, None),
    "Al's Space Land - Missing Toys Token":      TS2LocationData("Al's Space Land", LOC_BASE + 638, None),
    "Al's Space Land - Race Token":              TS2LocationData("Al's Space Land", LOC_BASE + 639, None),
    "Al's Space Land - Hidden Token":            TS2LocationData("Al's Space Land", LOC_BASE + 640, None),
    "Al's Space Land - Boss Token":              TS2LocationData("Al's Space Land", LOC_BASE + 641, None),

    # Missing Toys
    "Al's Space Land - Alien (Ballpit)":            TS2LocationData("Al's Space Land", LOC_BASE + 642, None),
    "Al's Space Land - Alien (Planet Mobile)":      TS2LocationData("Al's Space Land", LOC_BASE + 643, None),
    "Al's Space Land - Alien (End of Race)":        TS2LocationData("Al's Space Land", LOC_BASE + 644, None),
    "Al's Space Land - Alien (Middle of Zurg Aisle)": TS2LocationData("Al's Space Land", LOC_BASE + 645, None),
    "Al's Space Land - Alien (End of Zurg Aisle)":  TS2LocationData("Al's Space Land", LOC_BASE + 646, None),

    # Sanity
    "Al's Space Land - Life (Planet Mobile)":       TS2LocationData("Al's Space Land", LOC_BASE + 647, "lifesanity"),
    "Al's Space Land - Green Laser":                TS2LocationData("Al's Space Land", LOC_BASE + 648, "green_laser_sanity"),
    "Al's Space Land - Battery (Boss Arena)":       TS2LocationData("Al's Space Land", LOC_BASE + 649, "batterysanity"),
    "Al's Space Land - Battery (Arcade Cabinet)":   TS2LocationData("Al's Space Land", LOC_BASE + 650, "batterysanity"),
    "Al's Space Land - Battery (Blue Shelves)":     TS2LocationData("Al's Space Land", LOC_BASE + 651, "batterysanity"),
    "Al's Space Land - Battery (Red Shelf)":        TS2LocationData("Al's Space Land", LOC_BASE + 652, "batterysanity"),
    "Al's Space Land - Battery (Race Blue Shelf)":  TS2LocationData("Al's Space Land", LOC_BASE + 653, "batterysanity"),
    "Al's Space Land - Talk to Rex":                TS2LocationData("Al's Space Land", LOC_BASE + 654, "rexsanity"),

    # ══════════════════════════════════════════════════════
    # TOY BARN ENCOUNTER
    # ══════════════════════════════════════════════════════

    "Toy Barn Encounter - Defeat Reward 1":         TS2LocationData("Toy Barn Encounter", LOC_BASE + 655, None),
    "Toy Barn Encounter - Defeat Reward 2":         TS2LocationData("Toy Barn Encounter", LOC_BASE + 656, None),
    "Toy Barn Encounter - Battery (South)":         TS2LocationData("Toy Barn Encounter", LOC_BASE + 657, "batterysanity"),
    "Toy Barn Encounter - Battery (North)":         TS2LocationData("Toy Barn Encounter", LOC_BASE + 658, "batterysanity"),
    "Toy Barn Encounter - Battery (East)":          TS2LocationData("Toy Barn Encounter", LOC_BASE + 659, "batterysanity"),
    "Toy Barn Encounter - Battery (West)":          TS2LocationData("Toy Barn Encounter", LOC_BASE + 660, "batterysanity"),

    # ══════════════════════════════════════════════════════
    # ELEVATOR HOP
    # ══════════════════════════════════════════════════════

    # Coins

    # Tokens
    "Elevator Hop - Hamm's 50 Coins Token":     TS2LocationData("Elevator Hop", LOC_BASE + 724, None),
    "Elevator Hop - Missing Toys Token":         TS2LocationData("Elevator Hop", LOC_BASE + 725, None),
    "Elevator Hop - Race Token":                 TS2LocationData("Elevator Hop", LOC_BASE + 726, None),
    "Elevator Hop - Hidden Token":               TS2LocationData("Elevator Hop", LOC_BASE + 727, None),
    "Elevator Hop - Boss Token":                 TS2LocationData("Elevator Hop", LOC_BASE + 728, None),

    # Missing Toys
    "Elevator Hop - Mouse (Electrical Room)":    TS2LocationData("Elevator Hop", LOC_BASE + 729, None),
    "Elevator Hop - Mouse (Next to Rex)":        TS2LocationData("Elevator Hop", LOC_BASE + 730, None),
    "Elevator Hop - Mouse (Control Room)":       TS2LocationData("Elevator Hop", LOC_BASE + 731, None),
    "Elevator Hop - Mouse (Side of Elevator Shaft)": TS2LocationData("Elevator Hop", LOC_BASE + 732, None),
    "Elevator Hop - Mouse (Top of Elevator)":    TS2LocationData("Elevator Hop", LOC_BASE + 733, None),

    # Missing Part
    "Elevator Hop - Missing Foot":               TS2LocationData("Elevator Hop", LOC_BASE + 734, None),
    "Elevator Hop - Give Potato Head His Foot":  TS2LocationData("Elevator Hop", LOC_BASE + 735, None),

    # Sanity
    "Elevator Hop - Green Laser":                TS2LocationData("Elevator Hop", LOC_BASE + 736, "green_laser_sanity"),
    "Elevator Hop - Talk to Rex":                TS2LocationData("Elevator Hop", LOC_BASE + 737, "rexsanity"),

    # ══════════════════════════════════════════════════════
    # AL'S PENTHOUSE
    # ══════════════════════════════════════════════════════

    # Coins

    # Tokens
    "Al's Penthouse - Hamm's 50 Coins Token":   TS2LocationData("Al's Penthouse", LOC_BASE + 810, None),
    "Al's Penthouse - Missing Toys Token":       TS2LocationData("Al's Penthouse", LOC_BASE + 811, None),
    "Al's Penthouse - Race Token":               TS2LocationData("Al's Penthouse", LOC_BASE + 812, None),
    "Al's Penthouse - Hidden Token":             TS2LocationData("Al's Penthouse", LOC_BASE + 813, None),
    "Al's Penthouse - Boss Token":               TS2LocationData("Al's Penthouse", LOC_BASE + 814, None),

    # Missing Toys
    "Al's Penthouse - Critter (Living Room)":    TS2LocationData("Al's Penthouse", LOC_BASE + 815, None),
    "Al's Penthouse - Critter (Kitchen)":        TS2LocationData("Al's Penthouse", LOC_BASE + 816, None),
    "Al's Penthouse - Critter (Bathroom)":       TS2LocationData("Al's Penthouse", LOC_BASE + 817, None),
    "Al's Penthouse - Critter (Train Bed)":      TS2LocationData("Al's Penthouse", LOC_BASE + 818, None),
    "Al's Penthouse - Critter (Woody Room)":     TS2LocationData("Al's Penthouse", LOC_BASE + 819, None),

    # Sanity
    "Al's Penthouse - Life (Fireplace)":         TS2LocationData("Al's Penthouse", LOC_BASE + 822, "lifesanity"),
    "Al's Penthouse - Green Laser":              TS2LocationData("Al's Penthouse", LOC_BASE + 823, "green_laser_sanity"),
    "Al's Penthouse - Battery (Under Table)":    TS2LocationData("Al's Penthouse", LOC_BASE + 824, "batterysanity"),
    "Al's Penthouse - Battery (Bathroom)":       TS2LocationData("Al's Penthouse", LOC_BASE + 825, "batterysanity"),
    "Al's Penthouse - Battery (Kitchen)":        TS2LocationData("Al's Penthouse", LOC_BASE + 826, "batterysanity"),
    "Al's Penthouse - Battery (Train Bed)":      TS2LocationData("Al's Penthouse", LOC_BASE + 827, "batterysanity"),
    "Al's Penthouse - Battery (Television)":     TS2LocationData("Al's Penthouse", LOC_BASE + 828, "batterysanity"),
    "Al's Penthouse - Talk to Rex":              TS2LocationData("Al's Penthouse", LOC_BASE + 829, "rexsanity"),

    # ══════════════════════════════════════════════════════
    # THE EVIL EMPEROR ZURG
    # ══════════════════════════════════════════════════════

    "The Evil Emperor Zurg - Defeat Reward 1":  TS2LocationData("The Evil Emperor Zurg", LOC_BASE + 830, None),
    "The Evil Emperor Zurg - Defeat Reward 2":  TS2LocationData("The Evil Emperor Zurg", LOC_BASE + 831, None),

    # ══════════════════════════════════════════════════════
    # AIRPORT INFILTRATION
    # ══════════════════════════════════════════════════════

    # Coins

    # Tokens
    "Airport Infiltration - Hamm's 50 Coins Token": TS2LocationData("Airport Infiltration", LOC_BASE + 904, None),
    "Airport Infiltration - Missing Toys Token":     TS2LocationData("Airport Infiltration", LOC_BASE + 905, None),
    "Airport Infiltration - Race Token":             TS2LocationData("Airport Infiltration", LOC_BASE + 906, None),
    "Airport Infiltration - Hidden Token":           TS2LocationData("Airport Infiltration", LOC_BASE + 907, None),
    "Airport Infiltration - Boss Token":             TS2LocationData("Airport Infiltration", LOC_BASE + 908, None),

    # Missing Toys
    "Airport Infiltration - Passenger Tike (Near Start)":           TS2LocationData("Airport Infiltration", LOC_BASE + 909, None),
    "Airport Infiltration - Passenger Tike (Top of Conveyor Belts)": TS2LocationData("Airport Infiltration", LOC_BASE + 910, None),
    "Airport Infiltration - Passenger Tike (Near Boss Arena)":       TS2LocationData("Airport Infiltration", LOC_BASE + 911, None),
    "Airport Infiltration - Passenger Tike (Top of Jet)":            TS2LocationData("Airport Infiltration", LOC_BASE + 912, None),
    "Airport Infiltration - Passenger Tike (Scaffolding)":           TS2LocationData("Airport Infiltration", LOC_BASE + 913, None),

    # Missing Part
    "Airport Infiltration - Missing Mouth":              TS2LocationData("Airport Infiltration", LOC_BASE + 914, None),
    "Airport Infiltration - Give Potato Head His Mouth": TS2LocationData("Airport Infiltration", LOC_BASE + 915, None),

    # Sanity
    "Airport Infiltration - Green Laser":                TS2LocationData("Airport Infiltration", LOC_BASE + 916, "green_laser_sanity"),
    "Airport Infiltration - Battery (Luggage Pile)":     TS2LocationData("Airport Infiltration", LOC_BASE + 917, "batterysanity"),
    "Airport Infiltration - Battery (Near Hidden Token)": TS2LocationData("Airport Infiltration", LOC_BASE + 918, "batterysanity"),
    "Airport Infiltration - Battery (Boss Arena)":        TS2LocationData("Airport Infiltration", LOC_BASE + 919, "batterysanity"),
    "Airport Infiltration - Talk to Rex":                 TS2LocationData("Airport Infiltration", LOC_BASE + 920, "rexsanity"),

    # ══════════════════════════════════════════════════════
    # TARMAC TROUBLE
    # ══════════════════════════════════════════════════════

    # Coins

    # Tokens
    "Tarmac Trouble - Hamm's 50 Coins Token":   TS2LocationData("Tarmac Trouble", LOC_BASE + 1009, None),
    "Tarmac Trouble - Missing Toys Token":       TS2LocationData("Tarmac Trouble", LOC_BASE + 1010, None),
    "Tarmac Trouble - Race Token":               TS2LocationData("Tarmac Trouble", LOC_BASE + 1011, None),
    "Tarmac Trouble - Hidden Token":             TS2LocationData("Tarmac Trouble", LOC_BASE + 1012, None),
    "Tarmac Trouble - Boss Token":               TS2LocationData("Tarmac Trouble", LOC_BASE + 1013, None),

    # Missing Toys
    "Tarmac Trouble - Luggage (Top of Plane)":          TS2LocationData("Tarmac Trouble", LOC_BASE + 1014, None),
    "Tarmac Trouble - Luggage (Zone 2 Cart)":           TS2LocationData("Tarmac Trouble", LOC_BASE + 1015, None),
    "Tarmac Trouble - Luggage (Zone 8)":                TS2LocationData("Tarmac Trouble", LOC_BASE + 1016, None),
    "Tarmac Trouble - Luggage (Zone 6 Conveyor Belt)":  TS2LocationData("Tarmac Trouble", LOC_BASE + 1017, None),
    "Tarmac Trouble - Luggage (Zone 4)":                TS2LocationData("Tarmac Trouble", LOC_BASE + 1018, None),

    # Sanity
    "Tarmac Trouble - Life (Zone 6)":                   TS2LocationData("Tarmac Trouble", LOC_BASE + 1019, "lifesanity"),
    "Tarmac Trouble - Green Laser":                     TS2LocationData("Tarmac Trouble", LOC_BASE + 1020, "green_laser_sanity"),
    "Tarmac Trouble - Battery (Road Opposite Zone 8)":  TS2LocationData("Tarmac Trouble", LOC_BASE + 1021, "batterysanity"),
    "Tarmac Trouble - Battery (Helicopter Pad)":        TS2LocationData("Tarmac Trouble", LOC_BASE + 1022, "batterysanity"),
    "Tarmac Trouble - Battery (Zone 3)":                TS2LocationData("Tarmac Trouble", LOC_BASE + 1023, "batterysanity"),
    "Tarmac Trouble - Battery (Green Slime Maze)":      TS2LocationData("Tarmac Trouble", LOC_BASE + 1024, "batterysanity"),
    "Tarmac Trouble - Battery (Boss Arena)":            TS2LocationData("Tarmac Trouble", LOC_BASE + 1025, "batterysanity"),
    "Tarmac Trouble - Talk to Rex":                     TS2LocationData("Tarmac Trouble", LOC_BASE + 1026, "rexsanity"),

    # ══════════════════════════════════════════════════════
    # PROSPECTOR SHOWDOWN
    # ══════════════════════════════════════════════════════

    "Prospector Showdown - Defeat GOAL":    TS2LocationData("Prospector Showdown", None, None),

    # ══════════════════════════════════════════════════════
    # HINT BLOCK SANITY  (IDs 1027-1044)
    # ══════════════════════════════════════════════════════
    "Andy's House - Hint Block (Andy's Room Bookshelf)":     TS2LocationData("Andy's House", LOC_BASE + 1027, "hint_block_sanity"),
    "Andy's House - Hint Block (Andy's Room Bed)":           TS2LocationData("Andy's House", LOC_BASE + 1028, "hint_block_sanity"),
    "Andy's House - Hint Block (Andy's Room Dresser Shelf)": TS2LocationData("Andy's House", LOC_BASE + 1029, "hint_block_sanity"),
    "Andy's House - Hint Block (Andy's Room Crib)":          TS2LocationData("Andy's House", LOC_BASE + 1030, "hint_block_sanity"),
    "Andy's House - Hint Block (Top of Stairs)":             TS2LocationData("Andy's House", LOC_BASE + 1031, "hint_block_sanity"),
    "Andy's House - Hint Block (Attic)":                     TS2LocationData("Andy's House", LOC_BASE + 1032, "hint_block_sanity"),
    "Andy's House - Hint Block (Bottom of Stairs)":          TS2LocationData("Andy's House", LOC_BASE + 1033, "hint_block_sanity"),
    "Andy's House - Hint Block (Top of Garage)":             TS2LocationData("Andy's House", LOC_BASE + 1034, "hint_block_sanity"),
    "Andy's House - Hint Block (Living Room Recliner)":      TS2LocationData("Andy's House", LOC_BASE + 1035, "hint_block_sanity"),
    "Andy's Neighborhood - Hint Block (Lawnmower Yard)":     TS2LocationData("Andy's Neighborhood", LOC_BASE + 1036, "hint_block_sanity"),
    "Construction Yard - Hint Block (Paint Can Room)":       TS2LocationData("Construction Yard", LOC_BASE + 1037, "hint_block_sanity"),
    "Al's Toy Barn - Hint Block (Hay Bale Ride)":            TS2LocationData("Al's Toy Barn", LOC_BASE + 1038, "hint_block_sanity"),
    "Elevator Hop - Hint Block (East Shortcut Fan)":         TS2LocationData("Elevator Hop", LOC_BASE + 1039, "hint_block_sanity"),
    "Elevator Hop - Hint Block (West Shortcut Fan)":         TS2LocationData("Elevator Hop", LOC_BASE + 1040, "hint_block_sanity"),
    "Elevator Hop - Hint Block (Control Room)":              TS2LocationData("Elevator Hop", LOC_BASE + 1041, "hint_block_sanity"),
    "Al's Penthouse - Hint Block (Bathtub)":                 TS2LocationData("Al's Penthouse", LOC_BASE + 1042, "hint_block_sanity"),
    "Al's Penthouse - Hint Block (Train Bed)":               TS2LocationData("Al's Penthouse", LOC_BASE + 1043, "hint_block_sanity"),
    "Tarmac Trouble - Hint Block (Light Puzzle)":            TS2LocationData("Tarmac Trouble", LOC_BASE + 1044, "hint_block_sanity"),
}


# ── HELPER: locations by region ──────────────────────────────

def get_locations_for_region(region: str) -> Dict[str, TS2LocationData]:
    return {name: data for name, data in LOCATION_TABLE.items()
            if data.region == region}


def get_locations_by_option(option: Optional[str]) -> Dict[str, TS2LocationData]:
    return {name: data for name, data in LOCATION_TABLE.items()
            if data.option == option}