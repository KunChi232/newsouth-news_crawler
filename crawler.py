import requests
import pandas as pd
import numpy as np
import sys, time ,argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

parser = argparse.ArgumentParser()
parser.add_argument('--target', type = str, required = True)
parser.add_argument('--keywords', type = str, requests = True)
parser.add_argument('--count', type=int, requests = True)




def crawler(target):
    if(target == 'https://www.who.int/southeastasia'):
        pass
    elif(target == 'https://www.who.int/westernpacific'):
        pass
    elif(target == 'https://www.psychiatry.org/'):
        pass
    elif(target == 'https://timesofindia.indiatimes.com/'):
        pass
    elif(target == 'https://www.thejakartapost.com/'):
        pass
    elif(target == 'https://www.bangkokpost.com/'):
        pass
    else:
        print('Target website is not available')

def main():
    args = parser.parse_args()

if __name__ == '__main__' :
    main()

