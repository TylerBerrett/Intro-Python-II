from room import Room
from player import Player
from item import Item

# Declare all the rooms

room = {
    'outside': Room("Outside Cave Entrance",
                    "North of you, the cave mount beckons"),

    'foyer': Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow': Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
}

# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#
room['treasure'].items.append(Item("Card", "Grave Titan"))


def get_item(item_name, item_list):
    for index, find_item in enumerate(item_list):
        return index if find_item.name.lower() == item_name.lower() else None


# Make a new player object that is currently in the 'outside' room.
name = input("What is your name?: ")
player = Player(name, room['outside'])
default = f"I don't like the name {name} so I am going to call you bud"
print(default if name.lower() != "bud" else "That is a good name")
while True:
    room_to_go = None
    user_input = input("What do you want to do bud: ")
    if user_input in ['n', 'e', 's', 'w']:
        if user_input == 'n':
            room_to_go = player.current_room.n_to
        elif user_input == 'e':
            room_to_go = player.current_room.e_to
        elif user_input == 's':
            room_to_go = player.current_room.s_to
        elif user_input == 'w':
            room_to_go = player.current_room.w_to
        if room_to_go is not None:
            player.current_room = room_to_go
            print(player.current_room)
        else:
            print("No room that way bud")

    elif user_input == "search":
        if len(player.current_room.items) > 0:
            plural = "these items" if len(player.current_room.items) > 1 else "this item"
            print(f"Hey bud, the {player.current_room.name} contains {plural}")
            for item in player.current_room.items:
                print(item.name)
        else:
            print("Nothing in the room")

    elif len(user_input.split()) == 2:
        command = user_input.split()[0].lower()
        search_item = user_input.split()[1].lower()
        room_items = player.current_room.items

        if (command == "get" or "take") and get_item(search_item, room_items) is not None:
            index = get_item(search_item, room_items)
            item_got = room_items[0]
            item_got.on_take()
            room_items.remove(item_got)
            player.items.append(item_got)

        if command == "drop" and get_item(search_item, player.items) is not None:
            index = get_item(search_item, player.items)
            item_got = player.items[index]
            item_got.on_drop()
            player.items.remove(item_got)
            room_items.append(item_got)

    elif user_input == 'i':
        if len(player.items) == 1:
            print("This is your only item bud")
            print(player.items[0])
        elif len(player.items) > 1:
            print("These are your items bud")
            for player_item in player.items:
                print(player_item)
        else:
            print("You have no items bud")

    elif user_input == 'q':
        break

    else:
        print("What ever you did is wrong bud")

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.
