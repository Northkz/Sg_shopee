from selenium.common.exceptions import NoSuchElementException
import time, re, math
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


count = 0
number_of_keys = 0
product_specif = {}
order_dic_column = {}
order_dic_content = {}
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
available_item = []
brand_name = []


# rating score
def rating_score_product():
    Rate = product_driver.find_elements(by=By.XPATH, value="//div[@class='Bm+f5q']")
    if Rate:
        rating_score.append('No score')
    else:
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
    description_text = ""
    description = product_driver.find_elements(by=By.CLASS_NAME, value="hrQhmh")
    if not description:
        product_description.append("N/a")
    else:
        for desc in description:
            description_text += ("\n" + desc.text)
        product_description.append(description_text)


# product images from product page
def product_images():
    image1_url = []
    url_list = []
    image = product_driver.find_elements(by=By.XPATH, value="//div[@class='hGIHhp']/div")
    num = len(image)
    for i in range(num):
        test = product_driver.find_elements(by=By.XPATH, value="//div[@class='hGIHhp']/div["+str(i+1)+"]/div[1]/div[1]/div")
        for j in test:
            p = j.get_attribute("style")
            image1_url.append(p)

    for index in range(num):
        starting_index = image1_url[index].find('url("')
        end_index = image1_url[index].find('")')
        url_list.append(image1_url[index][(starting_index + 5):end_index])

    if url_list:
        product_all_images.append(url_list)
    else:
        product_all_images.append("N/a")


# available item's number
def stock():
    available = product_driver.find_elements(by=By.XPATH, value="//div[@class='flex items-center G2C2rT']/div[2]")
    if not available:
        available_item.append("N/a")
    else:
        for number in available:
            available_item.append(number.text)


#  function to get "key" of the dictionary
def get_key(dic, val):
    for key, value in dic.items():
        if val == value:
            return key
    return "There is no such Key"


def product_specification():
    # actual values
    value_of_category = product_driver.find_elements(by=By.XPATH, value="//div[@class='product-detail page-product__detail']/div[1]/div/div/div[1]")
    # categories of specs
    category_name = product_driver.find_elements(by=By.XPATH,
                                              value="//div[@class='product-detail page-product__detail']/div[1]/div/div/label")
    # if len(value_of_category) != len(category_name):
    #     for category in category_name:
    #
    # extract each individual value
    global count, number_of_keys
    count += 1

    # creates dictionary of column names(no dubicates) with empty list as value == product_specif
    # and dictionary of column names(no dubicates) with their order as value
    for value in category_name:
        variable = value.text
        if variable in product_specif.keys():
            continue
        else:
            number_of_keys += 1
            product_specif[f"{value.text}"] = []
            order_dic_column[f"{value.text}"] = number_of_keys

    # extract each corresponding category
    # creates dictionary of specifications with number(to which column it belongs)
    for i in range(len(value_of_category)):
        order_dic_content[f"{value_of_category[i].text}"] = order_dic_column[category_name[i].text]

    # fills product_specif with "N/a"
    for key in product_specif:
        for i in range(count):
            if len(product_specif[key]) < count:
                product_specif[key].append("N/a")
            else:
                break  # ???? not sure, maye 'continue'

    # replaces "N/a" to correspondent specification on correspondent index in dictionary
    for specification in order_dic_content:
        position_key = get_key(order_dic_column, order_dic_content[specification])
        product_specif[position_key][count-1] = specification
    order_dic_content.clear()
    # test and extract


# Search Page Scraping
def scrape_page(driver):

    # Name of the product
    item_name = driver.find_elements(by=By.XPATH, value="//div[@class='dpiR4u']/div[1]/div[1]")
    for name in item_name:
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
    time.sleep(0.15)


# Product Characteristics Scraping
def scrape_product_page():
    try:
        rating_score_product()  # scrap product rating score
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
        product_specification()  # scrap specification of the product

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
    shopee_find = "mmmm"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://shopee.sg/search?keyword=' + str(shopee_find))
    time.sleep(2)

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
        scroll_pause_time = 0.03
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
    start_time_2 = time.time()

    # search in shopee.sg
    search_product()
    item_num = 0
    print(f"item number {item_num}")
    # Part 2: Scrape Product Characteristics ##
    product_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # Automate Product Links
    for i in range(len(links)):
        start_time = time.time()
        test1 = {
            "Shop_Name": len(seller_name),
            "Shop_Rating_Counts": len(shop_rating),
            "Shop_Followers": len(shop_follower),
            "Shop_Response_Rate": len(shop_responserate),
            "Shop_Response_time": len(shop_responsetime),
            "Shop_Joined": len(shop_joined),
            "Product_Name": len(retail_name),
            "Product_Price": len(retail_price),
            "Quantity_Sold": len(Quantity_Sold),
            "Available number of item": len(available_item),
            "Product_Score": len(rating_score),
            "Product_Rating_Counts": len(rating_count),
            "Product_Favourite_Counts_by_User": len(fav_count),
            "Links": len(links),
            "Description": len(product_description),
            "Product Images URL": len(product_all_images)
        }
        item_num += 1
        print(f"left pages = {len(links) - item_num}")
        print("\n====================\n")
        print(pd.Series(test1))
        print("\n====================\n")
        product_driver.get(links[i])
        try:
            # Scoll html
            pause_time = 0
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
            # Scroll html
            pause_time = 0
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
        print("--- %s seconds ---" % (time.time() - start_time))
    product_driver.close()
    print(f"Dictionary length -> {len(product_specif)}")
    for i in product_specif:
        print(f"{i} = {len(product_specif[i])}")

    print(f"shop_name = {len(seller_name)}; shop_rating = {len(shop_rating)} ")
    print(f"Shop_Followers = {len(shop_follower)}, Available = {len(available_item)}")
    print(f"shop_responserate = {len(shop_responserate)}; shop_responsetime = {len(shop_responsetime)} ")
    print(f"shop_joined = {len(shop_joined)}; retail_name = {len(retail_name)} ")
    print(f"retail_price = {len(retail_price)}; Quantity_Sold = {len(Quantity_Sold)} ")
    print(f"rating_score = {len(rating_score)}; rating_count = {len(rating_count)} ")
    print(f"fav_count = {len(fav_count)}; links = {len(links)} ")
    print(f"Description = {len(product_description)}, Images = {len(product_all_images)}")
    print(product_specif)


    ## Create .csv file ##
    all_data_dict =  {
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
    all_data_dict.update(product_specif)
    df_shopee = pd.DataFrame(all_data_dict)

    df_shopee.to_csv('shopee_data.csv', index=False, encoding='utf-8')
    print("--- %s seconds for whole code ---" % (time.time() - start_time_2))
