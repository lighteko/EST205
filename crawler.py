from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import pandas as pd
import time
import progressbar
from google_play_scraper import app as Sort, reviews
import pandas as pd
from app_store_scraper import AppStore

class Crawler:
    def __init__(self, mode: int):
        self.mode = mode
        pass

    def run(self):
        if self.mode == 0:
            self.google_play()
        elif self.mode == 1:
            self.app_store()
        elif self.mode == 2:
            self.reddit()

    def get_shadow_root(self, driver, element):
        return driver.execute_script('return arguments[0].shadowRoot', element)
    
    def google_play(self):
        print("Step 1: Information Required")
        package = input("Enter the app package name: ")
        review_count = int(input("Enter the amount of reviews to scrape: "))
        
        print("Step 2: Scraping Reviews ...")
        bar = progressbar.ProgressBar(maxval=review_count).start()
        data, _ = reviews(
        package,
        lang='en',
        country='us',
        count=review_count,
        )
        res = []
        for (i, r) in enumerate(data):
            bar.update(i)
            if type(r['score']) != int or not r['score'] <= 5 and r['score'] >= 1:
                continue 
            res.append({
            'content': r['content'],
            'score': r['score'],
            })
        bar.finish()
        print("Step 3: Saving Data ...")
        name = input("Enter the name of the app: ")
        pd.DataFrame(res).to_csv(f'./res/{name}_google_play.csv')
        print("DONE")
    
    def app_store(self):
        print("Step 1: Information Required")
        name = input("Enter the name of the app: ")
        count = int(input("Enter the amount of reviews to scrape: "))
        data = AppStore(country="us", app_name=name)
        data.review(how_many=count)
        res = []
        bar = progressbar.ProgressBar(maxval=len(data.reviews)).start()
        for i, r in enumerate(data.reviews):
            bar.update(i)
            if not r['rating'] <= 5 and r['rating'] >= 1:
                continue 
            res.append({
                'content': r['title'] + ": " + r['review'],
                'score': r['rating'],
            })
        bar.finish()
        print("Step 3: Saving Data ...")
        pd.DataFrame(res).to_csv(f'./res/{name}_app_store.csv')
        print("DONE")
    
    def reddit(self):
        print("Step 0: Information Required")
        url = input("Enter the URL of the subreddit: ")
        name = input("Enter the name of the subreddit: ")
        review_count = int(input("Enter the amount of posts to scrape: "))
        options = Options()
        options.add_experimental_option('detach', True)
        driver = webdriver.Edge(options=options)

        driver.get(url)
        posts = []
        print("STEP 1: Scraping posts urls...")
        bar = progressbar.ProgressBar(maxval=review_count).start()
        while True:
            newPosts = driver.find_elements(By.TAG_NAME, 'shreddit-post')
            for new in newPosts:
                try:
                    link = new.get_attribute("content-href")
                except:
                    continue
                if link not in posts:
                    posts.append(link)
            if len(posts) >= review_count:
                break
            bar.update(len(posts))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        bar.finish()
        results = []
        print("STEP 2: Scraping posts content...")
        bar = progressbar.ProgressBar(maxval=len(posts)).start()
        for i, post in enumerate(posts):
            bar.update(i)
            driver.get(post)
            try:
                mainContent = driver.find_element(By.ID, "main-content")
                title = mainContent.find_element(By.TAG_NAME, 'shreddit-title').get_attribute('title')
                try:
                    readMore = mainContent.find_element(By.XPATH, '//*[contains(@id, "read-more-button")]')
                    if (readMore != None):
                        readMore.click()
                except:
                    pass
                content = mainContent.find_element(By.TAG_NAME, "shreddit-post")
                paragraphs = content.find_element(By.CLASS_NAME, "md.text-14").find_elements(By.TAG_NAME, 'p')
            except:
                continue
            text = ""
            for p in paragraphs:
                text += p.get_attribute('innerText') + "\n"
            shadowRoot = self.get_shadow_root(driver, content)
            upvote = shadowRoot.find_element(By.CSS_SELECTOR, 'div.flex.flex-row.items-center.flex-nowrap.overflow-hidden.justify-start.h-2xl.mt-md.px-md.xs\:px-0 > span > span > span > faceplate-number').get_attribute('number')
            date = content.get_attribute('created-timestamp')
            results.append({
                'date': date,
                'title': title,
                'content': text,
                'upvote': int(upvote),
            })
        bar.finish()
        print("STEP 3: Saving results...")
        pd.DataFrame(results).to_csv(f'./res/{name}_reddit.csv')
        driver.close()
        print("DONE")
