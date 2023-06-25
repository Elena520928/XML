import os
import sys
import datetime

import requests
from lxml import etree
import xml.etree.ElementTree as ET

import lxml
from lxml import etree, objectify
from lxml.etree import XMLSyntaxError


xml_url = "https://www.cbr.ru/scripts/XML_daily.asp"
response_xml = requests.get(xml_url)
a = response_xml.text
a1 = a[45:]
print(a1)
fw = open('../tests/xml1.xml', 'w', encoding='utf-8')
fw.write(a1)

xsd_url = "http://www.cbr.ru/StaticHtml/File/92172/ValCurs.xsd"
response_xsd = requests.get(xsd_url)
b = response_xsd.text
fww = open('../tests/xsd1.xsd', 'w', encoding='utf-8')
fww.write(b)
fww.close()
fww = open('../tests/xsd1.xsd', 'r', encoding='utf-8')
content = fww.readlines()
content = content[1:]
fww.close()
fww = open('../tests/xsd1.xsd', 'w', encoding='utf-8')
for i in content:
    fww.write(i + "\n")
fww.close()

try:
    schema = etree.XMLSchema(file='xsd1.xsd')
    parser = objectify.makeparser(schema = schema)
    objectify.fromstring(a1,parser)
    print("validated")
    b = 'validated'
except XMLSyntaxError:
    print ("not validated")
    pass

if b == "validated":
    response_body_as_xml = ET.fromstring(response_xml.content)
    xml_tree = ET.ElementTree(response_body_as_xml)
    root = xml_tree.getroot()
    for valute in root.findall('Valute'):
        a = []
        id = valute.get('ID')
        if id == '':
            print("отсутствует id валюты")
        numcode = valute.find('NumCode').text
        charcode = valute.find('CharCode').text
        if charcode is None:
            print("отсутствует charcode валюты")
        nominal = valute.find('Nominal').text
        name = valute.find('Name').text
        if name is None:
            print("отсутствует name валюты")
        value = valute.find('Value').text
        if value is None:
            print("отсутствует value валюты")
        a.append(id)
        try:
            a.append(numcode)
        except NameError:
            a.append('')
        a.append(charcode)
        a.append(nominal)
        a.append(name)
        a.append(value)
        print(a)

cur_cod_num = open('cur_code_num', 'r', encoding='utf-8')
cur_cod_num = cur_cod_num.read()

for valute in root.findall('Valute'):
    numcode = valute.find('NumCode').text
    if numcode in cur_cod_num:
        print(numcode)
        print("числовой код валюты " + numcode + " соответстсвует справочному значению")
    else:
        print("числовой код валюты " + numcode + " не соответствует справочному значению")


cur_cod_char = open('cur_code_char', 'r', encoding='utf-8')
cur_cod_char = cur_cod_char.read()

for valute in root.findall('Valute'):
    charcode = valute.find('CharCode').text
    if charcode in cur_cod_char:
        print(charcode)
        print("числовой код валюты " + charcode + " соответстсвует справочному значению")
    else:
        print("числовой код валюты " + charcode + " не соответствует справочному значению")


for valute in root.findall('Valute'):
    nominal = valute.find('Nominal').text
    list = ["1","10","100","1000","10000"]
    if nominal in list:
        print("значение номинала " + nominal + " корректно")
    else:
        print("значение номинала " + nominal + " не корректно")

for valute in root.findall('Valute'):
    value = valute.find('Value').text
    value_1 = value.replace(',','.')
    try:
        value_2 = float(value_1)
        print(value_2)
    except ValueError:
        print("could not convert string to float for value" + value)


for valute in root.findall('Valute'):
    value = valute.find('Value').text
    value_1 = value.replace(',', '.')
    try:
        value_2 = float(value_1)
        print(type(value_2))
    except ValueError:
        print("could not convert string to float for value " + value)

    if type(value_2) is float:
        print("значение переменной " + str(value_2) + " числовое")
    else:
        print("значение переменной " + str(value_2) + " не числовое")



















