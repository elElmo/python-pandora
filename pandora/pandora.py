import urllib2

from connection import PandoraConnection

class Pandora(object):
	backlog = []
	
	def __init__(self, connection):
		self.connection = connection
	
	def authenticate(self, username, password):
		return self.connection.get_user_authentication(username, password)
		
	def get_station_list(self, user):
		return self.connection.get_stations(user)
	
	def switch_station(self, user, station_id):
		self.backlog = []
		self.backlog = self.connection.get_fragment(user, station_id) + self.backlog
	
	def get_next_song(self, user, stationId):
		# get more songs
	#	if len(self.backlog) < 2:
	#		self.backlog = self.connection.get_fragment(user, stationId) + self.backlog
		
		# get next song
	#	return self.backlog.pop()
		return self.connection.get_fragment(user, stationId)
		
		
if __name__ == "__main__":
	connection = PandoraConnection()
	pandora = Pandora(connection)
	
	# read username
	print "Username: "
	username = raw_input()
	
	# read password
	print "Password: "
	password = raw_input()
	
	# read proxy config
	print "Proxy: "
	proxy = raw_input()
	if proxy:
		proxy_support = urllib2.ProxyHandler({"http" : proxy})
		opener = urllib2.build_opener(proxy_support)
		urllib2.install_opener(opener)
	
	# authenticate
	user = pandora.authenticate(username, password)
	print "Authenticated: " + str(user)
	
	# output stations (without QuickMix)
	print "users stations:"
	for station in pandora.get_station_list(user):
		if station['isQuickMix']: 
			quickmix = station
			print "\t" + station['stationName'] + "*"
		else:
			print "\t" + station['stationName']
	
	print "\n\n\n"
	quickmix = quickmix['stationId'] if type(quickmix) is dict else quickmix
	# switch to quickmix station
	pandora.switch_station(user, quickmix)
	
	# get one song from quickmix
	print "next song from quickmix:"
	n =  pandora.get_next_song(user, quickmix)[0]
	print n['artistName'] + ': ' + n['songName']
	print n['additionalAudioUrl']
	print n['audioUrlMap']['highQuality']['audioUrl']
	print n.keys()
	
	# download it
	#u = urllib2.urlopen(next['audioUrlMap']['highQuality']['audioUrl'])
	#f = open('test.mp3', 'wb')
	#f.write(u.read())
	#f.close()
	#u.close()
