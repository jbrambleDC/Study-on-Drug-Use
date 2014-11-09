from bs4 import BeautifulSoup as bs
from requests import get
import os
import sys
import xml.etree.ElementTree as ET

url_start = "https://www.erowid.org/experiences/subs/exp_"
drugs = "Salvia_divinorum_"
url_suffix = ["General.shtml","First_Times.shtml","Difficult_Experiences.shtml","Bad_Trips.shtml","Train_Wrecks_Trip_Disasters.shtml","Glowing_Experiences.shtml","Mystical_Experiences.shtml"]

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(f):
        os.makedirs(f)

def format_suffix(st):
    return st.split('.')[0].replace('_',' ')

def format_title(st):
    return st.replace('/',' ')

def get_href(doc):
    for this in doc.find_all('td'):
        for x in this.find_all('a'):
             if x.string != None and len(x.string) > 1:
                 if x.get('href'):
                     yield x.string,x.get('href')

def get_urls(drug):
    urls = {}
    for i in url_suffix:
        urls_cat = {}
        url = url_start + drug + i
        web = get(url)
        soup = bs(web.text)
        for x,y in get_href(soup):
            urls_cat[x] = y
        urls[format_suffix(i)] = urls_cat
    return urls
        #soup.prettify()

def download_reports(dic):
    for i in dic.keys():
        curr_dir = drugs + '/' + i
        ensure_dir(curr_dir)
        curr = dic[i]
        for j in curr.keys():
            path = curr_dir + '/' + format_title(j) +'.txt'
            link = 'http://www.erowid.org' + curr[j]
            soup = bs(get(link).text)
            text = soup.get_text()
            f = open(path,'wb')
            f.write(unicode(text).encode("utf-8"))
            f.close()
            print j + ' done'
        print 'section ' + i + ' done'

def main():
    results = get_urls(drugs)
    download_reports(results)

main()
