from lxml import etree

import pandas as pd
import numpy as np



def print_user(uid, age, sex, country):
    user = etree.Element('user', {'id': uid})

    if pd.notna(age):
        elem = etree.Element('age')
        elem.text = f'{age:.0f}'
        user.append(elem)

    if pd.notna(country):
        elem = etree.Element('country')
        elem.text = country
        user.append(elem)

    if pd.notna(sex):
        elem = etree.Element('sex')
        elem.text = sex
        user.append(elem)

    return user


def print_trackable(tid, ttype, name):
    trackable = etree.Element(ttype.lower(), {'id': str(tid)})

    label = etree.Element('label')
    label.text = name
    trackable.append(label)

    return trackable


def print_checkin(uid, tid, value, date, users):
    user = users.xpath(f"//user[@id='{uid}']")[0]
    checkin = etree.Element('checkin')
    user.append(checkin)

    elem = etree.Element('date')
    elem.text = date
    checkin.append(elem)

    elem = etree.Element('trackable')
    elem.text = str(tid)
    checkin.append(elem)

    if pd.notna(value):
        elem = etree.Element('value')
        elem.text = value
        checkin.append(elem)

    return user


header = '<?xml version="1.0" encoding="UTF-8" ?>'

data = pd.read_csv('dados/flaredown.csv')
trackables = data[['trackable_id', 'trackable_type', 'trackable_name']].drop_duplicates('trackable_id')
users = data[['user_id', 'age', 'sex', 'country']].drop_duplicates('user_id')
countries = sorted(data['country'].dropna().unique())

trackel = etree.Element('trackables')
trackables = trackables.apply((
    lambda row: print_trackable(row['trackable_id'], row['trackable_type'], row['trackable_name'])
), 'columns')
for trackable in trackables:
    trackel.append(trackable)

with open('dados/trackables.xml', 'w') as tfile:
    tfile.write(header)
    tfile.write('\n')
    tfile.write(etree.tostring(trackel, encoding='unicode', pretty_print=True))

usersel = etree.Element('users')
users = users.apply((
    lambda row: print_user(row['user_id'], row['age'], row['sex'], row['country'])
), 'columns')
for user in users:
    usersel.append(user)

data = data.apply((
    lambda row: print_checkin(row['user_id'], row['trackable_id'], row['trackable_value'], row['checkin_date'], usersel)
), 'columns')

with open('dados/users.xml', 'w') as ufile:
    ufile.write(header)
    ufile.write('\n')
    ufile.write(etree.tostring(usersel, encoding='unicode', pretty_print=True))
