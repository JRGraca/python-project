from playsound import playsound
import random

#list items in game room

couch = {
    "name": "couch",
    "type": "furniture",
}

door_a = {
    "name": "door a",
    "type": "door",
}

key_a = {
    "name": "key for door a",
    "type": "key",
    "target": door_a,
}

vampire = {
    "name": "vampire",
    "type": "monster",
}

#list rooms

game_room = {
    "name": "game room",
    "type": "room",
}

bedroom_1 = {
    "name": "Bedroom 1",
    "type": "room",
}

bedroom_2 = {
    "name": "Bedroom 2",
    "type": "room",
}

living_room = {
    "name": "living room",
    "type": "room",
}

outside = {
  "name": "outside"
}

#list items in bedroom 1

mummy = {
    "name": "mummy",
    "type": "monster"
}

door_b = {
    "name": "door b",
    "type": "door"
}

door_c = {
    "name": "door c",
    "type": "door"
}

key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,
}

#list items for living room

dining_table = {
    "name": "dining table",
    "type": "furniture"
}

door_d = {
    "name": "door d",
    "type": "door"
}

#list items for bedroom 2

witch = {
    "name": "witch",
    "type": "monster"
}

zombie = {
    "name": "zombie",
    "type": "monster"
}

key_c = {
    "name": "Key for Door C",
    "type": "key",
    "target": door_c
}

key_d = {
    "name": "key for door d",
    "type": "key",
    "target": door_d
}

all_rooms = [game_room, bedroom_1, bedroom_2, living_room, outside]

all_doors = [door_a, door_b, door_c, door_d]

# define which items/rooms are related

object_relations = {
    "game room": [couch, vampire, door_a],
    "vampire": [key_a],
    "outside": [door_d],
    "door a": [game_room, bedroom_1],
    "Bedroom 1": [mummy, door_a, door_b, door_c],
    "door b": [bedroom_1, bedroom_2],
    "mummy": [key_b],
    "witch": [key_c],
    "zombie": [key_d],
    "door c": [bedroom_1, living_room],
    "Bedroom 2": [witch, zombie, door_b],
    "living room": [dining_table, door_c, door_d],
    "door d": [living_room, outside],
}

# define game state. Do not directly change this dict. 
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This 
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": outside
}

def print_inventory():
    for i in game_state["keys_collected"]:
        print(i['name'])

def linebreak():
    """
    Print a line break
    """
    print("\n\n")

def start_game():
    """
    Start the game
    """
    print("You wake up on a couch and find yourself in a strange house with no windows which you have never been to before. You don't remember why you are here and what had happened before. You feel some unknown danger is approaching and you must get out of the house, NOW!")
    play_room(game_state["current_room"])

def fight():
    if random.random() < 0.75:
        positive_result = "You win."
        return positive_result
    else:
        negative_result = "You are almost there, keep fighting."
        return negative_result

def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either 
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        print("Congrats! You escaped the room!")
    else:
        print("You are now in " + room["name"])
        intended_action = input("What would you like to do? Type 'explore', 'examine' or 'inventory'?").strip()
        if intended_action == "explore":
            explore_room(room)
            play_room(room)
        elif intended_action.startswith("examine") == True:
            if intended_action[7:].strip() == "":
                examine_item(input("What would you like to examine?").strip())
            else:
                examine_item(intended_action[7:].strip())
        elif intended_action == 'inventory':
            print_inventory()
            play_room(room)
        else:
            print("Not sure what you mean. Type 'explore', 'examine' or 'inventory'.")
            play_room(room)
        linebreak()

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You explore the room. This is " + room["name"] + ". You find " + ", ".join(items))

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room

def open_door_sound():
    """"
    Play a sound when a door is open
    """
    playsound('mixkit-scary-wooden-door-opening-190.wav')

def examine_item(item_name):
    """
    Examine an item which can be a door or monster.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been 
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None

    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You examine " + item_name + ". "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "You unlock it with a key you have."
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "It is locked but you don't have the key."
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    valid = False
                    while valid == False:
                        intended_fight = input("Would you like to fight with " + item["name"] + "? Enter 'yes' or 'no'.").strip()   
                        if intended_fight == "no":
                            print("Come on, be brave! Go for it!")   
                        else:
                            if intended_fight == "yes":
                                result_fight = fight()
                                print(result_fight)
                                if result_fight == "You are almost there, keep fighting.":
                                    continue 
                                else:
                                    valid = True
                                    item_found = object_relations[item["name"]].pop()
                                    game_state["keys_collected"].append(item_found)
                                    output += "You find " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break

    if(output is None):
        print("The item you requested is not found in the current room.")
    
    if(next_room and input("Do you want to go to the next room? Enter 'yes' or 'no'").strip() == 'yes'):
        open_door_sound()
        play_room(next_room)
    else:
        play_room(current_room)
game_state = INIT_GAME_STATE.copy()


start_game()