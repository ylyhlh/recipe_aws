import boto.dynamodb
def getMarkets(food):
	conn = boto.dynamodb.connect_to_region('us-west-2')
	markets = conn.get_table('Markets')
	resultsMarkets = []
	food = food.replace(" ", "")
	realFoodName = food.lower()
	try:
		foodItem = markets.get_item(hash_key=realFoodName)
		#get the item in "Markets"
		positions = conn.get_table('Postiion')
		print foodItem
		#iterate over keys and get the position of markets from "Position"
		for market in foodItem.keys():
			if market != "FoodName":
				pos = positions.get_item(hash_key=market)['position'] 
				add = positions.get_item(hash_key=market)['address']
				resultsMarkets.append({'Name': market, 'Position': pos, 'Address': add})
	except boto.dynamodb.exceptions.DynamoDBKeyNotFoundError:
		pass
	return resultsMarkets
 




##test
#print getMarkets('tomato')

