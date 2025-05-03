from flask import jsonify, request, Blueprint, render_template, flash
from parties.trusted_party import get_trusted_party

import hashlib

from services.RSDSA import RSASignature
from services.encoding import ensure_bytes

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/transaction')
def transaction():
    return render_template('transaction.html')

@transaction_bp.route('/make-payment', methods=["POST"])
def make_payment():
    trusted_party = get_trusted_party()
    vendor = trusted_party.get_vendor()

    data = request.get_json()
    household_id = int(data.get('id_h'))
    price = data.get('price')
    reclaim_period = data.get('reclaim_period')

    db_entry = trusted_party.user_has_enough_balance(household_id, int(price))

    if db_entry == False:
        msg = "Household " + str(household_id) + " has insufficient balance!"
        return jsonify({"error": "Insufficient balance", 
                        "alert": {
                            "type": "warning",
                            "message": msg
                        }}), 400
  

    budget = db_entry['budget']
    ctr = db_entry['ctr']

    new_budget = int(budget) - int(price)
    new_ctr = ctr + 1

    commitment, com_r = trusted_party.commitment_scheme.commit(int(price))
    
    key = ensure_bytes(trusted_party.K)
    tag_message = ensure_bytes(household_id) + ensure_bytes(new_ctr)

    tag = hashlib.sha256(key + tag_message).digest()

    DSscheme = RSASignature()

    signature_message = ensure_bytes(tag) + ensure_bytes(reclaim_period) + ensure_bytes(commitment)
    signature = DSscheme.sign(trusted_party.sk_RS, signature_message)

    proof = (signature, tag, commitment, com_r)

    trusted_party.update_balance(household_id, new_budget, new_ctr)


    if vendor.verify(proof, price, reclaim_period, trusted_party.get_pedersen_commitment_scheme()) != None:
        msg = "Household " + str(household_id) + " has bought the item for " + str(price) + ". Balance is updated."
        flash(msg, 'success')
        return jsonify({
            "proof": {
                "signature": signature,
                "tag": tag.hex(),
                "commitment": commitment,
                "com_r": com_r
            }, 
            "alert": {
                "type": "success",
                "message": msg
            }
        }), 200
    else:
        return jsonify({"error": "Vendor could not verify proof.", 
                        "alert": {
                            "type": "warning",
                            "message": "Vendor could not verify proof."
                        }}), 400





@transaction_bp.route("/get-database")
def get_database():
    
    trusted_party = get_trusted_party()
    
    print(trusted_party.get_DB_view())

    households = [
        {
            "id": idx,
            "budget": data["budget"] if data else "-",
            "counter": data["ctr"] if data else "-"
        }
        for idx, data in enumerate(trusted_party.get_DB_view())
    ]

    return jsonify(households)



