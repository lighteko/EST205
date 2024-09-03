from google_play_scraper import app as Sort, reviews
import pandas as pd
from app_store_scraper import AppStore

# offerupAND, _ = reviews(
#     'com.offerup',
#     lang='en',
#     country='us',
#     count=20000, 
# )

# res = []
# for (i, r) in enumerate(offerupAND):
#     if not r['score'] <= 5 and r['score'] >= 1:
#         continue 
#     res.append({
#         'content': r['content'],
#         'score': r['score'],
#     })
# pd.DataFrame(res).to_csv('./res/offerup_google_play.csv')

# offerupIOS = AppStore(country="us", app_name="offerup-buy-sell-letgo")
# offerupIOS.review()
# iosRes = []

# for r in offerupIOS.reviews:
#     if not r['rating'] <= 5 and r['rating'] >= 1:
#         continue 
#     iosRes.append({
#         'content': r['title'] + ": " + r['review'],
#         'score': r['rating'],
#     })
# pd.DataFrame(iosRes).to_csv('./res/offerup_app_store.csv')

ebayAND, _ = reviews(
    'com.ebay.mobile',
    lang='en',
    country='us',
    count=20000,
)

res = []
for (i, r) in enumerate(ebayAND):
    if not r['score'] <= 5 and r['score'] >= 1:
        continue 
    res.append({
        'content': r['content'],
        'score': r['score'],
    })
pd.DataFrame(res).to_csv('./res/ebay_google_play.csv')

# ebayIOS = AppStore(country="us", app_name="ebay-online-shopping-selling")
# ebayIOS.review()

# iosRes = []
# for r in ebayIOS.reviews:
#     if not r['rating'] <= 5 and r['rating'] >= 1:
#         continue 
#     iosRes.append({
#         'content': r['title'] + ": " + r['review'],
#         'score': r['rating'],
#     })
# pd.DataFrame(iosRes).to_csv('./res/offerup_app_store.csv')

