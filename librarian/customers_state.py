import random

from customers import PERSONALITY_CONFIG_POOL
from customers import NO_BOOK_INTENT_POOL
from customers import HAS_BOOK_INTENT_POOL
from customers import NAME_POOL
from customers import DIALOGUE_POOL
from customers import GOODBYE_POOL

from MapGenerator import LIBRARY, READINGAREA, BOOKSHELF

import json

QUEUE_POSITIONS = [(9,3), (8,3), (8,2), (8,1)]
BOOKSHELF_INTENTS = ("borrow","purchase")

class customers_state :

    def __init__(self, name, patience, personality,id,intent,decay):
        self.name = name
        self.patience = patience
        self.personality = personality
        self.intent = intent
        self.id = id

        self.status = "waiting"
        self.pos = [0,0]
        self.has_book = False
        # to make judgment does customer borrowing the book and haven't return the book yet 
        self.borrow_count = 0
        self.fine_record = 0
        self.due_day = 0
        self.is_member = False
        self.decay = decay
        self.tick_customer = 0
        self.reading = False

        self.travel_stage = 0
        # travel stage marking down customer moving location
        self.seat_pos = None
        self.customer_take_book_pos = None
        self.returning_book = False
        self.just_spawned = False

    def to_dict (self) :
        return {
            "pos" : self.pos,
            "due_day" : self.due_day,
            "fine_record" : self.fine_record,
            "borrow_count" : self.borrow_count,
            "id" : self.id,
            "name" : self.name,
            "patience" : self.patience,
            "personality" : self.personality,
            "intent" : self.intent,
            "has_book" : self.has_book,
            "is_member" : self.is_member,
            "decay" : self.decay,
            "reading" : self.reading
        }
    
    @classmethod
    def from_dict (cls, data) :
        customer = cls(
            name=data["name"],
            patience=data["patience"],
            personality=data["personality"],
            id=data["id"],
            intent=data["intent"],
            decay=data["decay"]
        )
        customer.pos = data["pos"]
        customer.due_day = data["due_day"]
        customer.fine_record = data["fine_record"]
        customer.borrow_count = data["borrow_count"]
        customer.has_book = data["has_book"]  
        customer.is_member = data["is_member"]
        customer.reading = data["reading"]
        return customer
    
    def tick_due_day(self):
        if self.has_book :
            self.due_day -= 1
        
    def tick_patience(self, player):
        self.tick_customer += 1
        if self.tick_customer >= self.decay :
            self.tick_customer = 0
            self.lose_patience(1, player)

    def lose_patience(self, amount, player) :
        self.patience -= amount

        if self.patience <= 0:
            self.patience = 0
            self.status = "left"
            if self.reading == False :
                player.minus_score(2)

class customers_management :

    def __init__(self):
        self.customers = []
        self.customers_reading = []
        self.seat = self.build_reading_area(READINGAREA)
        self.bookshelf = list(self.build_reading_area(BOOKSHELF).keys())
        self.customers_next_id = 1
        self.total_members = 0

    def to_dict (self) :
        return {
            "customers": [customer.to_dict() for customer in self.customers],
            "customers_reading": [customer.to_dict() for customer in self.customers_reading],
            "customers_next_id": self.customers_next_id,
            "total_members" : self.total_members
        }
    
    @classmethod
    def from_dict(cls,data) :
        manage = cls()
        manage.customers_next_id = data["customers_next_id"]
        manage.total_members = data["total_members"]
        manage.customers = [customers_state.from_dict(c_data) for c_data in data["customers"]] 
        manage.customers_reading = [customers_state.from_dict(c_data) for c_data in data["customers_reading"]] 
        return manage
    
    def queue_up_position (self) :
        active = []
        for c in self.customers :
            if c.status == "waiting" and not c.reading :
                active.append(c)

        for i, c in enumerate(active):
            # enumerate , take the index and their value directly
            if i < len(QUEUE_POSITIONS):
                c.pos = list(QUEUE_POSITIONS[i])

    def build_reading_area(self, tile_type):
        seats = {}
        for r in range(len(LIBRARY)):
            for c in range(len(LIBRARY[0])):
                
                if LIBRARY[r][c] == tile_type:
                    seats[(r, c)] = True
                    
        return seats
    
    def check_seat(self, customer):
        for seat, is_empty in self.seat.items() :
            if is_empty :
                self.seat[seat] = False
                customer.reading = True
                customer.pos = list(seat)
                return True
            # return true here mean customer found the seat
        return False
        # return false here mean seat is full, close it

    def register_customer(self, customer):
        if customer.intent in BOOKSHELF_INTENTS and random.random() < 0.6 and self.check_seat(customer) == True:
            customer.seat_pos = customer.pos
            self.customers_reading.append(customer)
            # check go reading

        elif customer.intent in BOOKSHELF_INTENTS :
            customer.seat_pos = None
            self.customers.append(customer)
            # no go to seat reading, go to counter after grab a book

        else:
            customer.seat_pos = None
            self.customers.append(customer)
            self.queue_up_position()
            # go to counter directly

    def set_travelers(self, player):
        for customer in self.customers + self.customers_reading:
            if customer.status != "waiting":
                continue
            
            if customer.just_spawned:
                customer.just_spawned = False
                player.add_message(f"{customer.name} entered the library")
                continue
            # freeze customer 1 time, let player know customer was came in

            go_bookshelf = customer.intent in BOOKSHELF_INTENTS or customer.reading
            # check customer's event and do their route
    
            if customer.travel_stage == 0 and go_bookshelf:
                customer.pos = list(random.choice(self.bookshelf))
                customer.customer_take_book_pos = customer.pos
                customer.travel_stage = 1
                player.add_message(f"{customer.name} went to grab a book")
                # for all customer borrow book or go to read book

            elif customer.travel_stage == 1 and customer.reading and customer.seat_pos:
                customer.pos = customer.seat_pos
                customer.travel_stage = 2
                player.add_message(f"{customer.name} went to find a seat")
                # for customer want to reading and they are current at bookshelf

            elif customer.travel_stage in (0, 1) and not customer.reading:
                self.queue_up_position()
                customer.travel_stage = 2
                player.add_message(f"{customer.name} went to the counter")
                # for normal customer but go to counter straight or current at book shelf
                # travel_stage set for check the current direction, 0 for spawn area, 1 for go to bookshelf grab book, 2 for go to counter


    def tick_counter_customers (self, player) :
        for customer in self.customers:
            if customer.status == "left" :
                continue
            # skip all the customers who already left 

            customer.tick_patience(player)
            if customer.status == "left" :
                player.add_message(f"{customer.name} left the library")
                self.queue_up_position()
                # catch the customers who just left 

                if customer.intent == "scene" :
                    player.add_message(f"({customer.name}'s outburst startled other customers, customers are left)")
                    for other in self.customers:
                        if other.status == "waiting" and other.id != customer.id:
                            other.lose_patience(1, player)

                            if other.status == "left":
                                player.add_message(f"{other.name} left the library")
                                self.queue_up_position()

                            # judge again, make sure have no single message of departure was missed or the queue was re-established a round later after scene event

                # catch the customers who just left and their event is "Scene"

    # catch customers who go to counter 
    
    def tick_reading_customers(self, player):
        for read in self.customers_reading:
            if read.status == "left":
                continue

            if read.patience == 1 and not read.returning_book:
                read.pos = read.customer_take_book_pos
                read.returning_book = True
                player.add_message(f"{read.name} is putting the book back")
                continue

            read.tick_patience(player)
            if read.status == "left":
                seat = tuple(read.seat_pos)
                if seat in self.seat:
                    self.seat[seat] = True
                player.add_message(f"{read.name} finished reading and left the library")

    # catch customers who go to reading

    def tick_all(self, player) :
        self.tick_reading_customers(player)
        self.tick_counter_customers(player)

    def tick_all_due_day (self) :
        for customer in self.customers :
            if customer.has_book :
                customer.tick_due_day()
            
    def get_nearby(self, player_pos):
        for customer in self.customers:
            px, py = player_pos
            cx, cy = customer.pos 
            distance = abs(px - cx) + abs(py - cy)
            if customer.status == "waiting" and distance <= 1:
                return customer
            
    def spawn_random (self, pos) :
        emoji = []
        weight = [] 
        intent_event = []
        event_weight = []
        for personality in PERSONALITY_CONFIG_POOL:
            # for key in dict:
            emoji.append(personality)
            weight.append(PERSONALITY_CONFIG_POOL[personality]["weight"])

        random_personality = random.choices(emoji, weights=weight, k=1)[0]    
        patience_range = PERSONALITY_CONFIG_POOL[random_personality]["patience"]

        patience = random.randint(patience_range[0],patience_range[1])
        random_name = random.choice(NAME_POOL)

        for intent in NO_BOOK_INTENT_POOL :
            intent_event.append(intent)
            event_weight.append(NO_BOOK_INTENT_POOL[intent]["weight"])

        random_event = random.choices(intent_event, weights=event_weight, k=1)[0]    

        scene_chance = PERSONALITY_CONFIG_POOL[random_personality]["scene_chance"]
        if random.random() < scene_chance:
            random_event = "scene"

        decay = PERSONALITY_CONFIG_POOL[random_personality]["decay"]
        new_customer = customers_state(random_name, patience, random_personality, self.customers_next_id, random_event,decay)
        self.customers_next_id += 1

        spawn_pos = list(pos)
        new_customer.pos = spawn_pos
        new_customer.just_spawned = True
        # record and freeze the customer spawn coordinate

        self.register_customer(new_customer)
        new_customer.pos = spawn_pos
        return new_customer
    
    def event_borrow_book(self,customer) :
        customer.has_book = True
        customer.borrow_count += 1
        customer.due_day = random.randint(1,3)

    def event_buy_book(self, customer) :
        pass
    
    def event_fine_late(self, customer):
        if customer.due_day < 0:
            customer.fine_record += abs(customer.due_day) * 10

    def event_fine_lost(self, customer):
        customer.fine_record += 10

    def event_lost_book (self,customer) :
        customer.has_book = False

    def event_return_book (self, customer) :
        customer.has_book = False    

    def resolve(self, customer, event_type, player):

        if event_type == "borrow" and customer.has_book == False:
            line = random.choice(DIALOGUE_POOL[customer.personality]["borrow"])
            message = f"{customer.name}: {line}"
            player.add_message(message)

            self.event_borrow_book(customer)
            player.add_message(f"(You helped {customer.name} borrow a book)")

            score_delta = 1

        elif event_type == "fine" :
            line = random.choice(DIALOGUE_POOL[customer.personality]["fine"])
            message = f"{customer.name}: {line}"
            player.add_message(message)

            self.event_fine_lost(customer)
            player.add_message(f"({customer.name} has paid the fine)")
            
            score_delta = 1  

        elif event_type == "lost_book":
            line = random.choice(DIALOGUE_POOL[customer.personality]["lost_book"])
            message = f"{customer.name}: {line}"
            player.add_message(message)

            self.event_lost_book(customer)
            self.event_fine_lost(customer)
            player.add_message(f"({customer.name} has paid the fine for losing books)")

            score_delta = 1   

        elif event_type == "return_book" :
            line = random.choice(DIALOGUE_POOL[customer.personality]["return_book"])
            message = f"{customer.name}: {line}"
            player.add_message(message)

            if not customer.due_day < 0:
                self.event_return_book(customer)
                player.add_message(f"({customer.name} has returned the books)")
            else :
                self.event_return_book(customer)
                self.event_fine_late(customer)    
                player.add_message(f"({customer.name} has paid the fine for late to return books)")

            score_delta = 1 
            
        elif event_type == "directions":
            line = random.choice(DIALOGUE_POOL[customer.personality]["directions"])
            message = f"{customer.name}: {line}"
            player.add_message(message)

            player.add_message(f"(You helped {customer.name} directions to the toilet)")
            score_delta = 1

        elif event_type == "scene":
            line = random.choice(DIALOGUE_POOL[customer.personality]["scene"])
            message = f"{customer.name}: {line}"
            player.add_message(message)

            player.add_message(f"(You appease {customer.name} their patiences)")
            score_delta = 1
            
        elif event_type == "register":
            line = random.choice(DIALOGUE_POOL[customer.personality]["register"])
            message = f"{customer.name}: {line}"
            player.add_message(message)

            customer.is_member = True
            self.total_members += 1
            if player.snack < 10:
                player.snack += 1
                player.add_message("Welcome gift: you gotta bonus 1 snack")
            
            player.add_message(f"(You helped {customer.name} register their members)")

            score_delta = 1

        elif event_type == "complaint":
            line = random.choice(DIALOGUE_POOL[customer.personality]["complaint"])
            message = f"{customer.name}: {line}"
            player.add_message(message)

            player.add_message(f"(You settled {customer.name}'s problem)")
            score_delta = 1   

        elif event_type == "purchase" :
            line = random.choice(DIALOGUE_POOL[customer.personality]["purchase"])
            message = f"{customer.name}: {line}"
            player.add_message(message)
            
            self.event_buy_book(customer)
            player.add_message(f"({customer.name} has bought the book)")
            score_delta = 1   

        else :
            score_delta = 0    
        
        goodbye = random.choice(GOODBYE_POOL[customer.personality])
        player.add_message(f"{customer.name}: {goodbye}")

        customer.status = "left" 
        player.add_message(f"{customer.name} has left")
        self.queue_up_position()

        message = None
        if random.random() < 0.3 :
            if player.snack < 10:
                player.snack += 1
                message = "You gotta 1 snack" 
            else :
                message = "Your snack pouch is already full (max 10)"
                
            player.add_message(message)       
        return score_delta
    
    def get_returning_pool (self) :
        pool = []
        weights = []
        for customer in self.customers :
            if customer.status == "left" and customer.has_book == True :
                pool.append(customer)

                if customer.due_day == 3:
                    due_day_weights = 10
                elif customer.due_day == 2:
                    due_day_weights = 40
                elif customer.due_day <= 1:
                    due_day_weights = 80
                else :
                    due_day_weights = 0.5    

                weights.append(due_day_weights)

        return pool, weights    

    def spawn_returning_rate (self, pos) :
        intent_event = []
        event_weight = []
        if random.random() < 0.2 :
            pool,weights = self.get_returning_pool()
            if pool != []: 
                for intent in HAS_BOOK_INTENT_POOL :
                    intent_event.append(intent)
                    event_weight.append(HAS_BOOK_INTENT_POOL[intent]["weight"])

                back_intent = random.choices(intent_event, weights=event_weight, k=1)[0] 

                chosen = random.choices(pool, weights=weights, k=1)[0]
                chosen.intent = back_intent 
                chosen.status = "waiting"
                chosen.pos = pos
                chosen.travel_stage = 0
                chosen.just_spawned = True
                return chosen
                
        return self.spawn_random(pos)
        # the other 0.8 rate


if __name__ == "__main__" :
    from player_state import player_state

    manage = customers_management()
    player = player_state(pos=[0,0])
    player.snack = 9
    player.score_delta = 2

    c1 = manage.spawn_random(pos=[1,1])
    c1.has_book = True
    c1.due_day = 3
    c1.intent = "register"

    c2 = manage.spawn_random(pos=[2,1])
    c2.has_book = True
    c2.due_day = 1
    c2.patience = 1

    c3 = manage.spawn_random(pos=[3,1])
    c3.has_book = True
    c3.due_day = -2

    def test1 () :
        count = {
        "count1" : {},
        "count2" : {},
        "count3" : {}
        }
        for i in range(1000):
            result = manage.spawn_random([0,0])
            # print(f"{result.name}, {result.personality}, {result.patience}, {result.intent},{result.id}")
            count["count1"][result.intent] = count["count1"].get(result.intent, 0) + 1
            count["count2"][result.personality] = count["count2"].get(result.personality, 0) + 1
            count["count3"][result.name] = count["count3"].get(result.name,0) + 1
        print(count["count1"])
        print(count["count2"])
        print(count["count3"])  

        print("==========================================================")

        print(f"before is_member={c1.is_member}, total_members={manage.total_members}, snack={player.snack}")

        score = manage.resolve(c1, "register", player)

        print(f"after is_member={c1.is_member}, total_members={manage.total_members}, snack={player.snack}, score_delta={score}")
        for msg in player.flush_message():
            print(msg)

        print("==========================================================")

        print(f"before customer_patience: {c2.patience}, customer_state: {c2.status}, score: {player.score_delta}")
        c2.tick_patience(player)
        print(f"before customer_patience: {c2.patience}, customer_state: {c2.status}, score: {player.score_delta}")

        print("==========================================================\n")

        random.seed(1)
        N = 10000

        print("=== every personality independent testing scene rate ===")
        print(f"{'personality':<10} {'Settings':<8} {'Accuary':<10} {'Times'}")

        for personality, config in PERSONALITY_CONFIG_POOL.items():
            scene_chance = config["scene_chance"]
            hit_count = 0

            for i in range(N):
                if random.random() < scene_chance:
                    hit_count += 1

            actual_rate = hit_count / N
            print(f"{personality:<10} {scene_chance:<8} {actual_rate:<10.4f} {hit_count}/{N}")
