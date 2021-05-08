# lnbits-flask

This is a barebones flask web application that accepts lightning payments and withdrawals.

Customize to enable lightning payments and refunds in your web application.

lnbits.py wraps calls to LNBits API, configured in flaskapp.py:

```
 lnbits_kwargs = {
  "host": "http://YOUR LN NODE TOR ADDRESS.onion",
  "walletid": "YOUR LNBITS WALLET ID HERE",
  "adminkey": "YOUR LNBITS ADMIN KEY HERE",
  "invoicekey": "YOUR LNBITS INVOICE KEY HERE",
  "tor": True
 }
```

### LNBits behind Tor (e.g. Umbrel node)
Set tor=True, if LNBits host is an onion address.

You must have Tor running on the flask host.

You must have pysocks installed, to support Tor connection via socks5 proxy.

## Requirements
* LNBits wallet
* Python module: pysocks
* Python modules: bolt11 (https://github.com/nievk/bolt11)
* Tor running on host

## How to run
* Install requirements above
* Customize lnbits_kwargs in flaskapp.py
* $ python3 flaskapp.py
