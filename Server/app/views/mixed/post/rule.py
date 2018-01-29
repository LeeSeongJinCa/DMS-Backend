import json

from flasgger import swag_from
from flask import Blueprint, Response
from flask_restful import Api, Resource

from app.docs.mixed.post.rule import *
from app.models.post import RuleModel

from utils.access_controller import signed_account_only

api = Api(Blueprint('rule-api', __name__))


@api.resource('/rule')
class RuleList(Resource):
    @swag_from(RULE_LIST_GET)
    @signed_account_only
    def get(self):
        """
        기숙사규칙 리스트 조회
        """
        response = [{
            'id': str(rule.id),
            'write_time': str(rule.write_time)[:10],
            'author': rule.author,
            'title': rule.title,
            'pinned': rule.pinned
        } for rule in RuleModel.objects]

        return Response(json.dumps(response, ensure_ascii=False), content_type='application/json; charset=utf8')


@api.resource('/rule/<post_id>')
class RuleItem(Resource):
    @swag_from(RULE_ITEM_GET)
    @signed_account_only
    def get(self, post_id):
        """
        기숙사규칙 내용 조회
        """
        if len(post_id) != 24:
            return Response('', 204)

        rule = RuleModel.objects(id=post_id).first()
        if not rule:
            return Response('', 204)

        response = {
            'write_time': str(rule.write_time)[:10],
            'author': rule.author,
            'title': rule.title,
            'content': rule.content,
            'pinned': rule.pinned
        }

        return Response(json.dumps(response,ensure_ascii=False), content_type='application/json; charset=utf8')
