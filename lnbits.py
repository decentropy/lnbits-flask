import requests
import datetime as dt
import json
import bolt11 #https://github.com/nievk/bolt11

class LNbitsCalls: #LNBits

    def __init__(self, host, walletid, adminkey, invoicekey, tor=True):
        self.host = host
        self.walletid = walletid
        self.adminkey = adminkey
        self.invoicekey = invoicekey
        self.session = requests.session()       
        if tor:  #if onion host (requires pysocks module installed, and Tor running on host)
          self.session.proxies['http'] = 'socks5h://localhost:9050'
          self.session.proxies['https'] = 'socks5h://localhost:9050'

    def create_invoice(self, sats, memo):
        memo = "-" if memo=="" else memo
        data = {"out": False, "amount": sats, "memo": memo}
        r = self.session.post(self.host + "/api/v1/payments", headers={"X-Api-Key": self.invoicekey, "Content-type": "application/json"}, data=json.dumps(data))
        return {"payhash": r.json()["payment_hash"], "bolt11": r.json()["payment_request"], "sats": sats, "memo": memo, "expires": (dt.datetime.now()+ dt.timedelta(minutes=10)).isoformat()}

    def verify_paid(self, payhash):
        r = self.session.get(self.host + "/api/v1/payments/" + payhash, headers={"X-Api-Key": self.invoicekey})
        return r.json()['paid']

    def withdraw(self, invoice):
        data = {"out": True, "bolt11": invoice}
        r = self.session.post(self.host + "/api/v1/payments", headers={"X-Api-Key": self.adminkey, "Content-type": "application/json"}, data=json.dumps(data))
        return r.json()

    def bolt11amount(self, invoice): #Decode invoice amount (e.g. for checking before withdraw)
        try:
            return int(bolt11.decode(invoice)["amount"]/1000)
        except Exception as e:
            print(e)
            return 0

