import common

constituents = common.getConstituents("CNX NIFTY")
# print "total constituents:", len(constituents)
cleanConsts = common.removeActions(constituents, 30)
# print "total clean constituents:", len(cleanConsts)

for cc in cleanConsts:
	ticker = cc["SYMBOL"]
	print "checking", ticker, 
	techs = common.getTechnicals(ticker)
	if len(techs) == 0:
		print "skipping"
		continue
	
	print "."
	
	t = techs[len(techs)-1]
	price = common.getLivePrice(ticker)
	
	#check if the price is below the lower bollinger band

	if t["BB_DN"] > price:
		#there was a breakdown
		
		print "Buy:", ticker
		common.placeTrade(ticker, 1, "buy")
		


