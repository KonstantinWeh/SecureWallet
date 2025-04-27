from flask import jsonify, request, Blueprint, render_template
from parties.trusted_party import get_trusted_party

import hashlib

from services.RSADS import RSASignature


transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/transaction')
def transaction():
    return render_template('transaction.html')

@transaction_bp.route('/make-payment', methods=["POST"])
def make_payment():
    trusted_party = get_trusted_party()

    data = request.get_json()
    household_id = int(data.get('id_h'))
    price = data.get('price')
    reclaim_period = data.get('reclaim_period')

    db_entry = trusted_party.user_has_enough_balance(household_id, price)

    print(db_entry)

    if db_entry == False:
        return jsonify({"error": "Insufficient balance"}), 400
  

    budget = db_entry['budget']
    ctr = db_entry['ctr']

    new_budget = int(budget) - int(price)
    new_ctr = ctr + 1

    commitment, com_r = trusted_party.commitment_scheme.commit(int(price))

    key = str(trusted_party.K).encode('utf-8')
    tag_message = (str(household_id) + str(new_ctr)).encode('utf-8')
    
    tag = hashlib.sha256(key + tag_message).digest()

    DSscheme = RSASignature()
    signature_message = str(tag) + reclaim_period + str(commitment)
    signature_message = signature_message.encode('utf-8')
    signature = DSscheme.sign(trusted_party.sk_RS, signature_message)


    proof = (signature, tag, commitment, com_r)

    return jsonify({
        "proof": {
            "signature": signature,
            "tag": tag.hex(),
            "commitment": commitment,
            "com_r": com_r
        }
    }), 200





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



