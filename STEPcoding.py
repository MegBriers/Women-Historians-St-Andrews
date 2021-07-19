# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 13:51:02 2021

@author: Meg
"""

import os
import shutil
import time

import folium
import imageio
import webbrowser
import zipfile
import json
import fileinput

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from os import path
from branca.colormap import linear
from selenium import webdriver
from PIL import Image
from pathlib import Path

path = 'C:/Users/Meg/Desktop'

data = pd.read_excel('Location Of Graduates.xlsx')

list_lat = []
list_long = []

for i in range(0,61):
    letter_list = data.iloc[i]['Latitude, Longitude'].split(",")
    if len(letter_list) > 1:
        list_lat.append(float(letter_list[0]))
        list_long.append(float(letter_list[1]))

list_of_years = ['1906', '1914', '1923','1935', '1945', '1955', '1965', '1975']


# Turn ZoomControl off in each html file


from folium.plugins import FloatImage
image_file = 'C:/Users/Meg/Desktop/image2crop.PNG'

for i in range(len(list_of_years)):

    m_i = folium.Map(location=[55,-1], zoom_start=5, tiles="OpenStreetMap")


    FloatImage(image_file, bottom=50, left=0).add_to(m_i)
    
    # Add year label to the map
    title_html = '''
                 <h3 align="left" style="font-size:22px"><b>{}</b></h3>
                 '''.format('Year: ' + str(list_of_years[i]))   
    m_i.get_root().html.add_child(folium.Element(title_html))
    
    # add all the markers 
    markers = [[list_lat[j], list_long[j],data.iloc[j]['Class']] for j in range(len(data)) if str(int(data.iloc[j]['Graduation Year'])) == list_of_years[i]]
    
    colors = ['red','blue','yellow']
    # add all the markers
    for k in range(len(markers)):
        degreeClass = int(markers[k][2])
        colorz = colors[degreeClass - 1]
        print(colorz)
        folium.CircleMarker(
        location=[markers[k][0], markers[k][1]],
        radius=7,
        fill_color=colorz, 
        color = 'black',
        fill_opacity=1
        ).add_to(m_i)
        
    #print(i)
    m_i.save('GifMap/total_perYear_' + str(list_of_years[i]) + '.html')
    

for i in range(len(list_of_years)):
    with fileinput.FileInput('GifMap/total_perYear_' + str(list_of_years[i]) + '.html', inplace=True) as file:
        for line in file:
            print(line.replace('zoomControl: true', 'zoomControl: false'), end='')


# Turn ZoomControl off in each html file

for i in range(len(list_of_years)):
    with fileinput.FileInput('GifMap/total_perYear_' + str(list_of_years[i]) + '.html', inplace=True) as file:
        for line in file:
            print(line.replace('zoomControl: true', 'zoomControl: false'), end='')

# Convert html files to png (screenshot each html page)

# We use a delay because we dont want to take a screenshot of the browser before the map is loaded
delay=5

os.chdir(path)

for i in range(len(list_of_years)):
    fn='GifMap/total_perYear_' + str(list_of_years[i]) + '.html'
    tmpurl='file://{path}/{mapfile}'.format(path=os.getcwd(),mapfile=fn)

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)

    browser = webdriver.Chrome()
    browser.get(tmpurl)

    #Give the map tiles some time to load
    time.sleep(delay)
    browser.save_screenshot('GifMap/total_perYear_' + str(list_of_years[i]) + '.png')
    browser.quit()
    
    #remove html files
    #os.remove('total_perYear_' + str(list_of_years[i]) + '.html')
# Create Gif and remove each .png file

image_path = Path()

images = list(image_path.glob('GifMap/*.png'))
image_list = []
for file_name in images:
    image_list.append(imageio.imread(file_name))
    os.remove(file_name)
    
imageio.mimwrite('GifMap.gif', image_list, fps=2)