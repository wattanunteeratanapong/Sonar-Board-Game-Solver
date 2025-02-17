import copy


def print_format(board):
    if len(board) == 10 and len(board[0]) == 10:
        print("     " + "  ".join("ABCDEFGHIJ"))  
        for i, row in enumerate(board):
            print(f"{i+1:2}   {'  '.join(map(str, row))}")
    elif len(board) == 15 and len(board[0]) == 15:
        print("     " + "  ".join("ABCDEFGHIJKLMNO"))
        for i, row in enumerate(board):
            print(f"{i+1:2}   {'  '.join(map(str, row))}")


def get_drone_scans():
    global game_map
    if len(game_map) == 10 and len(game_map[0]) == 10:
        return {
            "drone1": (0, 5, 0, 5),
            "drone2": (0, 5, 5, 10),
            "drone3": (5, 10, 0, 5),
            "drone4": (5, 10, 5, 10)
        }
    elif len(game_map) == 15 and len(game_map[0]) == 15:
        return {
            "drone1": (0, 5, 0, 5),  
            "drone2": (0, 5, 5, 10),  
            "drone3": (0, 5, 10, 15),  
            "drone4": (5, 10, 0, 5),  
            "drone5": (5, 10, 5, 10),  
            "drone6": (5, 10, 10, 15),  
            "drone7": (10, 15, 0, 5),  
            "drone8": (10, 15, 5, 10),  
            "drone9": (10, 15, 10, 15)  
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
    global max_height, max_width

    new_positions = set()

    for y in range(len(opponent_spawns)):
        for x in range(len(opponent_spawns[y])):
            if opponent_spawns[y][x] == 1:
                cur_x, cur_y = x, y 
                
                valid = True
                for action in opponent_moves:
                    if action in ["w", "a", "s", "d"]:  
                        cur_x, cur_y = get_new_position_coordinate(cur_x, cur_y, action)
                        
                        if cur_x < 0 or cur_x >= max_width or cur_y < 0 or cur_y >= max_height or game_map[cur_y][cur_x] == 1:
                            valid = False
                            break
                    elif action[:6] in drone_zones:  
                        if action[6:] == "y":
                            y_start, y_end, x_start, x_end = drone_scans[action[:6]]
                            if not (y_start <= cur_y < y_end and x_start <= cur_x < x_end):
                                valid = False
                                break
                        if action[6:] == "n":
                            y_start, y_end, x_start, x_end = drone_scans[action[:6]]
                            if y_start <= cur_y < y_end and x_start <= cur_x < x_end:
                                valid = False
                                break
                    elif (action in points): 
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

            if (0 <= new_x < max_width and 0 <= new_y < max_height and game_map[new_y][new_x] == 0 and (new_x, new_y) not in visited):
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

def surface(sector_number):
    global opponent_positions, opponent_spawns, opponent_moves

    try:
        sector_number = int(sector_number)
    except ValueError:
        print("Invalid sector! Please enter a number (1, 2, 3, ...).")
        return

    sector_key = f"drone{sector_number}"
    if sector_key not in drone_scans:
        print("Invalid sector number! Please enter a valid sector.")
        return

    y_start, y_end, x_start, x_end = drone_scans[sector_key]

    for y in range(len(opponent_spawns)):
        for x in range(len(opponent_spawns[y])):
            if y_start <= y < y_end and x_start <= x < x_end and game_map[y][x] == 0 and opponent_positions[y][x] == 1:
                opponent_spawns[y][x] = 1  
                opponent_positions[y][x] = 1
            else:
                opponent_spawns[y][x] = 0
                opponent_positions[y][x] = 0

    opponent_moves.clear()  

    print(f"Opponent surfaced in sector {sector_number}! Possible locations updated.")

def torpedo(location, dammage):
    if dammage == 2:
        locate(location)
    elif dammage == 1:
        global opponent_positions

        col_num = ord(location[0].lower()) - 97  
        row_num = int(location[1:]) - 1  

        for y in range(len(opponent_positions)):
            for x in range(len(opponent_positions[y])):
                if (col_num - 1 <= x <= col_num + 1) and (row_num - 1 <= y <= row_num + 1) and game_map[y][x] == 0 and not (x == col_num and y == row_num) and opponent_positions[y][x] == 1:
                    opponent_spawns[y][x] = 1
                    opponent_positions[y][x] = 1
                else:
                    opponent_spawns[y][x] = 0
                    opponent_positions[y][x] = 0

        opponent_moves.clear()

def mine(location):
    global opponent_positions
    col_num = ord(location[0].lower()) - 97
    row_num = int(location[1]) - 1

    if not (0 <= row_num < len(game_map) and 0 <= col_num < len(game_map[0])):
        print("Invalid location! Out of bounds.")
        return

    if game_map[row_num][col_num] == 1:
        print("Invalid sea location! Please enter a land location.")
        return

    for y in range(len(opponent_positions)):
            for x in range(len(opponent_positions[y])):
                if (col_num - 1 <= x <= col_num + 1) and (row_num - 1 <= y <= row_num + 1) and game_map[y][x] == 0 and not (x == col_num and y == row_num) and opponent_positions[y][x] == 1:
                    opponent_spawns[y][x] = 1
                    opponent_positions[y][x] = 1
                elif x == col_num and y == row_num:
                    opponent_spawns[y][x] = 1
                    opponent_positions[y][x] = 1
                else:
                    opponent_spawns[y][x] = 0
                    opponent_positions[y][x] = 0

    opponent_moves.clear()

def locate(location):
    global opponent_positions, opponent_spawns, opponent_moves
    col_num = ord(location[0].lower()) - 97  
    row_num = int(location[1:]) - 1  

    if row_num < 0 or row_num >= max_height or col_num < 0 or col_num >= max_width:
        print("Invalid location! Out of bounds.")
        return

    if game_map[row_num][col_num] == 1:
        print("Invalid surface location! Please enter a sea location.")
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

#            # A  B  C  D  E  F  G  H  I  J  K  L  M  N  O
# game_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1
#             [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0],  # 2
#             [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],  # 3
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 4
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 5
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 6
#             [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],  # 7
#             [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 8
#             [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0],  # 9
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 10
#             [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 11
#             [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],  # 12
#             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # 13
#             [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],  # 14
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]  # 15

max_height, max_width = len(game_map), len(game_map[0])
if max_height == 10 and max_width == 10:
    drone_zones = ["drone1", "drone2", "drone3", "drone4"]
elif max_height == 15 and max_width == 15:
    drone_zones = ["drone1", "drone2", "drone3", "drone4", "drone5", "drone6", "drone7", "drone8", "drone9"]
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

drone_scans = get_drone_scans()
points = [chr(97 + j) + str(i + 1) for i in range(len(game_map)) for j in range(len(game_map[0]))]
col = [chr(97 + i) for i in range(len(game_map[0]))]
row = [i + 1 for i in range(len(game_map))]

while True:
    action = input("Enter opponent action (w/a/s/d/del/drone1(y/n)/drone2(y/n)/drone3(y/n)/drone4(y/n)/sonar(Coordinate)/silent/surface(1-9)/torpedo(Damage+Coordinate)/mine(Coordinate)/locate(Coordinate)): ").strip().lower()

    if action == "del":
        if opponent_moves:
            opponent_moves.pop()
            simulate_opponent_location()
            print(f"Current moves: {opponent_moves}")
        else:
            print("No moves to delete!")
    elif action in ["w", "a", "s", "d"]:
        opponent_moves.append(action)
        simulate_opponent_location()
        print(f"Current moves: {opponent_moves}")
    elif action[:6] in drone_zones:
        opponent_moves.append(action)
        simulate_opponent_location()
        print(f"Current moves: {opponent_moves}")
    elif action == "silent":
        opponent_moves.append(action)
        silent()
        print(f"Current moves: {opponent_moves}")
    elif action[:5] == "sonar":
        opponent_moves.append(action[5:])
        simulate_opponent_location()
        print(f"Current moves: {opponent_moves}")
    elif action[:7] == "surface":
        surface(action[7:])
        print(f"Current moves: {opponent_moves}")
    elif action[:7] == "torpedo":
        torpedo(action[8:], int(action[7]))
        print(f"Current moves: {opponent_moves}")
    elif action[:4] == "mine":
        mine(action[4:])
        print(f"Current moves: {opponent_moves}")
    elif action[:6] == "locate":
        locate(action[6:])
        print(f"Current moves: {opponent_moves}")
    else:
        print("Invalid Input!")
        continue


    print("\nOpponent Possible Current Locations")
    print_format(opponent_positions)
    print()
    print()
    print()
    print()
    print()


# drone1y    : Drone1y mean drone scan at section 1, and opponent is in that section
# drone1n    : Drone1n mean drone scan at section 1, and opponent is not in that section
# sonarE6    : Sonar and opponent give the location E6
# silent     : Opponent using silent to move away
# surface1   : Opponent surface at section 1
# torpedo2E6 : Torpedo hit 2 damage at location E6
# torpedo1E6 : Torpedo hit 1 damage at location E6
# mineE6     : Mine detonate at location E6 and hit
# locateE6   : Know opponent exact location at E6

