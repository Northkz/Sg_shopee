from selenium.common.exceptions import NoSuchElementException
import time, re, math
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Lists #
product_description = []
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
product_all_images = []
image1_url = []
image2_url = []
image3_url = []
image4_url = []
image5_url = []
available_item = []
brand_name = []


# rating score
def rating_score():
    Rate = product_driver.find_elements(by=By.XPATH, value="//div[@class='flex W2tD8-']/div[1]/div[1]")
    for score in Rate:
        if score.text:
            rating_score.append(score.text)
        else:
            rating_score.append('No score')


def rating_number_count():
    rating_c = product_driver.find_elements(by=By.XPATH, value="//div[@class='flex W2tD8-']/div[2]/div[1]")
    for rates in rating_c:
        rating_count.append(rates.text)


# favourite counts
def favorite_number():
    favorite1 = product_driver.find_elements(by=By.XPATH, value="//button[@class='YmlR4M']")
    for favor in favorite1:
        if favor.text == "" or favor.text == "Favorite" or favor.text == "Favorite (0)":
            fav_count.append("0")
        elif not favor.text:
            fav_count.append("N/a")
        else:
            fav_count.append(favor.text)


# shop name
def shop_name():
    sname = product_driver.find_elements(by=By.CLASS_NAME, value="_6HeM6T")
    for name in sname:
        seller_name.append(name.text)


# shop rating
def shop_rating_check():
    srating = product_driver.find_elements(by=By.XPATH, value="//div[@class='biYJq8']/div[1]/div[1]/span")
    for rate in srating:
        shop_rating.append(rate.text)


# shop's response rate
def shop_response_rate():
    sresponse = product_driver.find_elements(by=By.XPATH, value="//div[@class='biYJq8']/div[2]/div[1]/span")
    for responses in sresponse:
        shop_responserate.append(responses.text)


# shop's response time
def shop_response_time():
    srestime = product_driver.find_elements(by=By.XPATH, value="//div[@class='biYJq8']/div[2]/div[2]/span")
    for rtime in srestime:
        shop_responsetime.append(rtime.text)


# shop followers
def shop_follower_number():
    followers = product_driver.find_elements(by=By.XPATH, value="//div[@class='biYJq8']/div[3]/div[2]/span")
    for follower in followers:
        shop_follower.append(follower.text)


# shop joined
def shop_joined_date():
    joined = product_driver.find_elements(by=By.XPATH, value="//div[@class='biYJq8']/div[3]/div[1]/span")
    for join_num in joined:
        shop_joined.append(join_num.text)


# product description
def product_long_description():
    description = product_driver.find_elements(by=By.CLASS_NAME, value="hrQhmh")
    for desc in description:
        product_description.append(desc.text)


# product images from product page
def product_images():
    image_list = []
    url_list = []
    image_elements = product_driver.find_elements(by=By.XPATH, value="//div[@class='hGIHhp']/div")
    image_num = len(image_elements)
    for index in range(image_num):
        if image_num > 1:
            image = product_driver.find_elements(by=By.XPATH,
                                                 value=f"//div[@class='hGIHhp']/div[{i + 1}]/div/div/div")
        elif image_num == 1:
            image = product_driver.find_elements(by=By.XPATH,
                                                 value=f"//div[@class='hGIHhp']/div/div/div/div")
        image_style_url = image[0].get_attribute("style")
        image_list.append(image_style_url)

    for index in range(image_num):
        starting_index = image_list[index].find('url("')
        end_index = image_list[index].find('")')
        url_list.append(image_list[index][(starting_index + 5):end_index])

    if url_list:
        product_all_images.append(url_list)
    else:
        product_all_images.append("N/a")


# available item's number
def stock():
    available = product_driver.find_elements(by=By.XPATH, value="//div[@class='flex items-center G2C2rT']/div[2]")
    for number in available:
        available_item.append(number.text)


# Search Page Scraping
def scrape_page(driver):
    # Name of the product
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


# Product Characteristics Scraping
def scrape_product_page():
    try:
        rating_score()  # scrap product rating score
        rating_number_count()  # scrap number of product rating
        favorite_number()  # scrap number of "Favorite"
        shop_name()  # scrap shop name
        shop_rating_check()  # scrap shop rating
        shop_response_rate()  # scrap shop's response rate
        shop_response_time()  # scrap shop's response time
        shop_follower_number()  # scrap followers number of the shop
        shop_joined_date()  # scrap shop's joining date
        product_long_description()  # scrap long description of the product
        product_images()  # scrap images of the product
        stock()  # available items number

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



# Part 1: Scrape Search Engine Webpage #
# find products related to the "pet supplements"
def search_product():
    shopee_find = "nnnnn"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://shopee.sg/search?keyword=' + str(shopee_find))
    time.sleep(3)

    # Find total pages number
    num_pages = driver.find_elements(by=By.CLASS_NAME, value="shopee-mini-page-controller__total")
    num_page = 0
    for value in num_pages:
        num_page = int(value.text)

    # Automate Webpages
    for page in range(num_page):
        driver.get('https://shopee.sg/search?keyword=' + str(shopee_find) + '&page=' + str(page))
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
        scrape_page(driver)
    driver.close()


if __name__ == "__main__":
    # search in shopee.sg
    search_product()
    # Part 2: Scrape Product Characteristics ##
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
            scrape_product_page()
        except NoSuchElementException:
            # wait for web to load after press button
            time.sleep(3)

            # Scroll html
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
            scrape_product_page()
    product_driver.close()

    ## Create .csv file ##
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
            "Available number of item": available_item,
            "Product_Score": rating_score,
            "Product_Rating_Counts": rating_count,
            "Product_Favourite_Counts_by_User": fav_count,
            "Links": links,
            "Description": product_description,
            "Product Images URL": product_all_images
        }
    )
    df_shopee.to_csv('shopee_data.csv', index=False, encoding='utf-8')
