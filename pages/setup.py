from services.RSDSA import RSASignature 
from flask import jsonify# type: ignore
from flask import render_template# type: ignore
from services.ORAM import SimpleORAM
from flask import Blueprint, render_template # type: ignore
from parties.trusted_party import get_trusted_party

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
@home_bp.route('/setup')
def setup():
    return render_template('setup.html')

@home_bp.route("/trusted_party_initialization")
def generate_tpi_keys():
    
    trusted_party = get_trusted_party()

    return jsonify({
        'sk': trusted_party.sk.hex(),
        'K': trusted_party.K.hex()
    })


@home_bp.route("/registration-station-setup")
def generate_RS_keys():

    trusted_party = get_trusted_party()
    sk, pk = trusted_party.setup_signature()

    return jsonify({
        'sk': sk,
        'pk': pk
    })


@home_bp.route("/initialize-card")
def initialize_card():

    trusted_party = get_trusted_party()

    print(
        trusted_party.pk_RS,
        trusted_party.sk.hex(),
        trusted_party.pk_T,
        trusted_party.K.hex()  
    )
    return jsonify({
        'pkRS': trusted_party.pk_RS,
        'sk': trusted_party.sk.hex(),
        'pkT': trusted_party.pk_T,
        'K': trusted_party.K.hex()
    })


@home_bp.route("/get-params")
def get_params():

    trusted_party = get_trusted_party()

    print(
        trusted_party.pk_RS,
        trusted_party.sk_RS,
        trusted_party.sk.hex(),
        trusted_party.pk_T,
        trusted_party.K.hex(), 
    )
    return jsonify({
        'pkRS': trusted_party.pk_RS,
        'skRS': trusted_party.sk_RS,
        'sk': trusted_party.sk.hex(),
        'pkT': trusted_party.pk_T,
        'K': trusted_party.K.hex(),
    })