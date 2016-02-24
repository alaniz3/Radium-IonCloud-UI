from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import logging, time, pickle, urllib2, json
from socket import error as socket_error

from django.conf import settings

# Debug settings
debug = False
if debug:
    logging.basicConfig()
    logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)

class Stats():
	def __init__(self, rpc_user, rpc_pass, rpc_port):
		try:
			self.rpc = AuthServiceProxy(("http://%s:%s@127.0.0.1:%s/") % (rpc_user, rpc_pass, rpc_port))
			self.sync()
		except socket_error as e:
			self.stats = {'price': None, 'connections': None, 'connected': False, 'height': None}

	def getPrice(self):
		req = urllib2.Request('https://poloniex.com/public?command=returnTicker', headers={'User-Agent':'Magic Browser'})
		con = urllib2.urlopen(req)
		jsonreq = json.loads(con.read())
		return jsonreq['BTC_RADS']['last']

	def sync(self):
		getinfo = self.rpc.getinfo()
		try: 
			conns = getinfo['connections']
			height = "{:,}".format(getinfo['blocks'])
			conn_status = True
		except KeyError as e:
			conns = 0
			height = 'Unknown'
			conn_status = False
		self.stats = {'price': self.getPrice(), 'connections': conns, 'connected': conn_status, 'height': height}
