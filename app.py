import os
from flask import Flask
from pages.setup import home_bp
from pages.registration import registration_bp
from pages.transaction import transaction_bp
from pages.reclaim import reclaim_bp


app = Flask(__name__)
app.secret_key = os.urandom(24)

app.register_blueprint(home_bp)
app.register_blueprint(registration_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(reclaim_bp)


if __name__ == "__main__":
    app.run(debug=True)