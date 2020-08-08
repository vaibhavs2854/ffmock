import pickle
import csv
import matplotlib.pyplot as plt
import seaborn as sns

pickle_dump_array = []
with open('nflcsv1.csv') as file:
    filereader = csv.reader(file,delimiter=',')
    for row in filereader:
        pickle_dump_array.append(row[1:10]+row[11:12])

pickle_dump_array = pickle_dump_array[:171]
for index,i in enumerate(pickle_dump_array):
    print(i)

new_array = []
for index,i in enumerate(pickle_dump_array):
    if index==0:
        continue
    new_array.append((i[0],i[7]))

new_array = sorted(new_array,key=lambda tup:tup[1])
pickle.dump(pickle_dump_array,open("allinfo.p","wb"))
pickle.dump(new_array, open("nameranking.p", "wb"))


