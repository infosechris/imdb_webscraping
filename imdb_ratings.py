#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# April 2020
# Coded by Chris Min <infosechris@gmail.com>

import warnings
warnings.filterwarnings("ignore", "(?s).*MATPLOTLIBDATA.*", category=UserWarning)

import requests, csv, os
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup

#Whole code in to a while loop to check if user is done with it
done = False
while done == False:
    #print("IMDB, TV Show Ratings Chart Display")

    #Check if URL is valid, try and exception
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

        #User input title, search on IMDB, result in page with seasons
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
            print ('Found the Title on IMDB!')
        except:
            print ('Cannot find this TV Series Title on IMDB.\n')

    #Years on IMDB goes two ways, it's to check and delete last char accordingly
    if titleyear[-1] == ')':
        year = titleyear[-2] + titleyear[-1]
        del titleyear[-1]
        del titleyear[-1]
    else:
        year = titleyear[-1]
        del titleyear[-1]

    #Extracting Title
    title = ""
    for i in range(0, len(titleyear)):
        if i == 0:
            title += titleyear[i]
        else:
            title += ' ' + titleyear[i]

    #To get Seasons and Years
    t_seasons = []
    for option in soup.find_all('option'):
        stemp = option.text.split()
        t_seasons.append(stemp)

    c_seasons = [x for x in t_seasons if x]

    #Extract only the Seasons
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

    #Go through each seasons and get ratings per Eps
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

        #Ratings in to a list
        csvR.append(rating)

        #print ("Season:", season, 'of', len(seasons))
        #print ("Episodes:", eps)
        #print ("Ratings:", rating, "\n")

    #Eps in to a list
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

    #Create CSV file with Eps and Ratings
    csv_path = r"C:\Temp\Python\imdb_webscrapper\out.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(csvE)
        writer.writerows(csvR)
    
    #Read the CSV file and put it in a dataframe
    data = pd.read_csv(csv_path)
    df = pd.DataFrame(data)
    df.index = np.arange(1,len(df)+1)

    #Rest is to create a heatmap, adjustments to size, label, display
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
        fig.set_figwidth(20)
    #elif epsMax >= 25:
        #fig.set_figwidth(20)
    elif epsMax >= 16:
        fig.set_figwidth(15)

    if season >= 100:
        fig.set_figheight(80)
    elif season >= 35:
        fig.set_figheight(20)
    #elif season >= 25:
        #fig.set_figheight(20)
    elif season >= 20:
        fig.set_figheight(15)

    title = title.replace(':','')
    title = title.replace('?','')
    filename = title + ' ' + year + '.png'

    #If the screenshot already exist, remove it
    ss_path = r"C:\Temp\Python\imdb_webscrapper\screenshots\\"
    if os.path.exists(ss_path + filename):
        os.remove(ss_path + filename)

    #Save the heatmap as .PNG file
    fig.savefig(ss_path + filename)

    print ('Heatmap Image Saved!\n')

    #Opens the image once it's done
    os.startfile(ss_path + filename)

    #Asking if user is done with the application
    #Only way to break/exit the entire while loop initated at the start
    loopo = True
    notaskingagain = 0
    while loopo:
        finish = input("Run Search Again? (Y/N): ")
        if finish == 'N' or finish == 'n':
            print ("Application Closed\n")
            done = True
            loopo = False
        elif finish == 'y' or finish == 'y':
            loopo = False
            print ('\n')
        else:
            print ("Not a valid answer, please type Y or N\n")
            notaskingagain += 1
        
        if notaskingagain == 3:
            print ("Application Closed\n")
            done = True
            loopo = False