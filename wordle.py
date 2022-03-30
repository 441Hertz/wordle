from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests, webbrowser, time, selenium

class Solver():
    def __init__(self):
        pass

class Interacter():
    def __init__(self):
        PATH = 'C:\chromedriver.exe'
        self.browser = webdriver.Chrome(executable_path = PATH)

        self.open_browser()
        self.close_popup()
    def expand_shadow_element(self, element):
        shadow_root = self.browser.execute_script('return arguments[0].shadowRoot', element)
        return shadow_root

    def open_browser(self):
        url = 'https://www.nytimes.com/games/wordle/index.html'
        self.browser.get(url)
 
    def close_popup(self):
        time.sleep(3)
        root1 = self.browser.find_element_by_css_selector('body > game-app')
        shadow_root1 = self.expand_shadow_element(root1)
        root2 = shadow_root1.find_element_by_css_selector('game-theme-manager')
        shadow_root2 = self.expand_shadow_element(root2)
        root3 = shadow_root2.find_element_by_css_selector('#game > game-modal')
        shadow_root3 = self.expand_shadow_element(root3)
        root4 = shadow_root3.find_element_by_css_selector('div > div > div > game-icon')
        shadow_root4 = self.expand_shadow_element(root4)
        x_button = shadow_root4.find_element_by_css_selector('svg')
        time.sleep(3)

solver = Interacter()