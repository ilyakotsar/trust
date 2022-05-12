import random
import string
import tkinter as tk
try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    pass


class Tournament:
    
    @staticmethod
    def play(population, pun, sucker, reward, tempt, rounds, losers, mist_prob):
        result = {}
        for i in range(len(PLAYERS)):
            player_a = PLAYERS[i]
            for a in range(population[player_a.name]):
                for j in range(len(PLAYERS)):
                    player_b = PLAYERS[j]
                    for b in range(population[player_b.name]):
                        if i < j and a == b:
                            continue
                        elif i == j and a == b:
                            continue
                        else:
                            score_a, score_b = Game(player_a, player_b).play(pun, sucker, reward, tempt, rounds, mist_prob)
                            n = f'{player_a.name}{a + 1}'
                            if n in result:
                                result[n] += score_a
                            else:
                                result[n] = 0
                                result[n] += score_a
                            n = f'{player_b.name}{b + 1}'
                            if n in result:
                                result[n] += score_b
                            else:
                                result[n] = 0
                                result[n] += score_b
        # Evolution
        tuples = [(k, result[k]) for k in sorted(result, key=result.get, reverse=False)]
        for x in range(losers):
            loser = [i for i in tuples[x][0] if i not in string.digits]
            winner = [i for i in tuples[::-1][x][0] if i not in string.digits]
            population[''.join(loser)] -= 1
            population[''.join(winner)] += 1 


class Game:
    def __init__(self, player_a, player_b):
        self.player_a = player_a
        self.player_b = player_b

    def play(self, pun, sucker, reward, tempt, rounds, mist_prob):
        wrong_moves_a = Game.mistakes(rounds, mist_prob)
        wrong_moves_b = Game.mistakes(rounds, mist_prob)
        moves_a = []
        moves_b = []
        payoffs_a = []
        payoffs_b = []
        for i in range(rounds):
            if i > 0:
                move_a = self.player_a.next_move(i, moves_a, moves_b)
                move_b = self.player_b.next_move(i, moves_b, moves_a)
                if i in wrong_moves_a:
                    move_a = MOVES[::-1][MOVES.index(move_a)]
                if i in wrong_moves_b:
                    move_b = MOVES[::-1][MOVES.index(move_b)]
            else:
                move_a = self.player_a.first_move
                move_b = self.player_b.first_move
            moves_a.append(move_a)
            moves_b.append(move_b)
            pay_1, pay_2 = Game.get_payoffs(move_a, move_b, pun, sucker, reward, tempt)
            payoffs_a.append(pay_1)
            payoffs_b.append(pay_2)
        return sum(payoffs_a), sum(payoffs_b)

    @staticmethod
    def mistakes(rounds, mist_prob):
        true_mist_prob = (rounds - 2) * mist_prob / rounds
        number_of_mistakes = round((rounds - 2) * true_mist_prob / 100)
        wrong_moves = []
        if number_of_mistakes > 0:
            for i in range(number_of_mistakes):
                while True:
                    x = random.randint(1, rounds - 1)
                    if i > 0:
                        if x in wrong_moves:
                            wrong_moves.append(random.randint(1, rounds - 1))
                            break
                        else:
                            continue
                    else:
                        wrong_moves.append(random.randint(1, rounds - 1))
                        break
        return wrong_moves

    @staticmethod
    def get_payoffs(move_a, move_b, pun, sucker, reward, tempt):
        if move_a == 'cheat' and move_b == 'cheat':
            pay_a, pay_b = pun, pun
        elif move_a == 'cooperate' and move_b == 'cheat':
            pay_a, pay_b = sucker, tempt
        elif move_a == 'cheat' and move_b == 'cooperate':
            pay_a, pay_b = tempt, sucker
        elif move_a == 'cooperate' and move_b == 'cooperate':
            pay_a, pay_b = reward, reward
        return pay_a, pay_b


class Player:
    def __init__(self, name, first_move):
        self.name = name
        self.first_move = first_move


class Copycat(Player):
    @staticmethod
    def next_move(*args):
        i, other_moves = args[0], args[2]
        return other_moves[i - 1]


class Copykitten(Player):
    @staticmethod
    def next_move(*args):
        i, other_moves = args[0], args[2]
        if other_moves[i - 1] == 'cheat':
            if i > 0:
                if other_moves[i - 1] == other_moves[i - 2]:
                    move = 'cheat'
                else:
                    move = 'cooperate'
            else:
                move = 'cooperate'
        else:
            move = 'cooperate'
        return move


class Cheater(Player):
    @staticmethod
    def next_move(*args):
        return 'cheat'


class Cooperator(Player):
    @staticmethod
    def next_move(*args):
        return 'cooperate'


class Grudger(Player):
    @staticmethod
    def next_move(*args):
        other_moves = args[2]
        if 'cheat' in other_moves:
            move = 'cheat'
        else:
            move = 'cooperate'
        return move


class Detective(Player):
    @staticmethod
    def next_move(*args):
        i, other_moves = args[0], args[2]
        if i <= 3:
            if i == 1:
                move = 'cheat'
            else:
                move = 'cooperate'
        if 'cheat' in other_moves:
            move = other_moves[i - 1]
        else:
            move = 'cheat'
        return move


class Simpleton(Player):
    @staticmethod
    def next_move(*args):
        i, my_moves, other_moves = args[0], args[1], args[2]
        if other_moves[i - 1] == 'cooperate':
            move = my_moves[i - 1]
        else:
            if my_moves[i - 1] == 'cooperate':
                move = 'cheat'
            elif my_moves[i - 1] == 'cheat':
                move = 'cooperate'
        return move


class Random(Player):
    @staticmethod
    def next_move(*args):
        return random.choice(MOVES)


MOVES = ('cooperate', 'cheat')
CC = Copycat('Copycat', 'cooperate')
CK = Copykitten('Copykitten', 'cooperate')
CH = Cheater('Cheater', 'cheat')
CO = Cooperator('Cooperator', 'cooperate')
GR = Grudger('Grudger', 'cooperate')
DE = Detective('Detective', 'cooperate')
SI = Simpleton('Simpleton', 'cooperate')
RA = Random('Random', random.choice(MOVES))
PLAYERS = CC, CK, CH, CO, GR, DE, SI, RA
changes = {}


def calculate():
    try:
        population = {}
        population[cc_label['text']] = int(cc_var.get())
        population[ck_label['text']] = int(ck_var.get())
        population[ch_label['text']] = int(cc_var.get())
        population[co_label['text']] = int(co_var.get())
        population[gr_label['text']] = int(gr_var.get())
        population[de_label['text']] = int(de_var.get())
        population[si_label['text']] = int(si_var.get())
        population[ra_label['text']] = int(ra_var.get())
        pun = float(pun_var.get())
        sucker = float(sucker_var.get())
        reward = float(reward_var.get())
        tempt = float(tempt_var.get())
        rounds = int(rounds_var.get())
        cycles = int(cycles_var.get())
        losers = int(losers_var.get())
        mist_prob = float(mist_prob_var.get())
        if mist_prob < 0 or mist_prob > 100:
            return False
        else:
            changes.clear()
            for _ in range(cycles):
                Tournament().play(population, pun, sucker, reward, tempt, rounds, losers, mist_prob)
                for i in population:
                    if i in changes:
                        changes[i].append(population[i])
                    else:
                        changes[i] = []
                        changes[i].append(population[i])
            cc_res['text'] = f"{cc_label['text']}: {population[cc_label['text']]}"
            ck_res['text'] = f"{ck_label['text']}: {population[ck_label['text']]}"
            ch_res['text'] = f"{ch_label['text']}: {population[ch_label['text']]}"
            co_res['text'] = f"{co_label['text']}: {population[co_label['text']]}"
            gr_res['text'] = f"{gr_label['text']}: {population[gr_label['text']]}"
            de_res['text'] = f"{de_label['text']}: {population[de_label['text']]}"
            si_res['text'] = f"{si_label['text']}: {population[si_label['text']]}"
            ra_res['text'] = f"{ra_label['text']}: {population[ra_label['text']]}"
            graph_btn.grid(row=21, column=1)
            copyright_label['text'] = ''
            tk.Label(root, text='© Ilya Kotsar https://github.com/ilyakotsar').grid(row=22, column=6)
    except (ValueError, IndexError):
        return False


def show_graph(changes):
    try:
        for i in changes:
            plt.plot(changes[i], label=i)
        plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
        plt.title('Evolution')
        plt.xlabel('Cycles')
        plt.ylabel('Population')
        plt.grid()
        plt.show()
    except NameError:
        return False


root=tk.Tk()
root.geometry("1100x540")
root.title('Trust')

cc_var = tk.StringVar(root, value='20')
cc_label = tk.Label(root, text='Copycat')
cc_entry = tk.Entry(root, textvariable=cc_var)
ck_var = tk.StringVar(root, value='20')
ck_label = tk.Label(root, text='Copykitten')
ck_entry = tk.Entry(root, textvariable=ck_var)
ch_var = tk.StringVar(root, value='20')
ch_label = tk.Label(root, text='Cheater')
ch_entry = tk.Entry(root, textvariable=ch_var)
co_var = tk.StringVar(root, value='20')
co_label = tk.Label(root, text='Cooperator')
co_entry = tk.Entry(root, textvariable=co_var)
gr_var = tk.StringVar(root, value='20')
gr_label = tk.Label(root, text='Grudger')
gr_entry = tk.Entry(root, textvariable=gr_var)
de_var = tk.StringVar(root, value='20')
de_label = tk.Label(root, text='Detective')
de_entry = tk.Entry(root, textvariable=de_var)
si_var = tk.StringVar(root, value='20')
si_label = tk.Label(root, text='Simpleton')
si_entry = tk.Entry(root, textvariable=si_var)
ra_var = tk.StringVar(root, value='20')
ra_label = tk.Label(root, text='Random')
ra_entry = tk.Entry(root, textvariable=ra_var)
pun_var = tk.StringVar(root, value='0')
pun_label = tk.Label(root, text='Punishment')
pun_entry = tk.Entry(root, textvariable=pun_var)
sucker_var = tk.StringVar(root, value='-1')
sucker_label = tk.Label(root, text='Sucker')
sucker_entry = tk.Entry(root, textvariable=sucker_var)
reward_var = tk.StringVar(root, value='2')
reward_label = tk.Label(root, text='Reward')
reward_entry = tk.Entry(root, textvariable=reward_var)
tempt_var = tk.StringVar(root, value='3')
tempt_label = tk.Label(root, text='Temptation')
tempt_entry = tk.Entry(root, textvariable=tempt_var)
rounds_var = tk.StringVar(root, value='10')
rounds_label = tk.Label(root, text='Rounds')
rounds_entry = tk.Entry(root, textvariable=rounds_var)
cycles_var = tk.StringVar(root, value='5')
cycles_label = tk.Label(root, text='Cycles')
cycles_entry = tk.Entry(root, textvariable=cycles_var)
losers_var = tk.StringVar(root, value='20')
losers_label = tk.Label(root, text='Losers per cycle')
losers_entry = tk.Entry(root, textvariable=losers_var)
mist_prob_var = tk.StringVar(root, value='10')
mist_prob_label = tk.Label(root, text='Mistake probability (%)')
mist_prob_entry = tk.Entry(root, textvariable=mist_prob_var)
calculate_btn=tk.Button(root, text='Calculate', command=calculate)
graph_btn=tk.Button(root, text='Show graph', command=lambda: show_graph(changes))

tk.Label(root, text='').grid(row=0, column=0)
cc_label.grid(row=1,column=0)
cc_entry.grid(row=1,column=1)
ck_label.grid(row=2,column=0)
ck_entry.grid(row=2,column=1)
ch_label.grid(row=3,column=0)
ch_entry.grid(row=3,column=1)
co_label.grid(row=4,column=0)
co_entry.grid(row=4,column=1)
gr_label.grid(row=5,column=0)
gr_entry.grid(row=5,column=1)
de_label.grid(row=6,column=0)
de_entry.grid(row=6,column=1)
si_label.grid(row=7,column=0)
si_entry.grid(row=7,column=1)
ra_label.grid(row=8,column=0)
ra_entry.grid(row=8,column=1)
pun_label.grid(row=1,column=2)
pun_entry.grid(row=1,column=3)
sucker_label.grid(row=2,column=2)
sucker_entry.grid(row=2,column=3)
reward_label.grid(row=3,column=2)
reward_entry.grid(row=3,column=3)
tempt_label.grid(row=4,column=2)
tempt_entry.grid(row=4,column=3)
rounds_label.grid(row=1,column=4)
rounds_entry.grid(row=1,column=5)
cycles_label.grid(row=2,column=4)
cycles_entry.grid(row=2,column=5)
losers_label.grid(row=3,column=4)
losers_entry.grid(row=3,column=5)
mist_prob_label.grid(row=4,column=4)
mist_prob_entry.grid(row=4,column=5)

tk.Label(root, text='').grid(row=9, column=0)
calculate_btn.grid(row=10, column=1)
tk.Label(root, text='').grid(row=11, column=0)

cc_res = tk.Label(root, text='')
cc_res.grid(row=12, column=1)
ck_res = tk.Label(root, text='')
ck_res.grid(row=13, column=1)
ch_res = tk.Label(root, text='')
ch_res.grid(row=14, column=1)
co_res = tk.Label(root, text='')
co_res.grid(row=15, column=1)
gr_res = tk.Label(root, text='')
gr_res.grid(row=16, column=1)
de_res = tk.Label(root, text='')
de_res.grid(row=17, column=1)
si_res = tk.Label(root, text='')
si_res.grid(row=18, column=1)
ra_res = tk.Label(root, text='')
ra_res.grid(row=19, column=1)
tk.Label(root, text='').grid(row=20, column=0)
copyright_label = tk.Label(root, text='© Ilya Kotsar https://github.com/ilyakotsar')
copyright_label.grid(row=21, column=6)

root.mainloop()


# © Ilya Kotsar https://github.com/ilyakotsar