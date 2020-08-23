import requests
import pandas as pd
import numpy as np
import sys, time ,argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from functions import *

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

parser = argparse.ArgumentParser()
parser.add_argument('--target', type = str, required = True)
parser.add_argument('--keywords', type = str, required = True)
parser.add_argument('--counts', type=int, required = True)




def crawler(target, keywords, counts):
    if(target == 'https://www.who.int/southeastasia'):
        return crawlWhoSoutheastasia(keywords, counts)
    elif(target == 'https://www.who.int/westernpacific'):
        return crawlWhoWesternpacific(keywords,counts)
    elif(target == 'https://www.psychiatry.org'):
        return crawlPsychiatry(keywords, counts)
    elif(target == 'https://timesofindia.indiatimes.com'):
        return crawlTimesofindia(keywords, counts)
    elif(target == 'https://thejakartapost.com'):
        return crawlThejakartapost(keywords, counts)
    elif(target == 'https://www.bangkokpost.com'):
        return crawlBangkokpost(keywords, counts)
    else:
        print('Target website is not available')

def main(): 
    args = parser.parse_args()
    data = crawler(args.target, args.keywords, args.counts)
    if(data != None):
        save(data, args.target)

if __name__ == '__main__' :
    main()

