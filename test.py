import pickle
import preprocessing

preprocessing.generate_data()

with open(b'network.p','rb') as f:
    data = pickle.load(f)

for item in data.authors:
    print(item.name)