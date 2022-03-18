from driver_helper import SeleniumHelper
import time
import settings as env

class DiscordHelper:
	def __init__(self):
		self.sd = SeleniumHelper()
		self.sd.url("https://www.discord.com/login")
		time.sleep(1)
		self.login()
		#self.inject_js()
		self.channelC = self.sd.count_class('blobContainer-ikKyFs')
		self.cycle_channels()
		#self.done()
	def login(self):
		''' login '''
		self.sd.set_text('sankalpbas@gmail.com','name','email')
		self.sd.set_text('Xsbsankalp@741','name','password')
		self.sd.click('tag','button',1)
		time.sleep(5)
		self.sd.wait_until_presence('class','container-YkUktl')
		#self.sd.capcha_click()

	def inject_js(self):
		self.sd.wait_until_presence('class','slateTextArea-27tjG0')
		time.sleep(4)
		self.sd.execute_js(env.js)
		try:
			self.sd.click('id','dht-cfg-afm-switch')
			self.sd.click('id','dht-cfg-asm-switch')
			self.sd.click_out('id','dht-cfg-overlay')
		except:
			pass
		

	def cycle_channels2(self):
		for j in range(3):
			for i in range(0,self.channelC):
				self.sd.click('class','blobContainer-ikKyFs',i)
				time.sleep(5)
				self.top_channel(i)
				#self.sd.click('id','dht-ctrl-track')


	def cycle_channels(self):
		try:
			while True:
				for i in env.top_channels:
					self.sd.url("https://discord.com/channels/"+i)
					self.inject_js()
					time.sleep(3)
					self.sd.click('id','dht-ctrl-track')
					time.sleep(1)
					self.sd.wait_for_stop_track()
		except Exception as e:
			env.log("E",f"Error While looping {e}")
			self.sd.url("https://www.discord.com/login")
			time.sleep(1)
			self.login()
			self.cycle_channels()



	def top_channel(self,chno):
		channelsC = self.sd.count_class('icon-2W8DHg')#('channelName-3KPsGw')
		env.log("T",f"Total {channelsC} channels in channel no {chno+1}")
		self.sd.click('class','icon-2W8DHg',0)#('class','channelName-3KPsGw',0)

	def done(self):
		#sd.execute_js(env.js)
		self.sd.close()
