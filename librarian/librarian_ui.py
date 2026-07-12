from itertools import zip_longest
from player_state import player_state
from customers_state import customers_management
from MapGenerator import LIBRARY, BARRIER, COUNTER, BOOKSHELF, WALKABLESPACE, ENTRANCE, BLANK, READINGAREA, STORAGEAREA, SUPPLYDROPOFF
from environment_system import WEATHER_CONFIG

import random
import os
import json

GRID_H = len(LIBRARY)
GRID_W = len(LIBRARY[0])

class game_clock:
    def __init__(self):
        self.current_day = 1
        self.total_days = 7
        self.current_time = 13 * 60
        self.end_time = 18 * 60
        self.minutes_per_action = 1

    def advance(self):
        self.current_time += self.minutes_per_action

    def is_day_over(self):
        return self.current_time >= self.end_time

    def format_time(self):
        h, m = divmod(self.current_time, 60)
        return f"{h:02d}:{m:02d}"

    def reset_time(self):
        self.current_time = 13 * 60

    def is_game_over(self):
        return self.current_day > self.total_days

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
            f"Weather: {manage.weather}",
            f"Waiting at counter: {len(waiting)} ({', '.join(c.name for c in waiting)})",
            f"Last input: {player.last_command}",
            "-" * 20,
            "Log:",
            * [m for m, t in player.message_log],
        ]

    def render(self, player, manage):
        map_lines = self.build_map(player, manage)
        status_lines = self.build_status_lines(player, manage)
        for left, right in zip_longest(map_lines, status_lines, fillvalue=""):
            print(f"{left.ljust(24)} | {right}")

    def random_spawn_rate(self, manage) :
        if manage.library_closed:
            return   
        base_rate = 0.4
        rate = base_rate * (WEATHER_CONFIG[manage.weather]["customer_rate"] + manage.customer_event_bonus)
        if random.random() < rate:
            if random.random() < rate:
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
                clock = game_clock()
                self.game_loop(state, manage, ui, clock)

            elif choice == "2":
                state, manage = self.load_game()
                ui = game_ui()
                clock = game_clock()
                self.game_loop(state, manage, ui, clock)

            elif choice == "3":

                break
            else:
                print("Invalid choice")

    def game_loop(self, state, manage, ui, clock):

        while True:
            os.system("cls" if os.name == "nt" else "clear")
            ui.render(state, manage)
            user_input = input("Enter an action (Input '?' or 'help' to view command list): ")
            state.clear_goodbye()
            try:
                state.execute_command(user_input, manage)
            except ValueError as e:
                print(e)

            clock.advance() 
            ui.random_spawn_rate()
            state.tick_hunger()
            state.tick_dine_in()
            manage.tick_all(state)
            manage.set_travelers(state)
            state.flush_message()

            if clock.is_day_over():
                manage.force_clear_customers(state)
                result = self.end_of_day_menu(state, manage)
                clock.current_day += 1

                if clock.is_game_over():
                    self.show_final_results(state, manage)
                    return

                if result == "quit":
                    return

                manage.library_closed = False
                manage.customer_event_bonus = 0
                manage.skip_day = False  

    def end_of_day_menu(self, state, manage):
        print("Day complete!")
        print("1. Continue to next day")
        print("2. Save and continue")
        print("3. Save and quit")
        print("4. Quit without saving")
        choice = input("Choose: ")

        if choice in ("2", "3"):
            self.save_game(state, manage)
            # function didn't finish

        if choice in ("3", "4"):
            return "quit"   
        return "continue"

    def show_final_results(self, player, manage):
        print("=" * 30)
        print("7 DAYS COMPLETE - GAME OVER")
        print("=" * 30)
        print(f"Final Score: {player.score_delta}")
        print(f"Members Registered: {manage.total_members}")

    def save_game(self, state, manage, filename="save.json"):

        save_data = {
            "player": state.to_dict(),
            "manage": manage.to_dict(),
        }
        with open(filename, "w") as f:
            json.dump(save_data, f, indent=2)

    def load_game(self, filename="save.json"):

        with open(filename, "r") as f:
            data = json.load(f)
        state = player_state.from_dict(data["player"])
        manage = customers_management.from_dict(data["manage"])
        return state, manage

if __name__ == "__main__":
    state = player_state(pos=[10, 1])
    manage = customers_management()
    ui = game_ui()
    clock = game_clock()
    menu_ui().main_menu()
