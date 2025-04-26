from services.RSADS import RSASignature
from flask import jsonify
from flask import render_template
from services.ORAM import SimpleORAM
from flask import Blueprint, render_template
from parties.trusted_party import get_trusted_party

home_bp = Blueprint('home', __name__)

trusted_party = get_trusted_party()

@home_bp.route('/')
def setup():
    return render_template('setup.html')

@home_bp.route("/trusted_party_initialization")
def generate_tpi_keys():
    security_param_bits = 128
    num_blocks = 16

    oram = SimpleORAM(security_param_bits, num_blocks)
    sk, K, DB = oram.sk, oram.K, oram.DB

    print(sk)
    print(K)

    trusted_party.sk = sk.hex()
    trusted_party.K = K.hex()
    trusted_party.pk_T = "⊥"

    return jsonify({
        'sk': sk.hex(),
        'K': K.hex()
    })


@home_bp.route("/registration-station-setup")
def generate_RS_keys():
    sig = RSASignature(key_size_bits=1024)

    sk, pk = sig.keygen()

    message = b"Test message for RSA signature"
    signature = sig.sign(sk, message)

    print(f"Signature: {signature}")
    print(f"sk: {sk}")
    print(f"pk: {pk}")

    valid = sig.verify(pk, message, signature)
    print(f"Signature valid? {valid}")


    trusted_party.sk_RS = sk
    trusted_party.pk_RS = pk

    return jsonify({
        'sk': sk,
        'pk': pk
    })


@home_bp.route("/initialize-card")
def initialize_card():
    return jsonify({
        'pkRS': trusted_party.pk_RS,
        'sk': trusted_party.sk,
        'pkT': trusted_party.pk_T,
        'K': trusted_party.K
    })