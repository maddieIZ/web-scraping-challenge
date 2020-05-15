
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd



#choosing the executable path to driver
def init_browser(): 
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    #scraping data from the NASA Mars News Site
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = bs(response.text,'html.parser')


    # print(soup.prettify())



    #collecting the latest news title and paragraph text
    news_title = soup.find('div', class_= "content_title").find('a').text.strip()
    news_parag = soup.find('div', class_= "rollover_description_inner").text.strip()

    #printing results
    # print(news_title)
    # print(news_parag)



    #the URL for the JPL Featured Space Image through splinter
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)



    #creating HTML object and parsing
    html_image = browser.html
    soup = bs(html_image, 'html.parser')

    #retreieve the sub-url to the background image
    featured_image = soup.find('div',class_='carousel_items')
    # print(featured_image)



    #set to background image
    image_sub_url = featured_image('article')[0]['style'].    replace('background-image: url(','').replace(');','')[1:-1]

    #main_url
    main_url = 'https://www.jpl.nasa.gov'

    #creating the full url 
    featured_image_url = main_url + image_sub_url

    #print results
    # print(featured_image_url)


    #the URL for the Mars Weather 
    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweet_url)



    #creating HTML object and parsing
    html_weather = browser.html
    soup = bs(html_weather, 'html.parser')



    last_tweets = soup.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')
                                
    # print(last_tweets[8])



    #Loop on the tweets
    tweets_list = []
    for tweet in last_tweets:
        if 'sol' in (tweet.text):
            tweets_list.append(tweet.text)
    # print(tweets_list)


    # ### Mars Facts


    #url facts for mars
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)



    #reading in the tables on the url
    tables = pd.read_html(facts_url)

    #the second table on the page contains our "Mars Facts"
    mars_facts_raw = tables[1]
    mars_facts_raw



    #formatting data frame
    mars_facts=mars_facts_raw.rename(columns={'Mars - Earth Comparison':'Fact','Mars':'Value'})
    # mars_facts_table= mars_facts.set_index('Fact')


    # print(mars_facts_table)



    #converting to html
    mars_facts_html = mars_facts.to_html()
    # print(mars_facts_html)


    # ### Mars Hemispheres



    #visiting the URL for the Mars Weather Twitter Account
    hemisph_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisph_url)




    #creating HTML object and parsing
    html_hemisph = browser.html
    soup = bs(html_hemisph, 'html.parser')




    # image links
    items = soup.find_all('div', class_='item')
    # print(items)




    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'




    #for all the info containing the image links
    for i in items: 
        # Storing the title
        title = i.find('h3').text
        
        # Storing the url that has full image url
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        
        #test find
    #     print(partial_img_url)
    #     print(hemispheres_main_url + partial_img_url)

        # open the url
        browser.visit(hemispheres_main_url + partial_img_url)
        
        # HTML Object for full image url storage website
        partial_img_html = browser.html
        
    #     # Parsing HTML for that specific website
        soup = bs( partial_img_html, 'html.parser')
        
    #     # getting full image url 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        
    #     # Adding to dictionary
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

        mars_data = {
                    "Mars_News_Title": news_title,
                    "Mars_News_Paragraph": news_parag,
                    "Mars_Featured_Image": featured_image_url,
                    "Mars_Weather_Data": tweets_list,
                    "Mars_Facts": mars_facts_html,
                    "Mars_Hemisphere_Images": hemisphere_image_urls
                }

        browser.quit()

        return mars_data


    if __name__ == "__main__":
        print("Loading....")    
        print(scrape())

