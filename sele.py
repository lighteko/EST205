from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import pandas as pd
import time

options = Options()
options.add_experimental_option('detach', True)
options.add_argument("headless")
driver = webdriver.Edge(options=options)

def get_shadow_root(element):
    return driver.execute_script('return arguments[0].shadowRoot', element)

def marketplace_reviews():
    driver.get('https://www.productreview.com.au/listings/facebook-marketplace')
    reviews = driver.find_elements(By.CLASS_NAME, 'enable-container-query')
    # time.sleep(2)
    # driver.get("https://www.productreview.com.au/listings/facebook-marketplace?page=2"
    # reviews += driver.find_elements(By.CLASS_NAME, 'enable-container-query')
    # time.sleep(2)
    # driver.get("https://www.productreview.com.au/listings/facebook-marketplace?page=3")
    # reviews += driver.find_elements(By.CLASS_NAME, 'enable-container-query')

    res = []
    for review in reviews:
        res.append(
            {
                'score': int(review.find_element(By.CLASS_NAME, '_Xfwvv.awyZoO.amGpHl._G059D.FMDBVr.BkNVVp._hKC60.Os4Z9c.LUL88i').get_attribute('title')[0]),
                'content': review.find_element(By.CLASS_NAME, 'YzMyQX.__rWrp.vriYO8').get_attribute('innerText'),
            }
        )
    pd.DataFrame(res).to_csv('./res/facebook_marketplace.csv')

def marketplace_reddit():
    driver.get('https://www.reddit.com/r/FacebookMarketplace/?f=flair_name%3A%22Discussion%22')

    posts = []
    while True:
        newPosts = driver.find_elements(By.TAG_NAME, 'shreddit-post')
        for new in newPosts:
            link = new.find_element(By.CLASS_NAME, 'absolute.inset-0').get_attribute('href')
            if link not in posts:
                posts.append(link)
        if len(posts) > 2000:
            break
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    results = []
    for post in posts:
        driver.get(post)
        mainContent = driver.find_element(By.ID, "main-content")
        title = mainContent.find_element(By.TAG_NAME, 'shreddit-title').get_attribute('title')
        try:
            time.sleep(0.5)
            readMore = mainContent.find_element(By.XPATH, '//*[contains(@id, "read-more-button")]')
            if (readMore != None):
                readMore.click()
        except:
            pass
        content = mainContent.find_element(By.TAG_NAME, "shreddit-post")
        paragraphs = content.find_element(By.CLASS_NAME, "md.text-14").find_elements(By.TAG_NAME, 'p')
        text = ""
        for p in paragraphs:
            text += p.get_attribute('innerText') + "\n"
        shadowRoot = get_shadow_root(content)
        upvote = int(shadowRoot.find_element(By.CSS_SELECTOR, 'div.flex.flex-row.items-center.flex-nowrap.overflow-hidden.justify-start.h-2xl.mt-md.px-md.xs\:px-0 > span > span > span > faceplate-number').get_attribute('innerText'))
        
        results.append({
            'title': title,
            'content': text,
            'upvote': upvote,
        })
    pd.DataFrame(results).to_csv('./res/facebook_marketplace_reddit.csv')
    driver.close()

marketplace_reddit()
    

