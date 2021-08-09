from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time

# Set executable path and return browser
def init_browser():
    executable_path = {"executable_path": "C:/Users/Sean/.wdm/drivers/chromedriver/win32/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
    
def mars_data():
    
    #initialize browser
    browser = init_browser()
    
    #now we use the framework that we outlines in our .ipynb
    urla = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(urla)
    #mars news title and paragraph
    htmla = browser.html
    soupa = bs(htmla, 'lxml')
    
    title = soupa.find_all('div', class_="content_title")[1]
    title_string = title.a.text
    paragraph = soupa.find('div', class_="article_teaser_body")
    paragraph_string = paragraph.get_text()
    
    #featured image link
    urlb = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(urlb)
    
    htmlb = browser.html
    soupb = bs(htmlb, 'html.parser')
    
    image_link = soupb.find('img', class_="headerimage fade-in").get('src')
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + image_link
    
    #facts table
    urlc = "https://space-facts.com/mars/"
    table = pd.read_html(urlc)
    table_df = table[0]
    rename_df = table_df.rename(columns={0: "Category", 1: "Measurement"})
    rename_df = rename_df.set_index('Category')
    mars_facts = rename_df.to_html()
    
    # Hemisphere title and image link
    urld = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(urld)
    
    htmld = browser.html
    soupd = bs(htmld, 'html.parser')
    
    results = soupd.find_all("div", class_="description")

    hemisphere_image_urls=[]
    for result in results:
        link = result.find('a')
        href = link['href']
        title = link.find('h3').text
        url_hemisphere = "https://astrogeology.usgs.gov" + href
        browser.visit(url_hemisphere)
        html_hemisphere = browser.html
        soup_hemisphere = bs(html_hemisphere, 'html.parser')
        pic = soup_hemisphere.find("div", class_="downloads")
        pic_anchor = pic.find('a')
        pic_href = pic_anchor['href']
        hemisphere_image_urls.append({"title":title,"img_url":pic_href})
        
    #scaped dictionaryt to return to mongo DB
    mars_info_dict = {"news_title":title_string,"news_paragraph":paragraph_string,"featured_image":featured_image_url,
    "facts_table":mars_facts,"hemisphere_img":hemisphere_image_urls}
    
    # Close the browser after scraping
    browser.quit()
    
    # Return results
    return mars_info_dict

    
    
