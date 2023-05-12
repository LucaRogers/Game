import pickle
import sys
import time
import os

def type_out_text(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)
    print()

playerName = input("What is your name?")
play_intro = input(f"{playerName}, would you like to hear the intro and instructions?(input. 'yes','no')")
if play_intro == "yes":
    type_out_text(f"Welcome {playerName} to this adventure. You will have to face your fears on today's journey.")
    type_out_text("You are a knight in a castle searching for his king's lost treasure.")
    type_out_text("The castle has been taken over by an evil sorcerer. You must successfully defeat him in order to acquire the treasure.")
    instructions = """\nINSTRUCTIONS
    To navigate the castle, simply type the direction of one of the available exits.
    (Ex. 'north, south, east, west')
    To pick an item, input 'get' and the name of the item.
    To use an item input 'use' and then the item name.
    To save input 'save' to load input 'load'.
    To quit input 'quit'.
    To see this message again input 'i'"""
    type_out_text(instructions)
    input("Are you ready to begin this epic quest?\n")
    time.sleep(2)
    type_out_text("I don't care if you are or not because you don't really have an option...Good luck!\n")
    time.sleep(1)

elif play_intro == "no":
    type_out_text("Good luck!")

os.system('clear')


class Room():
    def __init__(self, name, description, exits, items = []):
        self.name = name
        self.description = description
        self.exits = exits
        self.items = items

    def display(self):
        print(self.name)
        type_out_text(self.description)
        print("\nExits: ")
        for direction in self.exits:
            print(direction)
        if self.items:
            print("Items: ")
            for item in self.items:
                print(item)


class Game():
    def __init__(self):
        self.rooms = []
        self.current_room = None
        self.inventory = []
        self.instructions = """\nINSTRUCTIONS
To navigate the castle, simply type the direction of one of the available exits.
(Ex. 'north, south, east, west')
To pick an item, input 'get' and the name of the item.
To use an item input 'use' and then the item name.
To save input 'save' to load input 'load'.
To quit input 'quit'.
To see this message again input 'i'"""
        
    def add_room(self, room):
        self.rooms.append(room)
        
    def start(self):
        self.current_room = self.rooms[0]
        self.play()
        
    def play(self):
        while True:
            os.system('clear')
            self.current_room.display()
            command = input(f"\nWhat would you like to do?\n(Inventory:{self.inventory})\n")
            if command in self.current_room.exits:
                 for room in self.rooms:
                    if room.name == self.current_room.exits[command]:
                        self.current_room = room
                        break

            elif command == "talk" and self.current_room.name == "Library":
                type_out_text("You talk to a librarian who was hiding in the corner.")
                type_out_text("Hello, I am Kurg. I have been a librarian here for many years.\nI am an expert on potions. I was a good friend to the the great King Magnus.\nI was devastated when he was found dead. So much so that I investigated his death.\nI found some clues but I was never able to piece them together.\nIf you do figure out the solution though, you will be rewarded.\nThe clues are found in the Storeroom. There is a hidden trap door there.\nTo go inside it simply input 'trap door' while in the storeroom.\n")
            
            elif command == "i":
                type_out_text(self.instructions)

            
            elif command == "save":
                with open("save_game.pickle", "wb") as f:
                    pickle.dump((self.current_room, self.inventory), f)
                type_out_text("Game saved.")
                    
            elif command == "load":
                try:
                    with open("save_game.pickle", "rb") as f:
                        self.current_room, self.inventory = pickle.load(f)
                    type_out_text("Game loaded.")
                except FileNotFoundError:
                    type_out_text("No save file found.")
        
            elif command.startswith("get "):
                item_name = command[4:]
                
                if item_name in self.current_room.items:
                    self.inventory.append(item_name)
                    self.current_room.items.remove(item_name)
                    type_out_text(f"You have picked up {item_name}.")
                    
                else:
                    type_out_text(f"{item_name} is not in this room.")
                    
            elif command.startswith("use "):
                item_name = command[4:]
                
                if item_name == "key" and "key" in self.inventory and self.current_room.name == "Treasure Room":
                    type_out_text("Congratulations! You have unlocked the treasure chest and found the treasure!")
                    break

                elif item_name == "book" and "book" in self.inventory and self.current_room.name == "Library":
                    type_out_text("You read a page of the book. It talks about an ancient potion of invisibility.\n")
                    self.inventory.remove("book")
                    
                elif item_name == "food" and "food" in self.inventory and self.current_room.name == "Cellar":
                    type_out_text("You give an old man some food. He thanks you by giving you a gold coin.")
                    self.inventory.append("coin")
                    self.inventory.remove("food")
                    
                elif item_name == "coin" and "coin" in self.inventory and self.current_room.name == "Dungeon Cell":
                    type_out_text("You pay a man and he gives you a potion in return\n")
                    self.inventory.remove("coin")
                    self.inventory.append("potion")
                
                elif item_name == "sword" and "sword" in self.inventory and self.current_room.name == "Cellar":
                    type_out_text("The old man was your only chance...You lose.")
                    break

                elif item_name == "sword" and "sword" in self.inventory and self.current_room.name == "Dungeon Cell":
                    if "potion" in self.inventory:
                        type_out_text("You stab the cloaked figure. That was sad.")
                        self.inventory.remove("sword")
        
                    else:
                        type_out_text("You stab the cloaked figure. He was your only chance to win.")
                        self.inventory.remove("sword")
                        break
                
                elif item_name == "sword" and "sword" in self.inventory and self.current_room.name == "Sorcerers Room":
                    type_out_text("You attempt to stab the Sorcerer. He easily avoids it.\nHe uses a spell to kill you. You are dead.")
                    break
                
                elif item_name == "potion" and "potion" in self.inventory and self.current_room.name == "Sorcerers Room":
                    if "sword" in self.inventory:
                        type_out_text("The man who gave you the potion alerted the Sorcerer. The Sorcerer was expecting your arrival.\nHe kills you with a powerfull spell.\n")
                        break
                    else:
                        type_out_text("You use the potion. It gives you invisibility.\nThe Sorcerer is looking around for you.\nHe casts as spell that rebounds off a mirror.\nIt hits him right in the face...He is dead.\nYou pick up a key that falls out of his pocket.")
                        self.inventory.remove("potion")
                        self.inventory.append("key")

                elif item_name == "potion" and "potion" in self.inventory and self.current_room.name == "Dungeon Cell":
                    type_out_text("You use the potion. It startles the cloaked figure.\nOut of fear it turns around and slashes you with a sword.\nBetter luck next time.")
                    break
                
                elif item_name == "book" and "book" in self.inventory and self.current_room.name == "Sorcerers Room":
                    type_out_text("You try to act cool and ask the Sorcerer if he knows anything about the book of potions.\nHe starts on an endless lecture about the history of potions. You die of old age after 67 years of learning about potions...")

                elif item_name == "book" and "book" in self.inventory and self.current_room.name == "Treasure Room":
                    if "key" in self.inventory:
                        type_out_text("You set aside the treasure chest key and start throwing the book at the treasure lock repeatedly.\nAfter an epic attmept at throwing the book, it rebounds and hits you in the face...\nYou wake up in heaven to your ancestors telling how you could have just used the dang key and been rich.")
                        break
                    else:
                        type_out_text("The book seems like its working. There is a micrioscopic dent in the chest. You feel satisfied and take nap.\nA dog thinks that you are food an eats you in your sleep. Bye!")
                        break
                   
                    
                else:
                    type_out_text("You can't use that here.")
            else:
                type_out_text("Invalid command.")
                
room1 = Room("Entrance", "You are standing in front of a castle entrance.", {"north": "Foyer"})
room2 = Room("Foyer", "You are standing in a grand foyer.", {"north": "Library", "east": "Dining Room", "south": "Entrance", "west": "Oratory"})
room3 = Room("Library", "You are standing in a large library.", {"south": "Foyer"}, ["book"])
room4 = Room("Dining Room", "You are standing in a spacious dining room.", {"west": "Foyer", "south": "Kitchen"})
room5 = Room("Kitchen", "You are standing in a busy kitchen.", {"north": "Dining Room", "east": "Garden"}, ["food"])    
room6 = Room("Garden", "You are standing in a beautiful garden with colorful flowers.", {"east": "Fountain", "west": "Kitchen"})
room7 = Room("Fountain", "You are standing in front of a grand fountain.", {"west": "Garden", "north": "Bedroom"})
room8 = Room("Bedroom", "There is an empty bed that is neatly made.", {"north": "Lavatories", "south": "Fountain", "east": "Gaurdroom"})
room9 = Room("Lavatories", "Nothing but an odd smell.", {"south": "Bedroom"})
room10 = Room("Gaurdroom", "Full of armor and a shiny sword.", {"west": "Bedroom", "east": "Dungeon Entrance"}, ["sword"])
room11 = Room("Oratory", "A private chapel.", {"east": "Foyer", "north": "Storeroom", "south": "Cellar"})
room12 = Room("Storeroom", "A room full of empty shelves.", {"south": "Oratory"})
room13 = Room("Cellar", "Full of cobwebs and unused storage space. It smells like moldy cheese.\nWait a second...An old man asks for some food.", {"north": "Oratory"})
room14 = Room("Dungeon Entrance", "Small and steep stairs lead you down the dark dungeon.", {"west": "Gaurdroom", "east": "Dungeon Cell", })
room15 = Room("Dungeon Cell", "You are closed off by iron bars. But wait... It looks like somebody broke through.\nThere is a cloaked figure in the corner.", {"west": "Dungeon Entrance", "east":"Dungeon Hallway"})
room16 = Room("Torture Chamber", "A dead man lays in a corner. There is a basket of heads near a guillotine. They look fresh.\nThere is no turning back now", {"south": "Sorcerers Room"})
room17 = Room("Dungeon Hallway", "It is very tight and oddly quiet. It smells odd.", {"west": "Dungeon Cell", "east": "Torture Chamber"})
room18 = Room("Sorcerers Room", "There is a powerful Sorcerer ready to kill you. You must defend yourself.", {"south": "Treasure Room"})
room19 = Room("Treasure Room", "You have found the treasure room!", {}, ["treasure chest"])
room20 = Room("Trap Door", "There is a trap door on the foor you didn't see before", {"north": "Graveyard", "south": "Storeroom"}) 
room21 = Room("Graveyard", "There is some writing on a tombstone that you want to read.", {"south":"Trap Door"})
 
game = Game()
game.add_room(room1) 
game.add_room(room3)
game.add_room(room4)
game.add_room(room5) 
game.add_room(room7)
game.add_room(room8)
game.add_room(room9)
game.add_room(room10)
game.add_room(room11)
game.add_room(room12)
game.add_room(room13)
game.add_room(room14)
game.add_room(room15)
game.add_room(room16)
game.add_room(room17)
game.add_room(room18)
game.add_room(room19)
game.add_room(room20)
game.add_room(room21)

game.start()