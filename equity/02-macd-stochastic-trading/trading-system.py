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
	tminus1 = techs[len(techs)-2]
	tminus2 = techs[len(techs)-3]
	
	#check if an macd or stochastic signal was given out

	signal = False
	if t["MACD"] > t["MACD_SIGNAL"]:
		#was there a stochastic crossover the last 2 days
		
		if (t["STOCH_FAST_K"] > t["STOCH_FAST_D"]
			and tminus1["STOCH_FAST_K"] < tminus1["STOCH_FAST_D"]):
				signal = True
		elif (tminus1["STOCH_FAST_K"] > tminus1["STOCH_FAST_D"]
			and tminus2["STOCH_FAST_K"] < tminus2["STOCH_FAST_D"]):
				signal = True
				
	if signal:
		print "Buy:", ticker
		common.placeTrade(ticker, 1, "buy")
		


