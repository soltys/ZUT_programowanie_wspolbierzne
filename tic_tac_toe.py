import time, thread
from copy import copy, deepcopy
import random
import sys
random.seed()
thread_counter = 0;
player_lock = thread.allocate_lock()
current_player = 'O'
board = [0] * 9

def print_board(board):
    print ''
    print '---'
    for i in xrange(9):
        if not i==0 and i % 3 == 0:
            print ''
        if board[i]==0:
            sys.stdout.write('_')
        if board[i]==1:
            sys.stdout.write('O')
        if board[i]==2:
            sys.stdout.write('X')
        

def change_player():
    global current_player
    if current_player == 'X':
        current_player = 'O'        
        return
    if current_player == 'O':
        current_player = 'X'
        return
        

def create_thread(fun, args):    
    def thread_fun(args):
        fun(*args)
        global thread_counter
        thread_counter -= 1
        
    global thread_counter
    thread_counter += 1
    thread.start_new_thread(thread_fun,(args,))
    
def end_game(board):
    count = 0
    for i in xrange(9):
        if not board[i] == 0:
            count += 1
    if count == 9:
        return -1
    for i in xrange(3):
        if board[0+i*3] == board[1+i*3] and board[1+i*3] == board[2+i*3]:
            return board[0+i*3]
            
        if board[i+0*3] == board[i+1*3] and board[i+1*3] == board[i+2*3]:
            return board[i+0*3] 
            
    if board[0] == board[4] and board[4] == board[8]:
        return board[0]
        
    if board[2] == board[4] and board[4] == board[6]:
        return board[2]

    return 0

def wait_thread():
    while thread_counter > 0:
        time.sleep(1)

def make_move(board, place, name):
    if name == 'O':
        board[place] = 1
    if name == 'X':
        board[place] = 2
        
def get_player_number(name):
    if name == 'O':
        return 1
    if name == 'X':
        return 2

def player_locked_work(name):
    #print name, " now working"
    global board
    moves = []
    for i in xrange(9):
        if board[i] == 0:
            board_copy = deepcopy(board)
            make_move(board_copy,i,name)
            moves.append({'index':i, 'result':end_game(board_copy)})
    
    player_number = get_player_number(name)
### Dodać obronę przed przeciwnikiem, sprawdzić wszystkie ruchy dla przeciwnika i sprawdzić czy któryś prowadzi do wygranej, i tam postawić swój ruch
    
    wining_moves = [x for x in moves if x['result'] == player_number]
    if len(wining_moves) > 0:
        make_move(board, wining_moves[0]['index'], name)
        return
        
    nothing_moves = [x for x in moves if x['result'] == 0]
    if len(nothing_moves) > 0:
        make_move(board, nothing_moves[random.randint(0,len(nothing_moves)-1)]['index'], name)
        return
        
    tie_moves = [x for x in moves if x['result'] == -1]
    if len(tie_moves) > 0:
        make_move(board, tie_moves[0]['index'], name)
        return
    
    make_move(board, moves[0]['index'],name)
    return

    
def player_work(name):
    #print name, " is waiting"
    global player_lock
    global board
    global current_player
    while end_game(board) == 0:
        if current_player == name:
            with player_lock:
                player_locked_work(name)
                print ''
                print "Gracz" , name, " wykonuje ruch"
                print_board(board)
                change_player()             


    
if __name__ == "__main__":
        
    create_thread(player_work,('O',))
    create_thread(player_work,('X',))
    
    #print "main thread awaits"
    wait_thread()
    print ''
    print "done"
