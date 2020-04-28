import csv
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
import logging
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER
from time import sleep, time


base_url = "http://www.tripadvisor.com.br/Restaurant_Review-g303631-d{}-or0"
input_file = "tripadvisor.csv"
output_file = "tripadvisor_metadata.csv"
output_dir = "tripadvisor"

restaurants = pd.read_csv(input_file, comment="#")
restaurants.fillna(0, inplace=True)
restaurants = dict(zip(restaurants["restaurant"].values, restaurants["id"].values.astype(int)))

restaurants_read = pd.read_csv(output_file, comment="#")
restaurants_read = restaurants_read["id"].values

timestamp = int(time())

# webdriver.DesiredCapabilities.FIREFOX['proxy']={
#     "httpProxy": os.environ["PROXY"],
#     "proxyType": "MANUAL",
# }

LOGGER.setLevel(logging.WARNING)

options = Options()
#options.headless = True
driver = webdriver.Firefox(options=options)

sleep(2)

for key in restaurants:
    if restaurants[key]==0:
        print("skipping", key)
        continue

    driver.get(base_url.format(str(restaurants[key])))
    
    sleep(5)
    
    title = driver.find_element(By.XPATH, "//h1[@class='ui_header h1']")
    title = title.text
    
    ranking = driver.find_elements(By.XPATH, "//span[@class='header_popularity popIndexValidation']")
    ranking = ranking[0].text.split(" ")[1] if len(ranking)>0 else 0

    nr_reviews = driver.find_elements(By.XPATH, "//label[@class='label container cx_brand_refresh_phase2']")
    nr_reviews = nr_reviews[1].text.split("(")[1][:-1].replace(".", "")
 
    pages = driver.find_elements(By.XPATH, "//a[@class='pageNum last   cx_brand_refresh_phase2']")
    pages = pages[-1].text if len(pages)>0 else 1

    reinvindicado = driver.find_elements(By.XPATH, "//div[contains(@class, 'restaurants-claimed-badge-ClaimedBadge__container--32Ufv')]")
    reinvindicado = reinvindicado[0].text

    address = driver.find_element(By.XPATH, "//span[@class='detail  ui_link level_4']")
    address = address.text

    headers = driver.find_elements(By.XPATH, "//div[@class='header_links']")
    headers = headers[0].text.split(",")

    price = headers[0]
    tags = ";".join(headers[1:])

    print(f"{title}; #{ranking} em SP; {pages} pages; {nr_reviews}")

    with open(output_file, "a", encoding="utf-8") as f_meta:
        fwriter_meta = csv.writer(f_meta)
        fwriter_meta.writerow([title, str(restaurants[key]), ranking, nr_reviews, reinvindicado, price, tags, address])

    if restaurants[key] in restaurants_read:
        continue

    f = open(os.path.join(output_dir, f"{key}_{timestamp}.csv"), "w", encoding="utf-8")
    fwriter = csv.writer(f)
 
    # read reviews
    cnt = 0
    while True:
        try:
            more_button = driver.find_element(By.XPATH, "//span[@class='taLnk ulBlueLinks']")
            if more_button is not None and more_button.text == "Mais":
                more_button.click()
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
        if len(next_button)==0:
            print("")
            f.close()
            break
        next_button[0].click()
        cnt = cnt+1
        sleep(3)
