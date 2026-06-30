"""
integration_demo.py — Shows how customer.py + player.py plug into library_demo.py
Run:  python integration_demo.py

This file is NOT the full game — it's a wiring example for teammates.
"""

import time
import os
from customer import CustomerManager
from player   import Player

# ── Setup ──────────────────────────────────────────────────────────────────────
GRID_W, GRID_H = 5, 4
GRID = [
    ["S", "S", "S", "S", "S"],
    ["S", ".", ".", ".", "S"],
    [".", ".", "D", ".", "."],
    [".", ".", ".", ".", "."],
]

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def time_str(minute):
    total = 9 * 60 + minute
    return f"{total // 60:02d}:{total % 60:02d}"

# ── Render ────────────────────────────────────────────────────────────────────
def render(player: Player, mgr: CustomerManager, day: int, minute: int):
    clear()
    ps  = player.get_state()
    px, py = ps["pos"]
    active = mgr.get_active()

    print("╔══════════════════════════════════════════════════╗")
    print(f"║  LIBRARIAN SIMULATOR   Day {day}/7   {time_str(minute)}          ║")
    print("╠══════════════════════════════════════════════════╣")

    # Build map
    map_lines = []
    for y in range(GRID_H):
        row = ""
        for x in range(GRID_W):
            if [x, y] == [px, py]:
                row += "@ "
            elif any(c["pos"] == [x, y] for c in active):
                row += "! "
            else:
                row += GRID[y][x] + " "
        map_lines.append(row.rstrip())

    stats = [
        f"  Stamina : {ps['stamina']}%",
        f"  {player.get_hunger_display()}",
        f"  Status  : {ps['status_line']}",
        f"  Waiting : {len(active)} customer(s)",
        "",
        "  Legend:",
        "  @ = you    S = shelf",
        "  D = desk   ! = customer",
    ]

    print("║  MAP                          STATUS              ║")
    for i, row in enumerate(map_lines):
        stat = stats[i] if i < len(stats) else ""
        print(f"║  {row:<16}       {stat:<30}║")

    print("╠══════════════════════════════════════════════════╣")

    # Show nearby customer hint
    nearby = mgr.get_nearby(ps["pos"])
    if nearby:
        print(f"║  ⚠  {nearby['name']} [{nearby['personality']}] patience={nearby['patience']}  →  type 'interact'  ║")
    else:
        print("║  Commands: north south east west  interact  eat  help  quit  ║")

    print("╚══════════════════════════════════════════════════╝")

# ── Main Loop ─────────────────────────────────────────────────────────────────
def main():
    day    = 1
    minute = 0

    player = Player(start_pos=[2, 3], grid_w=GRID_W, grid_h=GRID_H)
    mgr    = CustomerManager()

    # Spawn 4 customers for day 1
    mgr.spawn_customers(day=day, count=4, grid_w=GRID_W, grid_h=GRID_H, spawn_minute=0)

    render(player, mgr, day, minute)
    print("\n  Day 1 opens — customers are waiting.\n")

    MOVE_MAP = {
        "north": "north", "south": "south", "east": "east", "west": "west",
        "n": "north",     "s": "south",     "e": "east",    "w": "west",
    }

    while True:
        # ── Speed penalty: sleep before reading input ──────────────────────
        penalty = player.get_speed_penalty()
        if penalty > 0:
            time.sleep(penalty)

        try:
            raw = input("\n  librarian@library:~$ ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break

        if raw == "quit":
            print("\n  Goodbye!\n")
            break

        # ── Movement ───────────────────────────────────────────────────────
        elif raw in MOVE_MAP:
            result = player.move(MOVE_MAP[raw], current_minute=minute)
            minute += 1

            # tick both systems
            player.tick_minute(current_minute=minute)
            left = mgr.tick_minute(current_minute=minute)

            render(player, mgr, day, minute)

            if not result["success"]:
                print(f"\n  > {result['message']}")
            else:
                nearby = mgr.get_nearby(player.get_pos())
                if nearby:
                    print(f"\n  > ⚠  {nearby['name']} ({nearby['personality']}) is nearby! Type 'interact'.")

            if left:
                for c in left:
                    print(f"\n  > {c['name']} ran out of patience and left! (-patience)")

        # ── Interact ───────────────────────────────────────────────────────
        elif raw == "interact":
            ps = player.get_state()
            nearby = mgr.get_nearby(ps["pos"])
            if not nearby:
                render(player, mgr, day, minute)
                print("\n  > No one nearby.")
            else:
                # Resolve the customer's active event
                action = nearby["active_event"] or nearby["events"][0]
                result = mgr.resolve(nearby["id"], action=action, current_minute=minute)
                minute += 2
                player.tick_minute(current_minute=minute)
                mgr.tick_minute(current_minute=minute)

                render(player, mgr, day, minute)
                print(f"\n  > {result['message']}")
                print(f"  > +{result['score_delta']} points")

        # ── Eat ────────────────────────────────────────────────────────────
        elif raw == "eat":
            result = player.eat(amount=25, current_minute=minute)
            render(player, mgr, day, minute)
            print(f"\n  > {result['message']}")

        # ── Dine in ────────────────────────────────────────────────────────
        elif raw == "dine in":
            result = player.dine_in(duration_minutes=5, restore_amount=60, current_minute=minute)
            render(player, mgr, day, minute)
            print(f"\n  > {result['message']}")

        # ── Help ───────────────────────────────────────────────────────────
        elif raw in ("help", "?"):
            render(player, mgr, day, minute)
            print("\n  ┌─ Commands ───────────────────────────────┐")
            print("  │ north / south / east / west              │")
            print("  │ interact  — help nearby customer         │")
            print("  │ eat       — quick snack (+25 hunger)     │")
            print("  │ dine in   — sit meal (+60, locks 5 min)  │")
            print("  │ help / ?  — this list                    │")
            print("  │ quit      — exit                         │")
            print("  └──────────────────────────────────────────┘")

        else:
            render(player, mgr, day, minute)
            print("\n  > Invalid command. Type 'help' or '?' to show command list.")


if __name__ == "__main__":
    main()