from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import pandas as pd

options = Options()
driver = webdriver.Edge(options=options)
driver.get('https://play.google.com/store/apps/details?id=com.offerup&hl=en_US')

# allReviews = driver.find_element(By.CLASS_NAME, 'VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-dgl2Hf ksBjEc lKxP2d LQeN7 aLey0c')
# allReviews.click()
result = []

# driver.quit()
