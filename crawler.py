import requests
import pandas as pd
import numpy as np
import sys, time ,argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .functions import *

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

parser = argparse.ArgumentParser()
parser.add_argument('--target', type = str, required = True)
parser.add_argument('--keywords', type = str, requests = True)
parser.add_argument('--counts', type=int, requests = True)




def crawler(target, keywords, counts):
    if(target == 'https://www.who.int/southeastasia'):
        crawlWhoSoutheastasia(keywords, counts)
    elif(target == 'https://www.who.int/westernpacific'):
        crawlWhoWesternpacific(keywords,counts)
    elif(target == 'https://www.psychiatry.org/'):
        crawlPsychiatry(keywords, counts)
    elif(target == 'https://timesofindia.indiatimes.com/'):
        crawlTimesofindia(keywords, counts)
    elif(target == 'https://www.thejakartapost.com/'):
        crawlThejakartapost(keywords, counts)
    elif(target == 'https://www.bangkokpost.com/'):
        crawlBangkokpost(keywords, counts)
    else:
        print('Target website is not available')

def main():
    args = parser.parse_args()
    crawler(args.targe, args.keywords, args.counts)
    
if __name__ == '__main__' :
    main()

