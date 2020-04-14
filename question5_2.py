import pickle
import preprocessing
from matplotlib import pyplot as plt
import numpy as np


with open(b'network.p','rb') as f:
    data = pickle.load(f)


for author in data.authors:

    # Append all publications into a list
    publication_list = []
    for publication in author.publications:
        publication_list.append(publication)

    # To sort the list in place
    publication_list.sort(key=lambda x: x.year, reverse=False)

    # Create 2 empty list to store year and tier seperately
    year = []
    tier = []

    # Append the year and tier to the respective lists
    for i in range(len(publication_list)):

        year.append(int(publication_list[i].year))
        
        # Classify tier 1 as premium, tier 2 and 3 as non premium
        if publication_list[i].tier == 1:
            tier.append("Premium Venue")
        else:
            tier.append("Non-premium Venue")

    # Plot for each author's publications
    plt.plot(tier, year)

# Display from year 2005 onwards as there are no movement between premium and non-premium venues before 2005
plt.ylim(2004, 2020)
plt.yticks(np.arange(2005, 2020, 1))
plt.xlabel("Publication Tier")
plt.ylabel("Year")
plt.title('How likely an author can move from non-premium venues to premium venues in his/her career')
plt.show()

