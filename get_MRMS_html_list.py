# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from bs4 import BeautifulSoup
import requests
import re
import os
from pathlib import Path

"""
# MRMS_MergedReflectivityComposite_00.00_20190309-180440.grib2.gz
"""

dateMatch = re.compile('[0-9]{8}')
hourMatch = re.compile('(?<=-)[0-9]{2}')

baseDst = 'C:/data/'
#baseDst = '/home/tj/data/'

URLbase = "http://mrms.ncep.noaa.gov/data/2D/"
mrmsProds = ['ReflectivityAtLowestAltitude','MESH_Max_30min','RotationTrack30min','RotationTrackML30min','H60_Above_-20C']
searchStr = 'MRMS'

for prod in mrmsProds:
    urlBase = URLbase + prod + "/"
    url = urlBase + "?C=M;O=D"

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    for link in soup.find_all('a'):
        fName = str(link.get('href'))
        if searchStr in fName:
            dateMatches = dateMatch.search(fName)
            hourMatches = hourMatch.search(fName)            
            if dateMatches != None and hourMatches != None:
                dateStr = str(dateMatches.group())
                hourStr = str(hourMatches.group())
                dstDir = os.path.join(baseDst,r"MRMS",dateStr,hourStr,prod) + '/'
                dst = os.path.join(dstDir,fName)
                src = urlBase + fName
                os.makedirs(dstDir, exist_ok=True)

                my_file = Path(dst)
                if my_file.is_file():
                    pass
                elif dateStr == '20190314':
                    print(str(fName))
                    r = requests.get(src)
                    open(dst, 'wb').write(r.content)

"""
dstDir = baseDst + 'VWP/'
urlBase = 'https://climate.cod.edu/data/nexrad/GRR/NVW/'
url = urlBase + "?C=M;O=D"
page2 = requests.get(url)
soup2 = BeautifulSoup(page2.content, 'html.parser') 

for link in soup2.find_all('a'):
    fName = str(link.get('href'))
    #print(fName)

    newURL = urlBase + fName
    have = alreadyHave(dstDir,'g0tA')
    if re.search(r'g0tA',newURL) and fName not in have:
        print('new one!  ',fName )
        urlList.append(newURL)
        r = requests.get(newURL)
        dst = os.path.join(dstDir,fName)
        open(dst, 'wb').write(r.content)
"""