from parties.smartcard import SmartCard
from services.RSDSA import RSASignature
from flask import jsonify, request, Blueprint, render_template
from services.ORAM import SimpleORAM
from parties.trusted_party import get_trusted_party

reclaim_bp = Blueprint('reclaim', __name__)

@reclaim_bp.route('/reclaim')
@reclaim_bp.route('/audit')
def registration():
    return render_template('reclaim.html')

@reclaim_bp.route("/aggregate_proofs")
def allocate_budget():

    trusted_party = get_trusted_party()
    vendor = trusted_party.get_vendor()


    # vendor_db = ((signature, tag, commitment, com_r), int(price), int(reclaim_period))
    vendor_db = vendor.get_proofs()
    r_sum, price_sum = 0, 0

    for idx, data in enumerate(vendor_db):
        price_sum += data[1]
        r_sum += data[0][3]
   
    return jsonify({
        'price_sum': price_sum,
        'r_sum': r_sum
    })


@reclaim_bp.route("/get-claims")
def get_database():
    
    trusted_party = get_trusted_party()
    vendor = trusted_party.get_vendor()


    # vendor_db = ((signature, tag, commitment, com_r), int(price), int(reclaim_period))
    vendor_db = vendor.get_proofs()
    
    proofs = [
        {
            "id": idx,
            "signature": data[0][0].hex() if data else "-",
            "tag": data[0][1].hex() if data else "-",
            "commitment": data[0][2].hex() if data else "-",
            "com_r": data[0][3] if data else "-",
            "price": data[1] if data else "-",
            "reclaim_period": data[2] if data else "-"
        } for idx, data in enumerate(vendor_db)
    ]

    return jsonify(proofs)



