import unirest

mashape_auth = "YOUR_MASHAPE_API_KEY"
topics = ["economy", "gold", "TATAMOTORS", "DRREDDY"]
unirest.timeout(10)

for t in topics:
	print t
	response = unirest.get("https://stockviz.p.mashape.com/news/news", 
		params={
			"symbol": t
		},
		headers={
	    		"X-Mashape-Authorization": mashape_auth,
	    		"Accept": "application/json"
  		}
	);
	
	if response.code == 200:
		for r in response.body:
			if r.has_key('HEADLINE') and r.has_key('SOURCE'):
				print r['HEADLINE'].encode('cp850', errors='replace'), ": ", r['SOURCE']	
	else:
		print "response: ", response.code, ". skipping..."
