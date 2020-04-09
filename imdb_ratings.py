import requests
from bs4 import BeautifulSoup

season = 1
perEP = 0

url = 'https://www.imdb.com/title/tt0944947/' + 'episodes?season=' + str(season)
html = requests.get(url).text
soup = BeautifulSoup (html, 'html.parser')

t_seasons = []
for option in soup.find_all('option'):
    temp = option.text.split()
    t_seasons.append(temp)

c_seasons = [x for x in t_seasons if x]

seasons = []
for i in range(0, len(c_seasons)):
    k = int(c_seasons[i][0])
    if k <= 1000:
        seasons.append(c_seasons[i][0])
print (seasons)

#for i in range(0,len(season[0]))
#    print(season[i])

#for div in soup.body.find_all('div', attrs={'class': 'seasonAndYearNav'}):
 #   s = div.find('select', class_='current')
 #   print (s)

#epN = 0
#for div in soup.body.find_all('div', attrs={'class': 'ipl-rating-star small'}):
#    rating = div.find('span', class_='ipl-rating-star__rating')
#    epN += 1