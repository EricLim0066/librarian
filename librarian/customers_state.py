import random

from customers import PERSONALITY_CONFIG_POOL
from customers import NO_BOOK_INTENT_POOL
from customers import HAS_BOOK_INTENT_POOL
from customers import NAME_POOL

import json

class customers_state :

    def __init__(self, name, patience, personality,id,intent):
        self.name = name
        self.patience = patience
        self.personality = personality
        self.intent = intent
        self.id = id
        self.status = "waiting"
        self.pos = [0,0]
        self.has_book = False
        self.borrow_count = 0
        self.fine_record = 0
        self.due_day = 0

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
            "has_book" : self.has_book
        }
    
    @classmethod
    def from_dict (cls, data) :
        customer = cls(
        name=data["name"],
        patience=data["patience"],
        personality=data["personality"],
        id=data["id"],
        intent=data["intent"]
        )
        customer.pos = data["pos"]
        customer.due_day = data["due_day"]
        customer.fine_record = data["fine_record"]
        customer.borrow_count = data["borrow_count"]
        customer.has_book = data["has_book"]  
        return customer
        
    def tick_patience(self):
        self.patience -= 1

        if self.patience <= 0 :
            self.patience = 0
            self.status = "left"

class customers_management :

    def __init__(self):
        self.customers = []
        self.customers_next_id = 1

    def to_dict (self) :
        return {
            "customers": [customer.to_dict() for customer in self.customers],
            "customers_next_id": self.customers_next_id
        }
    
    @classmethod
    def from_dict(cls,data) :
        manage = cls()
        manage.customers_next_id = data["customers_next_id"]
        manage.customers = [customers_state.from_dict(c_data) for c_data in data["customers"]]  
        return manage

    def register_customer(self, customer):
        self.customers.append(customer)

    def tick_all (self) :
        for customer in self.customers:
            customer.tick_patience()
            
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

        new_customer = customers_state(random_name, patience, random_personality, self.customers_next_id, random_event)
        self.customers_next_id += 1

        new_customer.pos = pos
        self.register_customer(new_customer)
        return new_customer

    def event_borrow_book(self,customer) :
        customer.has_book = True
        customer.borrow_count += 1
        customer.due_day = random.randint(1,3)

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
            self.event_borrow_book(customer)

            score_delta = 1

        elif event_type == "fine" :
            self.event_fine_lost(customer)
            score_delta = 1       

        elif event_type == "lost_book":
            self.event_lost_book(customer)
            self.event_fine_lost(customer)
            score_delta = 1   

        elif event_type == "return_book" :
            if not customer.due_day < 0:
                self.event_return_book(customer)
            else :
                self.event_return_book(customer)
                self.event_fine_late(customer)    
            score_delta = 1 
            
        elif event_type == "directions":
            score_delta = 1

        elif event_type == "scene":
            score_delta = 1   
            
        elif event_type == "register":
            score_delta = 1

        elif event_type == "complaint":
            score_delta = 1   

        else :
            score_delta = 0    
        
        customer.status = "left" 

        message = None
        if random.random() < 0.3 :
            if player.snack < 10:
                player.snack += 1
                message = "You gotta 1 snack"
            else :
                message = "You are full holdings of snack"
                
            player.message_queue_up.append(message)       
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
                return chosen
                
        return self.spawn_random(pos)
        # the other 0.8 rate

if __name__ == "__main__" :
    from player_state import player_state

    manage = customers_management()
    player = player_state()

    c1 = manage.spawn_random(pos=[1,1])
    c1.has_book = True
    c1.due_day = 3

    c2 = manage.spawn_random(pos=[2,1])
    c2.has_book = True
    c2.due_day = 1

    c3 = manage.spawn_random(pos=[3,1])
    c3.has_book = True
    c3.due_day = -2

    count = {
    "count1" : {},
    "count2" : {},
    "count3" : {}
    }
    for i in range(100):
        result = manage.spawn_random([0,0])
        # print(f"{result.name}, {result.personality}, {result.patience}, {result.intent},{result.id}")
        count["count1"][result.intent] = count["count1"].get(result.intent, 0) + 1
        count["count2"][result.personality] = count["count2"].get(result.personality, 0) + 1
        count["count3"][result.name] = count["count3"].get(result.name,0) + 1
    print(count["count1"])
    print(count["count2"])
    print(count["count3"])  




