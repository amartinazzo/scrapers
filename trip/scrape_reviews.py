import csv
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
import logging
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER
from time import sleep


base_url = "http://www.tripadvisor.com.br/Restaurant_Review-g303631-d{}-or0"
profiles_file = "restaurants.csv"
output_dir = "reviews"

restaurants = pd.read_csv(profiles_file, comment="#", header=None)
restaurants = dict(zip(restaurants[0].values, restaurants[1].values))

# proxies = RequestProxy().get_proxy_list()
# PROXY = proxies[0].get_address()
# webdriver.DesiredCapabilities.FIREFOX['proxy']={
#     "httpProxy":PROXY,
#     "proxyType":"MANUAL",
# }

LOGGER.setLevel(logging.WARNING)

options = Options()
#options.headless = True
driver = webdriver.Firefox(options=options)

sleep(2)

for key in restaurants:
    f = open(os.path.join(output_dir, f"{key}.csv"), "w", encoding="utf-8")
    fwriter = csv.writer(f)

    driver.get(base_url.format(str(restaurants[key])))
    
    sleep(10)
    
    title = driver.find_element(By.XPATH, "//h1[@class='ui_header h1']")
    title = title.text
    
    ranking = driver.find_element(By.XPATH, "//span[@class='header_popularity popIndexValidation']")
    ranking = ranking.text.split(" ")[1]

    nr_reviews = driver.find_elements(By.XPATH, "//label[@class='label container cx_brand_refresh_phase2']")
    nr_reviews = nr_reviews[1].text.split("(")[1][:-1].replace(".", "")

    pages = driver.find_elements(By.XPATH, "//a[@class='pageNum last   cx_brand_refresh_phase2']")
    pages = int(pages[-1].text) - 1
    
    print(f"{title}; #{ranking} em SP; {pages} pages; {nr_reviews} reviews")
 
    pages = driver.find_elements(By.XPATH, "//a[@class='pageNum last   cx_brand_refresh_phase2']")
    pages = pages[-1].text
    
    print(f"{title}; #{ranking} em SP; {pages} pages")
 
    # read reviews
    cnt = 1
    while True:
        while True:
            try:
                more_button = driver.find_element(By.XPATH, "//span[@class='taLnk ulBlueLinks']")
                if more_button.text == "Mais":
                    more_button.click()
                break
            except:
                pass
                
        sleep(3)
        print(cnt)
        
        review_titles = driver.find_elements(By.XPATH, "//span[@class='noQuotes']")
        review_titles = [r.text for r in review_titles]
        
        review_dates = driver.find_elements(By.XPATH, "//div[@class='prw_rup prw_reviews_stay_date_hsx']")
        review_dates = [r.text.replace("Data da visita: ", "") for r in review_dates]
        
        review_ratings = driver.find_elements(
            By.XPATH, "//div[@class='ui_column is-9']/span[contains(@class, 'ui_bubble_rating')]")
        review_ratings = [r.get_attribute("class").split("_")[-1] for r in review_ratings]
        

        review_texts = driver.find_elements(
            By.XPATH, "//div[@class='ui_column is-9']/div[@class='prw_rup prw_reviews_text_summary_hsx']") #/p[@class='partial_entry']")
        review_texts = [r.text.replace("\n", "").replace("Mostrar menos", "") for r in review_texts]
        
        assert len(review_titles) == len(review_dates) == len(review_ratings) == len(review_texts)
        
        for i in range(len(review_titles)):
            fwriter.writerow([review_titles[i], review_dates[i], review_ratings[i], review_texts[i]])
            
        # paginate
        next_button = driver.find_elements(By.XPATH, "//a[@class='nav next ui_button primary  cx_brand_refresh_phase2']")
        if cnt==pages:
            print("")
            f.close()
            break
        next_button[0].click()
        cnt = cnt+1
        sleep(5)
