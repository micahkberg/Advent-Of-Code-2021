import itertools
import copy

from load import openfile

today = "Day21"
lines = openfile(today+".txt")
dice_count = 0


def roll_dice():
    global dice_count
    out = dice_count % 100 + 1
    dice_count += 1
    return out

def roll_dirac_dice():
    pass

class Game:
    def __init__(self, p1, p2, die_type="Trad"):
        self.p1 = [p1, 0]
        self.p2 = [p2, 0]
        self.score1 = 0
        self.score2 = 0
        self.gameover = False
        self.turn_num = 0
        self.current_player = self.p1
        self.die_type = die_type

    def play(self):
        while not self.gameover:
            self.turn()
            self.current_player = self.p2 if self.current_player==self.p1 else self.p1

    def turn(self):
        self.turn_num+=1
        if self.die_type == "Trad":
            num = roll_dice()+roll_dice()+roll_dice()
        elif self.die_type == "Dirac":
            num = roll_dirac_dice()+roll_dirac_dice()+roll_dirac_dice() # lol jk
        print(f"Player {1 if self.turn_num%2==1 else 2}: Rolled {num}")
        print(f"moving from {self.current_player[0]} to {(self.current_player[0] + num)%10}")
        self.current_player[0] = (self.current_player[0] + num)%10
        self.current_player[1] = self.current_player[1]+self.current_player[0]+1
        self.check_winner()


    def check_winner(self):
        print(f"Scoreboard {self.p1[1]} to {self.p2[1]}")
        if self.p1[1] > 999 or self.p2[1] > 999:
            global dice_count
            print(min([self.p1[1],self.p2[1]])*dice_count)
            self.gameover = True


pos1 = int(lines[0][-1]) -1
pos2 = int(lines[1][-1]) -1
new_Game = Game(pos1,pos2)
# new_Game.play()

# not 1098000
# not 934650
# whoops supposed to be losing player


def calc_universes():

    # on each players turn 27 new universes are formed, 27*27 on each turn cycle
    #
    outcome_rolls = list(itertools.product([1,2,3],repeat=3))

    outcome_sums = sorted([sum(i) for i in outcome_rolls])

    # make fast(er) list of rolls:
    outcomes = {}    # dictionary of rolls by the number of ways there are to get that roll
    for roll in outcome_sums:
        if roll not in outcomes.keys():
            outcomes[roll] = 1
        else:
            outcomes[roll] += 1

    open_game_dict = {((4, 0), (5, 0), 0): 1}
    p1_wins = 0
    p2_wins = 0
    # for each unfinished game state
    empty_list = False
    while open_game_dict.keys():
        # pop next game
        while True:
            if len(open_game_dict.keys())==0:
                empty_list = True
                break
            current_game = list(open_game_dict.keys())[0]
            current_game_count = open_game_dict.pop(current_game)
            #if current_game[0][1]>17 and current_game[2] == 0:
            #    p1_wins += 27*current_game_count
            #elif current_game[1][1]>17 and current_game[2] == 0:
            #    p2_wins += 27*27*current_game_count
            #elif current_game[1][1]>17 and current_game[2] == 1:
            #    p2_wins += 27*current_game_count
            #elif current_game[0][1]>17 and current_game[2] == 1:
            #    p1_wins += 27*27*current_game_count
            #else:
            break
        if empty_list:
            break
        # for each possible turn cycle
        for roll in outcomes.keys():
            # for current player
            new_pos = current_game[current_game[2]][0] + roll
            new_pos = new_pos - 10 if new_pos > 10 else new_pos
            new_score = current_game[current_game[2]][1]+new_pos
            if new_score > 20:
                if current_game[2] == 0:
                    p1_wins += current_game_count*outcomes[roll]
                elif current_game[2] == 1:
                    p2_wins += current_game_count*outcomes[roll]
            else:
                if current_game[2] == 0:
                    new_game = ((new_pos, new_score), current_game[1], 1)
                elif current_game[2] == 1:
                    new_game = (current_game[0], (new_pos, new_score), 0)
                else:
                    print("turn system broke")
                    break
                if new_game in open_game_dict.keys():
                    open_game_dict[new_game] += current_game_count*outcomes[roll]
                else:
                    open_game_dict[new_game] = current_game_count*outcomes[roll]

    print(max([p1_wins,p2_wins]))
    print(min([p1_wins,p2_wins]))

calc_universes()

#low 96152137
#low 704428672
#example 444356092776315
#ex lose 341960390180808
#ex test 444356092776315
#ex lose 341960390180808

#correct answers: 575111835924670 to 392525387812463

