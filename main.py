from selenium import webdriver
import urllib.request
from time import sleep


class myBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        # user profile
        self.driver.get("https://instagram.com/username")
        sleep(15)

        # scroll function
        lengthOfPage = self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight); var lengthOfPage = document.body.scrollHeight; return lengthOfPage;"
        )
        match = False
        while match == False:
            lastCount = lengthOfPage
            sleep(5)
            lengthOfPage = self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight); var lengthOfPage = document.body.scrollHeight; return lengthOfPage;"
            )
            # scroll to the bottom
            if lastCount == lengthOfPage:
                match = True

        posts = []
        links = self.driver.find_elements_by_tag_name("a")
        # scrapping posts
        for link in links:
            post = link.get_attribute("href")
            if "/p/" in post:
                posts.append(post)

        print(posts)

        download_url = ""
        # download posts
        for post in posts:
            self.driver.get(post)
            shortcode = self.driver.current_url.split("/")[-2]
            type = self.driver.find_element_by_xpath(
                '//meta[@property="og:type"]'
            ).get_attribute("content")
            if type == "video":
                download_url = self.driver.find_element_by_xpath(
                    '//meta[@property="og:video"]'
                ).get_attribute("content")
                urllib.request.urlretrieve(download_url, "{}.mp4".format(shortcode))
            else:
                download_url = self.driver.find_element_by_xpath(
                    '//meta[@property="og:image"]'
                ).get_attribute("content")
                urllib.request.urlretrieve(download_url, "{}.jpg".format(shortcode))

            print(download_url)


myapp = myBot()
