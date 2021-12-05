from load import openfile
import numpy as np

today = "Day04"
lines = openfile(today+".txt")

numbers = list(map(int, lines[0].split(",")))

data = lines[2:]

boards = []
board = []
marks = []
for line in data:
    if line:
        board.append(list(map(int, line.strip().split())))
    else:
        boards.append(np.array(board))
        marks.append(np.zeros(shape=(5,5)))
        board = []

def check_winner(mark):
    for i in range(len(mark)):
        if np.all(mark[:,i]) or np.all(mark[i,:]):
            return True
    return False


def get_winner_line(arr_t, arr_b):
    for v in range(5):
        if np.all(arr_t[v, :]):
            return arr_b[v, :]
        if np.all(arr_t[:, v]):
            return arr_b[:, v]

def get_score(arr_t, arr_b,number):
    nums = arr_b.reshape(25)
    truths = np.abs(arr_t.reshape(25)-1)
    #print(np.sum(nums*truths))
    return np.sum(nums*truths)*number

winner_found = False
for number in numbers:
    #print(number)
    for i in range(len(boards)):
        if number in boards[i]:
            marks[i][np.where(boards[i]==number)]=1
        if check_winner(marks[i]):
            print("winner!")
            #print(boards[i])
            ans = get_winner_line(marks[i], boards[i])
            #print(ans)
            print(get_score(marks[i],boards[i],number))
            winner_found = True
            break
    if winner_found:
        break

for i in range(len(marks)):
    marks[i][:] = 0
winners = []
done = False
for number in numbers:
    for i in range(len(boards)):
        if not list(boards[i].reshape(25)) in winners:
            if number in boards[i]:
                marks[i][np.where(boards[i]==number)]=1
            if check_winner(marks[i]):
                winners.append(list(boards[i].reshape(25)))
        if not len(winners) < len(boards):
            print("FInally, a winner")
            print(get_score(marks[i],boards[i],number))
            done = True
            break
    if done:
        break