import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from pytube import YouTube
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

def init():
    return webdriver.Chrome(executable_path="chromedriver.exe")

def search_and_download(search_term: str, driver_path: str, target_path="D:\YT", number_videos=2):
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # return fetch_video_urls(search_term, number_videos, wd=wd, sleep_between_interactions=2)
    # with webdriver.chrome(executable_path=driver_path) as wd:
    #     fetch_video_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)
    #counter = 0
    #for elem in res:

def fetch_video_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 2):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

def search_channel(query: str, wd):
    base_url = "https://www.youtube.com/results?search_query="
    search_url = base_url + query
    wd.get(search_url)

def open_channel(wd):
    channel_link = wd.find_element(By.XPATH,"//div[@id='content-section']//following-sibling::yt-formatted-string[1]")
    channel_link.click()

def open_video(wd):
    video_tab = wd.find_elements(By.CLASS_NAME, "tab-content")[1]
    video_tab.click()

def download(wd, number_videos):
    video_thumbnail_imgs = wd.find_elements(By.XPATH, "//ytd-grid-video-renderer//a[contains(@id,'thumbnail')]")
    i = 0
    urls = []
    while i < number_videos:
        urls.append(video_thumbnail_imgs[i].get_attribute("href"))
        i = i + 1
    for url in urls:
        YouTube(url).streams.filter(res="480p").first().download(output_path="target_folder")

    filename = search_term + ".csv"
    fw = open(filename, "w")
    headers = "Video Link, Comments, Commenters Name, Number of likes, Number of comments, Title of video, Thumbnail of video \n"
    fw.write(headers)
    reviews = []


    def comment_extract(wd):
        for i in urls:
            open_video = wd.find_elements(By.XPATH,"//div[@id='video-title']")
            open_video.click()
            time.sleep(3)
            #comments=wd.find_elements(By.XPATH,"//ytd-item-section-renderer//a[contains(@id,'contents')]")
            uClient = uReq(i)
            videopage = uClient.read()
            uClient.close()
            videopage_html = bs(videopage, "html.parser")
            comment_boxes = wd.find_elements(By.XPATH,"//ytd-item-section-renderer//a[contains(@id,'contents')]")
            comment_boxes_html = bs(comment_boxes_html, "html.parser")
            for comment in comment_boxes_html:
                try:
                    #name.encode(encoding='utf-8')
                    name = comment.div.div.div.div.div.find_all({'class': 'style-scope yt-formatted-string'})[0].text
                except:
                    name = 'No Name'
            mydict = {"Comment": comment}
            reviews.append(mydict)

            #print(comment_boxes_html)
            #commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})


if __name__ == '__main__':
    DRIVER_PATH = r'chromedriver.exe'
    search_term = '7 Dayz'
    wd = init()
    search_and_download(search_term=search_term, driver_path=DRIVER_PATH, number_videos=2)
    time.sleep(2)
    fetch_video_urls(search_term,2,wd)
    search_channel(search_term, wd)
    open_channel(wd)
    time.sleep(5)
    open_video(wd)
    time.sleep(5)
    download(wd, 2)
    wd.close()



    # def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
    #     def scroll_to_end(wd):
    #         wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #         time.sleep(sleep_between_interactions)
    #
    #         # build the google query
    #
    #     search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    #
    #     # load the page
    #     wd.get(search_url.format(q=query))
    #
    #     image_urls = set()
    #     image_count = 0
    #     results_start = 0
    #     while image_count < max_links_to_fetch:
    #         scroll_to_end(wd)
    #
    #         # get all image thumbnail results
    #         thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
    #         number_results = len(thumbnail_results)
    #
    #         print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
    #
    #         for img in thumbnail_results[results_start:number_results]:
    #             # try to click every thumbnail such that we can get the real image behind it
    #             try:
    #                 img.click()
    #                 time.sleep(sleep_between_interactions)
    #             except Exception:
    #                 continue
    #
    #             # extract image urls
    #             actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
    #             for actual_image in actual_images:
    #                 if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
    #                     image_urls.add(actual_image.get_attribute('src'))
    #
    #             image_count = len(image_urls)
    #
    #             if len(image_urls) >= max_links_to_fetch:
    #                 print(f"Found: {len(image_urls)} image links, done!")
    #                 break
    #         else:
    #             print("Found:", len(image_urls), "image links, looking for more ...")
    #             time.sleep(30)
    #             return
    #             load_more_button = wd.find_element_by_css_selector(".mye4qd")
    #             if load_more_button:
    #                 wd.execute_script("document.querySelector('.mye4qd').click();")
    #
    #         # move the result startpoint further down
    #         results_start = len(thumbnail_results)
    #
    #     return image_urls

