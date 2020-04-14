# April 2020
# Coded by Chris Min <infosechris@gmail.com>

import requests, csv
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup

#print("IMDB, TV Show Ratings Chart Display")

validUrl = True
while validUrl:

    # url1 = input("What is the IMDB TV Series URL: ")
    # url1 = url1.split('?', 1)[0]
    # if url1[-1] == '/':
    #     pass
    # elif url1[-1] == 'c':
    #     url1 = 'https://www.imdb.com/title/tt0306414/'
    # else:
    #     url1 += '/'

    title_search = input("IMDB TV Series Title Search: ")
    title_search = title_search.replace(' ', '+')
    url_search = 'https://www.imdb.com/find?q=' + title_search + '&ref_=nv_sr_sm'

    html_search = requests.get(url_search).text
    soup_search = BeautifulSoup (html_search, 'html.parser')
       
    try:
        href_list = []
        for link in soup_search.find_all('a', href=True):
            href_list.append(link['href'])

        title_list = []
        i=0
        for title in href_list:
            if '/title/t' in href_list[i]:
                title_list.append(href_list[i])
            i+=1
        
        season = 1
        url1 = 'https://www.imdb.com' + title_list[0]
        url2 = 'episodes?season='
        url3 = str(season)
        url4 = url1 + url2 + url3
        html = requests.get(url4).text
        soup = BeautifulSoup (html, 'html.parser')
        t1 = soup.find('h3', attrs={'itemprop': 'name'})
        titleyear = t1.text.split()
        validUrl = False
        print ('Found the Title! Processing....')
    except:
        print ('Cannot find this TV Series Title on IMDB.\n')

if titleyear[-1] == ')':
    year = titleyear[-2] + titleyear[-1]
    del titleyear[-1]
    del titleyear[-1]
else:
    year = titleyear[-1]
    del titleyear[-1]

title = ""
for i in range(0, len(titleyear)):
    if i == 0:
        title += titleyear[i]
    else:
        title += ' ' + titleyear[i]

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

#print ('Total Seasons:', len(seasons), '\n')
print ("Begin searching through ratings for all seasons and episodes...")
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

    csvR.append(rating)

    #print ("Season:", season, 'of', len(seasons))
    #print ("Episodes:", eps)
    #print ("Ratings:", rating, "\n")

tempE = []
i=1
while i <= epsMax:
    tempE.append(i)
    i+=1

csvE = []
csvE.append(tempE)

#print(csvR)
#print(csvE)
print ('Loop Completed! Creating Heatmap...')

with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(csvE)
    writer.writerows(csvR)

data = pd.read_csv(r'C:\Temp\Python\out.csv')
df = pd.DataFrame(data)
df.index = np.arange(1,len(df)+1)

ax = sns.heatmap(df, linewidths=.5, annot=True, cmap="RdYlGn", square=True, cbar_kws={'label': '\n\nApplication & Heatmap\nby infosechris@gmail.com'})

plt.title(title + ' ' + year, pad=20, size=16)
plt.ylabel('Seasons', labelpad=30, rotation=0)
plt.xlabel('Episodes', labelpad=10)

#ax.xaxis.tick_top()
ax.invert_yaxis()
plt.yticks(rotation=0)
plt.xticks(rotation=0)

fig = plt.gcf()
figsize = fig.get_size_inches()
fig.set_size_inches(figsize * 1.5)

if epsMax >= 100:
    fig.set_figwidth(80)
elif epsMax >= 35:
    fig.set_figwidth(25)
elif epsMax >= 26:
    fig.set_figwidth(20)
elif epsMax >= 15:
    fig.set_figwidth(15)
    
fig.savefig(title + ' ' + year + '.png')

print ('Heatmap Image Saved!\n')