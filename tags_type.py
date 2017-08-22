'''
This File has two fuctions 
1) count_tags which tell us how many types of tags in our osm file 
and how many times it repeated.
2) key_type fuction categorise all the tags in three categories according to there key value 
    > lower character words
    > lower character words with colon(:) between them
    > words which has problamatic characters
'''
#importing modules
import pprint
import re
import xml.etree.cElementTree as ET
from collections import defaultdict

#file path
OSM_PATH = "NewDelhi.osm"

#defining regular expressions
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

#fuction to determine the types of tags with there frequency of occurence
def count_tags(filename):
    tags = {}
    for event, elem in ET.iterparse(filename):
        if elem.tag in tags: 
            tags[elem.tag] += 1
        else:
            tags[elem.tag] = 1
    return tags

#categorize and count the tag in those categories
def key_type(element, keys):
    if element.tag == "tag":
        for tag in element.iter('tag'):
            k = tag.get('k')
            if lower.search(element.attrib['k']):
                keys['lower'] = keys['lower'] + 1
            elif lower_colon.search(element.attrib['k']):
                keys['lower_colon'] = keys['lower_colon'] + 1
            elif problemchars.search(element.attrib['k']):
                keys['problemchars'] = keys['problemchars'] + 1
            else:
                keys['other'] = keys['other'] + 1
    
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

#printing the result
pprint.pprint(count_tags(OSM_PATH))
pprint.pprint(process_map(OSM_PATH))

