import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import csv
import json
from bs4 import BeautifulSoup

# user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
options = webdriver.ChromeOptions()
# options.headless = True
# options.add_argument(f'user-agent={user_agent}')
# options.add_argument("--window-size=1920,1080")
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--allow-running-insecure-content')
# options.add_argument("--disable-extensions")
# options.add_argument("--proxy-server='direct://'")
# options.add_argument("--proxy-bypass-list=*")
# options.add_argument("--start-maximized")
# options.add_argument('--disable-gpu')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--no-sandbox')

# driver = webdriver.Chrome("/usr/bin/chromedriver")

driver = webdriver.Chrome(ChromeDriverManager().install())
action = ActionChains(driver)


def write_csv(ads):
    with open('results.csv', 'a') as f:
        fields = ['title', 'url', 'price', 'ranking']

        writer = csv.DictWriter(f, fieldnames=fields)
        for ad in ads:
            writer.writerow(ad)


def get_html(url):
    # driver.get("https://www.amazon.com/s?k=canon+5d&page=1&crid=3W06P6JS4UAQK&qid=1650609151&sprefix=canon+5d%2Caps%2C502&ref=sr_pg_2")
    driver.get(url)
    return driver.page_source


def scrape_data(card):
    try:
        h2 = card.h2
    except:
        title = ''
        url = ''
    else:
        title = h2.text
        url = h2.a.get('href')

    try:
        price = card.find('span', class_='a-price-whole').text.strip('.')
        ranking = card.find('span', class_='a-size-base s-underline-text').text.strip('.')
    except:
        price = ''
        ranking = ''
    else:
        price = ''.join(price.split(','))
        ranking = ''.join(ranking.split(','))
        print(price)
        print(ranking)

    data = {'title': title, 'url': url, 'price': price, 'ranking': ranking}

    return data


def main():
    ads_data = []
    for i in range(10):
        url = f'https://www.amazon.com/s?k=canon+5d&page={i}&crid=3W06P6JS4UAQK&qid=1650622982&sprefix=canon+5d%2Caps%2C502&ref=sr_pg_2'
        html = get_html(url)
        soup = BeautifulSoup(html, 'lxml')

        cards = soup.find_all('div', {'data-asin': True, 'data-component-type': 's-search-result'})

        for card in cards:
            data = scrape_data(card)
            ads_data.append(data)
    write_csv(ads_data)
    # assert "Amazon.com. Spend less. Smile more." in driver.title
    # elem = driver.find_element_by_name("field-keywords")
    # elem.clear()
    # elem.send_keys("baby")
    # elem.send_keys(Keys.RETURN)
    # assert "No results found." not in driver.page_source
    # driver.close()


def twitter_login():
    url = "https://twitter.com/i/flow/login"
    driver.get(url)
    #
    # email_xpath='/html/body/div/div/div/div/main/div/div/div/div[2]/div[2]/div[1]/div/div/div[5]/label/div/div[2]/div/input'
    # password_xpath='/html/body/div/div/div/div/main/div/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/label/div/div[2]/div[1]/input'
    # login_button_xpath='/html/body/div/div/div/div/main/div/div/div/div[2]/div[2]/div[2]/div/div/div[1]/div/div'
    try:
        myElem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")

    email_element = driver.find_element_by_xpath('//input[@name="text"]')
    email_element.send_keys('03096261615')
    next_button_element = driver.find_element_by_xpath("//*[contains(text(), 'Next')]")
    next_button_element.click()
    time.sleep(2)
    password_element = driver.find_element_by_xpath('//input[@name="password"]')
    password_element.send_keys('chohan543210')
    login_button_element = driver.find_element_by_xpath("//*[contains(text(), 'Log in')]")
    login_button_element.click()
    # login_button_element=driver.find_element_by_xpath('/html/body/div/div/div/div/main/div/div/div/div[2]/div[2]/div[2]/div/div/div[1]/div/div')

    time.sleep(3)
    tweet_button = driver.find_element_by_xpath('//a[@data-testid="SideNav_NewTweet_Button"]')
    tweet_button.click()
    time.sleep(2)
    tweet = "#MarchAgainstImportedGovt"
    tweet = driver.find_element_by_xpath('//div[@aria-autocomplete="list"]').send_keys(tweet)
    time.sleep(3)
    # tweet.send_keys(tweet)
    type_suggestion = driver.find_element_by_xpath('//div[@data-testid="typeaheadResult"]').click()
    submit_tweet = driver.find_element_by_xpath('//div[@data-testid="tweetButton"]').click()
    time.sleep(2)
    # submit_tweet.click()
    # url = "https://twitter.com/ImranKhanPTI"
    # driver.get(url)
    # time.sleep(3)
    # followers=driver.find_element_by_css_selector('a[href="/ImranKhanPTI/followers"] > span >span').text
    # print(followers+" Followers")
    #
    # time.sleep(3)
    # following = driver.find_element_by_css_selector('a[href="/ImranKhanPTI/following"] > span >span').text
    # print(following+" Following")
    mycookies = driver.get_cookies()
    print(len(mycookies))


def amazon_data():
    # url = "https://www.daraz.pk"
    # driver.get(url)
    # cap_button = driver.find_element_by_xpath('//input[@id="q"]').send_keys('ipods')
    #
    # amazon_search_box=driver.find_element_by_xpath('//div[@class="search-box__search--2fC5"]')
    # amazon_search_box.click()
    url = "https://www.amazon.com"
    # driver.maximize_window()
    # driver.minimize_window()
    driver.get(url)
    driver.find_element_by_xpath('//input[@id="twotabsearchtextbox"]').send_keys('camera')

    amazon_search_box = driver.find_element_by_xpath('//input[@id="nav-search-submit-button"]')
    amazon_search_box.click()
    # # html=driver.page_source
    # soup=BeautifulSoup(html,'lxml')
    # cards=soup.find_all('span',{'class':'a-size-medium a-color-base a-text-normal'})
    # print(len(cards))
    # product_class='a-size-medium a-color-base a-text-normal'
    # time.sleep(3)
    product_name = []
    # product = driver.find_element_by_xpath('//span[@class="a-size-medium a-color-base a-text-normal"]')
    # print(product)

    while True:
        # driver.get("https://www.amazon.com/s?k=canon+5d&qid=1652167898&ref=sr_pg_{}".format(i))
        # time.sleep(2)
        # driver.get("https://www.amazon.com/s?k=canon+5d&ref=nb_sb_noss")
        driver.execute_script("window.scrollTo(0, 4000);")
        time.sleep(3)
        items = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@data-component-type='s-search-result']")))
        # items = driver.find_element_by_xpath("//div[@class='s-result-item']")
        # items = WebDriverWait(driver, 8).until( EC.presence_of_all_elements_located((By.XPATH,
        # "//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']"))) print(
        # items)
        #
        for item in items:
            # print(item)
            # name = item.find_element_by_xpath('.//span[@class="a-size-medium a-color-base a-text-normal"]')
            product_name = item.find_element_by_tag_name("h2")
            print(product_name.text)
            link = item.find_element_by_tag_name("a")
            print(link.get_attribute('href'))
            # print(link)
            # print(item)
            # print(link)
            # product_name.append(product_name)
            # print(len(product_name))
        # next_button_element = driver.find_element_by_xpath("//*[contains(text(), 'Next')]")
        pagination_div = driver.find_element_by_xpath("//span[@class='s-pagination-strip']")
        next_button_element = pagination_div.find_element_by_xpath("//*[contains(text(), 'Next')]")
        if 's-pagination-item s-pagination-next s-pagination-disabled' in next_button_element.get_attribute('class'):
            break
        next_button_element.click()
        # used
        # print(item.text)
        # print(item.get_attribute('href'))

        # break

        # elems = items.find_elements_by_xpath("//h2[@class='a-size-mini a-spacing-none a-color-base
        # s-line-clamp-2']/a")

        # time.sleep(4)
        # print()

        # for item in items:
        #     name = item.find_element_by_xpath('.//span[@class="a-size-medium a-color-base a-text-normal"]')
        #     # print (name.text)
        #     products.append(name.text)
        #     # print(item)
        # print(elems)
        #

        # links = elems.get_attribute("href")
        # print(elems)
        # for elem in elems:
        #     links = elem.get_attribute("href")
        #     print(links)

        # links = [elem.get_attribute("href") for elem in elems]

        # break
        # if links == elem.get_attribute("href"):
        #     break
        # else:
        #      print(links)

        # print(item.find_element_by_xpath("//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-2']/a").get_attribute('href'))
        # print(links)
        # print(len(items))
        # print(len(products))

        # for product in products:
        #     print(product)

        # time.sleep(2)
        # next_button_element = driver.find_element_by_xpath("//*[contains(text(), 'Next')]")
        # if 's-pagination-item s-pagination-next s-pagination-disabled' in next_button_element.get_attribute('class'):
        #     break
        # next_button_element.click()

        # strUrl = driver.current_url
        # print(strUrl)

    # print(len(product_name))
    # product=driver.find_element_by_xpath("//div[@class='title--wFj93']").text
    # # products.extend(product)
    # print(len(product))
    #     next_button=driver.find_element_by_xpath("//li[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']")
    #     next_button.click()
    #     time.sleep(3)

    # main()
    # driver.quit()
    # twitter_login()


res = []
res2 = []
tweets = []
tweets_replies = []
Name = []
User_name = []
Description = []
Follow_following = []
from selenium.common import exceptions


def twitter_data():
    items = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='primaryColumn']")))
    print(len(items))

    for item in items:
        name = item.find_element_by_xpath("//div[@class='css-1dbjc4n r-1ny4l3l']")
        print(name.text)
        Name.append(name.text)
        user_name = item.find_element_by_xpath("//div[@dir='ltr']")
        print(user_name.text)
        User_name.append(user_name.text)
        description = item.find_element_by_xpath('//div[@data-testid="UserDescription"]')
        print(description.text)
        Description.append(description.text)
        follow_following = item.find_element_by_xpath('//div[@class="css-1dbjc4n r-13awgt0 r-18u37iz r-1w6e6rj"]')
        print(follow_following.text)
        Follow_following.append(follow_following.text)

    for i in range(5):
        items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='tweetText']")))
        print(len(items))
        time.sleep(3)
        body = driver.find_element_by_css_selector('body')
        body.send_keys(Keys.PAGE_DOWN)
        try:
            frame2 = (driver.find_element_by_xpath("//div[@data-testid='sheetDialog']"))
            exit_button = frame2.find_element_by_xpath("//div[@data-testid='app-bar-close']")
            exit_button.click()
        except Exception as e:
            print("items", e)
            try:
                for k in items:
                    res.append(k.text)
            except exceptions.StaleElementReferenceException as e:
                print(e)
                pass


def tweet_replies():
    # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    # time.sleep(3)
    # item = driver.find_element_by_xpath("//div[@data-testid='ScrollSnap-SwipeableList']")
    # tweet_replies_button = item.find_element_by_xpath("//*[contains(text(), 'Tweets & replies')]").click()
    url = "https://twitter.com/ImranKhanPTI/with_replies"
    driver.get(url)
    for i in range(5):
        items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='tweetText']")))
        print(len(items))
        body = driver.find_element_by_css_selector('body')
        body.send_keys(Keys.PAGE_DOWN)
        try:
            frame2 = (driver.find_element_by_xpath("//div[@data-testid='sheetDialog']"))
            exit_button = frame2.find_element_by_xpath("//div[@data-testid='app-bar-close']")
            exit_button.click()
        except Exception as e:
            print("items", e)
            try:
                for k in items:
                    res2.append(k.text)
            except exceptions.StaleElementReferenceException as e:
                print(e)
                pass


def media():
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(3)
    item = driver.find_element_by_xpath("//div[@data-testid='ScrollSnap-SwipeableList']")
    media_button = item.find_element_by_xpath("//*[contains(text(), 'Media')]").click()
    time.sleep(3)
    try:
        frame2 = (driver.find_element_by_xpath("//div[@data-testid='sheetDialog']"))
        exit_button = frame2.find_element_by_xpath("//div[@data-testid='app-bar-close']")
        exit_button.click()
    except Exception as e:
        print("items", e)


def likes():
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(3)
    item = driver.find_element_by_xpath("//div[@data-testid='ScrollSnap-SwipeableList']")
    like_button = item.find_element_by_xpath("//*[contains(text(), 'Likes')]").click()
    time.sleep(3)
    try:
        frame2 = (driver.find_element_by_xpath("//div[@data-testid='sheetDialog']"))
        exit_button = frame2.find_element_by_xpath("//div[@data-testid='app-bar-close']")
        exit_button.click()
    except Exception as e:
        print("items", e)


if __name__ == '__main__':
    url = "https://twitter.com/ImranKhanPTI"
    driver.get(url)
    # driver.implicitly_wait(10)
    time.sleep(3)
    twitter_data()
    res = list(dict.fromkeys(res))

    i = 1
    while (i <= 5):
        print(i, " = ", res[i])
        tweets.append(res[i])
        i = i + 1
    try:
        frame2 = (driver.find_element_by_xpath("//div[@data-testid='sheetDialog']"))
        exit_button = frame2.find_element_by_xpath("//div[@data-testid='app-bar-close']")
        exit_button.click()
    except Exception as e:
        print("items", e)
    tweet_replies()
    res2 = list(dict.fromkeys(res2))
    j = 1
    while (j <= 5):
        print(j, " = ", res2[j])
        tweets_replies.append(res2[j])
        j = j + 1
    try:
        frame2 = (driver.find_element_by_xpath("//div[@data-testid='sheetDialog']"))
        exit_button = frame2.find_element_by_xpath("//div[@data-testid='app-bar-close']")
        exit_button.click()
    except Exception as e:
        print("items", e)
    media()
    likes()
    dict={
        "name": Name,
        "user_name": User_name,
        "description":Description,
        "follow_following":Follow_following,
        "tweets":tweets,
        "tweets_replies":tweets_replies
    }
    print("\n")
    # name=json.dumps(Name)
    # user_name=json.dumps(User_name)
    # description=json.dumps(Description)
    # follow_following=json.dumps(Follow_following)
    # tweets=json.dumps(tweets)
    # tweets_replies=json.dumps(tweets_replies)
    # json.dumps([Name, User_name,Description,Follow_following,tweets,tweets_replies])
    # print(name)
    # print(user_name)
    # print(description)
    # print(follow_following)
    # print(tweets)
    # print(tweets_replies)
    # writing in json file
    # json_object = json.dumps([Name, User_name, Description, Follow_following, tweets, tweets_replies])
    json_object = json.dumps(dict)
    with open("data.json", "w", encoding='iso-8859-1') as wfile:
        wfile.write(json_object)

    with open('data.json', 'r') as f:
        data = json.load(f)
    print(data)
