import csv
##name: omer atia
## ID: 206667958


# Global BST root
ownerRoot = None

########################
# 0) Read from CSV -> HOENN_DATA
########################


def read_hoenn_csv(filename):
    """
    Reads 'hoenn_pokedex.csv' and returns a list of dicts:
      [ { "ID": int, "Name": str, "Type": str, "HP": int,
          "Attack": int, "Can Evolve": "TRUE"/"FALSE" },
        ... ]
    """
    data_list = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')  # Use comma as the delimiter
        first_row = True
        for row in reader:
            # It's the header row (like ID,Name,Type,HP,Attack,Can Evolve), skip it
            if first_row:
                first_row = False
                continue

            # row => [ID, Name, Type, HP, Attack, Can Evolve]
            if not row or not row[0].strip():
                break  # Empty or invalid row => stop
            d = {
                "ID": int(row[0]),
                "Name": str(row[1]),
                "Type": str(row[2]),
                "HP": int(row[3]),
                "Attack": int(row[4]),
                "Can Evolve": str(row[5]).upper()
            }
            data_list.append(d)
    return data_list


HOENN_DATA = read_hoenn_csv("hoenn_pokedex.csv")

########################
# 1) Helper Functions
########################

def read_int_safe(prompt):
    """
    Prompt the user for an integer, re-prompting on invalid input.
    """
    x = int(input())
    if x<0:
        print("Invalid choice.")
        return None
    return x

def get_poke_dict_by_id(poke_id):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by ID, or None if not found.
    """
    pass

def get_poke_dict_by_name(name):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by name, or None if not found.
    """
    pass

def display_pokemon_list(poke_list):
    """
    Display a list of Pokemon dicts, or a message if empty.
    """
    pass


########################
# 2) BST (By Owner Name)
########################

def create_owner_node(owner_name, first_pokemon=None):
    """
    Create and return a BST node dict with keys: 'owner', 'pokedex', 'left', 'right'.
    """
    new_owner = {'name':owner_name,'pokedex':[HOENN_DATA[first_pokemon]],'left':None,'right':None}
    return new_owner

def insert_owner_bst(root, new_node):
    if root == None:
        return new_node
    
    node_name = new_node['name'].lower()
    root_name = root['name'].lower()
    if root_name>node_name:
        root['left'] = insert_owner_bst(root['left'],new_node)    
    else:
        root['right'] = insert_owner_bst(root['right'],new_node)
    return root
    
    """
    Insert a new BST node by owner_name (alphabetically). Return updated root.
    """

def find_owner_bst(root, owner_name):
    if root is None:
        return None
    owner_name = owner_name.lower()
    curr_name = root['name'].lower()

    if owner_name == curr_name:
        return root
    elif owner_name>curr_name:
        return find_owner_bst(root['right'],owner_name)
    else:
        return find_owner_bst(root['left'],owner_name)


def min_node(node):
    current = node
    while current and current['left'] is not None:
        current = current['left']
    return current

def delete_owner_bst(root, owner_name):
    if root is None:
        return None
    
    owner_name_lower = owner_name.lower()
    root_name_lower = root['name'].lower()

    if owner_name_lower < root_name_lower:
        root['left'] = delete_owner_bst(root['left'], owner_name)
    elif owner_name_lower > root_name_lower:
        root['right'] = delete_owner_bst(root['right'], owner_name)
    else:
        #node has no children (leaf node)
        if root['left'] is None and root['right'] is None:
            return None

        #one children
        if root['left'] is None:
            return root['right']
        if root['right'] is None:
            return root['left']

        # node has two children
        # get minimum node in the right subtree
        successor = min_node(root['right'])
        root['name'] = successor['name']
        root['pokedex'] = successor['pokedex']
        # deleting the successor node from the right subtree
        root['right'] = delete_owner_bst(root['right'], successor['name'])

    return root

def delete_owner():
    global ownerRoot
    
    org_owner_name = input("Enter owner to delete: ").lower()
    owner_name = org_owner_name.lower()
    owner_to_delete = find_owner_bst(ownerRoot, owner_name)
    if owner_to_delete is None:
        print(f"Owner '{owner_name}' not found.")
        return

    print(f"Deleting {org_owner_name}'s entire Pokedex...")
    ownerRoot = delete_owner_bst(ownerRoot, owner_name)
    print("Pokedex deleted.")

def new_pokedex():
    global ownerRoot
    name_input = str(input("Owner name: "))
    exist_owner = find_owner_bst(ownerRoot,name_input)
    if exist_owner is not None:
        print(f"Owner '{name_input}' already exists. No new Pokedex created.\n")
        return
    print("Choose your starter Pokemon:")
    print("1) Treecko\n2) Torchic\n3) Mudkip")
    starter_index = int(input())
    if starter_index>3:
        print("Invalid. No new Pokedex created.\n")
        return
    starter_index = (starter_index-1)*3
    new_owner_node = create_owner_node(name_input,starter_index)
    ownerRoot = insert_owner_bst(ownerRoot,new_owner_node)

    starter_pokemon = HOENN_DATA[starter_index]
    print(f"New Pokedex created for {new_owner_node['name']} with starter:{starter_pokemon['Name']}\n")
    
########################
# 3) BST Traversals
########################

def bfs_traversal(root):

    #using queue 
    bfs_queue = [root]

    while bfs_queue:
        current_owner = bfs_queue.pop()
        print(f"Owner: {current_owner['name']}")
        print_pokemon_list(current_owner['pokedex'])

        if current_owner['left'] is not None:
            bfs_queue.append(current_owner['left'])
        if current_owner['right'] is not None:
            bfs_queue.append(current_owner['right'])

def pre_order(root):
    if root is None:
        return
    
    print(f"Owner: {root['name']}")
    print_pokemon_list(root['pokedex'])

    pre_order(root['left'])
    pre_order(root['right'])

    
def in_order(root):

    if root is None:
        return
    
    pre_order(root['left'])
    
    print(f"Owner: {root['name']}")
    print_pokemon_list(root['pokedex'])

    pre_order(root['right'])


def post_order(root):
    if root is None:
        return
    
    pre_order(root['left'])

    pre_order(root['right'])
    
    print(f"Owner: {root['name']}")
    print_pokemon_list(root['pokedex'])

 


########################
# 4) Pokedex Operations
########################

def add_pokemon_to_owner(owner_node):
    new_pokemon_index = int(input("Enter Pokemon ID to add: "))
    if new_pokemon_index<0 or new_pokemon_index>135:
        print(f"ID {new_pokemon_index} not found in Honen data.")
        return
    new_pokemon_data = HOENN_DATA[new_pokemon_index-1]
    for pokemon in owner_node['pokedex']:
        if pokemon['ID'] == new_pokemon_data['ID']:
            print("Pokemon already in the list. No changes made.")
            return
    owner_node['pokedex'].append(new_pokemon_data)
    print(f"Pokemon {new_pokemon_data['Name']} (ID {new_pokemon_data['ID']}) added to {owner_node['name']}'s Pokedex.")
    return

    """
    Prompt user for a Pokemon ID, find the data, and add to this owner's pokedex if not duplicate.
    """
    pass

def release_pokemon_by_name(owner_node):
    pokemon_name = str(input("Enter Pokemon Name to release: "))
    pokemon_name = pokemon_name.lower()

    for pokemon in owner_node['pokedex']:
        if pokemon['Name'].lower() == pokemon_name:
            owner_node['pokedex'].remove(pokemon)
            print(f"Releasing {pokemon['Name']} from {owner_node['name']}.")
            return
    print(f"No Pokemon named '{pokemon_name}' in {owner_node['name']}'s Pokedex.")

def evolve_pokemon_by_name(owner_node):
    pokemon_name = str(input("Enter Pokemon Name to evolve: ")).lower()
    existing_pokemon = None
    for pokemon in owner_node['pokedex']:
        if pokemon['Name'].lower() == pokemon_name:
            existing_pokemon = pokemon
            break
    if existing_pokemon == None:
        print(f"No Pokemon named '{pokemon_name}' in {owner_node['name']}'s Pokedex.")
        return
    if existing_pokemon['Can Evolve'] == 'FALSE' :
        print(f"{existing_pokemon['Name']} cannot evolve.")
        return
    
    new_id = existing_pokemon['ID']+1
    evolved_pokemon_data = HOENN_DATA[new_id-1]
    duplicate = None
    for pokemon in owner_node['pokedex']:
        if pokemon['ID'] == new_id:
            duplicate = pokemon
            break


    if duplicate:
        print(f"Pokemon evolved from {existing_pokemon['Name']} (ID {existing_pokemon['ID']}) to {evolved_pokemon_data['Name']} (ID {new_id}).")
        print(f"{evolved_pokemon_data['Name']} was already present; releasing {existing_pokemon['Name']} immediately.")
        owner_node['pokedex'].remove(existing_pokemon)
        return
    
    print(f"Pokemon evolved from {existing_pokemon['Name']} (ID {existing_pokemon['ID']}) to {evolved_pokemon_data['Name']} (ID {new_id}).")
    owner_node['pokedex'].remove(existing_pokemon)
    owner_node['pokedex'].append(evolved_pokemon_data)
    

    """
    Evolve a Pokemon by name:
    1) Check if it can evolve
    2) Remove old
    3) Insert new
    4) If new is a duplicate, remove it immediately
    """
    pass


########################
# 5) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, arr):
    if root is None:
        return
    gather_all_owners(root['left'],arr)
    gather_all_owners(root['right'],arr)
    arr.append(root)


def sort_owners_by_num_pokemon():
    if ownerRoot is None:
        print("No owners at all.")
        return
    
    owners_arr=[]
    gather_all_owners(ownerRoot,owners_arr)

    num_of_owners = len(owners_arr)
    for i in range(num_of_owners):
        for j in range(0,num_of_owners-1-i):
            if len(owners_arr[j]['pokedex'])> (len(owners_arr[j+1]['pokedex'])):
                owners_arr[j],owners_arr[j+1] = owners_arr[j+1],owners_arr[j]
            elif (len(owners_arr[j])== len(owners_arr[j+1])) and owners_arr[j]['name'].lower() > owners_arr[j + 1]['name'].lower():
                owners_arr[j],owners_arr[j+1] = owners_arr[j+1],owners_arr[j]


    print("=== The Owners we have, sorted by number of Pokemons ===")
    for owner in owners_arr:
        pokemon_num = len(owner['pokedex'])
        print(f"Owner: {owner['name']} (has {pokemon_num} Pokemon)")





    """
    Gather owners, sort them by (#pokedex size, then alpha), print results.
    """
    pass


########################
# 6) Print All
########################

def print_all_owners():
    print("1) BFS")
    print("2) Pre-Order")
    print("3) In-Order")
    print("4) Post-Order")

    user_input = int(input("Your choice: \n"))
    if user_input == 1:
        bfs_traversal(ownerRoot)
    elif user_input == 2:
        pre_order(ownerRoot)
    elif user_input == 3:
        in_order(ownerRoot)
    elif user_input == 4:
        post_order(ownerRoot)
    else:
        print("Invalid choice.")

def pre_order_print(node):
    """
    Helper to print data in pre-order.
    """
    pass

def in_order_print(node):
    """
    Helper to print data in in-order.
    """
    pass

def post_order_print(node):
    """
    Helper to print data in post-order.
    """
    pass


########################
# 7) The Display Filter Sub-Menu
########################

def display_filter_sub_menu(owner_node):
    """
    1) Only type X
    2) Only evolvable
    3) Only Attack above
    4) Only HP above
    5) Only name starts with
    6) All
    7) Back
    """
    pass


########################
# 8) Sub-menu & Main menu
########################
def print_pokemon_list(plist):
    if plist == None:
        print("There are no Pokemons in this Pokedex that match the criteria.")
    else:
        for p in plist:
            print(f"ID: {p['ID']}, Name: {p['Name']}, Type: {p['Type']}, HP: {p['HP']}, "
                  f"Attack: {p['Attack']}, Can Evolve: {p['Can Evolve']}")


def display_pokedex(owner_node):
    display_menu_on = True
    while display_menu_on:
        print("\n-- Display Filter Menu --")
        print("1. Only a certain Type")
        print("2. Only Evolvable")
        print("3. Only Attack above __")
        print("4. Only HP above __")
        print("5. Only names starting with letter(s)")
        print("6. All of them!")
        print("7. Back")
        user_input = int(input("Your choice: "))
        if user_input<0 or user_input>7:
            print("Invalid choice.\n")
        if user_input == 1:
            type_input = str(input("Which Type? (e.g. GRASS, WATER): "))
            type_input = type_input.lower()
            by_type = [pokemon for pokemon in owner_node['pokedex'] if pokemon['Type'].lower() == type_input]
            print_pokemon_list(by_type)
        if user_input == 2:
            evolvable = [pokemon for pokemon in owner_node['pokedex'] if pokemon['Can Evolve'] == 'TRUE']
            print_pokemon_list(evolvable)
        if user_input == 3:
            attack_threshold = int(input("Enter Attack threshold: "))
            attack_list = [pokemon for pokemon in owner_node['pokedex'] if pokemon['Attack']>attack_threshold]
            print_pokemon_list(attack_list)
        if user_input == 4:
            hp_thershold = int(input("Enter HP threshold: "))
            hp_list = [pokemon for pokemon in owner_node['pokedex'] if pokemon['HP'] > hp_thershold]
            print_pokemon_list(hp_list)
        if user_input == 5:
            starting_letters = str(input("Starting letter(s): "))
            starting_letters = starting_letters.lower()
            letters_len = len(starting_letters)
            if letters_len == 0:
                print_pokemon_list(owner_node['pokedex'])
                continue
            starting_list = [pokemon for pokemon in owner_node['pokedex'] if starting_letters == pokemon['Name'][:letters_len].lower()]
            print_pokemon_list(starting_list)
        if user_input == 6:
            print_pokemon_list(owner_node['pokedex'])
        if user_input == 7:
            print("Back to Pokedex Menu.")
            display_menu_on = False
        






    return

def existing_pokedex():
    owner_name = str(input("Owner name: "))
    owner_node = find_owner_bst(ownerRoot,owner_name)
    if owner_node is None:
        print(f"Owner '{owner_name} not found.")
        return
    menu_on = True
    while menu_on:
        print(f"\n-- {owner_node['name']}'s Pokedex Menu --")
        print("1. Add Pokemon")
        print("2. Display Pokedex")
        print("3. Release Pokemon")
        print("4. Evolve Pokemon")
        print("5. Back to Main")
        user_input = int(input("Your choice: "))
        if user_input<0 or user_input>5:
            print("Invalid choice.")
        if user_input == 1:
            add_pokemon_to_owner(owner_node)
        elif user_input == 2:
            display_pokedex(owner_node)
        elif user_input == 3:
            release_pokemon_by_name(owner_node)
        elif user_input == 4:
            evolve_pokemon_by_name(owner_node)
        else:
            menu_on = False
        

    




def print_main_menu():
    print("=== Main Menu ===")
    print("1. New Pokedex")
    print("2. Existing Pokedex")
    print("3. Delete a Pokedex")
    print("4. Display owners by number of Pokemon")
    print("5. Print All")
    print("6. Exit")

def main_menu():
    game_on= True
    while game_on:
        print_main_menu()
        user_input = int(input("Your choice: "))
        while user_input<0 or user_input>6:
            print("Invalid choice.\n")
            print_main_menu()
            user_input = int(input("Your choice: "))
        if user_input == 1:
            new_pokedex()
        elif user_input == 2:
            existing_pokedex()
        elif user_input == 3:
            delete_owner()
        elif user_input == 4:
            sort_owners_by_num_pokemon()
        elif user_input == 5:
            print_all_owners()
        else:
            print("Goodbye!")
            return

    

def main():
    """
    Entry point: calls main_menu().
    """
    main_menu()
    pass

if __name__ == "__main__":
    main()
