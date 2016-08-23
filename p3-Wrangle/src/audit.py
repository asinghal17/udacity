"""
Audit Files for Phone and Street
"""
import xml.etree.cElementTree as ET
import collections 
import re
import pprint

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Blvd,": "Boulevard",
            "Boulavard": "Boulevard",
            "Boulvard": "Boulevard",
            "Ct": "Court",
            "Dr": "Drive",
            "Dr.": "Drive",
            "E": "East",
            "Hwy": "Highway",
            "Ln": "Lane",
            "Ln.": "Lane",
            "Pl": "Place",
            "Plz": "Plaza",
            "Rd": "Road",
            "Rd.": "Road",
            "St": "Street",
            "St.": "Street",
            "st": "Street",
            "street": "Street",
            "square": "Square",
            "parkway": "Parkway"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def audit_phone(invalid_phone, phone):    
    if len(phone)!=10 or not phone[:3].isdigit():
        invalid_phone[phone]+=1


def is_phone(elem):
    return (elem.attrib['k'] == "phone")

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = collections.defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def audit_phone_(osmfile):
    osm_file = open(osmfile, "r")
    invalid_phone = collections.defaultdict(int)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_phone(tag):
                    audit_phone(invalid_phone,tag.attrib['v'])
    return invalid_phone


def update_name(name, mapping):
    r=street_type_re.search(name)
    if r:
        street_type=r.group()
        if street_type in mapping:
            name=re.sub(street_type_re,mapping[street_type],name)
    return name

def update_phone(phone):
    new_phone=""
    for i in phone:
        if str(i) in ('1234567890'):
            new_phone+=str(i)
            new_phone=new_phone[-10:]
    return new_phone
