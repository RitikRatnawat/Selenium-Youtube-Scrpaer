from matplotlib.pyplot import title
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

YOUTUBE_TRENDING_URL = "https://www.youtube.com/feed/trending"

def get_driver():
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver = webdriver.Chrome("WebDriver/chromedriver", options=driver_options)
    return driver

def get_videos(driver):
    driver.get(YOUTUBE_TRENDING_URL)
    videos = driver.find_elements_by_tag_name("ytd-video-renderer")
    return videos


def run_scraper():
    print("Creating the Driver")
    driver = get_driver()
    
    print("Fetching Trending Videos")
    videos = get_videos(driver)
    print(f"Found {len(videos)} Videos")
    
    print("Parsing the First video")
    # Title, Thumbnail URL, Channel, Views, Uploaded, Link, Description
    video = videos[0]
    title = video.find_element_by_id("video-title").text
    url = video.find_element_by_id("video-title").get_attribute('href')
    thumbnail_url = video.find_element_by_tag_name("img").get_attribute('src')
    print("Title : " + title)
    print("URL : " + url)
    print("Thumbnail URL : " + thumbnail_url)



if __name__ == "__main__":
    run_scraper()