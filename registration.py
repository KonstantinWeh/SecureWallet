from flask import Flask, jsonify
from flask import render_template
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)

@app.route('/')
@app.route('/setup')
def index(name=None):
    return render_template('setup.html', person=name)


@app.route("/generate-keys")
def generate_RS_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=1024)
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

    print(public_pem)

    return jsonify({
        'public_key': public_pem,
        'private_key': private_pem
    })


