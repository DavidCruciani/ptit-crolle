import os
from flask import Blueprint
from flask_restx import Api

api_blueprint = Blueprint(
    "api", __name__, url_prefix="/api"
)

authorizations = {
    "apikey": {
        "type": "apiKey",
        "in": "header",
        "name": "X-API-KEY",
    }
}

def version():
    with open(os.path.join(os.getcwd(),"version")) as read_version:
        loc = read_version.readlines()
    return loc[0].rstrip()


api = Api(api_blueprint,
    title='ptit-crolle API', 
    description="<a href='https://github.com/DavidCruciani/ptit-crolle' rel='noreferrer' target='_blank'>"
    "<img src='/static/image/crolle.png' width='200px' /></a><br />"
    'API to query ptit-crolle.',
    version=version(), 
    # license="GNU Affero General Public License version 3",
    # license_url="https://www.gnu.org/licenses/agpl-3.0.html",
    doc='/',
    security="apikey",
    authorizations=authorizations
)

from .account.account_api import account_ns

api.add_namespace(account_ns, path="/account")




