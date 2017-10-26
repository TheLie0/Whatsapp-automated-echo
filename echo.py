# coding=utf-8

import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import os
from googletrans import Translator

def getfile_local(name1): # just a functions that finds the path to files in the same directory as this one.
	name = os.path.basename(__file__)
	path = os.path.abspath(__file__)
	print path
	for i in range(len(name)):
		path = path[:len(path)-1]
		print path
	for i in range(len(name1)):
		path = path + name1[i]
		print path
	return path

def backw(strng):
	return strng[::-1]

def translate(text):
	"""returns an english translation of your input. 
	Translation provided by Google Translate"""
	translator = Translator()
	return translator.translate(text).text

def sqr(strng):
	"""MAKES THIS
	AKES THISM
	KES THISMA
	ES THISMAK
	S THISMAKE
	 THISMAKES"""
	out = ""
	for i in range(len(strng)):
		out += strng[i:] + strng[:i] + "\n"
	return out

def noFucks(text):
	if text == text[:]:
		return "ok."

def playInterested(text):
	"""Pretends to be interested in the message in german"""
	newText = text.replace(".","").replace(",","").replace("!","").replace("?","").replace(";","").replace(":","").replace("(","").replace(")","")
	while newText[-1] == " ":
		newText = newText[:-1]
	return "Jaja, " + newText.split(" ")[-1] + ", interessant."

def isThere(name):
	"""checks if the given name is in the chat tile"""
	try:
		title = driver.find_element_by_class_name("pane-chat-header")
		if name in title.text:
			return True
		else:
			return False
	except:
		return False

def boot_driver():
	"""initializes the selenium webdriver"""
	os.environ['MOZ_HEADLESS'] = '1'
	path_to_firefox = getfile_local("geckodriver.exe")
	path_to_profile = getfile_local("profile")
	profile = webdriver.FirefoxProfile(path_to_profile)
	driver = webdriver.Firefox(executable_path=path_to_firefox, firefox_profile = profile)
	return driver

def boot_whatsapp_interface():
	"""opens web.whatsapp.com"""
	driver = boot_driver()
	driver.get("https://web.whatsapp.com/")
	WebDriverWait(driver, 60)
	return driver

def process_messages(driver, botVar, spareList, lastText):
	"""handles detection of incoming messages and answering them according to the botVar function"""

	try:
		unread = driver.find_element_by_class_name("unread")
		unread.click()

	except:
		isSpared = False
		for name in spareList:
			if isThere(name):
				isSpared = True

		if not isSpared:

			try:
				in_messages = driver.find_elements_by_class_name("message-in")
				last_message = in_messages[-1].find_element_by_class_name("selectable-text")

				if last_message.text == "":
					last_message = in_messages[-1].find_element_by_class_name("large-emoji-container")

				text = last_message.text#.encode('utf-8')

				if text != lastText:  # this is the echo.
					input_box = driver.find_element_by_class_name("pluggable-input-body")
					input_box.click()
					input_box.send_keys((
											botVar(text)
										) + Keys.ENTER)  # this actually types the echo.
					lastText = text
					return lastText

				else:
					return lastText
			except:
				pass

		return lastText

def manage_whatsapp(maxWaitTime, botVar, spareList):
	""" will manage all your whatsapp messages forever"""
	driver = boot_whatsapp_interface()
	waitTime = 1
	lastText = ""
	secondToLastText = ""

	while True:
		print waitTime
		time.sleep(waitTime)
		lastText = process_messages(driver, botVar, spareList, lastText)

		if not secondToLastText == lastText:
			waitTime = 1
		elif not waitTime > maxWaitTime:
			waitTime += waitTime

		secondToLastText = lastText

if __name__ == '__main__':
	spareList = ["Geburtstagsfeier 30.10.", "MSS 13", "KMV Ober-Flörsheim"]
	manage_whatsapp(15, backw, spareList)
