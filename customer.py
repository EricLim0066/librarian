"""
customer.py — Customer data, personality, patience & event system
Author  : Lim Jing Xiang (Player Interaction)
Project : Librarian Simulator

HOW TEAMMATES CALL THIS MODULE
────────────────────────────────────────────────────────────────────────────────
    from customer import CustomerManager

    mgr = CustomerManager()

    # Spawn customers for a new day
    mgr.spawn_customers(day=1, count=5)

    # Tick every in-game minute (call this from the game loop)
    left_customers = mgr.tick_minute(current_minute=10)

    # Get a nearby customer (pass player grid position)
    cust = mgr.get_nearby(player_pos=[2, 3])

    # Resolve a customer event
    result = mgr.resolve(customer_id, action="return_book")
    print(result["message"], result["score_delta"])

    # Read one customer's full state
    info = mgr.get_state(customer_id)

    # All active (not-left) customers
    active = mgr.get_active()

DESIGN NOTES FOR TEAMMATES
────────────────────────────────────────────────────────────────────────────────
  • No external libraries — pure Python stdlib only.
  • CustomerManager owns the list; other modules should NOT mutate customer
    dicts directly — use the methods below so logs stay consistent.
  • Amirul  → save/load: call mgr.export_state() / mgr.import_state(data)
  • Lum     → scoring:   resolve() returns {"score_delta": int}
  • Bing Heng → events:  inject_random_event(customer_id, event_name) hook
"""

import random
from typing import Optional

# ── Constants ─────────────────────────────────────────────────────────────────

# Personality types and their base patience (in in-game minutes)
PERSONALITY_CONFIG = {
    # name          patience_range   scene_chance  events_available
    "loud":        {"patience": (3,  6),  "scene_chance": 0.70, "events": ["scene",   "directions"]},
    "borrow":      {"patience": (8, 12),  "scene_chance": 0.10, "events": ["borrow",  "register"]},
    "overdue":     {"patience": (5,  9),  "scene_chance": 0.25, "events": ["fine",    "return_book"]},
    "introvert":   {"patience": (12, 20), "scene_chance": 0.00, "events": ["borrow",  "quiet_help"]},
    "impatient":   {"patience": (2,  4),  "scene_chance": 0.80, "events": ["scene",   "directions", "fine"]},
    "regular":     {"patience": (8, 15),  "scene_chance": 0.05, "events": ["borrow",  "return_book", "register"]},
}

# Score awarded per resolved action
ACTION_SCORE = {
    "borrow":       15,
    "return_book":  20,
    "fine":         20,
    "directions":   10,
    "register":     15,
    "quiet_help":   10,
    "scene":        30,   # bonus for de-escalating a scene
}

# Customer name pool (extend freely)
FIRST_NAMES = [
    "Uncle Tan", "Aunty Siti", "Sarah", "Boy A", "Puan Rohani",
    "Mr Loh",    "Encik Farid", "Miss Wong", "Darren", "Priya",
    "Kevin",     "Mdm Noor",   "Thomas",    "Aisyah",  "Sam",
]

# ── Customer record schema (plain dict, no class needed for easy JSON export) ─
#
#   id            : int          unique per session
#   name          : str
#   personality   : str          key into PERSONALITY_CONFIG
#   pos           : [x, y]       grid position
#   patience      : int          minutes remaining before leaving
#   patience_max  : int          original patience value
#   status        : str          "waiting" | "being_served" | "resolved" | "left" | "scene"
#   events        : list[str]    possible actions for this customer
#   active_event  : str | None   the event currently awaiting resolution
#   borrow_record : dict | None  {"book_id": str, "due_day": int}  — set on borrow
#   fine_record   : dict | None  {"amount": float, "reason": str}  — set on fine
#   spawn_minute  : int          when they appeared (for Lum's performance formula)
#   resolve_minute: int | None   when they were resolved


# ── CustomerManager ───────────────────────────────────────────────────────────

class CustomerManager:
    """Central controller for all customer instances."""

    def __init__(self):
        self._customers: list[dict] = []
        self._next_id: int = 1
        self._action_log: list[dict] = []   # CREATE: player action log entries

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _new_customer(self, personality: str, pos: list, spawn_minute: int) -> dict:
        cfg = PERSONALITY_CONFIG[personality]
        patience = random.randint(*cfg["patience"])
        events   = cfg["events"][:]
        # Pick the first event as the active one (most urgent need)
        active   = random.choice(events)
        return {
            "id":             self._next_id,
            "name":           random.choice(FIRST_NAMES),
            "personality":    personality,
            "pos":            pos[:],
            "patience":       patience,
            "patience_max":   patience,
            "status":         "waiting",
            "events":         events,
            "active_event":   active,
            "borrow_record":  None,
            "fine_record":    None,
            "spawn_minute":   spawn_minute,
            "resolve_minute": None,
        }

    def _log(self, entry: dict):
        """CREATE: append to player action log."""
        self._action_log.append(entry)

    # ── Public API ────────────────────────────────────────────────────────────

    def spawn_customers(
        self,
        day: int,
        count: int,
        grid_w: int = 5,
        grid_h: int = 4,
        spawn_minute: int = 0,
        personalities: Optional[list] = None,
    ) -> list[dict]:
        """
        CREATE: Generate `count` new customer instances and add them to the pool.
        Returns the list of newly created customer dicts.

        personalities — optional list to force specific types, e.g. ["loud","borrow"]
                        If None, types are chosen randomly weighted by day number.
        """
        spawned = []
        available_types = list(PERSONALITY_CONFIG.keys())

        # Later days have more impatient / overdue customers (simple weight curve)
        weights = {
            "loud":      max(1, 3 - day // 2),
            "borrow":    3,
            "overdue":   min(5, 1 + day),
            "introvert": 2,
            "impatient": min(4, day),
            "regular":   3,
        }
        type_pool   = list(weights.keys())
        type_weight = [weights[t] for t in type_pool]

        for _ in range(count):
            if personalities:
                ptype = personalities[_ % len(personalities)]
            else:
                ptype = random.choices(type_pool, weights=type_weight, k=1)[0]

            # Random floor tile position (avoid shelves — caller can override)
            pos = [random.randint(0, grid_w - 1), random.randint(0, grid_h - 1)]

            cust = self._new_customer(ptype, pos, spawn_minute)
            self._next_id += 1
            self._customers.append(cust)
            spawned.append(cust)

        return spawned

    def tick_minute(self, current_minute: int) -> list[dict]:
        """
        UPDATE: Decrease patience by 1 for every waiting customer.
        Customers whose patience hits 0 → status = "left".
        Returns list of customers who just left this tick (for Bing Heng's events).
        """
        just_left = []
        for c in self._customers:
            if c["status"] not in ("waiting", "being_served"):
                continue
            c["patience"] -= 1
            if c["patience"] <= 0:
                c["status"] = "left"
                just_left.append(c)
                self._log({
                    "minute":  current_minute,
                    "event":   "customer_left",
                    "cust_id": c["id"],
                    "name":    c["name"],
                })
        return just_left

    def get_nearby(self, player_pos: list, radius: int = 1) -> Optional[dict]:
        """
        READ: Return the closest waiting customer within `radius` tiles.
        Returns None if nobody is nearby.
        """
        px, py = player_pos
        closest = None
        closest_dist = float("inf")
        for c in self._customers:
            if c["status"] not in ("waiting", "being_served"):
                continue
            cx, cy = c["pos"]
            dist = abs(cx - px) + abs(cy - py)   # Manhattan distance
            if dist <= radius and dist < closest_dist:
                closest_dist = dist
                closest = c
        return closest

    def resolve(self, customer_id: int, action: str, current_minute: int = 0, **kwargs) -> dict:
        """
        UPDATE: Resolve a customer's active event.

        action    — one of ACTION_SCORE keys, must match customer's active_event
        **kwargs  — extra data for record creation:
                      book_id (str), due_day (int)  → triggers borrow_record
                      fine_amount (float)           → triggers fine_record

        Returns dict:
            {
                "success":     bool,
                "message":     str,
                "score_delta": int,
                "customer":    dict,   # updated customer state
            }
        """
        cust = self.get_state(customer_id)
        if cust is None:
            return {"success": False, "message": "Customer not found.", "score_delta": 0, "customer": None}

        if cust["status"] == "left":
            return {"success": False, "message": f"{cust['name']} already left.", "score_delta": 0, "customer": cust}

        if cust["status"] == "resolved":
            return {"success": False, "message": f"{cust['name']} is already resolved.", "score_delta": 0, "customer": cust}

        if action not in cust["events"]:
            return {"success": False, "message": "This action doesn't apply to this customer.", "score_delta": 0, "customer": cust}

        # ── CREATE borrow record ──
        if action == "borrow":
            book_id  = kwargs.get("book_id", f"BOOK-{random.randint(100,999)}")
            due_day  = kwargs.get("due_day", 7)
            cust["borrow_record"] = {"book_id": book_id, "due_day": due_day}

        # ── CREATE fine record ──
        if action in ("fine", "overdue"):
            amount = kwargs.get("fine_amount", 2.00)
            cust["fine_record"] = {"amount": amount, "reason": action}

        score = ACTION_SCORE.get(action, 5)
        cust["status"]         = "resolved"
        cust["active_event"]   = None
        cust["resolve_minute"] = current_minute

        msg = _resolve_message(cust["name"], cust["personality"], action)
        self._log({
            "minute":      current_minute,
            "event":       "resolved",
            "cust_id":     cust["id"],
            "name":        cust["name"],
            "action":      action,
            "score_delta": score,
        })

        return {"success": True, "message": msg, "score_delta": score, "customer": cust}

    def inject_random_event(self, customer_id: int, event_name: str):
        """
        Hook for Bing Heng's random/weather event system.
        Adds a new event to an existing waiting customer.
        Example: a thunder event causes all 'loud' customers to make a scene.
        """
        cust = self.get_state(customer_id)
        if cust and cust["status"] == "waiting":
            if event_name not in cust["events"]:
                cust["events"].append(event_name)
            # Overwrite active event only if currently idle
            if cust["active_event"] is None:
                cust["active_event"] = event_name

    def make_scene(self, customer_id: int, current_minute: int = 0) -> dict:
        """
        UPDATE: Trigger a 'making a scene' event based on personality's scene_chance.
        Called automatically each tick by the game loop if desired,
        or manually triggered by Bing Heng's event system.
        Returns {"triggered": bool, "customer": dict}
        """
        cust = self.get_state(customer_id)
        if cust is None or cust["status"] != "waiting":
            return {"triggered": False, "customer": cust}

        chance = PERSONALITY_CONFIG[cust["personality"]]["scene_chance"]
        if random.random() < chance:
            cust["status"]       = "scene"
            cust["active_event"] = "scene"
            self._log({"minute": current_minute, "event": "scene_started", "cust_id": cust["id"]})
            return {"triggered": True, "customer": cust}

        return {"triggered": False, "customer": cust}

    # ── READ helpers ──────────────────────────────────────────────────────────

    def get_state(self, customer_id: int) -> Optional[dict]:
        """READ: Return the full state dict of one customer by id."""
        for c in self._customers:
            if c["id"] == customer_id:
                return c
        return None

    def get_active(self) -> list[dict]:
        """READ: All customers still in the library (not 'left' or 'resolved')."""
        return [c for c in self._customers if c["status"] in ("waiting", "being_served", "scene")]

    def get_all(self) -> list[dict]:
        """READ: Every customer this session (including left/resolved)."""
        return self._customers

    def get_action_log(self) -> list[dict]:
        """READ: Full player action log — useful for Lum's performance formula."""
        return self._action_log

    # ── Save / Load (for Amirul) ──────────────────────────────────────────────

    def export_state(self) -> dict:
        """Serialise everything to a plain dict (JSON-safe). Amirul calls this."""
        return {
            "next_id":    self._next_id,
            "customers":  self._customers,
            "action_log": self._action_log,
        }

    def import_state(self, data: dict):
        """Restore from a previously exported dict. Amirul calls this on load."""
        self._next_id    = data.get("next_id", 1)
        self._customers  = data.get("customers", [])
        self._action_log = data.get("action_log", [])


# ── Private helpers ───────────────────────────────────────────────────────────

def _resolve_message(name: str, personality: str, action: str) -> str:
    """Return a flavour message for the resolution screen."""
    msgs = {
        ("loud",      "directions"):  f"{name}: THANK YOU SO MUCH!! *storms off*",
        ("loud",      "scene"):       f"{name} calms down after your intervention. Phew.",
        ("borrow",    "borrow"):      f"{name}: Thank you! I'll return it on time.",
        ("overdue",   "fine"):        f"{name}: RM2.00... okay fine. *pays reluctantly*",
        ("overdue",   "return_book"): f"{name}: Sorry for the delay! Here's the book.",
        ("introvert", "quiet_help"):  f"{name} nods silently and walks away, satisfied.",
        ("impatient", "scene"):       f"{name}: Fine! FINE! *mutters and leaves*",
        ("regular",   "register"):    f"{name}: Great, I'm now a member!",
    }
    return msgs.get((personality, action), f"{name}: Thanks! *leaves satisfied*")