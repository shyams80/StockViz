import unirest
from goose import Goose

mashape_auth = "YOUR_MASHAPE_API_KEY"
topics = ["economy", "gold", "TATAMOTORS", "DRREDDY"]
unirest.timeout(10)
g = Goose({'browser_user_agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'})

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
				print r['HEADLINE'].encode('cp850', errors='replace')	
				article = g.extract(url=r['SOURCE'])
				cleaned = article.cleaned_text.encode('ascii', 'ignore')
				print cleaned
				print "========================================="
	else:
		print "response: ", response.code, ". skipping..."
