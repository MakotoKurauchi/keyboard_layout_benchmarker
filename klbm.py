# Keyboard layout benchmarker
# Copyright (c) 2017 MakotoKurauchi
# MIT License

import sys
import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

## load files

argvs = sys.argv
argc = len(argvs)

if (argc != 4):
	print ('Usage: $ python %s textfile keymap.json cost.json' % argvs[0])
	quit()

f = open(argvs[1],'r')
txt_lst = f.read()
f.close()
keycounter_dict = Counter(txt_lst)

f = open(argvs[2],'r')
keymap_dict = json.load(f)
f.close()

f = open(argvs[3],'r')
cost_dict = json.load(f)
f.close()
position_list = cost_dict['position']
hand_list = cost_dict['hand']
finger_list = cost_dict['finger']


## cost

p_cost = 0
h_cost = 0
count = 0
lasthand = 0
lastfinger = 0
for c in txt_lst:
	if c in keymap_dict:
		## position cost
		p_cost += position_list[keymap_dict[c][0]][keymap_dict[c][1]]

		## hand/finger cost
		if lasthand != hand_list[keymap_dict[c][0]][keymap_dict[c][1]]:
			h_cost += 1
		else:
			if lastfinger != finger_list[keymap_dict[c][0]][keymap_dict[c][1]]:
				h_cost += 4
			else:
				h_cost += 5

		lasthand = hand_list[keymap_dict[c][0]][keymap_dict[c][1]]
		lastfinger = finger_list[keymap_dict[c][0]][keymap_dict[c][1]]
		count += 1
		
print("Position cost   :", "{0:4d}".format(int(p_cost/count*100)))
print("Hand/Finger cost:", "{0:4d}".format(int(h_cost/count*100)))
print("Total cost      :", "{0:4d}".format(int((p_cost/count + h_cost/count)*100)))


## heatmap

lst = []
for k, v in keycounter_dict.items():
	if k in keymap_dict:
		lst.append([k, v, keymap_dict[k][0], keymap_dict[k][1]])
	#else:
		#print(k ,"is no match.")

df = pd.DataFrame(lst,columns=["key", "num", "row", "col"])
pivots = df.pivot("row","col","num")

sns.heatmap(pivots, annot=False, cbar=False, square=True, linewidths=1, cmap="PuRd")

plt.show()
