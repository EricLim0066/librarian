COMMAND_POOL = {
    "left" : "move to the left side",
    "right" : "move to the right side",
    "up" : "move foward",
    "down" : "move downward",
    "interact" : "interact to anything",
    "dine" : "eat dinner",
    "snack" : "eat snack",
    "help" : "call all the command",
    "?" : "show tutorial"
}
HUNGRY_TIPS_POOL = {
    "Full" : None,
    "Okay" : None,
    "Hungry" : "Attention, your state become hungry right now.",
    "Starving" : "Your state is starving right now, you need to replanish your hungry bar quickly !",
    "Collapsed" : "Your state is collapsed, you need to replenish your hungry bar as soon as possible !"
}
TUTORIAL_POOL = [

    ["~GAME GOALS~",
     "You are a librarian, you need to service as more customer as possible within 7 days",
     "Maintain your hunger bar to a good level to avoid decrease your movement speed",
     "Manage the library well to get high scores"],

    ["~MOVEMENT COMMANDS~", 
     "left/right/up/down — control the movement of the characters",
     "Cannot pass throught the area which are blocked and hit the wall"],
    
    ["~CUSTOMER INTERACTION~",
     "interact — interact with nearby customers(distance <=1 grid)",
     "Every customer has their own personality and stories",
     f"Earn your scores by dealing with customers, and there's a 30% chance you'll get snacks"],
    
    ["~DINE IN SYSTEM~",
     "dine — eat, replenishes a large amount of hunger(+75), you cannot move while eating",
     "snack — eat snack, replenish a small amount of hunger(+25), no waiting required",
     f"Player will enter \"Collapsed\" state while hunger down to 0"],
    
    ["CUSTOMER TYPE~",
     "new customers — randomise of personalities and events",
     f"repeat customers — there's a 20% chance of back to library, usually return books",
     "Customers with different personalites have different patience, please handle as soon as possible"],
]
