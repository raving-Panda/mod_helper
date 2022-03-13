from discordHelper import DiscordHelper
import settings as env
d = None
try:
	d = DiscordHelper()
except Exception as e:
	env.log("E",f"Caught error : {e}")
	with open('error.xsb','w') as f:
		f.write("error")