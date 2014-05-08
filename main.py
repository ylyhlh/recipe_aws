import boto
import boto.sqs
import database
import distance
from boto.sqs.message import RawMessage
from boto.sqs.message import Message

def getNearestMarket(here, markets):
	poss = []
	for market in markets:
		poss.append(market['Position'])
	dists = distance.getDistance("40.63319,-73.99440",poss)
	for i in range(len(markets)):
		markets[i]['Distance'] = dists[i] 
	return markets[0]

conn = boto.sqs.connect_to_region("us-west-2")
requestQueue = conn.get_queue('GredientRequest')
requestQueue.set_message_class(RawMessage)
while (True):
        rs = requestQueue.get_messages(1)
	if (len(rs) != 0):
		m = rs[0]
		body = m.get_body()
		print(body.split('_'))
		foodName = body.split('_')[0]
		requestQueue.delete_message(m)
		here = body.split('_')[1]
		responseQueue = conn.get_queue(body.split('_')[2])
		if responseQueue is not None:
			responseQueue.set_message_class(RawMessage)
			response = RawMessage()
			markets = database.getMarkets(foodName)
			if len(markets) == 0:
				response.set_body(foodName+" is not found in our database!!")
			else:
				nearest = getNearestMarket(here, markets)
				name = nearest['Name']
				address = nearest['Address']
				dis = nearest['Distance']
				response.set_body(foodName+" @ "+name+" @ "+address + " @ "+ dis)
			responseQueue.write(response)

