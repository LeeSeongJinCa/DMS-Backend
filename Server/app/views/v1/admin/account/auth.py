from binascii import hexlify
from hashlib import pbkdf2_hmac
from uuid import UUID

from flask import Blueprint, current_app, request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity, jwt_refresh_token_required
from flask_restful import Api, abort


from app.views.v1 import BaseResource


from app.models.account import AdminModel, TokenModel, AccessTokenModel, RefreshTokenModel

api = Api(Blueprint('admin-auth-api', __name__))
api.prefix = '/admin'


@api.resource('/auth')
class Auth(BaseResource):

    def post(self):
        """
        관리자 로그인
        """
        id = request.form['id']
        pw = request.form['pw']

        pw = hexlify(pbkdf2_hmac(
            hash_name='sha256',
            password=pw.encode(),
            salt=current_app.secret_key.encode(),
            iterations=100000
        )).decode('utf-8')
        # pbkdf2_hmac hash with salt(secret key) and 100000 iteration

        admin = AdminModel.objects(id=id, pw=pw).first()

        if not admin:
            abort(401)

        # --- Auth success

        return self.unicode_safe_json_response({
            'access_token': create_access_token(TokenModel.generate_token(AccessTokenModel, admin, request.headers['USER-AGENT'])),
            'refresh_token': create_refresh_token(TokenModel.generate_token(RefreshTokenModel, admin, request.headers['USER-AGENT']))
        }, 200)


@api.resource('/refresh')
class Refresh(BaseResource):

    @jwt_refresh_token_required
    def post(self):
        """
        새로운 Access Token 획득
        """
        token = RefreshTokenModel.objects(identity=UUID(get_jwt_identity())).first()

        if not token:
            abort(205)

        return self.unicode_safe_json_response({
            'access_token': create_access_token(TokenModel.generate_token(AccessTokenModel, token.owner, request.headers['USER_AGENT']))
        }, 200)
