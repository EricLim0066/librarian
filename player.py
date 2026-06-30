"""
player.py — Player state, hunger system, speed penalty & movement validation
Author  : Lim Jing Xiang (Player Interaction)
Project : Librarian Simulator

HOW TEAMMATES CALL THIS MODULE
────────────────────────────────────────────────────────────────────────────────
    from player import Player

    p = Player()

    # Move the player (returns result dict)
    result = p.move("north", grid_w=5, grid_h=4)
    print(result["success"], result["message"])

    # Tick hunger every in-game minute (call from game loop)
    p.tick_minute(current_minute=10)

    # Eat / dine mechanic
    p.eat(amount=30)
    p.dine_in(current_minute=10)

    # Read player state
    info = p.get_state()

    # Get current speed penalty for this minute (for Amirul's stamina / action cost)
    penalty = p.get_speed_penalty()   # returns float seconds of extra delay

DESIGN NOTES FOR TEAMMATES
────────────────────────────────────────────────────────────────────────────────
  • Amirul  → stamina: read p.state["stamina"] directly, or call
              p.apply_stamina_cost(n) to deduct from your system.
              save/load: p.export_state() / p.import_state(data)
  • Lum     → performance: p.get_action_log() for action history
  • Bing Heng → weather events that slow player:
              p.apply_speed_modifier(multiplier=1.5, duration_minutes=3)
"""

# ── Hunger tier config ────────────────────────────────────────────────────────
#
# hunger value    tier name    speed penalty (extra seconds per command)
# ──────────────  ──────────   ───────────────────────────────────────────
# 76 – 100        Full         0.0   (no penalty)
# 51 –  75        Okay         1.0
# 26 –  50        Hungry       3.0
#  1 –  25        Starving     6.0
#  0              Collapsed   10.0
#
HUNGER_TIERS = [
    {"name": "Full",      "min": 76, "max": 100, "penalty": 0.0},
    {"name": "Okay",      "min": 51, "max": 75,  "penalty": 1.0},
    {"name": "Hungry",    "min": 26, "max": 50,  "penalty": 3.0},
    {"name": "Starving",  "min":  1, "max": 25,  "penalty": 6.0},
    {"name": "Collapsed", "min":  0, "max":  0,  "penalty": 10.0},
]

# How many hunger points are lost per in-game minute
HUNGER_DECAY_PER_MINUTE = 1

# Direction → (dx, dy)
DIRECTION_VECTORS = {
    "north": (0, -1),
    "south": (0,  1),
    "east":  (1,  0),
    "west":  (-1, 0),
}


# ── Player ────────────────────────────────────────────────────────────────────

class Player:
    """Owns player position, hunger, dine state and movement validation."""

    def __init__(self, start_pos: list = None, grid_w: int = 5, grid_h: int = 4):
        self._grid_w = grid_w
        self._grid_h = grid_h
        self._action_log: list[dict] = []
        self._speed_modifiers: list[dict] = []  # for Bing Heng's weather effects

        # ── Core state dict (all teammates read from here) ────────────────────
        self.state: dict = {
            # position
            "pos":          list(start_pos) if start_pos else [2, 3],

            # hunger  0 = collapsed, 100 = full
            "hunger":       100,
            "hunger_tier":  "Full",

            # dine state  (affects hunger decay and movement)
            "is_dining":    False,
            "dine_end_minute": None,   # minute when dine-in finishes

            # stamina  — Amirul owns this, stored here for unified export
            "stamina":      100,

            # speed penalty in seconds (derived from hunger + modifiers)
            "speed_penalty": 0.0,

            # read-only summary for render()
            "status_line":  "Ready",
        }
        self._refresh_derived()

    # ── Internal ──────────────────────────────────────────────────────────────

    def _refresh_derived(self):
        """Recalculate hunger_tier, speed_penalty, status_line after any state change."""
        h = self.state["hunger"]

        tier = HUNGER_TIERS[-2]   # default: Starving (safest fallback)
        for t in HUNGER_TIERS:
            if t["min"] <= h <= t["max"]:
                tier = t
                break

        self.state["hunger_tier"] = tier["name"]

        # Base penalty from hunger
        base = tier["penalty"]

        # Add any active weather/event modifiers
        extra_mult = 1.0
        for mod in self._speed_modifiers:
            extra_mult *= mod["multiplier"]

        self.state["speed_penalty"] = round(base * extra_mult, 2)

        # Status line for display
        if self.state["is_dining"]:
            self.state["status_line"] = "Dining in…"
        elif h == 0:
            self.state["status_line"] = "⚠ Collapsed — eat something!"
        elif tier["name"] == "Starving":
            self.state["status_line"] = "⚠ Starving — find food!"
        elif tier["name"] == "Hungry":
            self.state["status_line"] = "Feeling hungry…"
        else:
            self.state["status_line"] = "Ready"

    def _log(self, entry: dict):
        self._action_log.append(entry)

    # ── Movement ──────────────────────────────────────────────────────────────

    def move(self, direction: str, grid_w: int = None, grid_h: int = None,
             current_minute: int = 0) -> dict:
        """
        UPDATE: Attempt to move the player one tile.

        Returns:
            {
                "success":        bool,
                "message":        str,
                "new_pos":        [x, y],
                "speed_penalty":  float,   # seconds to sleep before accepting next input
                "blocked_reason": str | None,
            }
        """
        gw = grid_w or self._grid_w
        gh = grid_h or self._grid_h

        direction = direction.lower().strip()
        if direction not in DIRECTION_VECTORS:
            return {
                "success": False,
                "message": f"Unknown direction '{direction}'.",
                "new_pos": self.state["pos"][:],
                "speed_penalty": 0.0,
                "blocked_reason": "invalid_direction",
            }

        # Cannot move while dining
        if self.state["is_dining"]:
            return {
                "success": False,
                "message": "You are dining in — finish your meal first.",
                "new_pos": self.state["pos"][:],
                "speed_penalty": 0.0,
                "blocked_reason": "dining",
            }

        # Cannot move if collapsed
        if self.state["hunger"] == 0:
            return {
                "success": False,
                "message": "You collapsed from hunger! Eat something immediately.",
                "new_pos": self.state["pos"][:],
                "speed_penalty": 10.0,
                "blocked_reason": "collapsed",
            }

        dx, dy = DIRECTION_VECTORS[direction]
        nx = self.state["pos"][0] + dx
        ny = self.state["pos"][1] + dy

        # Boundary check
        if nx < 0 or nx >= gw or ny < 0 or ny >= gh:
            return {
                "success": False,
                "message": f"Can't go {direction} — wall.",
                "new_pos": self.state["pos"][:],
                "speed_penalty": 0.0,
                "blocked_reason": "wall",
            }

        self.state["pos"] = [nx, ny]
        penalty = self.state["speed_penalty"]

        self._log({
            "minute":    current_minute,
            "action":    "move",
            "direction": direction,
            "new_pos":   [nx, ny],
        })

        return {
            "success": True,
            "message": f"Moved {direction}.",
            "new_pos": [nx, ny],
            "speed_penalty": penalty,
            "blocked_reason": None,
        }

    # ── Hunger system ─────────────────────────────────────────────────────────

    def tick_minute(self, current_minute: int = 0):
        """
        UPDATE: Called every in-game minute from the main game loop.
        Decays hunger, expires dine state, expires speed modifiers.
        """
        # Decay hunger (dine-in slows decay)
        decay = HUNGER_DECAY_PER_MINUTE // 2 if self.state["is_dining"] else HUNGER_DECAY_PER_MINUTE
        self.state["hunger"] = max(0, self.state["hunger"] - decay)

        # End dine-in if time is up
        if self.state["is_dining"] and self.state["dine_end_minute"] is not None:
            if current_minute >= self.state["dine_end_minute"]:
                self.state["is_dining"]        = False
                self.state["dine_end_minute"]  = None
                self._log({"minute": current_minute, "action": "dine_end"})

        # Expire speed modifiers
        self._speed_modifiers = [
            m for m in self._speed_modifiers
            if m.get("expire_minute") is None or m["expire_minute"] > current_minute
        ]

        self._refresh_derived()

    def eat(self, amount: int = 30, current_minute: int = 0) -> dict:
        """
        UPDATE: Quick eat (snack) — restores hunger by `amount`.
        Can be done anywhere.  Does not set is_dining.
        Returns {"hunger_after": int, "tier": str, "message": str}
        """
        before = self.state["hunger"]
        self.state["hunger"] = min(100, self.state["hunger"] + amount)
        self._refresh_derived()
        self._log({"minute": current_minute, "action": "eat", "amount": amount})
        return {
            "hunger_after": self.state["hunger"],
            "tier":         self.state["hunger_tier"],
            "message":      f"Ate something (+{amount} hunger). Feeling {self.state['hunger_tier']}.",
        }

    def dine_in(self, duration_minutes: int = 5, restore_amount: int = 60,
                current_minute: int = 0) -> dict:
        """
        UPDATE: Sit-down meal — locks movement for `duration_minutes`,
        restores `restore_amount` hunger at the end.
        Returns {"success": bool, "message": str, "end_minute": int}
        """
        if self.state["is_dining"]:
            return {"success": False, "message": "Already dining.", "end_minute": None}

        self.state["is_dining"]       = True
        self.state["dine_end_minute"] = current_minute + duration_minutes
        # Partial restore immediately so player sees feedback
        self.state["hunger"] = min(100, self.state["hunger"] + restore_amount)
        self._refresh_derived()
        self._log({"minute": current_minute, "action": "dine_in", "duration": duration_minutes})
        return {
            "success":    True,
            "message":    f"Dining in for {duration_minutes} min. Movement locked.",
            "end_minute": self.state["dine_end_minute"],
        }

    def dine_out(self, restore_amount: int = 40, current_minute: int = 0) -> dict:
        """
        UPDATE: Take-away meal (dine out) — no movement lock, less restore.
        """
        self.state["hunger"] = min(100, self.state["hunger"] + restore_amount)
        self._refresh_derived()
        self._log({"minute": current_minute, "action": "dine_out", "amount": restore_amount})
        return {
            "success": True,
            "message": f"Got takeaway (+{restore_amount} hunger). Feeling {self.state['hunger_tier']}.",
        }

    # ── Stamina bridge (Amirul fills this out) ────────────────────────────────

    def apply_stamina_cost(self, cost: int):
        """
        Amirul calls this to deduct stamina from his system into the unified state.
        Stored here so export_state() captures everything in one go.
        """
        self.state["stamina"] = max(0, self.state["stamina"] - cost)

    # ── Speed modifier (Bing Heng calls this for weather events) ─────────────

    def apply_speed_modifier(self, multiplier: float, duration_minutes: int,
                             current_minute: int = 0, reason: str = "event"):
        """
        Bing Heng calls this when a weather/random event should slow the player.
        multiplier > 1.0  →  slower.  e.g. 1.5 = 50% slower.
        Stacks multiplicatively with hunger penalty.
        """
        self._speed_modifiers.append({
            "reason":        reason,
            "multiplier":    multiplier,
            "expire_minute": current_minute + duration_minutes,
        })
        self._refresh_derived()

    # ── READ helpers ──────────────────────────────────────────────────────────

    def get_state(self) -> dict:
        """READ: Return the full player state dict (copy)."""
        return dict(self.state)

    def get_pos(self) -> list:
        """READ: Current [x, y] position."""
        return self.state["pos"][:]

    def get_speed_penalty(self) -> float:
        """READ: Current extra-delay in seconds before accepting next input."""
        return self.state["speed_penalty"]

    def get_hunger_display(self) -> str:
        """READ: e.g. 'Hunger: 42/100  [Hungry] +3.0s penalty'"""
        h = self.state["hunger"]
        tier = self.state["hunger_tier"]
        pen  = self.state["speed_penalty"]
        bar  = _hunger_bar(h)
        penalty_str = f"  +{pen:.1f}s" if pen > 0 else ""
        return f"Hunger: {bar} {h:3d}/100  [{tier}]{penalty_str}"

    def get_action_log(self) -> list[dict]:
        """READ: Full action log for Lum's performance formula."""
        return self._action_log

    # ── Save / Load (Amirul) ──────────────────────────────────────────────────

    def export_state(self) -> dict:
        return {
            "state":            self.state,
            "speed_modifiers":  self._speed_modifiers,
            "action_log":       self._action_log,
            "next_grid":        {"w": self._grid_w, "h": self._grid_h},
        }

    def import_state(self, data: dict):
        self.state             = data.get("state", self.state)
        self._speed_modifiers  = data.get("speed_modifiers", [])
        self._action_log       = data.get("action_log", [])
        grid = data.get("next_grid", {})
        self._grid_w = grid.get("w", self._grid_w)
        self._grid_h = grid.get("h", self._grid_h)
        self._refresh_derived()


# ── Private display helper ────────────────────────────────────────────────────

def _hunger_bar(value: int, width: int = 10) -> str:
    filled = round(value / 100 * width)
    return "[" + "█" * filled + "░" * (width - filled) + "]"