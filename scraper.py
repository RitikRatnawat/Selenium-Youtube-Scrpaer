import time
import pandas as pd
import smtplib
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

YOUTUBE_TRENDING_URL = "https://www.youtube.com/feed/trending"

def get_driver():
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver_options.add_argument("--no-sandbox")
    driver_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome("WebDriver/chromedriver", options=driver_options)
    return driver

def get_videos(driver):
    driver.get(YOUTUBE_TRENDING_URL)
    driver.find_element_by_tag_name('body').send_keys(Keys.END)
    time.sleep(15)
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
    

# def send_email(BODY):
#     try:
#         server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#         server_ssl.ehlo()
        
#         SENDER_ADDRESS = 'you@gmail.com'
#         SENDER_PASSWORD = "yourpassword"
        
#         RECEIVER_ADDRESSES = ['me@gmail.com', 'bill@gmail.com']
#         SUBJECT = 'Youtube Trending Videos'

#         EMAIL_TEXT = f"""
#         From: {SENDER_ADDRESS}
#         To: {", ".join(RECEIVER_ADDRESSES)}
#         Subject: {SUBJECT}

#         {BODY}
#         """
        
#         server_ssl.login(SENDER_ADDRESS, SENDER_PASSWORD)
#         server_ssl.sendmail(SENDER_ADDRESS, RECEIVER_ADDRESSES, EMAIL_TEXT)
#         server_ssl.close()
        
#     except:
#         print ('Something went wrong...')
        

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
    
    # print("Send an Email with the Results")
    # body = json.dumps(videos_data, indent=2)
    # send_email(body)
    
    print("Finished")
    

if __name__ == "__main__":
    run_scraper()