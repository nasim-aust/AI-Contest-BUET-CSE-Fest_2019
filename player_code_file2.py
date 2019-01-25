import time
import random
import sys
import copy
global grid
global player_color
grid_size = 8
global cnt

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

def chains(board):
	boardc = copy.deepcopy(board)
	lengths = []
	for pos in [(x,y) for x in range(grid_size) for y in range(grid_size)]:
		if boardc[pos[0]][pos[1]][0] == player_color and int(boardc[pos[0]][pos[1]][1]) == (critical_mass(pos) - 1):
			l = 0
			visiting_stack = []
			visiting_stack.append(pos)
			while visiting_stack:
				pos = visiting_stack.pop()
				boardc[pos[0]][pos[1]] = "No"
				l += 1
				for i in neighbors(pos):
					if boardc[i[0]][i[1]][0] == player_color and int(boardc[i[0]][i[1]][1]) == (critical_mass(pos) - 1):
						visiting_stack.append(i)
			lengths.append(l)
	return lengths


def neighbors(pos):
    n = []
    for i in [(pos[0],pos[1]+1), (pos[0],pos[1]-1), (pos[0]+1,pos[1]), (pos[0]-1,pos[1])]:
        if 0 <= i[0] < grid_size and 0 <= i[1] < grid_size:
            n.append(i)
    return n
def score(board, pos):
    global player_color
    boardc = copy.deepcopy(board)
    if(boardc[pos[0]][pos[1]][0] == player_color):
        boardc[pos[0]][pos[1]] = str(boardc[pos[0]][pos[1]][0])+str(int(boardc[pos[0]][pos[1]][1])+1) 
    else:
        boardc[pos[0]][pos[1]] = str(player_color)+str(1)
    sc = 0
    my_orbs, enemy_orbs = 0,0
    for pos in [(x,y) for x in range(grid_size) for y in range(grid_size)]:
        if boardc[pos[0]][pos[1]][0] == player_color:
            my_orbs += int(boardc[pos[0]][pos[1]][1])
            flag_not_vulnerable = True
            for i in neighbors(pos):
                if boardc[i[0]][i[1]][0] != player_color and boardc[i[0]][i[1]][0] != 'N' and (int(boardc[i[0]][i[1]][1]) == critical_mass(i) - 1):
                    sc -= 5-critical_mass(pos)
                    flag_not_vulnerable = False
            if flag_not_vulnerable:
                #The edge Heuristic
                if critical_mass(pos) == 3:
                    sc += 2
                #The corner Heuristic
                elif critical_mass(pos) == 2:
                    sc += 3
                #The unstability Heuristic
                if int(boardc[pos[0]][pos[1]][1]) == critical_mass(pos) - 1:
                    sc += 2
                #The vulnerablity Heuristic
        elif boardc[pos[0]][pos[1]][0] != 'N':
            enemy_orbs += int(boardc[pos[0]][pos[1]][1])
    #The number of Orbs Heuristic
    sc += my_orbs
    #You win when the enemy has no orbs
    if enemy_orbs == 0 and my_orbs > 1:
        return 10000
    #You loose when you have no orbs
    elif my_orbs == 0 and enemy_orbs > 1:
        return -10000
    #The chain Heuristic
    sc += sum([2*i for i in chains(boardc) if i > 1])
    return sc


def select_move(grid, player_color, cnt, vis):
    val = -999999
    dis = 100
    found = 0
    for pos in [(x,y) for x in range(grid_size) for y in range(grid_size)]:
        if grid[pos[0]][pos[1]][0]== 'N':
            if (min(pos[0],grid_size-pos[0]) + min(pos[1],grid_size-pos[1]))**2 <dis and pos not in vis:
                dis = (min(pos[0],grid_size-pos[0]) + min(pos[1],grid_size-pos[1]))**2
                found = 1
                best = pos
    if found == 1 and cnt <20:
        vis.append(best)
        return (best[0], best[1]),vis
    
    for pos in [(x,y) for x in range(grid_size) for y in range(grid_size)]:
        if grid[pos[0]][pos[1]][0]== player_color  or grid[pos[0]][pos[1]][0]=='N':
            mx = score(grid,pos)
            if(mx>val):
                val =mx
                best = pos
    print(val)
    
    return (best[0], best[1]), vis
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
    vis = []
    cnt = 0
    player_color = sys.argv[1]
    while True:
        while True:
            # grid = read_file(player_color)
            grid = read_file(player_color)
            if grid is not None:
                break
            time.sleep(.01)
        move, vis = select_move(grid, player_color, cnt, vis)
        cnt+=1
        write_move(move)


if __name__ == "__main__":
    main()