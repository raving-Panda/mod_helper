import datetime
import time
# from lib import settings as env
import settings as env
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.chrome.options import Options
#import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException,NoSuchElementException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

class SeleniumHelper:
	def __init__(self):
		env.log(" ","Initializing driver")
		options =  Options()
		# env.log(" ","\t\t User Agent - firefox")
		# options.add_argument('--user-agent=%s' % "firefox") 
		env.log(" ","Options : ")
		if env.HEADLESS:
			options.add_argument("--headless")
			env.log(" ","\t\tHeadless - True")
		else:
			env.log(" ","\tHeadless - False")
		#options.profile= webdriver.FirefoxProfile('/home/webuser/.mozilla/firefox/00996xgf.default-release')

		self.driver = webdriver.Firefox(options=options)

		self.driver.implicitly_wait(3)
		# self.driver = uc.Chrome()
		# options = webdriver.ChromeOptions()
		# options.add_experimental_option("excludeSwitches", ["enable-automation"])
		# options.add_experimental_option('useAutomationExtension', False)
		# options.add_argument("--disable-blink-features=AutomationControlled")
		# self.driver = webdriver.Chrome("./chromedriver",options=options)
		env.log(" ","Driver Ready")

	def url(self,uri):
		env.log(" ","GOTO : "+uri)
		self.driver.get(uri)

	def get_url(self):
		return self.driver.current_url

	def element(self,by,slug,x=-1):
		if(by=="id"):
			if x==-1:
				self.elem = self.driver.find_element_by_id(slug)
			else:
				self.elem = self.driver.find_elements_by_id(slug)[x]
		elif(by=="name"):
			if x==-1:
				self.elem = self.driver.find_element_by_name(slug)
			else:
				self.elem = self.driver.find_elements_by_name(slug)[x]
		elif(by=="class"):
			if x==-1:
				self.elem = self.driver.find_element_by_class_name(slug)
			else:
				self.elem = self.driver.find_elements_by_class_name(slug)[x]
		elif(by==""):
			if x==-1:
				self.elem = self.driver.find_element_by_css_selector(slug)
			else:
				self.elem = self.driver.find_elements_by_css_selector(slug)[x]
		elif(by=="tag"):
			if x==-1:
				self.elem = self.driver.find_element_by_tag_name(slug)
			else:
				self.elem = self.driver.find_elements_by_tag_name(slug)[x]
		else:
			self.elem = None

		env.log(" ","Element : "+by+"::"+slug+"::"+" ["+str(x)+"]")

	def by(self,by):
		if(by=="id"):
			return By.ID
		elif(by=="name"):
			return By.NAME
		elif(by=="class"):
			return By.CLASS_NAME
		elif(by=="tag"):
			return By.TAG_NAME
		#elif(by==""):
		#	self.elem = self.driver.find_elements_by_css_selector(slug)
		else:
			self.elem = None

	def set_text(self,text,by,slug,x=-1):
		env.log(" ","Typing :"+text+": into "+by+"::"+slug+"::"+str(x))
		self.element(by,slug,x)
		self.elem.send_keys(text)

	def enter(self):
		self.elem.send_keys(Keys.RETURN)

	def wait_until_presence(self,by,slug):
		env.log(" ","Waiting for "+by+"::"+slug)
		try:
			waiting = WebDriverWait(driver=self.driver,timeout= 10,poll_frequency=0.5,ignored_exceptions=[TimeoutException]).until(
				EC.presence_of_element_located((self.by(by), slug)))
		except NoSuchElementException as e:
			env.log("E",f"Rate Limited out of runebet.com")

	def wait_until_clickable(self,by,slug):
		try:
			waiting = WebDriverWait(driver=self.driver,timeout= 10,poll_frequency=0.5,ignored_exceptions=[TimeoutException]).until(
				EC.element_to_be_clickable((self.by(by), slug)))
		except Exception as e:
			env.log("E",f"Exception while waiting for clickable: "+by+"::"+slug+""+str(e))

	def select(self,by,slug,item):
		try:
			self.element(by,slug)
		except Exception as e:
			env.log("E",f"Element not found "+" BY:"+by+" SLUG :"+slug)

		select = Select(self.elem)

		try:
			select.select_by_value(item)
		except Exception as e:
			env.log("E",f"Select Item not found "+" BY:"+by+" SLUG :"+slug+" ITEM:"+item)
		
		selected_text=select.first_selected_option.text
		if selected_text == "Select...":
			env.log("I",f"Select Item Disabled "+" BY:"+by+" SLUG :"+slug+" ITEM:"+item)
			return False
		else:
			# env.log("I",f"Select Item  "+" BY:"+by+" SLUG :"+slug+" ITEM:"+item)
			return True

	def click(self,by,slug,x=-1):
		
		env.log(" ",f"Click "+by+"::"+slug+" ["+str(x)+"]")
		self.element(by,slug,x)
		self.elem.click()


	def click_out(self,by,slug,x=-1):
		action = webdriver.common.action_chains.ActionChains(self.driver)
		self.element(by,slug,x)
		action.move_to_element_with_offset(self.elem, 50, 50)
		action.click()
		action.perform()
	def capcha_click(self):
		
		env.log(" ",f"Capcha Click ")
		element_to_hover_over = self.driver.find_elements_by_tag_name("div")
		env.log("t",element_to_hover_over)

		#hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
		#hover.perform()
		#element_to_hover_over.click()

	def get_inner(self,elm):
		# env.log(" ",f"Click "+by+"::"+slug+" ["+str(x)+"]")
		return elm.get_attribute("innerHTML").strip()

	def execute_js(self,js):
		self.driver.execute_script(js)


	def count_class(self,classname):
		try:
			elems = self.driver.find_elements_by_class_name(classname)
			env.log("o",f"{len(elems)}")
			return len(elems)
		except Exception as e:
			env.log("E",f"Could not find class or {e}")
			env.outdate()

	def wait_for_stop_track2(self):
		try:
			waiter = WebDriverWait(driver=self.driver, timeout=20, poll_frequency=1)
			waiter.until(lambda drv: drv.find_element_by_class_name("dht-ctrl-track").text == "Start Tracking")
		except Exception as e:
			env.log('Wait',f'Error : {e}')


	def wait_for_stop_track(self):
		try:
			count = 0
			while True:
				time.sleep(1)
				count+=1
				classname = self.driver.find_element_by_id("dht-ctrl-settings")
				if classname.is_enabled() or count>69:
					break
		except Exception as e:
			env.log('Wait',f'Error : {e}')



	def close(self):
		self.driver.close()

	def __del__(self):
		pass#self.driver.close()
