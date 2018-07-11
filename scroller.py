# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
#
# chromedriver = "/Users/kylerood/Generic-Web-Classifier/image-classification-keras/chromedriver"
# browser = webdriver.Chrome(chromedriver)
# browser.get('https://images.google.com/')
#
# search = browser.find_element_by_name('q')
# search.send_keys("google search through python")
# search.send_keys(Keys.RETURN) # hit return after you enter search text
# time.sleep(5) # sleep for 5 seconds so you can see the results
#
# #execute scrolling on and infinite page
# SCROLL_PAUSE_TIME = 0.5
#
# # Get scroll height
# last_height = browser.execute_script("return document.body.scrollHeight")
#
# while True:
#     # Scroll down to bottom
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#
#     # Wait to load page
#     time.sleep(SCROLL_PAUSE_TIME)
#
#     # Calculate new scroll height and compare with last scroll height
#     new_height = browser.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height
#
# #browser.execute_script(open("./grab_images.js").read())
# # js = "var script = document.createElement('script'); script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js'; document.getElementsByTagName('head')[0].appendChild(script); var urls = $('.rg_di .rg_meta').map(function() { return JSON.parse($(this).text()).ou; }); var textToSave = urls.toArray().join('\n'); var hiddenElement = document.createElement('a'); hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave); hiddenElement.target = '_blank'; hiddenElement.download = 'urls.txt'; hiddenElement.click();"
# #
# # browser.execute_script(js)
#
# injected_javascript = (
#     "var script = document.createElement('script');"
#     "script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js';"
#     "document.getElementsByTagName('head')[0].appendChild(script);"
#     "var urls = $('.rg_di .rg_meta').map(function() { return JSON.parse($(this).text()).ou; });"
#     "var textToSave = urls.toArray().join('\n');"
#     "var hiddenElement = document.createElement('a');"
#     "hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);"
#     "hiddenElement.target = '_blank';"
#     "hiddenElement.download = 'urls.txt';"
#     "hiddenElement.click();"
#
# )
#
# browser.execute_async_script(injected_javascript)
#
# #browser.quit()

from bs4 import BeautifulSoup
import requests
import re
import urllib.request
import os
import http.cookiejar
import json

def get_soup(url):
    return BeautifulSoup(urllib.request.urlopen(url),'html.parser')


query = input("dogs")# you can change the query for the image  here
image_type="ActiOn"
query= query.split()
query='+'.join(query)
url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
print(url)
#add the directory for your image here
DIR="Pictures"
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}
soup = get_soup(url)


ActualImages=[]# contains the link for Large original images, type of  image
for a in soup.find_all("div",{"class":"rg_meta"}):
    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
    ActualImages.append((link,Type))

print("there are total" , len(ActualImages),"images")

if not os.path.exists(DIR):
            os.mkdir(DIR)
DIR = os.path.join(DIR, query.split()[0])

if not os.path.exists(DIR):
            os.mkdir(DIR)
###print images
for i , (img , Type) in enumerate( ActualImages):
    try:
        raw_img = urllib.request.urlopen(img).read()

        cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
        print(cntr)
        if len(Type)==0:
            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+".jpg"), 'wb')
        else :
            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+"."+Type), 'wb')


        f.write(raw_img)
        f.close()
    except Exception as e:
        print("could not load : "+img)
        print(e)
