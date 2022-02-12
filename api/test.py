from flask import Flask
from flask import *

app = Flask(__name__, static_folder='static')

@app.route('/')
def testing():
     return render_template('index.html')

if __name__ == '__main__':
    app.run()



    *** Authorization Request in Python ***|
 
import requests
url = "https://sandbox.safaricom.co.ke/oauth/v1/generate"
querystring = {"grant_type":"client_credentials"}
payload = ""
headers = {
  "Authorization": "Basic SWZPREdqdkdYM0FjWkFTcTdSa1RWZ2FTSklNY001RGQ6WUp4ZVcxMTZaV0dGNFIzaA=="
}
response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
print(response.text)