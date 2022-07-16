import pandas as pd
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

def get_videos_data(video):
    
    title = video.find_element_by_id("video-title").text
    video_url = video.find_element_by_id("video-title").get_attribute('href')
    thumbnail_url = video.find_element_by_tag_name("img").get_attribute('src')
    channel_name = video.find_element_by_class_name("ytd-channel-name").text
    views = video.find_element_by_id("metadata-line").text.split("\n")[0]
    posted_on = video.find_element_by_id("metadata-line").text.split("\n")[1]
    description = video.find_element_by_id("description-text").text
    
    return {
        "Title" : title,
        "Channel Name" : channel_name,
        "Description" : description,
        "Views" : views,
        "Posted On" : posted_on,
        "Video URL" : video_url,
        "Thumbnail URL" : thumbnail_url
    }
        

def run_scraper():
    print("Creating the Driver")
    driver = get_driver()
    
    print("Fetching Trending Videos")
    videos = get_videos(driver)
    print(f"Found {len(videos)} Videos")
    
    print("Parsing Top 10 Videos")
    # Title, Thumbnail URL, Channel, Views, Uploaded, Link, Description
    videos_data = [get_videos_data(video) for video in videos[:10]]
    df = pd.DataFrame(videos_data)
    
    print("Saving the Data to a CSV File")
    df.to_csv("trending.csv", index=None)
    
    



if __name__ == "__main__":
    run_scraper()