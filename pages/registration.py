from parties.smartcard import SmartCard
from services.RSDSA import RSASignature
from flask import jsonify, request, Blueprint, render_template
from services.ORAM import SimpleORAM
from parties.trusted_party import get_trusted_party

registration_bp = Blueprint('registration', __name__)

@registration_bp.route('/registration')
def registration():
    return render_template('registration.html')

@registration_bp.route("/budget-and-card-allocation", methods=["POST"])
def allocate_budget():

    trusted_party = get_trusted_party()

    data = request.get_json()
    budget = data.get('bud')
    household_id = data.get('id_h')
    if household_id != '':
        household_id = int(household_id)

    # Now you have `budget` and `household_id`
    print(budget, household_id)

    trusted_party.add_card(household_id, budget, 0)
   
    return {"status": "success", "budget": budget, "household_id": household_id}


@registration_bp.route("/get-smart-card-state", methods=["POST"])
def get_smart_card_state():

    data = request.get_json()
    household_id = data.get('id_h')

    trusted_party = get_trusted_party()
    
    if household_id != '':
        household_id = int(household_id) 


    return jsonify({
        'pkRS_e': trusted_party.pk_RS[0],
        'pkRS_n': trusted_party.pk_RS[1],
        'sk': trusted_party.sk.hex(),
        'pkT': trusted_party.pk_T,
        'K': trusted_party.K.hex(),
        'id_H': household_id
    })



@registration_bp.route("/get-database")
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



