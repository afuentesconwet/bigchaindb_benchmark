import time

from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

bdb_root_url = 'localhost:9984'  # Use YOUR BigchainDB Root URL here
bdb = BigchainDB(bdb_root_url)	#Without auth tokens, second param for the tokens.

bdb = BigchainDB(bdb_root_url)

alice, bob = generate_keypair(), generate_keypair()

numTx = 10000

assetList = []
txList = []
fulfilled_token_txList = []

for i in range(numTx):
	assetList.append(
		{
			'data': {
				'Temperature': i,
				'Humidity': 67,
				'Location': 'UPM-ETSIINF-CoNWetLab-uwa'
			}
		}
	)

for i in range(numTx):
	txList.append(
		bdb.transactions.prepare(
	    		operation='CREATE',
	    		signers=alice.public_key,
	    		recipients=[([bob.public_key], 10)],
	    		asset=assetList[i]
		)
	)

for i in range(numTx):
	fulfilled_token_txList.append(
		bdb.transactions.fulfill(
    			txList[i],
    			private_keys=alice.private_key
		)
	)

start = time.time()

for i in range(numTx):
	#startTx = time.time()
	bdb.transactions.send_async(fulfilled_token_txList[i])
	#endTx = time.time()
	#print("Sent new Tx in {} .".format(endTx - startTx))

end = time.time()

print("Sent {} TXs in {} .".format(numTx, end - start))
