from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import time
import pandas as pd


def init_browser():
    
    executable_path = {'executable_path': 'C:/chromedrv/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)



# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

# NASA MARS NEWS
def scrape_mars_news():
    # Initialize browser 
    browser = init_browser()
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url)

    news_html = browser.html

    news_soup = BeautifulSoup(news_html, 'html.parser')
    n_title = news_soup.find('div', class_='content_title').find('a').text.strip()
    n_description = news_soup.find('div', class_='rollover_description').text

    mars_info['news_title'] = n_title
    mars_info['news_paragraph'] = n_description

    return mars_info
    
    browser.quit()

# FEATURED IMAGE
def scrape_mars_image():
    base_image_url = 'https://www.jpl.nasa.gov'
    space_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(space_image_url)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(4)
    browser.click_link_by_partial_text('more info')
    image_html = browser.html
    time.sleep(2)
    image_soup = BeautifulSoup(image_html, 'html.parser')
    links =[]
    [links.append(item['href']) for item in image_soup.find_all('a', attrs={'href' : True})]
    featured_image_url  = base_image_url + links[56]

    mars_info['featured_image_url'] = featured_image_url 

    return mars_info

    browser.quit()

        

# Mars Weather 
def scrape_mars_weather():

    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    weather_html = browser.html
    weath_soup = BeautifulSoup(weather_html, 'html.parser')

    weather_twt = weath_soup.find_all('div', class_='context')
    #.find_all(class_='js-tweet-text-container')
    if weather_twt[0].text.strip() == 'Mars Weather Retweeted':
        weather_twt = weath_soup.find_all(class_='js-tweet-text-container')
        wt = weather_twt[1].text.strip()
    else:
        weather_twt = weath_soup.find_all(class_='js-tweet-text-container')
        wt = weather_twt[0].text.strip()
    #wt

    mars_info['weather_tweet'] = wt

    return mars_info

    browser.quit()


# Mars Facts
def scrape_mars_facts():

    facts_url = 'http://space-facts.com/mars/'

    #create a dataframe from the read data at position 0
    mars_facts = pd.DataFrame(pd.read_html(facts_url)[0])
    mars_facts

    mars_facts.columns = ['Description','Value']

    mars_facts.set_index('Description', inplace=True)

    table_html =  mars_facts.to_html()
    mars_info['mars_facts'] = table_html
    
    return mars_info


# MARS HEMISPHERES


def scrape_mars_hemispheres():

    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = 'https://astrogeology.usgs.gov'
    browser.visit(hemi_url)
    i=0
    hemi_html = browser.html
    hemi_soup = BeautifulSoup(hemi_html,'html.parser')
    hemi = hemi_soup.find_all('a',class_='itemLink product-item')
    hemi_urls =[]
    for h in hemi:
        try:
            link =  hemi[i]['href']
            i+=2
            hemi_urls.append(base_url + link)
        except(IndexError):
            print('done')

    j=0
    img_list=[]
    title_list =[]
    hemi_dict = []
    for u in hemi_urls:
        browser.visit(hemi_urls[j])
        html = browser.html
        ur = BeautifulSoup(html,'html.parser')
        img = ur.find('img',class_='wide-image')
        #cerb_img['img']
        img_list.append(base_url+img['src'])
        j+=1
        hemi_title = ur.find('h2').text
        hemi_title = hemi_title.replace(r' Enhanced', '')
        title_list.append(hemi_title)
        hemi_dict.append({"title" : hemi_title, "img_url" : base_url+img['src']})
    
    mars_info['hiu'] = hemi_dict 


# Return mars_data dictionary 

    return mars_info


    browser.quit()