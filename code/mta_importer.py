import csv
import pandas as pd
from bs4 import *
import urllib
import re

"""The primmary selector method, run this in order to pull from MTA website
    This can be used as a module to specify two dates, which will then pull
    the relevant files from the MTA website and compile them into one panda
    file.
    It also gives an option if you want to save a csv related with the file
"""
def mta_selector():
    #Define date period
    ds=input('Enter start Date (mm-dd-yy): ')
    de=input('Enter End Date (mm-dd-yy): ')
    #Run mta_updater which returns an updated list of links from MTA website
    links=mta_updater()
    sel=mta_importer(ds,de,links)
    df_list=[]
    clicks=0
    for url in links[sel[0]:sel[1]+1]:
        df_list.append(pd.read_csv(url[1],header=0))
        clicks+=1
        print ('%d/%d completed' % (clicks,sel[1]-sel[0]))

    #df_list=[(pd.read_csv(url[1],header=0),print() for url in links[sel[0]:sel[1]+1]]
    df=pd.concat(df_list,ignore_index=True)

    #Write to csv file
    csv_q=input('Do you want to write to csv (y/n): ')

    if csv_q[0]=='y' or csv_q[0]=='Y':
        name=input('CSV file name: ')
        df.to_csv(name, sep=',')

    return df

#Find all the data files on MTA website
def mta_updater():
    prefix='http://web.mta.info/developers/'
    html='http://web.mta.info/developers/turnstile.html'
    webv=urllib.request.urlopen(html)
    soup=BeautifulSoup(webv,"lxml")
    tags = soup('a')
    linkslist=[]
    for tag in tags:
        h=tag.get('href',None)
        if h is not None:
            if h.startswith('data'):
                dates=re.findall('.[_]([0-9]+)',h)[0]
                linkslist.append((int(dates),prefix+h))
    return linkslist

#Return the index of the files for the start and end dates
def mta_importer(ds,de,links):
    start=int(ds[-2:]+ds[0:2]+ds[3:5])
    end=int(de[-2:]+de[0:2]+de[3:5])
    i=0
    for date_end in links:
        if end >= date_end[0]+7:
            start_ind=i
            d_e=date_end[0]
            break
        else:
            i=i+1
    for date_start in links[start_ind:]:
        if start >= date_start[0]:
            end_ind=i
            d_s=date_start[0]
            break
        else:
            i+=1
    print ('Date Range: %s to %s' % (d_s,d_e))
    return ([start_ind,end_ind])
