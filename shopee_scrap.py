from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver


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


#  --------------------------------------------------Sanity check start----------------------------------------------  #
# getting rid of characters in columns with numbers
def remove_char(all_products_panda):
    sh_rate = all_products_panda['Shop_Response_Rate'].str.extract('(\d+)')
    all_products_panda['Shop_Response_Rate'] = sh_rate
    q_sold = all_products_panda['Quantity_Sold'].str.extract('(\d+)')
    all_products_panda['Quantity_Sold'] = q_sold
    avail_num = all_products_panda["Available number of item"].str.extract('(\d+)')
    all_products_panda["Available number of item"] = avail_num
    fav_count = all_products_panda['Product_Favourite_Counts_by_User'].str.extract('(\d+)')
    all_products_panda['Product_Favourite_Counts_by_User'] = fav_count


#  Correcting Shop_Response_time or replacing text to number:
#  within minutes == 0
#  within hours == 1
#  within days == 2
# others == 3
def correct_time(all_products_panda):
        minutes = all_products_panda['Shop_Response_time'].replace("within minutes", 0)
        all_products_panda['Shop_Response_time'] = minutes
        hr = all_products_panda['Shop_Response_time'].replace("within hours", 1)
        all_products_panda['Shop_Response_time'] = hr
        days = all_products_panda['Shop_Response_time'].replace("within days", 2)
        all_products_panda['Shop_Response_time'] = days
        all_products_panda['Shop_Response_time'] = pd.to_numeric(all_products_panda['Shop_Response_time'], errors='coerce').fillna(3).astype('int')


# getting rid of 'k' in numbers like 1,8k for 'Shop_Rating_Counts' and 'Shop_Followers' columns
def remove_k(all_products_panda):
    result_shop_rating = []
    for i in all_products_panda['Shop_Rating_Counts'].tolist():
        if 'k' in i:
            i = i.replace('k', '')
            i = float(i)
            i *= 1000
            result_shop_rating.append(int(i))
        else:
            result_shop_rating.append(int(i))
    all_products_panda['Shop_Rating_Counts'] = result_shop_rating

    result_shop_followers = []
    for i in all_products_panda['Shop_Followers'].tolist():
        if 'k' in i:
            i = i.replace('k', '')
            i = float(i)
            i *= 1000
            result_shop_followers.append(int(i))
        else:
            result_shop_followers.append(int(i))
    all_products_panda['Shop_Followers'] = result_shop_followers

    result_product_rating = []
    for i in all_products_panda['Product_Rating_Counts'].tolist():
        if 'k' in i:
            i = i.replace('k', '')
            i = float(i)
            i *= 1000
            result_product_rating.append(int(i))
        else:
            result_product_rating.append(int(i))
    all_products_panda['Product_Rating_Counts'] = result_product_rating


#  Correcting Category
def category_correcting(all_products_panda):
    category_list = all_products_panda['Category'].tolist()
    final_category_list = []
    for i in category_list:
        split_category = i.split("\n")
        final_category_list.append(split_category)
    all_products_panda['Category'] = final_category_list


#  Replacing words, and storing only numbers(days)
def correcting_joined_date(all_products_panda):
    joined_ago = all_products_panda['Shop_Joined'].tolist()
    processed_joined_ago_list = []
    for i in joined_ago:
        if 'month' in i:
            number_in_text = [int(x) for x in i.split() if x.isdigit()]
            processed_joined_ago_list.append(int(number_in_text[0] * 30))
        elif "day" in i:
            number_in_text = [int(x) for x in i.split() if x.isdigit()]
            processed_joined_ago_list.append(int(number_in_text[0] * 30))
        else:
            processed_joined_ago_list.append(0)
    all_products_panda['Shop_Joined'] = processed_joined_ago_list


#  --------------------------------------------------Sanity check end----------------------------------------------  #


#  --------------------------------------------------Main processes----------------------------------------------  #
# rating score
def rating_score_product():
    Rate = product_driver.find_elements(by=By.XPATH, value="//div[@class='Bm+f5q']")
    if Rate:
        rating_score.append('N/A')
    else:
        Rate = product_driver.find_elements(by=By.XPATH, value="//div[@class='flex W2tD8-']/div[1]/div[1]")
        for score in Rate:
            if score.text:
                rating_score.append(score.text)
            else:
                rating_score.append('N/A')


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
            fav_count.append("N/A")
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
        product_description.append("N/A")
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
        product_all_images.append("N/A")


# available item's number
def stock():
    available = product_driver.find_elements(by=By.XPATH, value="//div[@class='flex items-center G2C2rT']/div[2]")
    if not available:
        available_item.append("N/A")
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
    global count, number_of_keys
    count += 1
    # actual values
    value_of_category = product_driver.find_elements(by=By.XPATH, value="//div[@class='product-detail "
                                                                        "page-product__detail']/div[1]/div/div")
    # categories of specs
    category_name = product_driver.find_elements(by=By.XPATH,
                                              value="//div[@class='product-detail page-product__detail']/div["
                                                    "1]/div/div/label")
    if not category_name:
        return 0

    # creates dictionary of column names(no duplicates) with empty list (this dictionary will be final output)
    # and dictionary of column names(no duplicates) with their order of appearing as value
    for value in category_name:
        variable = value.text
        if variable in product_specif.keys():
            continue
        else:
            number_of_keys += 1
            product_specif[f"{value.text}"] = []
            order_dic_column[f"{value.text}"] = number_of_keys

    # creates dictionary of product specification value with number(to which column it belongs,based on appearing order)
    for i in range(len(value_of_category)):
        link_in_specific = value_of_category[i].find_elements(By.TAG_NAME, 'a')
        if link_in_specific:
            value_of_category[i] = link_in_specific[0]
        else:
            no_link_in_specific = value_of_category[i].find_elements(By.TAG_NAME, 'div')
            value_of_category[i] = no_link_in_specific[0]
        order_dic_content[f"{value_of_category[i].text}"] = order_dic_column[category_name[i].text]

    # fills product_specif with "N/a"
    for key in product_specif:
        for i in range(count):
            if len(product_specif[key]) < count:
                product_specif[key].append("N/A")
            else:
                break

    # replaces "N/a" to correspondent specification on correspondent index in dictionary
    for specification in order_dic_content:
        position_key = get_key(order_dic_column, order_dic_content[specification])
        product_specif[position_key][count-1] = specification
    order_dic_content.clear()
    # test and extract


# Search Page Scraping
def scrape_page(driver):
    time.sleep(1)
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
    shopee_find = "kle"
    driver = webdriver.Chrome(executable_path="/Users/north/Desktop/research/webscrap/chromedriver")
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
        scroll_pause_time = 0.2
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

    product_driver = webdriver.Chrome(executable_path="/Users/north/Desktop/research/webscrap/chromedriver")
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
        print(f"left pages = {len(links) + 1 - item_num}")
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

    remove_char(df_shopee)
    correct_time(df_shopee)
    remove_k(df_shopee)
    category_correcting(df_shopee)
    correcting_joined_date(df_shopee)


    df_shopee.to_csv('shopee_data.csv', index=False, encoding='utf-8')
    print("--- %s seconds for whole code ---" % (time.time() - start_time_2))
