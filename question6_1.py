import pickle
import preprocessing
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns

def count_2_publications(list):
    count = 0
    for i in range(len(list)):
        if list[i] >= 2:
            count+=1
    
    return count


with open(b'network.p','rb') as f:
    data = pickle.load(f)

tier_1_list = []
tier_2_list = []
tier_3_list = []
for author in data.authors:
    
    # Append all publications into a list
    publication_list = []
    for publication in author.publications:
        publication_list.append(publication)

    # To sort the list in place
    publication_list.sort(key=lambda x: x.year, reverse=False)

    no_of_tier_1_publications = 0

    for i in range(len(publication_list)):
        if publication_list[i].tier == 1:
            no_of_tier_1_publications += 1

    if publication_list[0].tier == 1:
        tier_1_list.append(no_of_tier_1_publications)
    elif publication_list[0].tier == 2:
        tier_2_list.append(no_of_tier_1_publications)
    else:
        tier_3_list.append(no_of_tier_1_publications)

author_count = [count_2_publications(tier_1_list), count_2_publications(tier_2_list), count_2_publications(tier_3_list)]
tier = [1, 2, 3]
plt.bar(tier, author_count)
plt.xlabel("Initial publication tier of authors")
plt.ylabel("Total number of authors that published in premium venues at least twice")
plt.title('Does initial reputation of publication venues predict success?')

for i, v in enumerate(author_count):
    plt.text(i+0.99, 
              v + 0.4, 
              author_count[i], 
              fontsize=10, color='red')

plt.show()



