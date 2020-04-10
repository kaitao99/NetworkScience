import pickle
import preprocessing

#preprocessing.generate_data()
#print("done.")

with open(b'network.p','rb') as f:
    data = pickle.load(f)

for item in data.publications:
    print(item.title)

for item in data.authors:
    print(item.name)

for item in data.institute:
    print(item.name)
