from urllib.request import urlopen  # b_soup_1.py
from bs4 import BeautifulSoup
import string
import re
html = urlopen('http://www.city-data.com/zipmaps/Pittsburgh-Pennsylvania.html')

bsyc = BeautifulSoup(html.read(),"html.parser")

fout = open('bsyc_citizen.txt', 'wt', encoding='utf-8')

fout.write(str(bsyc))

fout.close()

zipdata_list = bsyc.findAll('div',{'class':'zip data-block'})
print('there are', len(zipdata_list), 'zip data-block')
dataout=open('demo.csv','wt',encoding='utf-8')
for t in zipdata_list:
    zipcode=str(t)[56:62]
    print(zipcode)
    population=str(t)[140:196].translate(str.maketrans('<br/>','     '))
    population=re.sub(r'\s+',' ',population)
    population=re.sub(r',','',population)
    print(population)
    dataout.write(zipcode+",")
    dataout.write(population+'\n')
