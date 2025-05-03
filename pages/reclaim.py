from parties.smartcard import SmartCard
from services.RSDSA import RSASignature
from flask import jsonify, request, Blueprint, render_template
from services.ORAM import SimpleORAM
from parties.trusted_party import get_trusted_party
from services.encoding import ensure_bytes

reclaim_bp = Blueprint('reclaim', __name__)

@reclaim_bp.route('/reclaim')
@reclaim_bp.route('/audit')
def registration():
    return render_template('reclaim.html')

@reclaim_bp.route("/verify_signatures")
def verify_signature():
    trusted_party = get_trusted_party()
    vendor = trusted_party.get_vendor()

    # vendor_db = ((signature, tag, commitment, com_r), int(price), int(reclaim_period))
    vendor_db = vendor.get_proofs()

    signatures = []

    for idx, data in enumerate(vendor_db):
        signature = data[0][0]
        tag = ensure_bytes(data[0][1])
        commitment = ensure_bytes(data[0][2])
        reclaim_period = ensure_bytes(str(data[2]))

        message = tag + reclaim_period + commitment

        valid = vendor.verify_signature(signature, message)
        signatures.append((signature.hex(), valid))
    
    print(signatures)

    return jsonify(signatures)


@reclaim_bp.route("/verify_tags")
def verify_tags():
    trusted_party = get_trusted_party()
    vendor = trusted_party.get_vendor()

    # vendor_db = ((signature, tag, commitment, com_r), int(price), int(reclaim_period))
    vendor_db = vendor.get_proofs()

    tags = []

    for idx, data in enumerate(vendor_db):
        tag = data[0][1]

        unique = "unique" if tag not in tags else "not unique"
        tags.append((tag.hex(), unique))
    
    print(tags)

    return jsonify(tags)


@reclaim_bp.route("/verify_commitment")
def verify_commitment():
    trusted_party = get_trusted_party()
    vendor = trusted_party.get_vendor()

    # vendor_db = ((signature, tag, commitment, com_r), int(price), int(reclaim_period))
    vendor_db = vendor.get_proofs()

    total_sum, total_com_r = 0, 0

    commitments = []
    product_of_commitments = 1

    q = trusted_party.commitment_scheme.get_mod_q()
    print(q)

    for idx, data in enumerate(vendor_db):
        signature = data[0][0]
        tag = ensure_bytes(data[0][1])
        commitment = ensure_bytes(data[0][2])
        com_r = data[0][3]
        price = data[1]
        reclaim_period = ensure_bytes(str(data[2])) 

        total_sum += price
        total_com_r += com_r

        commitment_int = int.from_bytes(commitment, byteorder='big')
        product_of_commitments = (product_of_commitments * commitment_int) % q   

        commitments.append((commitment.hex(), price))

    total_sum_commitment, total_sum_com_r = trusted_party.commitment_scheme.commit(int(total_sum), total_com_r)
    
    same = (total_sum_commitment == product_of_commitments)


    return jsonify({
        "commitments": commitments,
        "product_of_commitments": product_of_commitments,
        "total_sum_commitment": total_sum_commitment,
        "same": same
    })


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



