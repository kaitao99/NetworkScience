import pickle
import preprocessing
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np


with open(b'network.p','rb') as f:
    data = pickle.load(f)



count = 0
author_publication_list = []
for author in data.authors:

    publication_list = []
    for publication in author.publications:
        publication_list.append([publication.year, publication.tier])
    author_publication_list.append(publication_list)
    count += 1

    if count == 100:
        break

year_final = []
publication_tier_final = []
for publication_list in author_publication_list:
    
    year = []
    publication_tier = []
    for i in publication_list:
        year.append(i[0])
        publication_tier.append(i[1])

    year_final.append(year)
    publication_tier_final.append(publication_tier)

for i in range(len(year_final)):
    plt.plot(year_final[i], publication_tier_final[i])

plt.xlabel("Year")
plt.ylabel("Publication Tier")
plt.title('How likely an author can move from non-premium venues to premium venues in his/her career')
#plt.xticks(np.arange(2000, 2020, 1))
plt.yticks(np.arange(1, 4, 1))
plt.show()
