from itertools import zip_longest
from player_state import player_state
from customers_state import customers_management
from MapGenerator import LIBRARY, BARRIER, COUNTER, BOOKSHELF, WALKABLESPACE, ENTRANCE, BLANK, READINGAREA, STORAGEAREA, SUPPLYDROPOFF

import random
import os

GRID_H = len(LIBRARY)
GRID_W = len(LIBRARY[0])

class game_ui :

    def build_map(self, player, manage):
            lines = []
            for r in range(GRID_H):
                row_str = ""
                for c in range(GRID_W):
                    if [r, c] == player.pos: 
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

                lines.append(row_str)
            return lines

    def build_status_lines(self, player, manage):
        waiting = [c for c in manage.customers if c.status == "waiting"]
        return [
            f"Hunger: {player.stage} ({player.hungry})",
            f"Snack: {player.snack}",
            f"Score: {player.score_delta}",
            f"Waiting at counter: {len(waiting)} ({', '.join(c.name for c in waiting)})",
            f"Last input: {player.last_command}",
            "-" * 20,
            "Log:",
            *player.message_log,
        ]

    def render(self, player, manage):
        map_lines = self.build_map(player, manage)
        status_lines = self.build_status_lines(player, manage)
        for left, right in zip_longest(map_lines, status_lines, fillvalue=""):
            print(f"{left.ljust(24)} | {right}")

    def random_spawn_rate(self) :
            if random.random() > 0.6 :
                if random.random() > 0.5 :
                    manage.spawn_returning_rate([10,1])
                else :
                    manage.spawn_returning_rate([10,2])

class menu_ui :
    def main_menu(self):
        while True:
            print("=" * 30)
            print("LIBRARIAN SIMULATOR")
            print("=" * 30)
            print("1. Start new game")
            print("2. Load save")
            print("3. Quit")
            choice = input("Choose: ")

            if choice == "1":

                state = player_state(pos=[10, 1])
                manage = customers_management()
                ui = game_ui()
                self.game_loop(state, manage, ui)
            elif choice == "2":

                state, manage = load_game()
                # function didn't finish
                self.game_loop(state, manage, ui)
            elif choice == "3":

                break
            else:
                print("Invalid choice")

    def game_loop(self, state, manage, ui):
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            ui.render(state, manage)
            user_input = input("Enter an action (Input '?' or 'help' to view command list): ")
            try:
                state.execute_command(user_input, manage)
            except ValueError as e:
                print(e)

            ui.random_spawn_rate()
            state.tick_hunger()
            state.tick_dine_in()
            manage.tick_all(state)
            manage.set_travelers(state)

            if day_end:
                # function didn't finish

                self.end_of_day_menu(state, manage)   

    def end_of_day_menu(self, state, manage):
        print("Day complete!")
        print("1. Continue to next day")
        print("2. Save and continue")
        print("3. Save and quit")
        print("4. Quit without saving")
        choice = input("Choose: ")

        if choice in ("2", "3"):
            save_game(state, manage)
            # function didn't finish

        if choice in ("3", "4"):
            return "quit"   
        return "continue"

if __name__ == "__main__":
    state = player_state(pos=[10, 1])
    manage = customers_management()
    ui = game_ui()

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        ui.render(state, manage)
        user_input = input("Enter an action (Input '?' or 'help' to view command list): ")
        try:
            state.execute_command(user_input, manage)
        except ValueError as e:
            print(e)

        ui.random_spawn_rate()
        state.tick_hunger()
        state.tick_dine_in()
        manage.tick_all(state)
        manage.set_travelers(state)
