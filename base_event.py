import random
from typing import Dict, Any, Optional

class BaseEvent:
    name: str = "Random Event"                                # Event Name
    description: str = ""                                     # info about the event (show to group members)
    happen_rate: float = 0.5                                  # rate of event happen
    trigger_days: list = list(range(1, 8))                    # set time duration (7 days)

    def __init__(self, game_context: Dict[str, Any] = None):
        # receive and storing progress information about the main thread
        
        self.context = game_context if game_context else {}

    def condition(self, current_day: int, current_minute: int) -> bool:
        # check does have any conditions that can trigger this

        return current_day in self.trigger_days

    def execute(self) -> Optional[Dict[str, Any]]:
        # what thing to do while event happend

        raise NotImplementedError(f"{self.__class__.__name__} inplement execute()")

    def try_trigger(self, current_day: int, current_minute: int) -> Optional[Dict[str, Any]]:
        # ask main thread call the current thread

        if not self.condition(current_day, current_minute):
            return None
        if random.random() > self.happen_rate:
            return None
        return self.execute()