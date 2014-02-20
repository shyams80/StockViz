import unirest
import datetime
import urllib

mashape_auth = "YOUR_MASHAPE_API_KEY"
unirest.timeout(10)

# function to place a trade in your StockViz account
def getLivePrice(symbol):
	#get the latest price
	pResponse = unirest.get("https://stockviz.p.mashape.com/marketdata/livePriceEquity", 
		params={
			"symbol": symbol
		},
		headers={
			"X-Mashape-Authorization": mashape_auth,
			"Accept": "application/json"
		}
	);
	
	if pResponse.code == 200:
		price = pResponse.body[0]["LAST_PRICE"]
		return price
	
#function to get EPS
def getEps(symbol):
	# print "eps for", symbol
	response = unirest.get("https://stockviz.p.mashape.com/fundamental/quarterlyEps", 
		params={
			"symbol": symbol
		},
		headers={
			"X-Mashape-Authorization": mashape_auth,
			"Accept": "application/json"
		}
	);

	if response.code == 200:
		# print len(response.body)
		return response.body	
	else:
		# print "call failed"
		# print response.code, response.headers
		return []
		
#function to get technicals
def getTechnicals(symbol, start=datetime.date.today()-datetime.timedelta(days=10)):
	# print "Techs for", symbol
	response = unirest.get("https://stockviz.p.mashape.com/technicaldata/technicalsEquity", 
		params={
			"symbol": symbol
		},
		headers={
			"X-Mashape-Authorization": mashape_auth,
			"Accept": "application/json"
		}
	);

	if response.code == 200:
		# print len(response.body)
		return response.body	
	else:
		# print "call failed"
		# print response.code, response.headers
		return []

# function to get index constituents
def getConstituents(indexName):
	iResponse = unirest.get("https://stockviz.p.mashape.com/marketdata/indexlist", 
		headers={
			"X-Mashape-Authorization": mashape_auth,
			"Accept": "application/json"
		}
	);
	
	if iResponse.code == 200:
		i = (item for item in iResponse.body if item["INDEX_NAME"] == indexName).next()
		indexId = i["INDEX_ID"]
		cResponse = unirest.get("https://stockviz.p.mashape.com/marketdata/symbolsOfIndex", 
			params={
				"id": indexId
			},
			headers={
				"X-Mashape-Authorization": mashape_auth,
				"Accept": "application/json"
			}
		);
		
		if cResponse.code == 200:
			return cResponse.body
			
# function to remove stocks from a dictionary (with key "SYMBOL") that has had a bonus/split/dividend
def removeActions(stocks, lookback):
	cleanList = []
	for s in stocks:
		urlSym = s["SYMBOL"]
		# urlSym = urllib.quote_plus(s["SYMBOL"])
		# print "downloading actions for", urlSym
		
		pResponse = unirest.get("https://stockviz.p.mashape.com/news/corporateActions", 
			params={
				"symbol": urlSym
			},
			headers={
				"X-Mashape-Authorization": mashape_auth,
				"Accept": "application/json"
			}
		);
		
		if pResponse.code == 200:
			d=datetime.date.today()-datetime.timedelta(days=lookback)
			ca = pResponse.body[len(pResponse.body)-1]
			lcad = datetime.datetime.strptime(ca["EX_DATE"], "%Y-%m-%dT%H:%M:%S").date()
			if d > lcad:
				# print " adding", s["SYMBOL"]
				cleanList.append(s)
				
	return cleanList

# function to place a trade in your StockViz account
def placeTrade(symbol, qty, buyOrSell):
	price = getLivePrice(symbol)

	#place the trade
	localtime = datetime.date.today()
	strTime = datetime.datetime.strftime(localtime, "%Y-%m-%d")
	print "placing trade asof: ", strTime

	tResponse = unirest.get("https://stockviz.p.mashape.com/account/OrderEquity", 
			params={
				"symbol": symbol,
				"qty": qty,
				"bs": buyOrSell,
				"t": "regular",
				"px": price,
				"asof": strTime
			},
			headers={
				"X-Mashape-Authorization": mashape_auth,
				"Accept": "application/json"
			}
	);

	if tResponse.code == 200:
		print "done."
	else:
		print "error placing trade"
