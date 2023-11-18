import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import lxml
import requests
from bs4 import BeautifulSoup

browser = webdriver.Chrome(ChromeDriverManager().install())
url = "https://www.melon.com/chart/index.htm"

browser.get(url)
time.sleep(1)

soup = BeautifulSoup(browser.page_source, "lxml")
top100 = soup.find("div", attrs = {"class" : "service_list_song type02 d_song_list"})

title = top100.findAll("div", attrs = {"class" : "ellipsis rank01"})
author = top100.findAll("div", attrs = {"class" : "ellipsis rank02"})
atitle = top100.findAll("div", attrs = {"class" : "ellipsis rank03"})
ilke = top100.findAll("button", attrs = {"class" : "button_etc like"})
# rate = top3.findAll("span", attrs = {"class" : "Rating__star_area--dFzsb"})


print("-----실시간 인기 웹툰 5-----")
for i in range(5):
  author_cut = len(author[i].text) // 2
  a = title[i].text.strip('\n')
  b = author[i].text[author_cut:].strip('\n')
  c = atitle[i].text.strip('\n')
  d = ilke[i].text[9:].strip('\n')
  print(f"{i+1} - {a} || {b} || {c} || {d}")
# || {rate[1].text}")
