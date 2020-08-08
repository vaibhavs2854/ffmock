import pickle
import csv
import operator
import random
import numpy as np

global arr

draftpos = 10
totalpos = []
temp = draftpos
for i in range(15):
    totalpos.append(draftpos + i*28)
    totalpos.append(draftpos + i*28 + 9)
totalpos = totalpos[:15]
print(totalpos)

new_array = pickle.load(open("nameranking.p", "rb"))
fullarray = pickle.load(open("allinfo.p","rb"))

arr = []

"""
for i in enumerate(fullarray):
    print(i)
print(len(fullarray))
"""

#name,valuescore,adp
for index,i in enumerate(fullarray):
    if index==0:
        continue
    arr.append((i[0],float(i[7]),int(i[9]),i[3]))

arr = sorted(arr, key=lambda x:x[2])



for i in arr:
    print(i)
print(len(new_array))


pickplayerarr = []
for i in range(12):
    lower = totalpos[i]-2
    upper = totalpos[i]+5
    player_list = []
    for j in range(lower,upper+1,1):
        player_list.append(arr[j-1][0])
    pickplayerarr.append(player_list)


for index,i in enumerate(pickplayerarr):
    print("Choices for Pick " + str(index+1) + " Are: " + str(i))

def findposition(round,string):
    middle = totalpos[round-1]
    lower = middle-7
    upper = middle+7
    for j in range(lower,upper+1,1):
        if arr[j][0]==string:
            return arr[j][3][:2].upper()
    return "AB"


def quarterback_in_round(roundnum, round):
    for i in round:
        if i=="Patrick Mahomes":
            bob = 5
        middle = totalpos[roundnum-1]
        lower = middle-10
        upper = middle+10
        for j in range(lower,upper+1,1):
            if arr[j][0]==i:
                if arr[j][3][:2]=="QB":
                    return True
    return False

def create_weights(lower,upper,length):
    #lower is how low from adp
    #upper is how high from adp
    assert lower + upper + 1 == length

    equal_prob = 1.0/length
    low_prob = equal_prob/2
    upper_prob = (1.0-equal_prob*4-low_prob*(lower-1))/(length-lower+1-4)
    weights = []
    for i in range(lower-1):
        weights.append(low_prob)
    for i in range(4):
        weights.append(equal_prob)
    for i in range(upper-2):
        weights.append(upper_prob)

    print(np.sum(weights))
    assert len(weights)==length
    assert np.sum(weights) == 1.0

    return weights


def create_dict():
    dict = {}
    dict["QB"] = ""
    dict["RB1"] = ""
    dict["RB2"] = ""
    dict["WR1"] = ""
    dict["WR2"] = ""
    dict["TE"] = ""
    dict["B1"] = ""
    dict["B2"] = ""
    dict["B3"] = ""
    dict["B4"] = ""
    dict["B5"] = ""
    dict["B6"] = ""
    return dict

def print_dict(dict):
    for key in dict.keys():
        print(str(key)+": " + str(dict[key]))

#picking out of the choices
qbchoices = []
for i in range(12):
    if quarterback_in_round(i+1,pickplayerarr[i]):
        qbchoices.append(i+1)
qbpos = random.choice(qbchoices)
print(qbpos)
round_number = 6
print(quarterback_in_round(round_number,pickplayerarr[round_number-1]))

draftdict = create_dict()

#drafting
alreadytightend = False
weights = create_weights(2,5,8)
for i in range(12):
    round = i+1
    #QB
    if qbpos == round:
        for j in pickplayerarr[i]:
            if findposition(round,j)=="QB":
                draftdict["QB"] = j + " " + str(round)
                break
    else:
        #pick random guy
        pick = random.choice(pickplayerarr[i])
        position = findposition(round,pick)
        while(position=="QB"):
            pick = random.choice(pickplayerarr[i])
            position = findposition(round, pick)
        #Tight End
        if alreadytightend:
            while(position=="TE" or position=="QB"):
                pick = random.choice(pickplayerarr[i])
                position = findposition(round, pick)
        else:
            if position=="TE":
                if not alreadytightend:
                    draftdict[position] = pick + " " + str(round)
                    alreadytightend = True
                    continue
        if not draftdict[position+"1"]=="":
            if not draftdict[position+"2"]=="":
                counter = 1
                while not draftdict["B"+str(counter)] == "":
                    counter+=1
                draftdict["B"+str(counter)] = pick + " " + str(round)
            else:
                draftdict[position + "2"] = pick + " " + str(round)
        else:
            draftdict[position + "1"] = pick + " " + str(round)
print("done")

print_dict(draftdict)

