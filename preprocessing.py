from lxml import etree
import re
import csv
from fuzzywuzzy import fuzz
import pickle
import sys

sys.setrecursionlimit(2147000000)
datapath = "C:\\dblp.xml"
config = "C:\\config.xml"
uniData = "C:\\timesData.csv"

class institute:
  name:str
  location:str
  prestige:int
  def __init__(self):
      self.name = None
      self.location = None
      self.prestige = None
      return
  def set_name(self, name:str):
      self.name = name
      return
  def set_location(self, location:str):
      self.location = location
      return
  def set_prestige(self, prestige:int):
       self.prestige = prestige
       return

class network:
  def __init__(self):
      self.publications = []
      self.authors = []
      self.institute = []
      return
  def add_author(self, author):
      self.authors.append(author)
      return
  def add_publication(self, publication):
      self.publications.append(publication)
      return
  def add_institute(self, institute):
      self.institute.append(institute)
      return
  def save(self):
      with open(b'network.p',"wb") as wf:
        pickle.dump(self, wf, protocol = pickle.HIGHEST_PROTOCOL)
      wf.close()
      return

class publication:
  title:str
  tier:int
  year:int
  authors:[]
  def __init__(self):   
      self.title = None
      self.tier = None
      self.year = None
      self.authors = []
      return
  def add_author(self, author):
      self.authors.append(author)
      return
  def set_title(self,title:str):
      self.title = title
      return
  def set_year(self,year:int):
      self.year = year
      return
  def set_tier(self,tier:int):
      self.tier = tier
      return

class person:
  name:str
  publications:[]
  institute:str
  prestige:str
  def __init__(self):
      self.name = None
      self.publications = []
  def add_publications(self,object):
      self.publications.append(object)
      return
  def set_name(self,name:str):
      self.name = name
      return
  def set_institute(self, institute):
       self.institute = institute
       return
  def set_prestige(self,prestige:str):
      self.prestige = prestige
      return
 
class article:
 authors:[str]
 title:str
 year:str
 crossref:str
 tier:int
 institute_name:str
 def __init__(self):
     self.authors = []
     self.title = None
     self.year = None
     self.crossref = None
     self.tier = 0
     self.institute_name = None
     return
 def add_author(self,name:str):
    self.authors.append(name)
    return
 def set_title(self,title:str):
    self.title = title
    return
 def set_year(self,year:int):
    self.year = year
    return
 def add_crossref(self,crossref:str):
     self.crossref = crossref
     return
 def add_tier(self,tier:int):
     self.tier = tier
     return
 def set_institute_name(self,institute_name:str):
     self.institute_name = institute_name
     return
 
def parse_data_article(datapath:str):
 networked = network()
 xmlp = etree.XMLParser(recover = True)
 #parses an xml section into an element tree incrementally
 itertree = etree.iterparse(datapath, load_dtd = True)
 #iterate recursively over all sub-tree below
 itertree = iter(itertree)
 previous = None
 count = 0;
 scount = 0;
 for event,elem in itertree: #read first line
     if elem.tag == 'inproceedings' or elem.tag == 'phdthesis' or elem.tag == 'mastersthesis':
         previous = article()
     if previous != None:
         if elem.tag == 'author':
             previous.add_author(elem.text)
         elif elem.tag == 'title':
             previous.set_title(elem.text)
         elif elem.tag == 'year':
             previous.set_year(elem.text)
         elif elem.tag == 'crossref':
             previous.add_crossref(elem.text)
             article_tier(previous,configuration)
             if previous.tier >= 1:
                   count += 1
                   print(str(count)+" articles parsed.")
                   auto_add_authors(previous,networked)
                   auto_add_publication(previous,networked)
             previous = None
         elif elem.tag == 'school':
               scount += 1
               print(str(scount)+" schools parsed.")
               institute_name = elem.text
               previous.set_institute_name(institute_name)
               auto_add_institute(previous, networked)
               previous = None
     elem.clear()
     if (count >= 3000):
         break
 return networked

def load_configuration(file_location:str):
  xmlp = etree.XMLParser(recover = True)
  itertree = etree.iterparse(file_location, load_dtd = True)
  itertree = iter(itertree)
  tierlist = {'1':[],'2':[],'3':[]}
  for event, elem in itertree:
      if elem.tag == 'tier1':
          tierlist['1'].append(elem.text)
      elif elem.tag == 'tier2':
          tierlist['2'].append(elem.text)
      elif elem.tag == 'tier3':
          tierlist['3'].append(elem.text)
  return tierlist
def article_tier(a: article, tier:dict):
 crossref = re.search('/(.*)/', a.crossref)
 if (crossref.group(1) in tier["1"]):
     a.tier = 1
     return
 if (crossref.group(1) in tier["2"]):
     a.tier = 2
     return
 if (crossref.group(1) in tier["3"]):
     a.tier = 3
     return
def auto_add_authors(articled:article, networked:network):
   #create a list of authors within the article if not in network yet
   for author in articled.authors:
       inside = False
       for nauthor in networked.authors:
           if nauthor.name == author:
               inside = True
               break
   #create person object for each author and add it to netowrk class
       if inside == False:
           new_author = person()
           new_author.name = author
           networked.add_author(new_author)
   return
 
def auto_add_publication(articled:article, networked:network):
   #create publication object for each article
   #if author of article matches person object in network class, add author to publications class, person class and network class
   new_publication = publication()
   new_publication.set_title(articled.title)
   new_publication.set_tier(articled.tier)
   new_publication.set_year(articled.year)
   for author in articled.authors:
       for nauthor in networked.authors:
           if nauthor.name == author:
               nauthor.publications.append(new_publication)
               new_publication.add_author(nauthor)
   networked.add_publication(new_publication)
   return
 
def calculate_prestige(author:person):
   prestige = 0
   for item in author.publications:
       if item.tier == 1:
           prestige += 3
       elif item.tier == 2:
           prestige += 2
       elif item.tier == 3:
           prestige += 1
   return prestige
  
def auto_add_institute(articled:article, networked:network):
   #if author of article matches person object in network class, add institute to person class and network class
   new_institute = institute()
   with open(uniData, newline='', encoding = 'latin-1') as csvfile:
      for author in articled.authors:
           for nauthor in networked.authors:
               if nauthor.name == author:
                   new_institute.set_name(articled.institute_name)
                   reader = csv.DictReader(csvfile)
                   stopwords = ['University','Technology']
                   querywords = new_institute.name.split()
                   resultwords  = [word for word in querywords if word not in stopwords]
                   new_name = ' '.join(resultwords)
                   for row in reader:
                       if (row["year"] == '2016'):
                           location_init = row["country"]
                           prestige_init = row["wworld_rank"]
                           new_institute.set_location(location_init)
                           new_institute.set_prestige(prestige_init)
                           uni_name_country = [' '.join([row["university_name"], row["country"]])]
                           fuzz_ratio_init =  fuzz.ratio(uni_name_country, new_name)
                           break
                   for row in reader:
                       if (row["year"] == '2016'):
                           uni_name_country = [' '.join([row["university_name"], row["country"]])]
                           val = fuzz.ratio(uni_name_country, new_name)
                           if (val > fuzz_ratio_init):
                               new_institute.set_location(row["country"])
                               new_institute.set_prestige(row["wworld_rank"])
                               fuzz_ratio_init = val
                   networked.add_institute(new_institute)
   csvfile.close()
   return
 
def generate_data():
    final_network = parse_data_article(datapath)
    final_network.save()

configuration = load_configuration(config)