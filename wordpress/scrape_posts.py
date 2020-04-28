import csv
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER
import sys
from time import sleep, time

if len(sys.argv) < 3:
    print('usage: python {} <url> <output_file>'.format(sys.argv[0]))
    exit(1)

url = sys.argv[1]
output_file = sys.argv[2].split('.')[0] + str(int(time())) + '.csv'

LOGGER.setLevel(logging.WARNING)

driver = webdriver.Firefox()
driver.get(url)

sleep(1)

read_more = driver.find_elements(By.XPATH, "//a[@class='more-link']")
read_more[0].click()

f = open(output_file, "w", encoding="utf-8")
fwriter = csv.writer(f)

fwriter.writerow(["title", "author", "date", "text"])

# read posts
cnt = 1
while True: 
    sleep(1)

    title = driver.find_element(By.XPATH, "//h1[@class='entry-title']").text
    author = driver.find_element(By.XPATH, "//span[@class='author vcard']").text.lower()
    date = driver.find_element(By.XPATH, "//span[@class='date']").text.lower()

    print(f"{cnt}: {date}, {title}, {author}")

    content = driver.find_elements(By.XPATH, "//div[@class='entry-content']/*[not(self::div)]")

    text = ""
    for c in content:
        if c.text != "":
            text = text + "\\n" + c.text.strip()

    fwriter.writerow([title, author, date, text])
        
    # paginate
    prev_button = driver.find_elements(By.XPATH, "//div[@class='nav-previous']/a")
    if len(prev_button) == 0:
        print('prev button not found')
        f.close()
        break
    href = prev_button[0].get_attribute("href")
    driver.get(href)
    cnt = cnt+1