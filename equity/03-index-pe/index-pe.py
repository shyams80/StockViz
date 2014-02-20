import common

indexName = "CNX NIFTY"
constituents = common.getConstituents(indexName)
# print "total constituents:", len(constituents)

indexPe = 0
for cc in constituents:
	ticker = cc["SYMBOL"]
	print ticker,
	
	price = common.getLivePrice(ticker)
	print price,
	
	epss = common.getEps(ticker)
	
	annualEps = 0
	for i in range(0,4):
		annualEps += epss[i]["EPS_DILUTED_AEI"]
		
	print annualEps, price/annualEps
	
	indexPe += price/annualEps * cc["WEIGHTAGE"]
	
indexPe /= 100

print indexName, indexPe


