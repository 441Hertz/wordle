import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint
import requests, webbrowser, time, selenium, string

# LIMITATIONS
# Only guesses from possible ANSWERS
# Has not actually been tested to work with all possible cases of answers
# Algorithm to find best guess is shoddy at best - Only looks at the percent composition of each letter in the alphabet 
# to find the best 'weight' of each word in question 
# For example, the sum of the letters percentage composition in alert/alter/later is 39.39, 
# making them the best opening words (out of the unqiue words)
# In reality they are not, and there is little strategy in involved because math is hard
# But that was not the entire goal of this mini project!
# WHAT I LEARNED
# Selenium automation and common HTML jargon
# How to access those **** shadow DOMS
# pprint :)
# More algorithm practice!
# FUTURE
# Code is not very optimized at all, and is very unreadable!
# So good luck if you want to refine this in the future - this is just for me
# I'm retiring this for now
# TODO 
# Readable Code
# Better Algo
# Better Testing
# There are some redundant/testing functions

class Solver():
    def __init__(self):
        self.words = self.load_words()
        print(self.word_weight(self.unique_words()))
    def play_game(self):
        inter = Interacter()
        counter = 0
        # guess = self.opener_word()
        guess = 'crate'
        while inter.running(counter - 1):
            if counter > 0:
                ev = inter.read_ev(counter - 1)
                self.exclude_guess(guess)
                self.exclude_absents(ev, guess)
                self.exclude_presents(ev, guess)
                self.include_corrects(ev, guess)
                guess = self.best_guess()
            inter.submit(guess)
            counter += 1
        time.sleep(10)
        print(f"Answer was '{guess}' - Took {counter - 1} tries")
    def is_dup(self, word):
        for letter in word:
            if word.count(letter) > 1:
                return True
        return False
    def exclude_guess(self, guess):
        self.words.remove(guess)
    def best_guess(self):
        words = self.word_weight(self.words)
        return words[0][0]                        
    def remove(self, ev, guess, word, index):
        guess_occur = guess.count(guess[index])
        word_occur = word.count(guess[index])
        if guess_occur > 1 and guess[index] == word[index]:
            index = self.get_dup_index(guess)
            letters = [guess[i] for i in index]
            ev = [ev[i] for i in index]
            non_absent = ev.count('correct') + ev.count('present')
            absent = ev.count('absent')
            if non_absent > 0:
                if absent > 0:
                    exact = non_absent
                    if word_occur == exact:
                        return False
                elif absent == 0:
                    minimum = non_absent
                    if word_occur >= minimum:
                        return False
        self.words.remove(word)
        return True
        # TODO 
        # DOES NOT REMOVE LETTERS THAT DO NOT HAVE A GREEN LETTER
        # MAYBE WE CAN REWRITE FUNCTIIONS SO THAT WE SKIP OVER DUPLICATED WORDS? 
        # FOR EXAMPLE COLON BECOMES COLN AND WE SKIP OVER THE ITERATION 
    
    def include_corrects(self, ev, guess):
        for index in self.index_ev(ev, 'correct'):
            words = self.words[:]
            for word in words:
                if word[index] not in guess[index]:
                    self.words.remove(word)
                    # self.remove(ev, guess, word, index)
    def exclude_presents(self, ev, guess):
        for index in self.index_ev(ev, 'present'):
            words = self.words[:]
            for word in words:
                if guess[index] in word[index]:
                    self.words.remove(word)
                elif guess[index] not in word:
                    self.words.remove(word)
                    # self.remove(ev, guess, word, index)
    def exclude_absents(self, ev, guess):
        # If letter contains a non absent duplicate - KEEP those that have the exact amount of letters
        # Remove those that have a letter at that position (kinda treat as present)
        # Minimums?
        letters = self.absent_letters(ev, guess)
        for letter in letters:
            words = self.words[:]
            for word in words:
                if self.is_non_absent_dup(ev, guess, letter):
                    exact = self.get_non_absent_dup_count(ev, guess, letter)
                    if word.count(letter) != exact:
                        self.words.remove(word)
                        # self.remove(ev, guess, word, guess.index(letter))
                elif letter in word:
                    self.words.remove(word)
                    # self.remove(ev, guess, word, guess.index(letter))
    def get_letter_dup_index(self, word, letter):
        matching = [i for i in range(5) if word[i] == letter]
        if len(matching) < 2:
            matching = []
        return matching
    def get_non_absent_dup_count(self, ev, guess, letter):
        index = self.get_letter_dup_index(guess, letter)
        counter = 0
        for i in index:
            if ev[i] != 'absent':
                counter += 1
        return counter
    def is_non_absent_dup(self, ev, guess, letter):
        index = self.get_letter_dup_index(guess, letter)
        for i in index:
            if ev[i] != 'absent':
                return True
        return False
    def get_dup_index(self, word):
        return [i for i in range(5) if word.count(word[i]) > 1]
    def absent_letters(self, ev, guess):
        return [guess[i] for i in range(5) if ev[i] == 'absent']
    def index_ev(self, ev, cond):
        index_ev = []
        for i in range(5):
            if ev[i] == cond:
                index_ev.append(i)
        return index_ev

    def opener_word(self):
        return self.word_weight(self.unique_words())[0][0]
    def load_words(self):
        with open('words.txt', 'r') as file:
            lines = file.read()
            words = lines.split('\n')
            return words
    def unique_words(self):
        words = self.load_words()
        unique_words = []
        for word in words:
            if not self.is_dup(word):
                unique_words.append(word)
        return unique_words      
    def empty_freq(self):
        letters = string.ascii_lowercase
        freq = {}
        for letter in letters:
            freq[letter] = [0, 0, 0, 0, 0]
        return freq
    def freq(self):
        words = self.load_words()
        total_words = len(words)
        freq = self.empty_freq()
        for i in range(5):
            for word in words:
                letter = word[i]
                freq[letter][i] += 1
            for key, value in freq.items():
                percentage = (value[i]/total_words)*100
                percentage = round(percentage, 2)
                freq[key][i] = percentage
        return freq
    def avg_freq(self):
        freq = self.freq()
        for key, value in freq.items():
            avg = sum(value)/5
            freq[key] = round(avg, 2)
        return freq
    def word_weight(self, words):
        freq = self.avg_freq()
        word_dict = {}
        for word in words:
            weighing = 0
            for letter in word:
                weighing += freq[letter]
            word_dict[word] = round(weighing, 2)
        return self.sort_dict(word_dict)
    def sort_dict(self, dt):
        return sorted(dt.items(), key = lambda x: x[1], reverse = True)
        
class Interacter():
    def __init__(self):
        PATH = 'C:\chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path = PATH)
        self.open_wordle()
        self.close_popup()
        time.sleep(1)
    def open_wordle(self):
        url = 'https://www.nytimes.com/games/wordle/index.html'
        self.driver.get(url)
    def expand_shadow_element(self, element):
        shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
        return shadow_root
    def close_popup(self):
        html = self.driver.find_element(By.TAG_NAME, 'html')
        html.click()
    def submit(self, word):
        html = self.driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(word)
        html.send_keys(Keys.ENTER)
    def get_shadow_game_app(self):
        game_app = self.driver.find_element(By.CSS_SELECTOR, 'body > game-app')
        shadow_game_app = self.expand_shadow_element(game_app)
        return shadow_game_app
    def get_board(self):
        board = self.get_shadow_game_app().find_element(By.ID, 'board')
        return board
    def get_row(self, n):
        rows = self.get_board().find_elements(By.TAG_NAME, 'game-row')
        game_row = rows[n]
        shadow_game_row = self.expand_shadow_element(game_row)
        row = shadow_game_row.find_element(By.CLASS_NAME, 'row')
        return row
    def read_ev(self, n):
        time.sleep(1)
        row = self.get_row(n)
        letters = row.find_elements(By.TAG_NAME, 'game-tile')
        ev = [letter.get_attribute('evaluation') for letter in letters]
        return ev
    def running(self, counter):
        # game_modal = self.get_shadow_game_app().find_element(By.CSS_SELECTOR, '#game > game-modal')
        # return not game_modal.is_displayed()
        for value in self.read_ev(counter):
            if value != 'correct':
                return counter != 5
        return False
        
# inter = Interacter()
# inter.read_ev(0)
solver = Solver()
solver.play_game()