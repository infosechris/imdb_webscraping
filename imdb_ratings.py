import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import csv
import sys

season = 1
perEP = 0

url1 = 'https://www.imdb.com/title/tt0903747/'
url2 = 'episodes?season='
url3 = str(season)
url4 = url1 + url2 + url3
html = requests.get(url4).text
soup = BeautifulSoup (html, 'html.parser')

t1 = soup.find('h3', attrs={'itemprop': 'name'})
titleyear = t1.text.split()
if titleyear[-1] == ')':
    year = titleyear[-2] + titleyear[-1]
    del titleyear[-1]
    del titleyear[-1]
else:
    year = titleyear[-1]
    del titleyear[-1]

title = ""
for i in range(0, len(titleyear)):
    title = title + " " + titleyear[i]

print ('Title: ' + title + '\nYears: ' + year)

t_seasons = []
for option in soup.find_all('option'):
    stemp = option.text.split()
    t_seasons.append(stemp)

c_seasons = [x for x in t_seasons if x]

seasons = []
for i in range(0, len(c_seasons)):
    if c_seasons[i][0].isnumeric():
        k = int(c_seasons[i][0])
        if k <= 1000:
            seasons.append(c_seasons[i][0])
    else:
        seasons.append(c_seasons[i][0])

print ('Total Seasons:', len(seasons), '\n')

#array = np.array([])
#f = open(sys.argv[1], 'wt')
#writer = csv.writer(f)

csvR = []
epsMax = 0
for season in range(1, len(seasons)+1):
    url4 = url1 + url2 + str(season)
    html = requests.get(url4).text
    soup = BeautifulSoup (html, 'html.parser')

    rating = []
    eps = []
    counter = 0
    for div in soup.body.find_all('div', attrs={'class': 'ipl-rating-star small'}):
        rtemp = div.find('span', class_='ipl-rating-star__rating')
        rating.append(rtemp.text)
        counter += 1
        eps.append(counter)
        
        if epsMax < counter:
            epsMax = counter   

    csvR.append([season] + rating)

tempE = ['']
i=1
while i <= epsMax:
    tempE.append(i)
    i+=1

csvE = []
csvE.append(tempE)

print(csvR)
print(csvE)

with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(csvE)
    writer.writerows(csvR)

    #print ("Season:", season, 'of', len(seasons))
    #print ("Episodes:", eps)
    #print ("Ratings:", rating, "\n")


    #rating.insert(len(rating),'n')
    #tempA = np.array(rating)
    #array = np.append(array, tempA, axis=0)

data = pd.read_csv(r'C:\Temp\Python\out.csv')
df = pd.DataFrame(data)

plt.imshow(df, cmap="YlGnBu")
plt.colorbar()
plt.xticks(range(len(df.columns)),df.columns)
plt.yticks(range(len(df.index)),df.index)
plt.show()