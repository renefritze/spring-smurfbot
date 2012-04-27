import feedparser

class Main(IPlugin):

	def __init__(self,name,tasc):
		IPlugin.__init__(self,name,tasc)

	def cmd_pong(self):
		self.logger.debug( "onpong(rss_smurfbot)" )
		if math.floor(time.time()/60) > rsstime+10:
			f = feedparser.parse('http://balancedannihilation.org/forums/rss')
				s = str(f['entries'][0]['summary']).split('\n')
				self.tasclient.say('teh'+' '+s[0])
			rsstime = math.floor(time.time()/60)