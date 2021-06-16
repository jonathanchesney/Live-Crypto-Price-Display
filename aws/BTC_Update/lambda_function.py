import urllib.request
import urllib.parse
import json
import boto3
import logging
 
logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
client = boto3.client('iot-data')

def get_conditions():
	api_conditions_url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD"
	try:
		f = urllib.request.urlopen(api_conditions_url)
	except:
		print("Failed to get conditions")
		return False
	json_conditions = f.read()
	f.close()
	return json.loads(json_conditions)

 
def lambda_handler(event, context):
    #print("CC3200_Thing: " + json.dumps(event['queryStringParameters']['CC3200_Thing']))
    logger.info("Attempting to fetch Shadow State")
    THINGNAME='CC3200_Thing'
    SHADOWNAME='BTC_Shadow'
    arr = -1
    try:
        response = client.get_thing_shadow(thingName=THINGNAME, shadowName=SHADOWNAME)
        logger.info("Shadow State Received")
        res = response['payload'].read()
        res_json = json.loads(res)
        print(json.dumps(res_json))
        vals = res_json['state']['desired']
        logger.info("Received From IoT: " + json.dumps(vals))
        logger.info("\nChanging for website\n")
        arr = vals['btc-vals-by-minute']
    except:
        print("Failed: Device Shadow Data Read")
        exit()
    print(arr)

    conditions = get_conditions()

    read_byte = urllib.parse.urlencode({'USD':conditions['USD']})
    new_val = read_byte.split('=')
    print(new_val[1])
    
    i = 1
    while (i < 20):
        arr[20-i] = arr[19-i]
        i=i+1
    arr[0] = float(new_val[1])
    print(arr)
    
    payload = json.dumps({'state': { 'desired': { 'btc-vals-by-minute': arr } }})

    logger.info("Attempting to Update Shadow State to ON")
    response = client.update_thing_shadow(
        thingName=THINGNAME,
        shadowName=SHADOWNAME,
        payload=payload
    )
    logger.info("IOT Shadow Updated")
    return {
        'statusCode': 200,
        "headers": {
            'Access-Control-Allow-Origin':'*',
            'Access-Control-Allow-Headers':'Content-Type,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods':'GET,OPTIONS'
        },
        'body': json.dumps('Shadow Updated!')
    }