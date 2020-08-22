import requests
import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")


def save(data, target):
    import csv
    from time import gmtime, strftime

    df = pd.DataFrame(data=np.array(data).T, columns=[
                      'title', 'content', 'published', 'keyword', 'url', 'source'])
    fileName = strftime("%Y-%m-%d", gmtime()) + "_" + target + '.csv'
    df.to_csv(fileName, sep=',')


def crawlPsychiatry(keywords, counts):
    data = [[], [], [], [], [], []]
    driver = webdriver.Chrome(chrome_options=options)
    keywords = keywords.split(',')
    for key in keywords:
        driver.get(
            'https://www.psychiatry.org/home/search-results?k={}'.format(key))
        time.sleep(3)
        try:
            driver.find_element_by_id('btnAccept').click()
        except:
            pass
        current_page = 1
        last_page = int(driver.find_elements_by_css_selector(
            'main li')[-1].find_element_by_tag_name('a').text)
        driver.find_element_by_css_selector('li.pagination-current').click()
        base_url = driver.current_url[:-1]
        count = 0
        while(1):
            if(count >= counts):
                continue
            all_news = driver.find_elements_by_css_selector(
                '.slab.slab--search')
            for i in range(len(all_news)):
                title = all_news[i].find_element_by_tag_name('h2').text

                link = all_news[i].find_element_by_css_selector(
                    'h2 a').get_attribute('href')
                if(link.endswith(('.pdf', '.csv', '.xlsx', '.pptx', '.ppt', '.doc'))):
                    continue
                driver.get(link)
                try:
                    date = driver.find_element_by_tag_name('time').text
                except:
                    date = ''
                try:
                    contents = driver.find_element_by_tag_name('main').text
                except:
                    contents = ''
                data[0].append(title.encode('ascii', 'ignore'))
                data[1].append(contents.encode('ascii', 'ignore'))
                data[2].append(date)
                data[3].append(key)
                data[4].append(link)
                data[5].append('https://www.psychiatry.org')

                driver.execute_script("window.history.go(-1)")
                time.sleep(3)
                all_news = driver.find_elements_by_css_selector(
                    '.slab.slab--search')
            if((current_page + 1) == last_page):
                break
            current_page += 1
            driver.get(base_url + str(current_page))
            last_page = int(driver.find_elements_by_css_selector(
                'main li')[-1].find_element_by_tag_name('a').text)
    return data


def crawlWhoWesternpacific(keywords, counts):
    data = [[], [], [], [], [], []]
    driver = webdriver.Chrome(chrome_options=options)
    keywords = keywords.split(',')
    for key in keywords:

        driver.get("https://www.who.int/southeastasia/search-results?page=1&pagesize=99999&query={}&sort=relevance&sortdir=desc&cname=highlight-searo&cname=searo&default=AND&f.Countries.size=100&f.Lang.filter=en&f.RegionalSites.filter=South-East%20Asia&f.RegionalSites.size=100&f.Topics.size=100&f.contenttype.filter=html&f.contenttype.size=100&f.doctype.size=101&facet.field=RegionalSites&facet.field=Topics&facet.field=doctype&facet.field=Countries&facet.field=contenttype&facet.field=Lang&tune=true&tune.0=3&tune.1=2&tune.2=2&tune.3=3&tune.4=180&tune.5=75".format(key))
        time.sleep(10)
        all_news = driver.find_elements_by_id(
            'results-container')[0].find_elements_by_css_selector('.col-sm-12 .single-result-container')

        count = 0

        for news in all_news:

            if(count >= counts):
                continue

            title = news.find_element_by_class_name('result-title').text
            link = news.find_element_by_class_name(
                'result-title').get_attribute('href')
            try:
                time.sleep(1)
                r = requests.get(link)
            except Exception as e:
                continue
            soup = BeautifulSoup(r.text, 'html.parser')
            try:
                day = soup.find('span', class_='timestamp').text.strip()
                contents = soup.find(class_='sf-detail-body-wrapper').text
            except Exception as e:
                continue
            data[0].append(title.encode('ascii', 'ignore'))
            data[1].append(contents.encode('ascii', 'ignore'))
            data[2].append(day)
            data[3].append(key)
            data[4].append(link)
            data[5].append('https://www.who.int/southeastasia')
            count += 1
        time.sleep(10)

    return data


def crawlWhoSoutheastasia(keywords, counts):
    data = [[], [], [], [], [], []]
    driver = webdriver.Chrome(chrome_options=options)
    keywords = keywords.split(',')
    for key in keywords:

        driver.get("https://www.who.int/southeastasia/search-results?page=1&pagesize=99999&query={}&sort=relevance&sortdir=desc&cname=highlight-searo&cname=searo&default=AND&f.Countries.size=100&f.Lang.filter=en&f.RegionalSites.filter=South-East%20Asia&f.RegionalSites.size=100&f.Topics.size=100&f.contenttype.filter=html&f.contenttype.size=100&f.doctype.size=101&facet.field=RegionalSites&facet.field=Topics&facet.field=doctype&facet.field=Countries&facet.field=contenttype&facet.field=Lang&tune=true&tune.0=3&tune.1=2&tune.2=2&tune.3=3&tune.4=180&tune.5=75".format(key))
        time.sleep(10)
        all_news = driver.find_elements_by_id(
            'results-container')[0].find_elements_by_css_selector('.col-sm-12 .single-result-container')

        count = 0

        for news in all_news:

            if(count > counts):
                continue

            title = news.find_element_by_class_name('result-title').text
            link = news.find_element_by_class_name(
                'result-title').get_attribute('href')
            try:
                time.sleep(1)
                r = requests.get(link)
            except Exception as e:
                continue
            soup = BeautifulSoup(r.text, 'html.parser')
            try:
                day = soup.find('span', class_='timestamp').text.strip()
                contents = soup.find(class_='sf-detail-body-wrapper').text
            except Exception as e:
                continue
            data[0].append(title.encode('ascii', 'ignore'))
            data[1].append(contents.encode('ascii', 'ignore'))
            data[2].append(day)
            data[3].append(key)
            data[4].append(link)
            data[5].append('https://www.who.int/southeastasia')
            count += 1
        time.sleep(10)

    return data
