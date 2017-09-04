'''
This is the file where we audit our data
here we correct some street adresses. 
'''
#importing required modules
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

#file path
OSMFILE = "NewDelhi.osm"

#regular exp to find the last word in the name
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
# regular expression for the valid postal code
POSTAL_CODE_RE = re.compile('^[1-9][0-9]{5}$')

#these are the common types of locations 
expected = ["Park", "Open Market", "Roundabout", "Delhi", "Flats", "Garden", "Gate", "Janpath", "Lane", "Road", "Market", "Town"] 

#mapping from some correct or unusual words to the more common words defined above
mapping = { "Bagh": "Park",
            "Bazaar": "Market",
            "Chowk": "Open Market",
            "Circle": "Roundabout",
            "Circus": "Roundabout",
            "circle": "Roundabout",
            "Delhi.": "Delhi",
            "delhi": "Delhi",
            "flats": "Flats",
            "gate": "Gate",
            "gate": "Gate",
            "lane": "Lane",
            "ln": "Lane",
            "Ln": "Lane",
            "Marg": "Road",
            "marg": "Road",
            "Marg,": "Road",
            "Nagar": "Town",
            "road": "Road",
            "Rd.": "Road"
            }

#filtering the street type which have wierd names
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def audit_post_code(postcodes,postcode):
    a = POSTAL_CODE_RE.search(postcode)
    if not a:
        postcodes[postcode]+=1
#checking if it is a street location
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

#checking if it is a postcode tag
def is_postal_code(elem):
    return (elem.attrib['k'] == "addr:postcode")

#main fuction from where auditing start and filter the tags which namr tag from rest
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    postcodes = defaultdict(int)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                if is_postal_code(tag):
                    audit_post_code(postcodes,tag.attrib['v'])
    osm_file.close()

    print postcodes
    return street_types

#checking for the valid postcode 
def check_postcode(postcode):
    m = POSTAL_CODE_RE.search(postcode)
    if m:
        return postcode
    return None

#making a better name from a wierd one
def update_name(name, mapping=mapping):
    a = street_type_re.search(name)
    m = a.group()
    if m in mapping: 
      return street_type_re.sub(mapping[a.group()],name)
    return name

#main fuction to load file and call
def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name


if __name__ == '__main__':
    test()