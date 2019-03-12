
# this is the web scrapping of a playground and park dataset of the city of Pittsburgh, using geoJSON api
# convert the geoJSON into csv, and merged table from "playground.csv" to add the neighborhood name to playgrounds and parks



import requests # to parse url to json
import csv
import pandas as pd


# pittsburgh playground dataset from WPRDC.org
# this is a geoJSON
json_data = requests.get("https://data.wprdc.org/dataset/37e7a776-c98b-4e08-ad61"
                         "-a8c8e23ec9ab/resource/12d59d62-e86d-4f37-af19-463050496ed6/download/playgrounds_img.geojson").json()


#drop the geometry feature on original geoJSON file with longitude and latitude information
#extract the features that we need
p_id = []
imageURL = []
street = []
playground_name = []
park = []
maintenance_responsibility = []

for i in range(len(json_data['features'])):
    p_id.append(json_data['features'][i]['properties']['id'])
    imageURL.append(json_data['features'][i]['properties']['image'])
    playground_name.append(json_data['features'][i]['properties']['name'])
    park.append(json_data['features'][i]['properties']['park'])
    maintenance_responsibility.append(json_data['features'][i]['properties']['maintenance_responsibility'])
    street.append(json_data['features'][i]['properties']['street'])


dct1 = {'ID': p_id,
          'Park': park,
          'Playground': playground_name,
'Street': street,
'Maintenance_responsibility': maintenance_responsibility,
'ImageURL': imageURL}



# feature engineering: merge two tables with same id and add the neighborhood name
neighborhood = []
id_new = []
file = open("playground_neighborhood.csv")
for line in file:
    id_new.append(line.split(",")[0])
    neighborhood.append(line.split(",")[1])
id_new.pop(0) # get rid of the header, leave only values
neighborhood.pop(0) # get rid of the header, leave only values
id_new.pop(120) # make sure they are the same length as the previous JSON output
neighborhood.pop(120)
id_new.pop(119)
neighborhood.pop(119)
dict2 = {'Neighborhood': neighborhood}
dct1.update(dict2)


# 119 rows × 7 columns
df = pd.DataFrame(dct1)



df.to_csv("playground_park_neighborhood.csv")



