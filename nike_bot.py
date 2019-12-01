if __name__ == "__main__":
	import requests
	import time
	import twitter

	# setup your own account and get these values from twitter
	api = twitter.Api(consumer_key="CONSUMER_KEY_HERE",
		consumer_secret="CONSUMER_SECRET_HERE",
		access_token_key="ACCESS_TOKEN_HERE",
		access_token_secret="ACCESS_TOKEN_SECRET")

	t = time.time()

	while True:
		try:
			r = requests.get('https://www.nike.com/launch/')
			s = r.text.split('div')

			# stored the products in a file
			o = []
			with open("/root/dev/product_list.txt", "r") as f:
				for line in f:
					o.append(line)

			n = []

			for sub in s:
				if 'class="product-card' in sub:
					try:
						n.append("{}{}".format(sub, s[s.index(sub) + 1].encode('utf-8')).split("aria-label=")[1].split(" class")[0])
					except Exception as e:
						print("{} : {}\n".format(time.time(), e))
						pass

			x = []
			st = ""

			for q in n:
				if "{}\n".format(q) not in o:

					if len(st) > 1:
						st = "{}, {}".format(st, q.replace("&#x27;", "'").replace("&amp;", "&").replace("Release Date", ""))
					else:
						st = "{}".format(q.replace("&#x27;", "'").replace("&amp;", "&").replace("Release Date", ""))

					x.append(q)

			st = "".join(i for i in st if ord(i) < 128)

			# tweet if new products
			if len(x) > 0:
				api.PostUpdate(st[:279])

				with open("/root/dev/product_list.txt", "a") as f:
					for p in x:
						f.write("{}\n".format(p))

			# sleep for one second
			time.sleep(60.0 - ((time.time() - t) % 60.0))
		except Exception as e:
			print("{} : {}\n".format(time.time(), e))
			# LOL who cares about exceptions?
			pass
