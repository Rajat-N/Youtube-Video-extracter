import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from pytube import YouTube

def init():
    return webdriver.Chrome(executable_path="chromedriver.exe")

def search_channel(channel_name,wd):
    base_url = "https://www.youtube.com/results?search_query="
    search_url = base_url + channel_name
    wd.get(search_url)

def open_channel(wd):
    channel_link = wd.find_element(By.XPATH, "//div[@id='content-section']//following-sibling::yt-formatted-string[1]")
    channel_link.click()

def open_video(wd):
    video_tab = wd.find_elements(By.CLASS_NAME,"tab-content")[1]
    video_tab.click()

def download(wd, limit):
    video_thumbnail_imgs = wd.find_elements(By.XPATH,"//ytd-grid-video-renderer//a[contains(@id,'thumbnail')]")
    i = 0
    urls=[]
    while i < limit:
        urls.append(video_thumbnail_imgs[i].get_attribute("href"))
        i=i+1
    for url in urls:
        YouTube(url).streams.filter(res="480p").first().download(output_path=r"C:\Users\rajat\PycharmProjects\YTExtract\Extracted_Videos")

if __name__ == '__main__':
    wd = init()
    search_channel("darkvibes", wd)
    open_channel(wd)
    time.sleep(5)
    open_video(wd)
    time.sleep(5)
    download(wd, 1)
    wd.close()

##def extract():
    # wd = init()
    # search_channel("krish naik", wd)
    # open_channel(wd)
    # time.sleep(5)
    # open_video(wd)
    # time.sleep(5)
    # download(wd, 1)
    # wd.close()


# if __name__ == '__main__':
#     extract()
#










