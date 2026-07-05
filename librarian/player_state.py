from command_pool import COMMAND_POOL
from command_pool import HUNGRY_TIPS_POOL
from command_pool import TUTORIAL_POOL
import json

GRID_W = 5
GRID_H = 4
BLOCKED = [[0,0],[1,0],[2,0],[3,0],[4,0],[0,1],[4,1]]

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
        if self.hungry > 0 :
            self.hungry -= 1
        self.check_hungry_warning()    

    def eating (self, amount) :
        self.hungry += amount
        if self.hungry > 100 :
            self.hungry = 100 

    def move (self, direction) :
        new_x = self.pos[0]
        new_y = self.pos[1]
        message = None

        if self.dine_in:
            message = "You can't move, you're current dine in right now "
            self.add_message(message)
            return

        if direction == "up" :
            new_y -= 1        
        elif direction == "down" :
            new_y += 1
        elif direction == "right" :
            new_x += 1    
        elif direction == "left" :
            new_x -= 1    

        if new_x < 0 or new_x > 4 or new_y < 0 or new_y > 3 :
            message = "You hitted the wall"
            self.add_message(message)  

        elif [new_x, new_y] in BLOCKED :
            message = "The path is blocked, please bypass"
            self.add_message(message)

        else :
            self.pos[0] = new_x
            self.pos[1] = new_y

    def minus_score(self, amount):
        self.score_delta -= amount
        if self.score_delta <= 0 :
            self.score_delta = 0

    def start_dine_in (self, current_minute) :
        self.dine_in = True
        self.dine_in_end = current_minute + 2
        self.eating(75)

        message = f"Eating... cannot move for 2 minutes"
        self.add_message(message)

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
        if command in move_comp:
            self.move(command)

        elif command == system_comp[0]:
            customer = manage.get_nearby(self.pos)
            if customer is None :
                message = f"Sorry no customers nearby"
                self.add_message(message)
                return
            
            event_type = customer.intent
            self.score_delta += manage.resolve(customer, event_type, self)
            

        elif command == system_comp[1]:
            if self.dine_in == True :
                self.add_message("You're current eating now")
                return
            self.start_dine_in(2)

        elif command == system_comp[2]:
            self.eat_snack()

        elif command == system_comp[3]:
            for cmd, description in COMMAND_POOL.items():
                message = f"{cmd:<8} - {description}"
                self.add_message(message)
            return
        
        elif command == system_comp[4]:
            for tutorial in TUTORIAL_POOL : 
                for line in tutorial :
                    message = line
                    self.add_message(message)
                self.add_message("_" * 30)
                
        else :
            message ="This command isn't implemented yet"
            self.add_message(message)
            return
        
    def get_score(self):
        return self.score_delta
        
    def add_message (self, message) :
        if message is not None :
            self.message_queue_up.append(message)

    def flush_message(self) :
        message = self.message_queue_up
        self.message_queue_up = []
        return message



if __name__ == "__main__" :
    from customers_state import customers_management
    from customers_state import customers_state

    state = player_state(pos=[2,1])
    state.snack = 5
    state.score_delta = 10

    manage = customers_management()
    c = manage.spawn_random(pos=[1,1])
    c.has_book = True
    c.due_day = 2

    save_data = {
        "player" : state.to_dict(),
        "customer" : c.to_dict()
    }

    with open ("test_save.json","w") as f:
        json.dump(save_data,f , indent=2)

    print("file saved")

    
    with open("test_save.json", "r") as f:
        loaded_data = json.load(f)
    
    new_player = player_state.from_dict(loaded_data["player"])    
    new_customer = customers_state.from_dict(loaded_data["customer"])    # not c.from_dict
    
    print(f"before pos={state.pos}, snack={state.snack}, score={state.score_delta}")
    print(f"after pos={new_player.pos}, snack={new_player.snack}, score={new_player.score_delta}")
    print(f"before customer due_day={c.due_day}, has_book={c.has_book}")
    print(f"after customer due_day={new_customer.due_day}, has_book={new_customer.has_book}")

    print("Welcome to librarian Simulater Game!")
    print("Press '?' to show tutorial")
    print("Press 'help' to call all the command")
    while True:
        
        user_input = input("Please enter command: ")
        try:
            state.execute_command(user_input, manage)
            state.tick_hunger()
            manage.tick_all(state)

            for message in state.flush_message() :
                print(message)
        except ValueError as e:
            print(e)

        