import datetime

class Cookie:
	def __init__(self):
		self._data = ''
		self._ip = ''
		self._hostname = ''
		self._request = ''
		self._headers = {}

	def getRequest(self):
		return self._request
	def setRequest(self, aRequest):
		self._request = aRequest
	def getData(self):
		return self._data
	def setData(self, aData):
		self._data = aData
	def getIP(self):
		return self._ip
	def setIP(self, anIP):
		self._ip = anIP
	def getHostname(self):
		return self._hostname
	def setHostname(self, aHostname):
		self._hostname = aHostname


class ProbeRequest:
	def __init__(self):
		self._src = ''
		self._dst = ''
		self._bssid = ''
		self._pkt = None
		self._ssid = 'NotSet'
		self._channel = 0
		self._firstSeen = None
		self._lastSeen = None

	def setSRC(self, asrc):
		self._src = asrc
	def setDST(self, adst):
		self._dst = adst
	def setBSSID(self, abssid):
		self._bssid = abssid
	def setPKT(self, apkt):
		self._pkt = apkt
	def setFirstSeen(self, thedatetime):
		self._firstSeen = thedatetime
	def setLastSeen(self, lastdatetime):
		self._lastSeen = lastdatetime
	def setSSID(self, aSSID):
		self._ssid = aSSID
	def setChannel(self, achannel):
		self._channel = achannel
	def getSRC(self):
		return self._src
	def getDST(self):
		return self._dst
	def getBSSID(self):
		return self._bssid
	def getPKT(self):
		return self._pkt
	def getFirstSeen(self):
		return self._firstSeen
	def getLastSeen(self):
		return self._lastSeen
	def getSSID(self):
		return self._ssid
	def getChannel(self):
		return self._channel

class WifiClient:
	def __init__(self):
		self._mac = ''
		self._channel = 0
		self._foundWhen = ''
		self._lastSeen = ''

	def getMAC(self):
		return self._mac
	def getChannel(self):
		return self._channel
	def setMAC(self, aMAC):
		self._mac = aMAC
	def setChannel(self, aChannel):
		self._channel = aChannel

class AccessPoint:
	def __init__(self):
		self._bssid = ''
		self._ssid = ''
		self._channel = 0 
		self._Encrypted = 0
		self._foundWhen = ''
		self._isProtected = 0
		# TODO
		self._lastSeen = ''
		self._ClientsList = []
		

	def addClient(self, aWifiClient):
		self._ClientsList.append( aWifiClient )
		return

	def getClientbyMAC(self, aMAC):
		for client in self._ClientsList:
			if client.getMAC() == aMAC:
				return client
		return None

	def isProtected(self):
		return self._isProtected

	def getBSSID(self):
		return self._bssid

	def getSSID(self):
		return self._ssid

	def getChannel(self):
		return self._channel

	def getFoundWhen(self):
		return self._foundWhen

	def getFoundWhenString(self):
		return str(self._foundWhen)

	def setProtected(self, isprotected=1):
		self._isProtected = isprotected 

	def setBSSID(self, abssid):
		self._bssid = abssid

	def setSSID(self, assid):
		self._ssid = assid

	def setChannel(self, achannel):
		self._channel = achannel


	def setFoundWhen(self, aDateTime):
		self._foundWhen = aDateTime

