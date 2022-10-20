import os
import time
import requests
from selenium import webdriver


def search_and_download(search_term: str, driver_path: str, target_path='./Extracted_Videos', number_images=10):
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome(executable_path=driver_path) as wd:
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)

    counter = 0
    for elem in res:
        persist_image(target_folder, elem, counter)
        counter += 1

def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

        # build the google query

    search_url = "https://www.youtube.com/results?search_query={q}"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        channel_link = wd.find_element(By.XPATH,"//div[@id='content-section']//following-sibling::yt-formatted-string[1]")
        channel_link.click()
        time.sleep(sleep_between_interactions)

        video_tab = wd.find_elements(By.CLASS_NAME, "tab-content")[1]
        video_tab.click()
        time.sleep(sleep_between_interactions)

    def download(wd,limit: max_links_to_fetch):
        video_thumbnail_imgs = wd.find_elements(By.XPATH, "//ytd-grid-video-renderer//a[contains(@id,'thumbnail')]")
        i = 0
        urls = []
        while i < limit:
            urls.append(video_thumbnail_imgs[i].get_attribute("href"))
            i = i + 1
        for url in urls:
            YouTube(url).streams.filter(res="480p").first().download(output_path="D:\YT")

        # thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        # number_results = len(thumbnail_results)

        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(30)
            return
            load_more_button = wd.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls


