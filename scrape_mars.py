#dependencies used in jupyter notebook
import pandas as pd
import os
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver
driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver.exe"))
import requests
import html5lib
import time
import numpy as np

#browser = Browser("chrome", **executable_path, headless=False)
browser = Browser("chrome", executable_path=os.path.abspath("chromedriver.exe"), headless=False)

def scrape():
    mars_data = {}
    output = marsNews()
    mars_data["mars_news"] = output[0]
    mars_data["mars_paragraph"] = output[1]
    mars_data["mars_image"] = marsImage()
    mars_data["mars_weather"] = marsWeather()
    mars_data["mars_facts"] = marsFacts()
    mars_data["mars_hemispheres"] = marsHem()
    print(mars_data)
    return mars_data





#Mars News portion
def marsNews():
    mars_news = {}
    mars_para = []

    base_url = "https://mars.nasa.gov/" 
    news_url = "https://mars.nasa.gov/news"
    resp_1 = requests.get(news_url) 
                                              

    mars_soup = bs(resp_1.text, 'html.parser') 

    class_div = mars_soup.find(class_="slide")                                  
    marssoup_news = class_div.find_all('a')                                           
    marsnews_title = marssoup_news[1].get_text().strip()

    soup_p = class_div.find_all('a', href=True)                                 
    soup_p_url = soup_p[0]['href']                                               
    paragraph_url = base_url + soup_p_url                                        
    response_2 = requests.get(paragraph_url)                                          
    paragraph_soup = bs(response_2.text, "html.parser")                               
    mars_paragraphs = paragraph_soup.find(class_='wysiwyg_content')                     
    paragraphs = mars_paragraphs.find_all('p')

    for paragraph in paragraphs:                                                 
        simple_paragraph = paragraph.get_text().strip()                              
        mars_para.append(simple_paragraph) 
    
    mars_news["news_title"] = marsnews_title
    mars_news["paragraph_1"] = mars_para[0]
    mars_news["paragraph_2"] = mars_para[1]
    #mars_news[]
    print(mars_news)

marsNews()

#Now get images from the jpl site to bring in to the web page
def marsImage():


    browser = Browser('chrome', headless=False) 
    jpl_base_url = 'https://photojournal.jpl.nasa.gov/jpeg/'               
    jpl_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(jpl_image_url)
    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')

    featured_image_list = []
    for image in image_soup.find_all('div',class_="img"):
        featured_image_list.append(image.find('img').get('src'))

    picture_shown = featured_image_list[0]
    remove_size = picture_shown.split('-')
    remove_fn = remove_size[0].split('/')
    featured_image_url = jpl_base_url + remove_fn[-1] + '.jpg'

    featured_image_url
    browser.quit()
marsImage()


#Get Mars Twitter feed

def marsWeather():

    browser = Browser('chrome', headless=False)
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)

    twitter_html = browser.html
    twitter_soup = bs(twitter_html, 'html.parser')

    mars_weather = twitter_soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(mars_weather)
marsWeather()

#Get Mars Facts
def marsFacts():

    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts_pd = pd.read_html(mars_facts_url)
    mars_facts_df = mars_facts_pd[0]
    mars_facts_table = mars_facts_df.to_html(header=False, index=False)
    print(mars_facts_table)

marsFacts()

# Get Mars Hemispheres Photos
def marsHem():

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup= bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})

    mars_hemisphere
    marsHem()

