import unirest
import time

# function to place a trade in your StockViz account
def placeTrade(symbol, qty, buyOrSell):
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
		
		#place the trade
		localtime = time.localtime(time.time())
		strTime = time.strftime("%Y-%m-%d", localtime)
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
	else:
		print "error getting live price"
	
	return
		

mashape_auth = "YOUR_MASHAPE_API_KEY"
ticker="NIFTYBEES"
unirest.timeout(10)

# get the latest technicals

response = unirest.get("https://stockviz.p.mashape.com/technicaldata/technicalsEquity", 
	params={
		"symbol": ticker
	},
	headers={
		"X-Mashape-Authorization": mashape_auth,
		"Accept": "application/json"
	}
);

if response.code == 200:
	timeSeries = response.body
	
	# was there a cross-over in the last two days?
	t = timeSeries[len(timeSeries)-1]
	tminus1 = timeSeries[len(timeSeries)-2]
	
	if(tminus1["SMA_50"] < tminus1["SMA_200"]
		and t["SMA_50"] > t["SMA_200"]):
		print "Golden Cross"
		placeTrade(ticker, 1, "buy")
		
	elif(tminus1["SMA_50"] > tminus1["SMA_200"]
		and t["SMA_50"] < t["SMA_200"]):
		print "Death Cross"
		placeTrade(ticker, 1, "sell")
	
