from authlib.integrations.flask_client import OAuth
from urllib.parse import quote_plus, urlencode
from flask_setup import app

AUTH0_CLIENT_ID="WS6cNXPHvZEw7mRLF6NfoZhmvODjwUPw"
AUTH0_CLIENT_SECRET="5RD5Kz8vII1Fut2WOlV5Yc_QSX6KVI3M6f_tIMyYqKUNJWQaP8Nz55vXlyxSdgz7"
AUTH0_DOMAIN="storage-solution.eu.auth0.com"

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{AUTH0_DOMAIN}/.well-known/openid-configuration'
)