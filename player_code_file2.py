import time
import random
import sys
import copy
global grid
global cnt
global player_color
grid_size = 8

def read_file(player_color):
    with open("shared_file.txt") as f:
        lines = f.readlines()
    if len(lines) == 0:
        return None
    if lines[0].strip('\n') == str(player_color):
        temp_grid = []
        for line in lines[1:]:
            temp_grid.append(line.strip('\n').split(" ")[:-1])
        return temp_grid
    return None

def critical_mass(pos):
    if pos == (0,0) or pos == (grid_size - 1, grid_size - 1) or pos == (grid_size - 1, 0) or pos == (0, grid_size - 1):
        return 2
    elif pos[0] == 0 or pos[0] == grid_size -1 or pos[1] == 0 or pos[1] == grid_size-1:
        return 3
    else:
        return 4

def neighbors(pos):
    n = []
    for i in [(pos[0],pos[1]+1), (pos[0],pos[1]-1), (pos[0]+1,pos[1]), (pos[0]-1,pos[1])]:
        if 0 <= i[0] < grid_size and 0 <= i[1] < grid_size:
            n.append(i)
    return n

def select_move(grid, player_color, cnt):
    val = -999999
    found = 0
    dis = 99999
    if cnt<6:
        print("comes")
        ok = True
        for pos in [(x,y) for x in range(grid_size) for y in range(grid_size)]:
            if grid[pos[0]][pos[1]][0] != 'N':
                continue
            n = neighbors(pos)
            if len(n)<4:
                continue
            for i in n:
                if grid[i[0]][i[1]][0] != 'N':
                    ok = False
            print("comes2")
            if(ok):
                print("comes3")
                return (pos[0], pos[1])
            
    for pos in [(x,y) for x in range(grid_size) for y in range(grid_size)]:
        if grid[pos[0]][pos[1]][0]== 'N':
            if (min(pos[0],grid_size-pos[0]) + min(pos[1],grid_size-pos[1]))**2 <dis:
                dis = (min(pos[0],grid_size-pos[0]) + min(pos[1],grid_size-pos[1]))**2
                found = 1
                best = pos
      
    if found == 1 and cnt <25:
        return (best[0], best[1])
    print(cnt)
    for pos in [(x,y) for x in range(grid_size) for y in range(grid_size)]:
        if grid[pos[0]][pos[1]][0]== player_color  or grid[pos[0]][pos[1]][0]=='N':
            n= neighbors(pos)
            vl = 0
            for i in n:
                if grid[i[0]][i[1]][0]!= player_color and grid[i[0]][i[1]][0] !='N':
                    vl += int(grid[i[0]][i[1]][1]) * (7-(critical_mass(i)- int(grid[i[0]][i[1]][1])))**2
                    if grid[pos[0]][pos[1]][0] == player_color:
                        vl += int(grid[pos[0]][pos[1]][1])*(7-(critical_mass(pos)-int(grid[pos[0]][pos[1]][1])))**2
                    if(vl>val):
                        val = vl
                        best = pos
    print(val)
    return (best[0], best[1])
    '''
    while True:
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        if grid[x][y] == 'No' or grid[x][y][0] == player_color:
            return x, y
    '''


def write_move(move):
    str_to_write = '0\n' + str(move[0]) + " " + str(move[1])
    with open("shared_file.txt", 'w') as f:
        f.write(str_to_write)


def main():
    global player_color
    cnt = 0
    player_color = sys.argv[1]
    while True:
        while True:
            # grid = read_file(player_color)
            grid = read_file(player_color)
            if grid is not None:
                break
            time.sleep(.01)
        move = select_move(grid, player_color, cnt)
        cnt += 1
        write_move(move)


if __name__ == "__main__":
    main()