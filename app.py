
# coding: utf-8

# In[ ]:

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

from requests import put

# Flask app should start in global layout
app = Flask(__name__)



@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "Traiter":
        return {}
    
    result = req.get("result")
    text = result.get("resolvedQuery")
    contexts = result.get("contexts")
    parameters=contexts[0].get("parameters")
    fonction=parameters.get("Fonction")
    
    baseurl = "http://52.15.100.135:5000/"
    if fonction=="tags":
        url=baseurl+"tags/"
    if fonction=="articles similaires":
        url=baseurl+"similar_articles/"
    reponse = put(url, 
               data={"text": text})
    data=reponse.json()
    #data=fonction
    #data = json.loads(result)
    res = makeWebhookResult(data)
    return res


# def makeYqlQuery(req):
#     result = req.get("result")
#     parameters = result.get("parameters")
#     city = parameters.get("geo-city")
#     if city is None:
#         return None

#     return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):


    # print(json.dumps(item, indent=4))

    speech = str(data)

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')


# In[ ]:



