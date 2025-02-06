import copy


def print_format(board):
    print("     " + "  ".join("ABCDEFGHIJ"))  
    for i, row in enumerate(board):
        print(f"{i+1:2}   {'  '.join(map(str, row))}")


def get_drone_scans(map_height, map_width):
    mid_height = map_height // 2
    mid_width = map_width // 2
    return {
        "drone1": (0, mid_height, 0, mid_width),  
        "drone2": (0, mid_height, mid_width, map_width),  
        "drone3": (mid_height, map_height, 0, mid_width),  
        "drone4": (mid_height, map_height, mid_width, map_width)  
    }


def get_new_position_coordinate(x, y, direction):
    if direction == "w":
        return x, y - 1
    elif direction == "s":
        return x, y + 1
    elif direction == "a":
        return x - 1, y
    elif direction == "d":
        return x + 1, y
    return x, y

def simulate_opponent_location():
    global opponent_positions

    new_positions = set()

    for y in range(len(opponent_spawns)):
        for x in range(len(opponent_spawns[y])):
            if opponent_spawns[y][x] == 1:
                cur_x, cur_y = x, y 
                
                valid = True
                for action in opponent_moves:
                    if action in ["w", "a", "s", "d"]:  
                        cur_x, cur_y = get_new_position_coordinate(cur_x, cur_y, action)
                        
                        if cur_x < 0 or cur_x >= 10 or cur_y < 0 or cur_y >= 10 or game_map[cur_y][cur_x] == 1:
                            valid = False
                            break
                    elif action in ["drone1", "drone2", "drone3", "drone4"]:  
                        y_start, y_end, x_start, x_end = drone_scans[action]
                        if not (y_start <= cur_y < y_end and x_start <= cur_x < x_end):
                            valid = False
                            break
                    elif action in points: 
                        col_num = ord(action[0].lower()) - 97
                        row_num = int(action[1]) - 1
                        if cur_x != col_num and cur_y != row_num:
                            valid = False
                            break

                if valid:
                    new_positions.add((cur_x, cur_y))  
    
    opponent_positions = [[0 for _ in range(len(opponent_spawns[0]))] for _ in range(len(opponent_spawns))]
    for x, y in new_positions:
        opponent_positions[y][x] = 1

def silent():
    global opponent_positions, opponent_spawns, opponent_moves

    silent_length = 4  
    new_positions = set()

    def dfs(x, y, steps_remaining, visited):
        if steps_remaining == 0:
            new_positions.add((x, y))
            return

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  
            new_x, new_y = x + dx, y + dy

            if (0 <= new_x < 10 and 0 <= new_y < 10 and 
                game_map[new_y][new_x] == 0 and (new_x, new_y) not in visited):
                
                dfs(new_x, new_y, steps_remaining - 1, visited | {(new_x, new_y)})  

    for y in range(len(opponent_positions)):
        for x in range(len(opponent_positions[y])):
            if opponent_positions[y][x] == 1:
                dfs(x, y, silent_length, {(x, y)})  

    if new_positions:
        opponent_positions = [[0 for _ in range(len(opponent_spawns[0]))] for _ in range(len(opponent_spawns))]
        opponent_spawns = [[0 for _ in range(len(opponent_spawns[0]))] for _ in range(len(opponent_spawns))]

        for x, y in new_positions:
            opponent_positions[y][x] = 1
            opponent_spawns[y][x] = 1  

    opponent_moves.clear()

def surface(location):
    global opponent_positions, opponent_spawns, opponent_moves

    col_num = ord(location[0].lower()) - 97
    row_num = int(location[1]) - 1

    if game_map[row_num][col_num] == 1:
        print("Invalid surface location! Please enter sea location.")
        return

    for y in range(len(opponent_spawns)):
        for x in range(len(opponent_spawns[y])):
            if x == col_num and y == row_num:
                opponent_spawns[y][x] = 1
                opponent_positions[y][x] = 1
            else:
                opponent_spawns[y][x] = 0
                opponent_positions[y][x] = 0

    opponent_moves.clear()





# Game Map
# 10x10 board
# 0 is for sea
# 1 is for land
           # A  B  C  D  E  F  G  H  I  J
game_map = [[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # 1
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # 2
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 3
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],  # 4
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 5
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 6
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],  # 7
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 8
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # 9
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]  # 10
print()
print()
print()
print()
print("\nMap")
print_format(game_map)
print()



# Opponent possible spawn points
# 0 is for impossible area
# 1 is for possible area
opponent_spawns = [[1 if cell == 0 else 0 for cell in row] for row in game_map]

print("Opponent Spawns")
print_format(opponent_spawns)
print()
print()
print()
print()
print()





# Game Loop
opponent_moves = []
opponent_positions = copy.deepcopy(opponent_spawns)

drone_scans = get_drone_scans(len(game_map), len(game_map[0]))
points = [chr(97 + j) + str(i + 1) for i in range(len(game_map)) for j in range(len(game_map[0]))]

while True:
    action = input("Enter opponent action (w/a/s/d/delete/drone1/drone2/drone3/drone4/sonar(A3,E6)/silent/surface(surfaceE6)): ").strip().lower()

    if action == "delete":
        if opponent_moves:
            opponent_moves.pop()
            print(f"Current moves: {opponent_moves}")
        else:
            print("No moves to delete!")
    elif action in ["w", "a", "s", "d"]:
        opponent_moves.append(action)
        print(f"Current moves: {opponent_moves}")
    elif action in ["drone1", "drone2", "drone3", "drone4"]:
        opponent_moves.append(action)
        print(f"Current moves: {opponent_moves}")
    elif action == "silent":
        opponent_moves.append(action)
        silent()
        print(f"Current moves: {opponent_moves}")
    elif action in points:
        opponent_moves.append(action)
    elif action[:7] == "surface":
        surface(action[7:])
        print(f"Current moves: {opponent_moves}")
    else:
        print("Invalid input! Please enter a valid action.")
        continue

    simulate_opponent_location()

    print("\nOpponent Possible Current Locations")
    print_format(opponent_positions)
    print()
    print()
    print()
    print()
    print()
