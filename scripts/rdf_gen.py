from collections import defaultdict

import pandas as pd
import numpy as np


def print_predicates(subject, triples, indent=4):
    indent = " " * indent
    sep = f"\n{indent*2}, "

    print(f'<#{subject}>')

    last = len(triples) - 1
    for i, (predicate, objects) in enumerate(triples.items()):
        obj_list = sep.join(objects)
        end = "." if i >= last else ";"

        print(f"{indent}{predicate} {obj_list} {end}")


def print_user(uid, age, sex, country):
    triples = defaultdict(list)

    triples['rdf:type'].append("def:Person")

    if pd.notna(age):
        triples['val:age'].append(f'"{int(age)}"^^xsd:integer')

    if pd.notna(country):
        triples['val:country'].append(f'<#{country}>')

    if pd.notna(sex):
        if sex.lower() == "female":
            triples['val:sex'].append('<#female>')
        elif sex.lower() == "male":
            triples['val:sex'].append('<#male>')

    print_predicates(f'U{uid}', triples)


def print_trackable(tid, ttype, name):
    definitions = ["def:Trackable", f"def:{ttype}"]
    if ttype == 'Symptom' or ttype == 'Tag':
        definitions.append("mesh:D012816")
    elif ttype == 'Condition':
        definitions.append("mesh:D003214")
    elif ttype == 'Food':
        definitions.append("mesh:D005502")
    elif ttype == 'Weather':
        definitions.append("mesh:D014887")

    print_predicates(f"T{tid}", {
        'rdf:type': definitions,
        'rdfs:label': [f'"{name}"']
    })


def print_checkin(uid, tid):
    print(f'<#U{uid}> val:checkin <#T{tid}> .')



namespace = "kb"
prefixes = {
    'def':      f"http://localhost:9999/blazegraph/{namespace}/def#",
    'val':      f"http://localhost:9999/blazegraph/{namespace}/val#",
    'rdf':      "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    'rdfs':     "http://www.w3.org/2000/01/rdf-schema#",
    'xsd':      "http://www.w3.org/2001/XMLSchema#",
    'owl':      "http://www.w3.org/2002/07/owl#",
    'meshv':    "http://id.nlm.nih.gov/mesh/vocab#",
    'mesh':     "http://id.nlm.nih.gov/mesh/"
}
print(f"@base <http://localhost:9999/blazegraph/{namespace}> .")
for prefix, uri in prefixes.items():
    print(f"@prefix {prefix}: <{uri}> .")

print("""
def:Person rdf:type rdfs:Class .
def:Sex rdf:type rdfs:Class .
<#male> rdf:type def:Sex .
<#female> rdf:type def:Sex .
def:Country rdf:type rdfs:Class .

val:age
    rdf:type rdf:Property ;
    rdf:range xsd:integer ;
    rdf:domain def:Person .
val:sex
    rdf:type rdf:Property ;
    rdf:range def:Sex ;
    rdf:domain def:Person .
val:country
    rdf:type rdf:Property ;
    rdf:range def:Country ;
    rdf:domain def:Person .

def:Trackable rdf:type rdfs:Class .
def:Sympton rdf:type def:Trackable .
def:Treatment rdf:type def:Trackable .
def:Condition rdf:type def:Trackable .
def:Tag rdf:type def:Trackable .
def:Weather rdf:type def:Trackable .
def:Food rdf:type def:Trackable .

val:checkin
    rdf:type rdf:Property ;
    rdf:range def:Trackable ;
    rdf:domain def:Person .
""")

data = pd.read_csv('flaredown.csv')
trackables = data[['trackable_id', 'trackable_type', 'trackable_name']].drop_duplicates('trackable_id')
users = data[['user_id', 'age', 'sex', 'country']].drop_duplicates('user_id')
countries = sorted(data['country'].dropna().unique())

for country in countries:
    print(f'<#{country}> rdf:type def:Country .')
print()

trackables.apply((
    lambda row: print_trackable(row['trackable_id'], row['trackable_type'], row['trackable_name'])
), 'columns')
print()

users.apply((
    lambda row: print_user(row['user_id'], row['age'], row['sex'], row['country'])
), 'columns')
print()

data.apply((
    lambda row: print_checkin(row['user_id'], row['trackable_id'])
), 'columns')
print()
