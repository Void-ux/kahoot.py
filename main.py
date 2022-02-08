from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pathlib import Path

import json
import time

from random import choice

path = Path(__file__).resolve().parent / 'config.json'
with open(path, 'r') as config_file:
	config_dict = json.load(config_file)
assert 0 < config_dict['number_of_bots'] < 1000

path = Path(__file__).resolve().parent / 'usernames.txt'
with open(path, 'r') as username_file:
	username_list = username_file.read().split('\n')
	username_file.close()

chrome_options = Options()
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-error')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument("log-level=3")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

s = Path(__file__).resolve().parent / 'chromedriver.exe'
driver = webdriver.Chrome(executable_path=str(s), options=chrome_options)

print("Length of bots: {}".format(len(range(config_dict['number_of_bots']))))
for i in range(config_dict['number_of_bots']):
	driver.get(config_dict['url'])
	try:
		nck_inp_element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.ID, 'nickname'))
		)
	except:
		driver.quit()

	username = choice(username_list)
	nck_inp_element.send_keys(username + Keys.ENTER)
	time.sleep(0.1)

	# No need to create a new tab if amt is just one
	print("i: {}".format(i))
	print("I less than length: {}".format(i < len(range(config_dict['number_of_bots']))))
	if i < (len(range(config_dict['number_of_bots'])) - 1):
		driver.execute_script('''window.open("https://www.google.com", "_blank");''')
		driver.switch_to.window(driver.window_handles[i + 1])
