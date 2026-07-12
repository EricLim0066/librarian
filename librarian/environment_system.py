"""
Librarian Simulator

Module: Environment System
Developer: Chong Bing Heng

Responsibilities:
- Weather system
- Random events
- Event effects
- Bookshelf management
- Memory system
"""


import random
import copy

from save_manager import load_save, write_save



# =====================================================
# WEATHER SYSTEM
# =====================================================

WEATHER_CONFIG = {

    "Sunny": {
        "customer_rate": 1.2,
        "score_bonus": 1,
        "description": "Good weather. More customers visit."
    },

    "Rainy": {
        "customer_rate": 0.8,
        "score_bonus": 0,
        "description": "Rain reduces customers."
    },

    "Cloudy": {
        "customer_rate": 1,
        "score_bonus": 0,
        "description": "Normal library day."
    },

    "Storm": {
        "customer_rate": 0.5,
        "score_bonus": -2,
        "description": "Storm causes difficulties."
    }

}


WEATHER_LIST = list(WEATHER_CONFIG.keys())


# =====================================================
# BOOK DATABASE
# =====================================================

DEFAULT_BOOKSHELF = {

    "A1": {
        "title": "Python Programming",
        "author": "Guido van Rossum",
        "category": "Programming",
        "available": True,
        "borrow_count": 0
    },

    "A2": {
        "title": "Database System",
        "author": "C.J Date",
        "category": "Database",
        "available": True,
        "borrow_count": 0
    },

    "A3": {
        "title": "Data Structures and Algorithms",
        "author": "Robert Lafore",
        "category": "Computer Science",
        "available": True,
        "borrow_count": 0
    },

    "A4": {
        "title": "Operating System Concepts",
        "author": "Abraham Silberschatz",
        "category": "Operating System",
        "available": True,
        "borrow_count": 0
    },

    "B1": {
        "title": "Computer Networks",
        "author": "Andrew Tanenbaum",
        "category": "Networking",
        "available": True,
        "borrow_count": 0
    },

    "B2": {
        "title": "Artificial Intelligence",
        "author": "Russell",
        "category": "AI",
        "available": True,
        "borrow_count": 0
    },

    "B3": {
        "title": "Machine Learning Fundamentals",
        "author": "Tom Mitchell",
        "category": "AI",
        "available": True,
        "borrow_count": 0
    },

    "B4": {
        "title": "Cyber Security Basics",
        "author": "William Stallings",
        "category": "Security",
        "available": True,
        "borrow_count": 0
    },

    "C1": {
        "title": "Software Engineering",
        "author": "Ian Sommerville",
        "category": "Software",
        "available": True,
        "borrow_count": 0
    },

    "C2": {
        "title": "Web Development",
        "author": "Jon Duckett",
        "category": "Web",
        "available": True,
        "borrow_count": 0
    },

    "C3": {
        "title": "Mobile Application Development",
        "author": "Jeff McWherter",
        "category": "Mobile",
        "available": True,
        "borrow_count": 0
    },

    "C4": {
        "title": "Programming Principles",
        "author": "Bjarne Stroustrup",
        "category": "Programming",
        "available": True,
        "borrow_count": 0
    },

    "D1": {
        "title": "Computer Graphics",
        "author": "John F. Hughes",
        "category": "Graphics",
        "available": True,
        "borrow_count": 0
    },

    "D2": {
        "title": "Human Computer Interaction",
        "author": "Alan Dix",
        "category": "HCI",
        "available": True,
        "borrow_count": 0
    },

    "D3": {
        "title": "Cloud Computing",
        "author": "Rajkumar Buyya",
        "category": "Cloud",
        "available": True,
        "borrow_count": 0
    },

    "D4": {
        "title": "Big Data Analytics",
        "author": "Nathan Marz",
        "category": "Data Science",
        "available": True,
        "borrow_count": 0
    },

    "E1": {
        "title": "Mathematics for Computing",
        "author": "Kenneth Rosen",
        "category": "Mathematics",
        "available": True,
        "borrow_count": 0
    },

    "E2": {
        "title": "Discrete Mathematics",
        "author": "Kenneth Rosen",
        "category": "Mathematics",
        "available": True,
        "borrow_count": 0
    },

    "E3": {
        "title": "Computer Architecture",
        "author": "David Patterson",
        "category": "Hardware",
        "available": True,
        "borrow_count": 0
    },

    "E4": {
        "title": "Introduction to Algorithms",
        "author": "Thomas Cormen",
        "category": "Algorithms",
        "available": True,
        "borrow_count": 0
    }

}


# =====================================================
# WORLD INITIALISATION
# =====================================================

def initialise_world(world):

    if "bookshelf" not in world:
        world["bookshelf"] = copy.deepcopy(
            DEFAULT_BOOKSHELF
        )


    if "memory_log" not in world:
        world["memory_log"] = []


    if "events" not in world:
        world["events"] = []


    if "active_effects" not in world:
        world["active_effects"] = {}


    if "weather" not in world:
        world["weather"] = "Cloudy"


    if "weather_effect" not in world:
        world["weather_effect"] = {}


    if "customer_bonus" not in world:
        world["customer_bonus"] = 0


    if "library_closed" not in world:
        world["library_closed"] = False




def initialise_player(player):

    if "score" not in player:
        player["score"] = 0


    if "stamina" not in player:
        player["stamina"] = 100


# =====================================================
# MEMORY SYSTEM
# =====================================================

def add_memory(slot_name, message):

    data = load_save()

    save = data["save_slots"][slot_name]

    game = save["game_state"]


    world = game.setdefault(
        "world_events",
        {}
    )

    initialise_world(world)

    day = save.get(
        "day_counter",
        0
    )

    world["memory_log"].append({
    "day": day,
    "message": message
})
    if len(world["memory_log"]) > 50:
        world["memory_log"].pop(0)

    write_save(data)



# =====================================================
# WEATHER UPDATE
# =====================================================

def generate_weather():

    return random.choice(
        WEATHER_LIST
    )




def update_weather(slot_name):

    data = load_save()

    save = data["save_slots"][slot_name]

    game = save["game_state"]

    world = game.setdefault(
        "world_events",
        {}
    )

    initialise_world(world)

    weather = generate_weather()

    world["weather"] = weather

    world["weather_effect"] = copy.deepcopy(
        WEATHER_CONFIG[weather]
    )

    write_save(data)

    add_memory(
        slot_name,
        "Weather changed to " + weather
    )

    return weather



# =====================================================
# EVENT SYSTEM
# =====================================================

EVENT_POOL = {

    "Sunny": [
        ("VIP Visitor", 30),
        ("Library Promotion", 70)
    ],

    "Rainy": [
        ("More Customers", 40),
        ("Quiet Reading Day", 60)
    ],

    "Cloudy": [
        ("Normal Day", 100)
    ],

    "Storm": [
        ("Power Failure", 70),
        ("Emergency Closure", 30)
    ]

}




EVENT_EFFECT = {

    "VIP Visitor": {
        "type": "score",
        "value": 5
    },


    "Library Promotion": {
        "type": "customer",
        "value": 2
    },


    "More Customers": {
        "type": "customer",
        "value": 3
    },


    "Quiet Reading Day": {
        "type": "score",
        "value": 1
    },


    "Power Failure": {
        "type": "stamina",
        "value": -20
    },


    "Emergency Closure": {
        "type": "closure",
        "value": True
    },


    "Normal Day": {
        "type": "none",
        "value": 0
    }

}




def generate_event(weather):

    events = EVENT_POOL.get(
        weather,
        EVENT_POOL["Cloudy"]
    )


    names = []
    weights = []


    for name, weight in events:

        names.append(name)
        weights.append(weight)



    return random.choices(
        names,
        weights=weights
    )[0]

# =====================================================
# EVENT EFFECT SYSTEM
# =====================================================

def apply_event_effect(slot_name, event):

    data = load_save()

    save = data["save_slots"][slot_name]

    game = save["game_state"]


    world = game.setdefault(
        "world_events",
        {}
    )


    player = game.setdefault(
        "player_stats",
        {}
    )

    initialise_world(world)


    initialise_player(player)

    effect = copy.deepcopy(EVENT_EFFECT[event])

    world["active_effects"] = effect


    if effect["type"] == "score":

        player["score"] += effect["value"]



    elif effect["type"] == "customer":

        world["customer_bonus"] = effect["value"]



    elif effect["type"] == "stamina":

        player["stamina"] += effect["value"]


        if player["stamina"] < 0:

            player["stamina"] = 0



    elif effect["type"] == "closure":

        world["library_closed"] = True

    write_save(data)


    add_memory(
        slot_name,
        "Event occurred: " + event
    )


    return effect




def update_event(slot_name):

    data = load_save()

    save = data["save_slots"][slot_name]

    world = save["game_state"].setdefault(
        "world_events",
        {}
    )

    initialise_world(world)

    event = generate_event(
        world["weather"]
    )

    world["events"] = [
        event
    ]

    write_save(data)

    effect = apply_event_effect(
        slot_name,
        event
    )

    return {

        "event": event,
        "effect": effect

    }


# =====================================================
# BOOKSHELF SYSTEM
# =====================================================

def get_books(slot_name):

    data = load_save()

    world = data["save_slots"][slot_name]["game_state"].setdefault(
        "world_events",
        {}
    )

    initialise_world(world)

    return world["bookshelf"]



def search_book(slot_name, keyword):

    books = get_books(slot_name)

    result = []

    for shelf, book in books.items():
            
        if (keyword.lower() in book["title"].lower()
            or
            keyword.lower() in book["author"].lower()
            or
            keyword.lower() in book["category"].lower()
            ):

            result.append(
                {
                    "shelf": shelf,
                    "title": book["title"],
                    "author": book["author"],
                    "category": book["category"],
                    "available": book["available"]
                }
            )

    return result



def borrow_book(slot_name, shelf):

    data = load_save()

    world = data["save_slots"][slot_name]["game_state"].setdefault(
        "world_events",
        {}
    )

    initialise_world(world)

    if world["library_closed"]:

        return False

    book = world["bookshelf"].get(
        shelf
    )

    if book and book["available"]:

        book["available"] = False

        book["borrow_count"] += 1

        write_save(data)

        add_memory(
            slot_name,
            "Borrowed " + book["title"]
        )

        return True

    return False



def return_book(slot_name, shelf):

    data = load_save()

    world = data["save_slots"][slot_name]["game_state"].setdefault(
        "world_events",
        {}
    )

    initialise_world(world)

    book = world["bookshelf"].get(
        shelf
    )

    if book:

        book["available"] = True

        write_save(data)

        add_memory(
            slot_name,
            "Returned " + book["title"]
        )

        return True

    return False



def remove_book(slot_name, shelf):

    data = load_save()

    world = data["save_slots"][slot_name]["game_state"].setdefault(
        "world_events",
        {}
    )

    initialise_world(world)

    if shelf in world["bookshelf"]:

        title = world["bookshelf"][shelf]["title"]

        del world["bookshelf"][shelf]

        write_save(data)

        add_memory(
            slot_name,
            "Removed " + title
        )

        return True

    return False


# =====================================================
# DAILY UPDATE
# =====================================================

def next_day_environment(slot_name):

    data = load_save()

    world = data["save_slots"][slot_name]["game_state"].setdefault(
        "world_events",
        {}
    )

    initialise_world(world)

    # reset previous day effects
    world["library_closed"] = False
    world["customer_bonus"] = 0
    world["active_effects"] = {}
    world["events"] = []

    write_save(data)

    weather = update_weather(
        slot_name
    )


    event_data = update_event(
        slot_name
    )


    return {

        "weather": weather,
        "event": event_data["event"],
        "effect": event_data["effect"]

    }


# =====================================================
# GET ENVIRONMENT
# =====================================================

def get_environment(slot_name):

    data = load_save()

    world = data["save_slots"][slot_name]["game_state"].setdefault(
        "world_events",
        {}
    )

    initialise_world(world)

    write_save(data)

    return world