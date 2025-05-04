import tkinter as tk
import tkinter.font as tkFont
import itertools as it
import random
import math
import sys
import os

def get_path(relative_path):
    try:
        base_path = sys._MEIPASS  # pyinstaller打包后的路径
    except AttributeError:
        base_path = os.path.abspath(".")  # 当前工作目录的路径
    return os.path.normpath(os.path.join(base_path, relative_path))  # 返回实际路径

attack_page = tk.Tk()
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(family="宋体", size=14)
attack_page.title("星趴战斗计算器 by B站@SLzkm")
attack_page.geometry("854x480")
attack_page.resizable(False, False)
attack_page.iconbitmap(get_path("Icon/Icon_Jasmine.ico"))

# Create a label widget
label_atk_CN = tk.Label(attack_page, text="输入我方战斗卡和属性!")
label_atk_CN.place(x=160, y=25)
label_dfs_CN = tk.Label(attack_page, text="输入敌方防御力和血量!")
label_dfs_CN.place(x=520, y=25)

class ClassSpinbox:
    def __init__(self, name, root, x, y, maxn=6, minn=0):
        self.name = name
        self.fr = tk.Frame(root)
        self.fr.place(x=x, y=y)
        self.maxn = maxn
        self.minn = minn
        tk.Label(self.fr, text=name, width=25).grid(row=0, column=0)
        self.spinbox = tk.Spinbox(self.fr, from_=minn, to=maxn, width=5)
        self.spinbox.configure(validate="key")
        valid_cmd = (self.fr.register(self.__between), "%P")
        self.spinbox.configure(validatecommand=valid_cmd)
        self.spinbox.grid(row=0, column=1)

    def __between(self, num):
        if num == "":
            return True
        if not num.isdigit():
            return False
        if self.maxn >= int(num) >= self.minn:
            return True
        else:
            return False

    def get(self):
        if self.spinbox.get() == "":
            return self.minn
        else:
            return int(self.spinbox.get())

ATK = ClassSpinbox("攻击力/ATK(0-999)", attack_page, 100, 75, 999)
ATK_M = ClassSpinbox("攻击（中）/ATK(M)(0-6)", attack_page, 100, 117)
ATK_L = ClassSpinbox("攻击（大）/ATK(L)(0-3)", attack_page, 100, 159, 3)
ATK_G = ClassSpinbox("攻击（特大）/ATK(G)(0-2)", attack_page, 100, 201, 2)
Gawu_Cut = ClassSpinbox("嘎呜切/Gawu Cut(0-1)", attack_page, 100, 243, 1)
Shadow_ATK = ClassSpinbox("暗影突袭/Shadow ATK(0-3)", attack_page, 100, 285, 3)
Charge = ClassSpinbox("蓄力/Charge(0-1)", attack_page, 100, 327, 1)
Powerful_ATK = ClassSpinbox("全力攻击/Powerful ATK(0-2)", attack_page, 100, 369, 2)
Cost = ClassSpinbox("费用/Max Cost(3-6)", attack_page, 100, 411, 6, 3)
ATK_list = [ATK_M, ATK_L, ATK_G, Gawu_Cut, Shadow_ATK, Charge, Powerful_ATK]
Cost_list = [1,2,3,4,2,5,3]
Damage_list = [3,6,10,20,3,5,6]

DFS = ClassSpinbox("防御力/DFS(0-999)", attack_page, 450, 75, 999)
HP = ClassSpinbox("生命值/HP(1-999)", attack_page, 450, 117, 999, 1)
Enemy_list = [DFS, HP]

HaiQ_var = tk.BooleanVar()
HaiQ = tk.Checkbutton(attack_page, text="蓝海晴技能", variable=HaiQ_var)
HaiQ.place(x=500,y=159)
Mark_var = tk.BooleanVar()
Mark = tk.Checkbutton(attack_page, text="标记", variable=Mark_var)
Mark.place(x=675,y=159)
buff = 0

Out = tk.Frame(attack_page)
Out.place(x=475,y=220)

ans_no_text1 = "这里显示不出牌击败敌人的概率"
label_ans_no1_CN = tk.Label(Out, text=ans_no_text1)
label_ans_no1_CN.grid(row=0, sticky="we")

ans_max_text1 = "这里显示击败敌人概率最大的方案"
ans_max_text2 = " "
label_ans_max1_CN = tk.Label(Out, text=ans_max_text1)
label_ans_max2_CN = tk.Label(Out, text=ans_max_text2)
label_ans_max1_CN.grid(row=2)
label_ans_max2_CN.grid(row=3)

ans_avg_text1 = "这里显示该方案下平均造成的伤害"
label_ans_avg1_CN = tk.Label(Out, text=ans_avg_text1)
label_ans_avg1_CN.grid(row=4)

simulations = 100000  # 模拟次数
def roll_damage(damage_range):
    return random.randint(1,damage_range)

def battle(cards,attack):
    total_damage = 0
    flag = 0
    for i,card in enumerate(cards):
        for temp in range(card):
            if i<4:
                total_damage += roll_damage(Damage_list[i])
            else:
                total_damage += Damage_list[i]
        if i==6 and card>0:
            flag = 1
    total_damage += random.randint(1,6)
    total_damage += attack
    if flag == 1:
        total_damage = math.ceil(total_damage * 1.5)
    return total_damage
def MonteCarlo(cards,attack,health,defense):
    win = 0
    damage_sum = 0
    for _ in range(simulations):
        pre_damage = battle(cards,attack)
        final_defense = defense + random.randint(1,6)
        final_damage = max(pre_damage - final_defense, 1) + buff
        if final_damage >= health:
            win += 1
        damage_sum += final_damage
    return [win / simulations, damage_sum / simulations]
def Calculate():
    global ans_no_text1
    global label_ans_no1_CN
    global ans_max_text1
    global ans_max_text2
    global label_ans_max1_CN
    global label_ans_max2_CN
    global ans_avg_text1
    global label_ans_avg1_CN

    ans_no = 0
    ans_max = 0
    max_text = [0 for _ in range(7)]
    ans_avg = 1
    atk_count = []
    for temp in ATK_list:
        atk_count.append(temp.get())
    card_ranges = [range(limit + 1) for limit in atk_count]
    # 使用itertools.product生成所有可能的组合
    all_combinations = list(it.product(*card_ranges))
    global buff
    buff = HaiQ_var.get() + Mark_var.get()
    health = HP.get()
    defense = DFS.get()
    attack = ATK.get()
    for temp in all_combinations:
        cost_limit = Cost.get()
        total_cost = 0
        for i,card in enumerate(temp):
            total_cost += Cost_list[i] * card
        if total_cost > cost_limit:
            continue
        ans_temp = MonteCarlo(temp,attack,health,defense)
        ans = ans_temp[0]
        dmg = ans_temp[1]
        if ans > ans_max or (ans == ans_max < 0.5 and dmg >ans_avg):
            ans_max = ans
            max_text = temp
            ans_avg = dmg
        if total_cost == 0:
            ans_no = ans
    if ans_no == 0:
        ans_no_text1 = "目前不出牌 *不可能* 击败敌人！"
    elif ans_no == 1:
        ans_no_text1 = "目前不出牌 *一定能* 击败敌人！"
    else:
        ans_no_text1 = "不出牌击败敌人的概率为：" + format(ans_no*100,'.2f') + '%'
    label_ans_no1_CN.config(text=ans_no_text1)

    ans_max_text1 = "多出牌击败敌人的概率为：" + format(ans_max*100, '.2f') + '%'
    ans_max_text2 = "方案是：" + str(max_text)
    label_ans_max1_CN.config(text=ans_max_text1)
    label_ans_max2_CN.config(text=ans_max_text2)

    ans_avg_text1 = "该方案下造成的平均伤害为：" + format(ans_avg, '.2f')
    label_ans_avg1_CN.config(text=ans_avg_text1)
    return

tk.Button(attack_page, text="计算", command=Calculate).place(x=600, y=350)
label_atk1_CN = tk.Label(attack_page, text="10w次模拟所得结果，未必完全准确。")
label_atk1_CN.place(x=475, y=400)
label_atk2_CN = tk.Label(attack_page, text="只输入想使用的牌可以更快获得结果！")
label_atk2_CN.place(x=475, y=425)

attack_page.mainloop()