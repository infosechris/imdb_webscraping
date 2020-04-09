import requests
from bs4 import BeautifulSoup

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
year = titleyear[-1]
del titleyear[-1]

title = ""
for i in range(0, len(titleyear)):
    title = title + " " + titleyear[i]

print ('Title: ' + title + '\nYear(s): ' + year)

t_seasons = []
for option in soup.find_all('option'):
    stemp = option.text.split()
    t_seasons.append(stemp)

c_seasons = [x for x in t_seasons if x]

seasons = []
for i in range(0, len(c_seasons)):
    k = int(c_seasons[i][0])
    if k <= 1000:
        seasons.append(c_seasons[i][0])

print ('Total Seasons:', seasons[-1], '\n')

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

    print ("Season:", season)
    print ("Episodes: ", eps)
    print ("Ratings: ", rating, "\n")

    