from matplotlib import pyplot as plt
import pickle
import preprocessing


with open(b'network.p','rb') as f:
    data = pickle.load(f)

# A list consisting of publication objects
publication_list = []

# Add all tier 1 venues to the list
for publication in data.publications:
    if publication.tier == 1:
        publication_list.append(publication)


# A list consisting of author objects
author_list = []

# Add all authors from publication_list to the list
for publication in publication_list:
    for author in publication.authors:
        if author not in author_list:
            author_list.append(author)


# A list consisting of lists of institutes and author count
institute_list= []

# Add all institutes' prestige to the list
for institute in data.institute:
    # Initiate author count is set to 0
    institute_list.append([institute.prestige, 0])

# Update author count for all institutes
for author in author_list:
    for institute in institute_list:
        if author.institute == institute[0]:
            institute[1] += 1

# 2 lists containing institutes' prestige and its author count
institute_prestige = []
author_count = []

# Copy over the respective institutes' prestige and author count to the 2 lists
for institute in institute_list:
    institute_prestige.append(institute[0])
    author_count.append(institute[1])

# Visualise the plot
# These are sample values
#institute_prestige = [1, 2, 3, 4, 5]
#author_count = [2, 4, 6, 8, 10]

plt.plot(institute_prestige, author_count)
plt.xlabel("Prestigue of Institute")
plt.ylabel("No of Authors")
plt.show()

