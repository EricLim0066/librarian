from command_pool import COMMAND_POOL
from command_pool import HUNGRY_TIPS_POOL
from command_pool import TUTORIAL_POOL
import json

from MapGenerator import LIBRARY, BARRIER, COUNTER, BOOKSHELF, WALKABLESPACE, ENTRANCE, BLANK, READINGAREA, STORAGEAREA,SUPPLYDROPOFF

GRID_H = len(LIBRARY)       # 12 height
GRID_W = len(LIBRARY[0])    # 7 width

class player_state :

    def __init__(self, pos=None, snack=0) :
        self.pos = pos
        self.hungry = 100
        self.stage = "Full"
        self.warned = None
        self.snack = snack
        self.dine_in = False
        self.dine_in_end = None 
        self.message_queue_up = []
        self.score_delta = 0
        self.dine_in_remaining = 0
        self.dine_in_count = 0
        self.dine_in_limit = 3
        self.pretty = 3
        self.message_log = []
        self.last_command = None
 
    def to_dict (self) :
        return {
            "pos" : self.pos,
            "snack" : self.snack,
            "score_delta" : self.score_delta
        }
    
    @classmethod
    def from_dict (cls, data) :
        player = cls(pos=data["pos"], snack=data["snack"])
        player.score_delta = data["score_delta"]
        return player
        

    def get_hunger_tier (self) :

        if self.hungry >= 75 :
            self.stage = "Full"
        elif self.hungry >= 50 :
            self.stage = "Okay"
        elif self.hungry >= 25 :
            self.stage = "Hungry"
        elif self.hungry >= 1 :
            self.stage = "Starving"
        else :
            self.stage = "Collapsed"        

        return self.stage
    
    # get_hungry_tier change the state of hungry bar
    
    def check_hungry_warning (self) :
        message = None
        stage = self.get_hunger_tier()

        if stage in HUNGRY_TIPS_POOL and stage != self.warned  :
            self.warned = stage
            message = HUNGRY_TIPS_POOL.get(stage)
            self.add_message(message)

    # every move, will use the check_hungry_warning and return message out, so add a compress lock with variable stage and self.warned
    # example, "Full" != None is True, execute change self.warned's stage, then return message out which from pool,
    # else, "Full" != "Full" is False, no execute and return empty message out, that mean user will not see the tips again, also to let the tips only work 1 time
    
    def tick_hunger (self) :

        if self.dine_in == True :
            return
        
        elif self.hungry > 0 :
            self.hungry -= 1

            if self.get_hunger_tier() == "Hungry" :
                self.hungry -= 1

            elif self.get_hunger_tier() == "Starving" :
                self.hungry -= 2
        
        self.check_hungry_warning()    

    def eating (self, amount) :
        self.hungry += amount
        if self.hungry > 100 :
            self.hungry = 100 

    def move (self, direction) :
        new_row = self.pos[0]
        new_col = self.pos[1]
        message = None

        if self.dine_in:
            message = "You can't move, you're current dine in right now "
            self.add_message(message)
            return
        
        elif self.get_hunger_tier() == "Collapsed" :
            message = "Your hungry state is Collapsed, u can't move"
            self.add_message(message)
            return

        if direction == "up" :
            new_row -= 1        
        elif direction == "down" :
            new_row += 1
        elif direction == "right" :
            new_col += 1    
        elif direction == "left" :
            new_col -= 1    

        if new_row < 0 or new_row > GRID_H - 1 or new_col < 0 or new_col > GRID_W - 1 :
            # check out of index 

            message = "You hitted the wall"
            self.add_message(message)  

        elif LIBRARY[new_row][new_col] == BARRIER :
            message = "The path is blocked, please bypass"
            self.add_message(message)

        else :
            self.pos[0] = new_row
            self.pos[1] = new_col

    def minus_score(self, amount):
        self.score_delta -= amount
        if self.score_delta <= 0 :
            self.score_delta = 0

    def start_dine_in (self) :
        if self.dine_in_count >= self.dine_in_limit:
            self.add_message("You've reached today's dine-in limit, no more meals until tomorrow")
            return
        
        self.dine_in = True
        self.dine_in_remaining = 2
        self.dine_in_count += 1
        self.eating(75)

        message = f"Eating... cannot move for 2 times"
        self.add_message(message)


    def tick_dine_in (self) :
        extra_time = 0
        if self.dine_in :
            self.dine_in_remaining -= 1
            if self.dine_in_remaining <= 0 :
                self.finish_dine_in()
                extra_time += 30
        
        return extra_time

    def eat_snack(self):
        message = None
        if self.snack > 0 :
            self.eating(25)
            self.snack -= 1
            message = "You ate 1 snack, hungry bar +25"
        else :
            message = "Sorry the snack is finish"
            
        self.add_message(message)

    def finish_dine_in (self) :
        self.dine_in = False
        self.dine_in_end = None     

        message = f"You're finished counsume foods, current {self.hungry} now"
        self.add_message(message)

    def parse_command(self,user_input):
        normalize = user_input.casefold()
        if normalize in COMMAND_POOL:
            return normalize
        else :
            raise ValueError (f"Sorry command error, please try agian")


    def execute_command(self,command,manage) :
        move_comp = ["left","right","up","down"]
        system_comp =["interact","dine","snack",'help',"?"]
        message = None
        
        command = self.parse_command(command)
        self.last_command = command

        if command in move_comp:
            self.move(command)

        elif command == system_comp[0]:
            customer = manage.get_nearby(self.pos)
            if customer is None :
                message = f"Sorry no customers nearby"
                self.add_message(message)
                return
            
            elif customer.reading == True :
                message = f"Sorry cannot interact to customer which is reading and resting"
                self.add_message(message)
                return
            
            event_type = customer.intent
            self.score_delta += manage.resolve(customer, event_type, self)
            

        elif command == system_comp[1]:
            if self.dine_in == True :
                self.add_message("You're current eating now")
                return
            self.start_dine_in()

        elif command == system_comp[2]:
            self.eat_snack()

        elif command == system_comp[3]:
            for cmd, description in COMMAND_POOL.items():
                message = f"{cmd:<8} - {description}"
                print(message)
            print("_" * 30)
            input("\nPress Enter to continue...")
            return
        
        elif command == system_comp[4]:
            for tutorial in TUTORIAL_POOL : 
                for line in tutorial :
                    print(line)
                print("_" * 30)

            input("\nPress Enter to continue...")
            return
                
        else :
            message ="This command isn't implemented yet"
            self.add_message(message)
            return
        
    def get_score(self):
        return self.score_delta
        
    def add_message (self, message, tag=None) :
        if message is not None :
            self.message_queue_up.append(message)
            self.message_log.append((message, tag))
            self.message_log = self.message_log[-6:]

    def flush_message(self) :
        message = self.message_queue_up
        self.message_queue_up = []
        return message
    
    def clear_goodbye(self):
        self.message_log = [(m, t) for m, t in self.message_log if t != "goodbye"]

    def print_map(self, manage):
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



if __name__ == "__main__" :
    from customers_state import customers_management
    from customers_state import customers_state
    from librarian_ui import game_clock

    import random

    state = player_state(pos=[2,1])
    state.snack = 5
    state.score_delta = 10

    manage = customers_management()
    clock = game_clock()
    # c = manage.spawn_random(pos=[1,1])
    # d1 = manage.spawn_random(pos=[3,1])
    # f1 = manage.spawn_random(pos=[3,3])

    save_data = {
        "player" : state.to_dict(),
        "customer" : manage.to_dict()
    }

    with open ("test_save.json","w") as f:
        json.dump(save_data,f , indent=2)

    print("file saved")

    
    with open("test_save.json", "r") as f:
        loaded_data = json.load(f)
    
    new_player = player_state.from_dict(loaded_data["player"])    
    new_customer = customers_management.from_dict(loaded_data["customer"])    # not c.from_dict
    
    def test1 () :
        print(f"before pos={state.pos}, snack={state.snack}, score={state.score_delta}")
        print(f"after pos={new_player.pos}, snack={new_player.snack}, score={new_player.score_delta}")
        print(f"before customer due_day={manage.due_day}, has_book={manage.has_book}")
        print(f"after customer due_day={new_customer.due_day}, has_book={new_customer.has_book}")
    
    def test2() :
        print("=== testing seat ===")

        manage.seat = {(1,1): True, (2,1): True, (3,1): True}

        test_customers = []
        for i in range(5):
            c_test = manage.spawn_random(pos=[0,0])
            test_customers.append(c_test)

        print(f"\ncustomers(counter) people: {len(manage.customers)}")
        print(f"customers_reading(reading area) people: {len(manage.customers_reading)}")
        print(f"seat state: {manage.seat}")

        for c_test in test_customers:
            print(f"{c_test.name}(id={c_test.id}): reading={c_test.reading}, pos={c_test.pos}")

        print("\n=== test finished ===\n")

        print("Welcome to librarian Simulater Game!")
        print("Press '?' to show tutorial")
        print("Press 'help' to call all the command")
    
    def random_spawn_rate() :
        if random.random() > 0.6 :
            if random.random() > 0.5 :
                manage.spawn_returning_rate([10,1])
            else :
                manage.spawn_returning_rate([10,2])
        

    while True:
        
        state.print_map(manage)
        user_input = input("Please enter command: ")
        try:
            print(f"player hungry state= {state.stage}, player hungry bar = {state.hungry}")
            state.execute_command(user_input, manage)
        except ValueError as e:
            print(e)

        random_spawn_rate()
        state.tick_hunger()
        state.tick_dine_in()
        manage.tick_all(state)
        manage.set_travelers(state)
                
        for message in state.flush_message() :
            print(message)
        

