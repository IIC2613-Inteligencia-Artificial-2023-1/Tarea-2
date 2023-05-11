import random
import json

# Map's parameters
NUM_COLORS = 14
NUM_TUBES = 16
TUBE_CAPACITY = 6
RANDOM_MOVES = 2000
MAP_NAME = "new_map"

assert NUM_COLORS <= NUM_TUBES, "Make sure there's more tubes than colors available"

tubes = []

# We create the tubes with balls inside of them
for i in range(NUM_COLORS):
    tubes.append([i] * TUBE_CAPACITY)

# We create the empty tubes
for i in range(NUM_TUBES - NUM_COLORS):
    tubes.append([])

def random_move(tubes):

    '''
       Randomly performs a move across two tubes.

       Parameters:
            tubes (list(int)) : list containing each of the map's tubes.
    '''

    from_idx = random.choice([i for i in range(len(tubes)) if len(tubes[i]) > 0])
    to_idx = random.choice([i for i in range(len(tubes)) if len(tubes[i]) < TUBE_CAPACITY and i != from_idx])
    tubes[to_idx].append(tubes[from_idx].pop())
    return tubes

# Perform a RANDOM_MOVES ammount of random moves
for i in range(RANDOM_MOVES):
    tubes = random_move(tubes)

# We create the map's JSON file
map_json = {"num_tubes": NUM_TUBES, "tube_capacity": TUBE_CAPACITY, "tubes_layout": tubes}

# We write the newly created map into a JSON file
with open(f'maps/{MAP_NAME}.json', 'w') as outfile:
    json_string = json.dumps(map_json)
    outfile.write(json_string)
