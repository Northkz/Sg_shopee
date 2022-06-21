from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time, re, math
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

## Search Page Scraping ##
def scrape_page():
    # Name
    shop_name = driver.find_elements(by=By.XPATH, value="//div[@class='dpiR4u']/div[1]/div[1]")
    for name in shop_name:
        retail_name.append(name.text)


    # market lowest possible price
    price = driver.find_elements(by=By.XPATH, value="//div[@class='vioxXd rVLWG6']/span[2]")
    for prices in price:
        retail_price.append(prices.text)



    # Quantity Sold
    sold = driver.find_elements(by=By.CLASS_NAME, value="r6HknA")
    for Quantity in sold:
        Quantity_Sold.append(Quantity.text)
    for i in range(len(Quantity_Sold)):
        if Quantity_Sold[i] == '':
            Quantity_Sold[i] = '0 sold'

    # Link for each item
    Link = driver.find_elements(by=By.XPATH, value='//a[@data-sqe="link"]')
    for href in Link:
        links.append(href.get_attribute('href'))

    # Sleep for new URL
    time.sleep(2)


## Product Characteristics Scraping ##
def scrape_product():
    try:
        # rating score
        Rate = product_driver.find_elements(by=By.XPATH, value="//div[@class='flex W2tD8-']/div[1]/div[1]")
        if not Rate:
            rating_score.append('No score')
        else:
            for score in Rate:
                if score.text:
                    rating_score.append(score.text)
                else:
                    rating_score.append('No score')

        # rating counts
        rating_c = product_driver.find_elements(by=By.XPATH, value="//div[@class='flex W2tD8-']/div[2]/div[1]")
        for rates in rating_c:
            rating_count.append(rates.text)

        # favourite counts
        favorite1 = product_driver.find_elements(by=By.XPATH, value="//div[@class='YmlR4M']/div[1]")
        if not favorite1:
            fav_count.append("N/a")
        else:
            for favor in favorite1:
                print(f"favor ->{favor.text}")
                if(favor.text == "" or favor.text == "Favorite" or favor.text == "Favorite (0)"):
                    fav_count.append("0")
                elif not favor.text:
                    fav_count.append("N/a")
                else:
                    fav_count.append(favor.text)



        sname = product_driver.find_elements(by=By.CLASS_NAME, value="_6HeM6T")
        for name in sname:
            seller_name.append(name.text)

        # shop rating
        srating = product_driver.find_elements(by=By.XPATH, value="//div[@class='biYJq8']/div[1]/div[1]/span")
        for rate in srating:
            shop_rating.append(rate.text)

        # shop responserate
        sresponse = product_driver.find_elements(by=By.XPATH, value="//div[@class='biYJq8']/div[2]/div[1]/span")
        for responses in sresponse:
            shop_responserate.append(responses.text)

        # shop responsetime
        srestime = product_driver.find_elements(by=By.XPATH, value="//div[@class='biYJq8']/div[2]/div[2]/span")
        for rtime in srestime:
            shop_responsetime.append(rtime.text)

        # shop followers
        followers = product_driver.find_elements(by=By.XPATH, value="/div[@class='JfALJ- page-product__shop']/div[2]/div[3]/div[2]/span[@class=_32ZDbL]")
        if not followers:
            shop_follower.append("N/a")
        else:
            for follower in followers:
                print(f"follower->{follower.text}")
                shop_follower.append(follower.text)
        #shop joined
        joined = product_driver.find_elements(by=By.XPATH, value="/div[@class='JfALJ- page-product__shop']/div[2]/div[3]/div[1]/span[@class=_32ZDbL]")
        if not joined:
            shop_joined.append('N/a')
        else:
            for join_num in joined:
                print(f"shop join->{join_num.text}")
                shop_joined.append(join_num.text)

    except NoSuchElementException:
        rating_score.append('No Rating Score On This Product')
        rating_count.append('No Rating Count On This Product')
        fav_count.append('No Favourite Count On This Product')
        seller_name.append('No Shop On This Product')
        shop_rating.append('No Shop Ratings On This Product')
        shop_responserate.append('No Shop Response Rate On This Product')
        shop_responsetime.append('No Shop Response Time On This Product')
        shop_follower.append('No Shop Followes On This Product')
        shop_joined.append('No Joined Date On This Product')

## Lists ##
retail_name = []
retail_price = []
Quantity_Sold = []
links = []
rating_score = []
rating_count = []
fav_count = []
seller_name = []
shop_rating = []
shop_responserate = []
shop_responsetime = []
product_comments = []
shop_follower = []
shop_joined = []

## Part 1: Scrape Search Engine Webpage ##

# type in product name
inp ="sssss"
shopee_find = inp

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://shopee.sg/search?keyword=' + str(shopee_find))

time.sleep(3)


# Find total pages number
num_pages = driver.find_elements(by=By.CLASS_NAME, value="shopee-mini-page-controller__total")
print(num_pages)
num_page = 0
for value in num_pages:
    num_page = int(value.text)
print(num_page)
# Automate Webpages
for page in range(num_page):
    driver.get('https://shopee.sg/search?keyword=' + str(shopee_find) + '&page=' + str(page))
    # Sleep
    time.sleep(1)

    # Scrolling web
    scroll_pause_time = 1
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script('window.scrollTo(0, window.scrollY + 500);')
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script('return document.body.scrollHeight')

        if new_height == last_height:
            driver.execute_script('window.scrollTo(0, window.scrollY + 500)')
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                break
            else:
                last_height = new_height
                continue

    scrape_page()
driver.close()

## Part 2: Scrape Product Characteristics ##
product_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# Automate Product Links
for i in range(len(links)):
    product_driver.get(links[i])

    time.sleep(2)

    try:
        time.sleep(3)
        # Scoll html
        pause_time = 2
        while True:

            # Get the height of page
            last_height = product_driver.execute_script("return document.body.scrollHeight")
            product_driver.execute_script('window.scrollTo(0, window.scrollY + 500);')
            time.sleep(pause_time)

            # Calculate new height
            new_height = product_driver.execute_script('return document.body.scrollHeight')

            if new_height == last_height:
                product_driver.execute_script('window.scrollTo(0, window.scrollY + 500);')
                time.sleep(pause_time)
                new_height = product_driver.execute_script('return document.body.scrollHeight')
                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                    continue

        while True:

            # Get the height of page
            last_height = product_driver.execute_script("return document.body.scrollHeight")
            product_driver.execute_script('window.scrollTo(0, window.scrollY + 750);')
            time.sleep(pause_time)

            # Calculate new height
            new_height = product_driver.execute_script('return document.body.scrollHeight')

            if new_height == last_height:
                product_driver.execute_script('window.scrollTo(0, window.scrollY + 750);')
                time.sleep(pause_time)
                new_height = product_driver.execute_script('return document.body.scrollHeight')
                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                    continue

        while True:

            # Get the height of page
            last_height = product_driver.execute_script("return document.body.scrollHeight")
            product_driver.execute_script('window.scrollTo(0, window.scrollY + 750);')
            time.sleep(pause_time)

            # Calculate new height
            new_height = product_driver.execute_script('return document.body.scrollHeight')

            if new_height == last_height:
                product_driver.execute_script('window.scrollTo(0, window.scrollY + 750);')
                time.sleep(pause_time)
                new_height = product_driver.execute_script('return document.body.scrollHeight')
                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                    continue

        scrape_product()

    except NoSuchElementException:

        # wait for web to load after press button
        time.sleep(3)

        # Scoll html
        pause_time = 2
        while True:
            # Get the height of page
            last_height = product_driver.execute_script("return document.body.scrollHeight")
            product_driver.execute_script('window.scrollTo(0, window.scrollY + 500);')
            time.sleep(pause_time)

            # Calculate new height
            new_height = product_driver.execute_script('return document.body.scrollHeight')

            if new_height == last_height:
                product_driver.execute_script('window.scrollTo(0, window.scrollY + 500);')
                time.sleep(pause_time)
                new_height = product_driver.execute_script('return document.body.scrollHeight')
                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                    continue
        while True:
            # Get the height of page
            last_height = product_driver.execute_script("return document.body.scrollHeight")
            product_driver.execute_script('window.scrollTo(0, window.scrollY + 750);')
            time.sleep(pause_time)

            # Calculate new height
            new_height = product_driver.execute_script('return document.body.scrollHeight')

            if new_height == last_height:
                product_driver.execute_script('window.scrollTo(0, window.scrollY + 750);')
                time.sleep(pause_time)
                new_height = product_driver.execute_script('return document.body.scrollHeight')
                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                    continue

        while True:
            # Get the height of page
            last_height = product_driver.execute_script("return document.body.scrollHeight")
            product_driver.execute_script('window.scrollTo(0, window.scrollY + 750);')
            time.sleep(pause_time)

            # Calculate new height
            new_height = product_driver.execute_script('return document.body.scrollHeight')

            if new_height == last_height:
                product_driver.execute_script('window.scrollTo(0, window.scrollY + 750);')
                time.sleep(pause_time)
                new_height = product_driver.execute_script('return document.body.scrollHeight')
                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                    continue

        scrape_product()
product_driver.close()

## Part 3: Saving ##

## Create .csv file ##
print(f"shop_name = {len(seller_name)}; shop_rating = {len(shop_rating)} ")
print(f"Shop_Followers = {len(shop_follower)} ")
print(f"shop_responserate = {len(shop_responserate)}; shop_responsetime = {len(shop_responsetime)} ")
print(f"shop_joined = {len(shop_joined)}; retail_name = {len(retail_name)} ")
print(f"retail_price = {len(retail_price)}; Quantity_Sold = {len(Quantity_Sold)} ")
print(f"rating_score = {len(rating_score)}; rating_count = {len(rating_count)} ")
print(f"fav_count = {len(fav_count)}; links = {len(links)} ")


df_shopee = pd.DataFrame(
    {
        "Shop_Name": seller_name,
        "Shop_Rating_Counts": shop_rating,
        "Shop_Followers": shop_follower,
        "Shop_Response_Rate": shop_responserate,
        "Shop_Response_time": shop_responsetime,
        "Shop_Joined": shop_joined,
        "Product_Name": retail_name,
        "Product_Price": retail_price,
        "Quantity_Sold": Quantity_Sold,
        "Product_Score": rating_score,
        "Product_Rating_Counts": rating_count,
        "Product_Favourite_Counts_by_User": fav_count,
        "Links": links
    }
)
df_shopee.to_csv('shopee_data.csv', index=False, encoding='utf-8')
