from itertools import zip_longest
from player_state import player_state
from customers_state import customers_management
from MapGenerator import LIBRARY, BARRIER, COUNTER, BOOKSHELF, WALKABLESPACE, ENTRANCE, BLANK, READINGAREA, STORAGEAREA, SUPPLYDROPOFF

GRID_H = len(LIBRARY)
GRID_W = len(LIBRARY[0])

def print_map(self):
        for r in range(GRID_H):
            row_str = ""
            for c in range(GRID_W):
                if [r, c] == self.pos: 
                    row_str += " @ "
                elif any([r, c] == cust.pos and cust.status == "waiting" for cust in manage.customers + manage.customers_reading):
                    row_str += " ^ "
                elif LIBRARY[r][c] == BARRIER:
                    row_str += " # "
                elif LIBRARY[r][c] == COUNTER:
                    row_str += " C "
                elif LIBRARY[r][c] == BOOKSHELF:
                    row_str += " B "
                elif LIBRARY[r][c] == WALKABLESPACE :
                    row_str += " . "
                elif LIBRARY[r][c] == ENTRANCE :
                    row_str += " $ "
                elif LIBRARY[r][c] == BLANK :
                    row_str += "   "
                elif LIBRARY[r][c] == READINGAREA :
                    row_str += " r "
                elif LIBRARY[r][c] == STORAGEAREA :
                    row_str += " S "
                elif LIBRARY[r][c] == SUPPLYDROPOFF :
                    row_str += " u "

            print(row_str)

def build_status_lines(player):
    return [
        f"Hunger: {player.stage} ({player.hungry})",
        f"Snack: {player.snack}",
        f"Score: {player.score_delta}",
        "-" * 20,
        "Log:",
        *player.message_log,
    ]

def render(player, manage):
    map_lines = build_map_lines(player, manage)
    status_lines = build_status_lines(player)
    for left, right in zip_longest(map_lines, status_lines, fillvalue=""):
        print(f"{left.ljust(24)} | {right}")

if __name__ == "__main__":
    state = player_state(pos=[10, 1])
    manage = customers_management()

    while True:
        render(state, manage)
        user_input = input("Please enter command: ")
        try:
            state.execute_command(user_input, manage)
        except ValueError as e:
            print(e)

        manage.spawn_returning_rate([10, 1])
        state.tick_hunger()
        state.tick_dine_in()
        manage.tick_all(state)
        manage.set_travelers(state)

        state.flush_message()
