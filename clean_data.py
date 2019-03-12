#DFP project
#Clean data
#Author: Yuwei Zhu

#import module
import pandas as pd
import re

#read file
data_houseprice = pd.read_csv('data_houseprice.csv')
del data_houseprice['Unnamed: 0']

data_demo = pd.read_csv('demographic.csv')
data_demo = data_demo.dropna()

#playground and park
df_playground = pd.read_csv("playground_park_neighborhood.csv")

#clean data: drop useless columns
del df_playground['Unnamed: 0']
del df_playground['ImageURL']
del df_playground['ID']
neighborhood = [i.strip() for i in df_playground['Neighborhood']] # get rid of /r and /n

#update playground and park df
df_playground['Neighborhood'] = neighborhood

#clean demographic data
#first delete some useless columns
del data_demo['% Pop. Change, 00-10']
del data_demo['Total Street Miles']
del data_demo['#Part 2 Reports (2010)']
del data_demo['#Other Police Reports (2010)']
del data_demo['Part 2 Crime per 100 Persons (2010)']
del data_demo['Resident Jobs: Other']

#join demogaphic and playground data first because they have similari niegoborhood naming
# merge playground and park onto the previous merged table
data_demo = data_demo.merge(df_playground, left_on = 'Neighborhood', right_on = 'Neighborhood', how = 'outer')

#rename columns
data_demo.columns = ['Neighborhood', 'Sectors', 'Population','Pop % of City', 'Major Roads', 'Street Density',
                            'Major Crime Report', 'Crime %', '# Playgrounds',
                            'Jobs:Construction', 'Jobs:Manufacturing', 'Jobs:Retail', 'Jobs:Transportation', 'Jobs:Information',
                            'Jobs: Finance', 'Jobs:Science', 'Jobs:Educ', "Jobs: Arits", 'Jobs: Public',
                     'Park', 'Playground','Street','Maintenance_responsibility']
data_houseprice.columns = ['Address', 'Neighborhood', 'Price', 'Beds', 'Baths']

#deal with data type
#some of columns in data_demo represent as str format to represent percentage instead of number
percent_col = ['Pop % of City', 'Jobs:Construction', 'Jobs:Manufacturing', 'Jobs:Retail', 'Jobs:Transportation', 'Jobs:Information',
                            'Jobs: Finance', 'Jobs:Science', 'Jobs:Educ', "Jobs: Arits", 'Jobs: Public']


for i in percent_col:
    number_list = []
    for m in data_demo[i]:
        x = round((float(m.strip("%")) / 100), 2)
        number_list.append(x)
    data_demo[i] = number_list

#change population column data type
pop_list = []
for i in data_demo['Population']:
    if re.search(',',i):
        n = i.replace(',', '')
        x = float(n)
    else:
        x = float(i)
    pop_list+=[x]

data_demo['Population'] = pop_list

#deal with $ in house price data
price_list = []
for i in data_houseprice['Price']:
    if re.search(r'(\$).*\,.*',i):
        i = i.replace(',','')
        i = i.replace('$','')
        x = float(i)
    else:
        x = i
    price_list += [x]

data_houseprice['Price'] = price_list

#transform Beds and baths columns
beds_list = []
bath_list = []

for i in data_houseprice['Beds']:
    try:
        i = round(float(i),0)
    except:
        i = 0
    beds_list += [i]


for i in data_houseprice['Baths']:
    try:
        i = round(float(i),0)
    except:
        i = 0
    bath_list += [i]

data_houseprice['Beds'] = beds_list
data_houseprice['Baths'] = bath_list

#we are planning to use Neighborhood as primary key to merge
#However, these two tables have different neighborhood names
#In house price tables, we didn't differenciate south, west, east, north and center part of a neighborhood
neighbor = data_demo.Neighborhood
pat = r'south|north|west|east|central'
neighbor = neighbor.str.lower()
bool_index = neighbor.str.contains(pat)

#look at unique neiborhood names in house price data
house_ne = data_houseprice.Neighborhood.unique()
redudent_ne = data_demo[bool_index].Neighborhood

print(redudent_ne)

#Next we search for these duplicated keys to find the value in house price dataset
pat1 = r'Allegheny'
pat2 = r'Northside'
pat3 = r'Carnegie'
pat4 = r'Hills'
pat5 = r'Liberty'
pat6 = r'Homewood'
pat7 = r'Oakland'
pat8 = r'Shore'
pat9 = r'Perry'
pat10 = r'Breeze'
pat11 = r'Side'
pat12 = r'Squirrel Hill'
pat13 = r'End'
pat14 = r'Westwood'
pat15 = r'Lawrenceville'

pat = [pat1, pat2, pat3, pat4, pat5, pat6, pat7, pat8, pat9, pat10, pat11, pat12, pat13, pat14, pat15]

match = {}
for i in house_ne:
    for pattern in pat:
        if re.search(pattern, i):
            if pattern in match:
                match[pattern].append(i)
            else:
                match[pattern] = [i]


print(match)


#if we find single match, we can replace it. For multiple matches, we leave it as it is.
new_match = {}
for key,value in match.items():
    if len(value) == 1:
        new_match[key] = ''.join(value)


print(new_match)



#based on match result, we modify our demographic table
#replace neighborhood with modified name
for i in data_demo.Neighborhood:
    for key, value in new_match.items():
        if re.search(key, i):
            data_demo.Neighborhood = data_demo.Neighborhood.replace(i,value)


data_demo = data_demo.drop_duplicates(subset=['Neighborhood'])


#merge two tables
df = data_demo.merge(data_houseprice, left_on='Neighborhood', right_on='Neighborhood', how = 'outer')

# merge playground and park onto the previous merged table
#df1 = df.merge(df_playground, left_on = 'Neighborhood', right_on = 'Neighborhood', how = 'outer')

#write clean data csv file
df.to_csv('clean_all.csv')

