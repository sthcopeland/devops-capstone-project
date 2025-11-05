"""
Account Service

This microservice handles the lifecycle of Accounts
"""
# pylint: disable=unused-import
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401
from service.models import Account
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
            # paths=url_for("list_accounts", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# CREATE A NEW ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    This endpoint will create an Account based the data in the body that is posted
    """
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    # Uncomment once get_accounts has been implemented
    # location_url = url_for("get_accounts", account_id=account.id, _external=True)
    location_url = "/"  # Remove once get_accounts has been implemented
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


######################################################################
# LIST ALL ACCOUNTS
######################################################################

# ... place you code here to LIST accounts ...


######################################################################
# READ AN ACCOUNT
######################################################################

# ... place you code here to READ an account ...


######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################

# ... place you code here to UPDATE an account ...


######################################################################
# DELETE AN ACCOUNT
######################################################################

# ... place you code here to DELETE an account ...


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )


# --- appended CRUD routes ---
from flask import jsonify, request, abort
from service.models import Account, db


@app.get("/accounts/<int:account_id>")
def read_account(account_id: int):
    account = Account.query.get(account_id)
    if not account:
        abort(404, description=f"Account {account_id} not found")
    return jsonify(account.serialize()), 200


@app.get("/accounts")
def list_accounts():
    accounts = Account.query.all()
    return jsonify([a.serialize() for a in accounts]), 200


@app.put("/accounts/<int:account_id>")
def update_account(account_id: int):
    account = Account.query.get(account_id)
    if not account:
        abort(404, description=f"Account {account_id} not found")
    data = request.get_json() or {}
    for f in ("name", "email", "address", "phone_number"):
        if f in data:
            setattr(account, f, data[f])
    db.session.commit()
    return jsonify(account.serialize()), 200


@app.delete("/accounts/<int:account_id>")
def delete_account(account_id: int):
    account = Account.query.get(account_id)
    if not account:
        abort(404, description=f"Account {account_id} not found")
    db.session.delete(account)
    db.session.commit()
    return ("", 204)


# --- end appended CRUD routes ---
