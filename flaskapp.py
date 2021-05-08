from flask import Flask, flash, request, redirect, render_template, session
import datetime as dt
from lnbits import LNbitsCalls

#Flask
app = Flask(__name__)
app.secret_key = "test123" #CHANGE THIS

# CHANGE THESE
lnbits_kwargs = {
 "host": "http://YOUR LN NODE TOR ADDRESS.onion",
 "walletid": "YOUR LNBITS WALLET ID HERE",
 "adminkey": "YOUR LNBITS ADMIN KEY HERE",
 "invoicekey": "YOUR LNBITS INVOICE KEY HERE",
 "tor": True
}
lnbits = LNbitsCalls(**lnbits_kwargs)

#Main UI
@app.route("/", methods=["GET"])
@app.route("/lightning", methods=["GET"])
def page_lightning():
  return render_template("lightning.html", page="lightning")

#Payment QR Code
@app.route("/lightning/pay", methods=["GET"])
def page_pay():
  return render_template("lightning.html", page="pay")

#LNBits actions
@app.route("/lnbits/<string:action>", methods=["GET"])
def api_lnbits(action=''):
  data = {}

  if action=="invoice": #create inbound invoice
      session["invoice"] = lnbits.create_invoice(int(request.args["sats"]), request.args.get("memo"))
      return redirect("/lightning/pay")

  if action=="verify": #verify lnbits paid
      if lnbits.verify_paid(session["invoice"]["payhash"]):
          # =============================
          #INSERT CODE: PAYMENT ACTION
          # =============================
          flash(str(session["invoice"]["sats"]) + ' sats received for ' + session["invoice"]["memo"], 'success')
          session["invoice"] = {}
          return redirect("/lightning")
      else:
          flash('payment not yet received', 'error')
          return redirect("/lightning/pay")
  
  if action=="withdraw": #pay outbound invoice
      bolt11 = request.args.get("withdrawbolt11")
      if bolt11:
          amount = lnbits.bolt11amount(bolt11)
          if 0 < amount:
              # =============================
              #INSERT CODE: WITHDRAWAL CONDITIONS
              # =============================
              res = lnbits.withdraw(bolt11)
              if res.get("payment_hash"):
                  # =============================
                  #INSERT CODE: WITHDRAWAL ACTION
                  # =============================
                  flash('payment sent', 'success')
              else:
                  flash(res.get("message"), 'error')                    
          else:
              flash('invoice not valid', 'error')                
      else:
          flash('submit an invoice', 'error')
      return redirect("/lightning")


if __name__ == "__main__":
    debug = True
    app.run(debug=debug)

