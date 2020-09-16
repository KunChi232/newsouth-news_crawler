import requests
import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
import re

import os
import requests

def _post_data(dataframe):

    loginid = os.getenv('LOGINID')
    password = os.getenv('PASSWORD')
    prev_url = os.getenv('PREV_URL')
    post_url = os.getenv('POST_URL')
    
    session = requests.Session()
    _ = session.get(prev_url)

    db = pd.read_csv('ns_crawler/news.csv')
    contents_db = db['content']

    for index, row in dataframe.iterrows():
        content = row['content']

        if (contents_db==content).any():
            dataframe.drop(index, inplace=True)
            continue

        title = row['title']
        url = row['source'] + row['url']

        data = {
            'loginid': loginid,
            'password': password,
            'title': title,
            'content': content,
            'published': row['published'],
            'keyword': row['keyword'],
            'url': url
        }

        temp_df = pd.DataFrame(
            data = {
                'title': [title],
                'content': [content],
                'url': [url]
            }
        )

        db = db.append(
            temp_df
        )


        r = session.post(post_url, data = data)

    db.to_csv('ns_crawler/news.csv', sep=',', quotechar='"', header=['title', 'content', 'url'], index = False)




def save(data, target):
    import csv
    from time import gmtime, strftime

    df = pd.DataFrame(data=np.array(data).T, columns=[
                      'title', 'content', 'published', 'keyword', 'url', 'source'])

    # Post data to db
    _post_data(df)

    fileName = strftime("%Y-%m-%d", gmtime()) + '.csv'
    df.to_csv(fileName, sep=',', quotechar='"', index = False)



def crawlBangkokpost(keywords, counts):
    data = [[], [], [], [], [], []]
    keywords = keywords.split(',')
    for key in keywords:
        r = requests.get(
            "https://search.bangkokpost.com/search/result?category=news&q={}/".format(key))
        if(r.status_code == requests.codes.ok):
            soup = BeautifulSoup(r.text, 'html.parser')
            content = soup.find(id='content')
            search_list = content.find('ul', class_='SearchList')
            pages = content.find('p', class_='page-Navigation')

            count = 0

            while(pages.find_all('a')[-2].contents[0] == 'Next'):
                for i, h3 in enumerate(search_list.find_all('h3')):
                    if(count >= counts):
                        break

                    news_link = h3.find('a')['href']
                    head = h3.find('a').text.strip()
                    news_publish = search_list.find_all('p', class_='writerdetail')[
                        i].find('span').text.strip()
                    news_request = requests.get(news_link)
                    if(news_request.status_code == requests.codes.ok):
                        news_soup = BeautifulSoup(
                            news_request.text, 'html.parser')
                        try:
                            news_content = news_soup.find(
                                'div', class_=['articl-content', 'articleContents']).text.strip()
                            data[0].append(head.encode('ascii', 'ignore'))
                            data[1].append(
                                news_content.encode('ascii', 'ignore'))
                            data[2].append(news_publish)
                            data[3].append(key)
                            data[4].append(news_link)
                            data[5].append('https://www.bangkokpost.com/')
                            count += 1
                        except Exception as e:
                            continue
                if(count >= counts):
                    break

                r = requests.get(pages.find_all('a')[-2]['href'])
                soup = BeautifulSoup(r.text, 'html.parser')
                content = soup.find(id='content')
                search_list = content.find('ul', class_='SearchList')
                pages = content.find('p', class_='page-Navigation')

            for i, h3 in enumerate(search_list.find_all('h3')):
                if(count >= counts):
                    break

                news_link = h3.find('a')['href']
                head = h3.find('a').text.strip()
                news_publish = search_list.find_all('p', class_='writerdetail')[
                    i].find('span').text.strip()
                news_request = requests.get(news_link)
                if(news_request.status_code == requests.codes.ok):
                    news_soup = BeautifulSoup(news_request.text, 'html.parser')
                    try:
                        news_content = news_soup.find(
                            'div', class_=['articl-content', 'articleContents']).text.strip()
                        data[0].append(head.encode('ascii', 'ignore'))
                        data[1].append(news_content.encode('ascii', 'ignore'))
                        data[2].append(news_publish)
                        data[3].append(key)
                        data[4].append(news_link)
                        data[5].append('https://www.bangkokpost.com/')
                    except Exception as e:
                        continue
    return data

def crawlThejakartapost(keywords, counts):
    data = [[], [], [], [], [], []]
    # driver = webdriver.Chrome(chrome_options=options)
    driver = webdriver.Chrome()

    keywords = keywords.split(',')
    for key in keywords:
        driver.get("https://www.thejakartapost.com/news")
        time.sleep(1)
        searchBtn = driver.find_element_by_class_name('search')
        searchBtn.click()
        search_input = driver.find_element_by_name('q')
        time.sleep(1)
        search_input.send_keys(key)
        time.sleep(1)
        search_input.send_keys(Keys.ENTER)
        time.sleep(1)

        numOfPages = len(
            driver.find_elements_by_css_selector('.gsc-cursor-page'))
        count = 0
        for page in range(numOfPages):
            pages = driver.find_elements_by_css_selector('.gsc-cursor-page')
            pages[page].click()
            time.sleep(1)
            for link in driver.find_elements_by_css_selector(".gsc-thumbnail-inside .gs-title a.gs-title"):
                if(count >= counts):
                    break
                try:
                    time.sleep(1)
                    r = requests.get(link.get_attribute("href"))
                except Exception as e:
                    continue
                soup = BeautifulSoup(r.text, 'html.parser')
                try:
                    title = soup.find(
                        ['h1', 'h3'], class_='title-large').text.strip()
                    day = soup.find_all(class_='day')
                    if(len(day) > 1):
                        day = day[1].text.strip()
                    else:
                        day = day[0].text.strip()
                    contents = soup.find(
                        'div', class_=['show-define-text', 'detailNews'])
                    text = ''
                    for p in contents.find_all('p'):
                        text += p.text.strip()
                    data[0].append(title.encode('ascii', 'ignore'))
                    data[1].append(text.encode('ascii', 'ignore'))
                    data[2].append(day)
                    data[3].append(key)
                    data[4].append(link.get_attribute("href"))
                    data[5].append('https://www.thejakartapost.com/')
                    count += 1
                except Exception as e:
                    continue
            if(count >= counts):
                break
        time.sleep(3)
    return data


def crawlTimesofindia(keywords, counts):
    data = [[], [], [], [], [], []]
    keywords = keywords.split(',')
    for key in keywords:
        count = 0
        for i in range(15):
            try:
                r = requests.get(
                    'https://timesofindia.indiatimes.com/topic/{}/news/{}'.format(key, i+1))
                soup = BeautifulSoup(r.text, 'html.parser')
            except:
                continue
            itemList = soup.find(itemprop='ItemList').find_all('li')
            for news in itemList:
                if(count >= counts):
                    break
                link = news.find('div', class_='content').a['href']
                title = news.find('div', class_='content').a.span.text
                date = news.find('div', class_='content').a.find(
                    'span', class_='meta').text
                try:
                    r = requests.get(
                        'https://timesofindia.indiatimes.com/' + link)
                    news_soup = BeautifulSoup(r.text, 'html.parser')
                    contents = news_soup.find(
                        'div', class_=['article_content', '_1_Akb', 'section1']).text
                except:
                    continue

                data[0].append(title.encode('ascii', 'ignore'))
                data[1].append(contents.encode('ascii', 'ignore'))
                data[2].append(date)
                data[3].append(key)
                data[4].append(link)
                data[5].append('https://timesofindia.indiatimes.com/')
                count += 1
            if(count >= counts):
                break
    return data


def crawlPsychiatry(keywords, counts):
    data = [[], [], [], [], [], []]
    # driver = webdriver.Chrome(chrome_options=options)
    driver = webdriver.Chrome()

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
                if(count >= counts):
                    break
                try:
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
                    data[0].append(title.encode('unicode_escape'))
                    data[1].append(contents.encode('unicode_escape'))
                    data[2].append(date.encode('unicode_escape'))
                    data[3].append(key.encode('unicode_escape'))
                    data[4].append(link.encode('unicode_escape'))
                    data[5].append('https://www.psychiatry.org')
                    count += 1

                    driver.execute_script("window.history.go(-1)")
                    time.sleep(3)
                    all_news = driver.find_elements_by_css_selector(
                        '.slab.slab--search')
                except exceptions.StaleElementReferenceException as e:
                    all_news = driver.find_elements_by_css_selector('.slab.slab--search')
            if(count >= counts):
                break
            if((current_page + 1) == last_page):
                break
            current_page += 1
            driver.get(base_url + str(current_page))
            last_page = int(driver.find_elements_by_css_selector(
                'main li')[-1].find_element_by_tag_name('a').text)
    return data


def crawlWhoWesternpacific(keywords, counts):
    data = [[], [], [], [], [], []]
    # driver = webdriver.Chrome(chrome_options=options)
    driver = webdriver.Chrome()
    keywords = keywords.split(',')
    for key in keywords:

        driver.get("https://www.who.int/southeastasia/search-results?page=1&pagesize=99999&query={}&sort=relevance&sortdir=desc&cname=highlight-searo&cname=searo&default=AND&f.Countries.size=100&f.Lang.filter=en&f.RegionalSites.filter=South-East%20Asia&f.RegionalSites.size=100&f.Topics.size=100&f.contenttype.filter=html&f.contenttype.size=100&f.doctype.size=101&facet.field=RegionalSites&facet.field=Topics&facet.field=doctype&facet.field=Countries&facet.field=contenttype&facet.field=Lang&tune=true&tune.0=3&tune.1=2&tune.2=2&tune.3=3&tune.4=180&tune.5=75".format(key))
        time.sleep(10)
        all_news = driver.find_elements_by_id(
            'results-container')[0].find_elements_by_css_selector('.col-sm-12 .single-result-container')

        count = 0

        for news in all_news:

            if(count >= counts):
                break

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
        time.sleep(3)

    return data


def crawlWhoSoutheastasia(keywords, counts):
    data = [[], [], [], [], [], []]
    # driver = webdriver.Chrome(chrome_options=options)
    driver = webdriver.Chrome()
    keywords = keywords.split(',')
    for key in keywords:

        driver.get("https://www.who.int/southeastasia/search-results?page=1&pagesize=99999&query={}&sort=relevance&sortdir=desc&cname=highlight-searo&cname=searo&default=AND&f.Countries.size=100&f.Lang.filter=en&f.RegionalSites.filter=South-East%20Asia&f.RegionalSites.size=100&f.Topics.size=100&f.contenttype.filter=html&f.contenttype.size=100&f.doctype.size=101&facet.field=RegionalSites&facet.field=Topics&facet.field=doctype&facet.field=Countries&facet.field=contenttype&facet.field=Lang&tune=true&tune.0=3&tune.1=2&tune.2=2&tune.3=3&tune.4=180&tune.5=75".format(key))
        time.sleep(10)
        all_news = driver.find_elements_by_id(
            'results-container')[0].find_elements_by_css_selector('.col-sm-12 .single-result-container')

        count = 0

        for news in all_news:

            if(count >= counts):
                break

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
        time.sleep(3)

    return data
