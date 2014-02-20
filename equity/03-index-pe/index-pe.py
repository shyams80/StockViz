import common

indices = common.getIndices()
for index in indices:
	indexName = index["INDEX_NAME"]
	indexId = index["INDEX_ID"]

	#indexName = "CNX 500"
	
	#constituents = common.getConstituentsByName(indexName)
	constituents = common.getConstituentsByIndexId(indexId)
	# print "total constituents:", len(constituents)
	
	if len(constituents) > 90:
		continue

	print indexName,
	
	indexPe = 0
	for cc in constituents:
		ticker = cc["SYMBOL"]
		#print ticker,

		price = common.getLivePrice(ticker)
		#print price,

		epss = common.getEps(ticker)

		annualEps = 0
		for i in range(0,4):
			annualEps += epss[i]["EPS_DILUTED_AEI"]

		if annualEps != 0:
			#print annualEps, price/annualEps
			indexPe += price/annualEps * cc["WEIGHTAGE"]

	indexPe /= 100

	print indexPe


