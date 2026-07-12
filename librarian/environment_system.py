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

EVENT_POOL = {
    "Sunny": [("VIP Visitor", 30), ("Library Promotion", 70)],
    "Rainy": [("Quiet Reading Day", 60), ("More Customers", 40)],
    "Cloudy": [("Normal Day", 100)],
    "Storm": [("Power Outage", 30), ("Emergency Closure", 70)],
}

EVENT_EFFECT = {
    "VIP Visitor": {"type": "score", "value": 5},
    "Library Promotion": {"type": "customer_bonus", "value": 0.3},
    "Quiet Reading Day": {"type": "score", "value": 1},
    "More Customers": {"type": "customer_bonus", "value": 0.3},
    "Normal Day": {"type": "none", "value": 0},
    "Power Outage": {"type": "score", "value": -2},
    "Emergency Closure": {"type": "closure", "value": True},
}

# =====================================================
# WEATHER UPDATE
# =====================================================

def generate_weather():

    return random.choice(
        WEATHER_LIST
    )


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