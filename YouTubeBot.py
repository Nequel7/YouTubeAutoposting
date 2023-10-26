import pywinauto
from selenium import webdriver
import undetected_chromedriver as uc
import time
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import pickle
import dotenv
from video_title import HASHTAGS_YT
from supports import random_proxy

dotenv.load_dotenv()
video = 'ешкере 2.mp4'


class BotYT:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('--proxy-server=%s' % random_proxy())
        self.browser = uc.Chrome(use_subprocess=False, driver_executable_path=os.getenv('DRIVER_PATH'),
                                 options=self.options)

    # close driver
    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def auth(self, account):
        browser = self.browser
        browser.get('https://www.youtube.com/')
        browser.maximize_window()
        time.sleep(3)
        # 1839 30
        # three_dots = browser.find_element(By.ID, 'buttons')
        # print('1111')
        # action = ActionChains(browser)
        # action.move_to_element(three_dots).move_by_offset(xoffset=2, yoffset=0).click().perform()
        # time.sleep(10000)
        notif_icon = WebDriverWait(browser, 120).until(
            EC.element_to_be_clickable((By.ID, "icon")))

        # insert cookie
        pickle.dump(
            browser.get_cookies(),
            open(f'{os.getenv("COOKIES_PATH")}{account}_cookies', 'wb')
        )
        print('Cookies saved successfully !')

    def load_video(self, account, i):
        filters = len(os.listdir('video'))
        videos_list = os.listdir('video')
        browser = self.browser
        browser.get('https://www.youtube.com/')
        browser.maximize_window()
        time.sleep(3)
        for cookie in pickle.load(
                open(f'{os.getenv("COOKIES_PATH")}{account}', 'rb')):
            browser.add_cookie(cookie)

        time.sleep(2)
        browser.refresh()
        time.sleep(2)
        # press create (circle btn)
        btns = browser.find_element(By.ID, 'buttons')
        action = ActionChains(browser)
        action.move_to_element(btns).move_by_offset(xoffset=-68,
                                                    yoffset=0).click().move_by_offset(xoffset=5,
                                                                                      yoffset=50).click().perform()
        time.sleep(3)
        # select video
        browser.find_element(By.ID, 'select-files-button').click()
        time.sleep(3)

        app = pywinauto.application.Application()
        app.connect(title='Открытие')
        app.Dialog.Edit0.type_keys(
            f"{os.getenv('VIDEO_PATH')}{videos_list[i % filters]}",
            with_spaces=True)
        app.Dialog.Edit0.type_keys('{ENTER}')
        time.sleep(3)
        # set hashtags

        # imprt = browser.find_element(By.ID, 'reuse-details-button')
        # for hashtag in HASHTAGS_YT:
        #     action = ActionChains(browser)
        #     action.move_to_element(imprt).move_by_offset(xoffset=85, yoffset=85).click().send_keys(
        #         f'#{hashtag}').perform()
        #     time.sleep(2)
        #     action.send_keys(Keys.ENTER).perform()

        no_kids = browser.find_element(By.CSS_SELECTOR,
                                       "tp-yt-paper-radio-button[name='VIDEO_MADE_FOR_KIDS_NOT_MFK']")
        # not for kids
        action = ActionChains(browser)
        action.move_to_element(no_kids).click().perform()
        time.sleep(1)
        # 3 times next
        for i in range(3):
            browser.find_element(By.ID, 'next-button').click()
            time.sleep(0.25)

        # public access
        browser.find_element(By.ID, 'first-container').find_element(By.CSS_SELECTOR,
                                                                    "tp-yt-paper-radio-button[name='PUBLIC']").click()
        browser.find_element(By.ID, 'done-button').click()
        time.sleep(3)
        print(f"✅ Video uploaded successfully in account ({account.split('_')[0]})")
        # wait loading video

        # WebDriverWait(browser, 20).until(
        #     EC.element_to_be_clickable(
        #         (By.ID, "close-icon-button")))
        # print(f"✅ Video uploaded successfully in account ({mail.split('_')[0]})")


if __name__ == "__main__":
    bot = BotYT()
    bot.load_video(account='utkin4393@gmail.com_cookies', i=1)
    bot.close_browser()
