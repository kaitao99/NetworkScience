import pickle
import preprocessing

#preprocessing.generate_data()
#print("done.")

with open(b'network.p','rb') as f:
    data = pickle.load(f)

for item in data.publications:
    print(item.title)
