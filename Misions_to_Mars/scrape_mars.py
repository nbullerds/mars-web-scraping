import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # browser = init_brower()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ########## Scrape news from redplanetscience.com ##########
    # create dictionary to store scraped variables
    mars_scrape = {}

    # Gather latest news information from redplanetscience.com
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find all news story elements
    results = soup.find_all('div', class_='list_text')

    # Iterate through found story elements
    for result in results[0]:
        # collect latest news title
        ltst_news_title = soup.find('div', class_='content_title').get_text()
    
        # collect latest news paragraph
        ltst_news_text = soup.find('div', class_='article_teaser_body').get_text()

    # store results in mars_scrape
    mars_scrape["latest_news_title"] = ltst_news_title
    mars_scrape["latest_news_text"] = ltst_news_text

    ########## Scrape featured image from spaceimages-mars.com ##########
    # Gather image from current featured mars image from spaceimages-mars.com
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find all news story elements
    results = soup.find_all('div', class_='header')

    for result in results[0]:
        img = soup.find('img', class_='headerimage')
        src = img['src']

    # Store the results in mars_scrape
    featured_image_url = url + src
    mars_scrape["featured_image_url"] = featured_image_url

    ########## Scrape mars info table from galaxyfacts-mars.com ##########
    # Read all tables from 'https://galaxyfacts-mars.com/' into pandas
    mars_table = pd.read_html('https://galaxyfacts-mars.com/')

    # Convert target table into a dataframe to check scrape results
    mars_info_df = mars_table[0]

    # grab the first row for the header
    new_header = mars_info_df.iloc[0]

    # take the data less the header row
    mars_info_df = mars_info_df[1:]

    # set the header row as the df header
    mars_info_df.columns = new_header

    # convert df to html table and store in mars_scrape
    mars_info_html = mars_info_df.to_html
    mars_scrape["mars_info_html"] = mars_info_html

    ########## Scrape hemisphere images from marshemispheres.com ##########
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find all links to images
    image_links = soup.find_all('div', class_='item')

    # Create list and find/store image links in it
    link_list = []
    for image_link in image_links:
        link = image_link.find('a', class_='itemLink product-item')
        link_list.append(url + link['href'])

    # list to store image information
    hemisphere_image_urls = []

    for link in link_list:
        
        # go to the url with the high-quality image
        browser.visit(link)
        html = browser.html
        
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find all news story elements
        images_info = soup.find_all('div', class_='cover')
        
        for image_info in images_info:
            # create dictionary to store image information
            img_dict = {}

            # scrape title and image url
            title = image_info.find('h2', class_='title').get_text()
            title_strip = title.rstrip('Enhanced')
            description = image_info.find('div', class_='description')
            a = description.find('a')
            image_url = url + a['href']
            img_dict["title"] = title_strip[0:len(title_strip) - 1]
            img_dict["img_url"] = image_url
            hemisphere_image_urls.append(img_dict)

    # store image url list in mars_scrape
    mars_scrape["hemisphere_images"] = hemisphere_image_urls

    return mars_scrape