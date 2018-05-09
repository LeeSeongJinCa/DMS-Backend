from flask import Blueprint, Response, abort, g, request
from flask_restful import Api
from flasgger import swag_from

from app.docs.v2.admin.point.rule import *
from app.models.account import AdminModel
from app.models.point import PointRuleModel
from app.views.v2 import BaseResource, auth_required, json_required

api = Api(Blueprint(__name__, __name__, url_prefix='/admin/point/rule'))


@api.resource('')
class Rule(BaseResource):
    @auth_required(AdminModel)
    @swag_from(RULE_GET)
    def get(self):
        """
        상벌점 규칙 목록 조회
        """
        return self.unicode_safe_json_dumps([{
            'id': str(rule.id),
            'name': rule.name,
            'pointType': rule.point_type,
            'minPoint': rule.min_point,
            'maxPoint': rule.max_point
        } for rule in PointRuleModel.objects])

    @auth_required(AdminModel)
    @json_required('name', 'pointType', 'minPoint', 'maxPoint')
    @swag_from(RULE_POST)
    def post(self):
        """
        상벌점 규칙 추가
        """
        name = request.json['name']
        point_type = request.json['pointType']
        min_point = request.json['minPoint']
        max_point = request.json['maxPoint']

        if min_point > max_point:
            abort(400)

        rule = PointRuleModel(
            name=name,
            point_type=point_type,
            min_point=min_point,
            max_point=max_point
        ).save()

        return {
            'id': str(rule.id)
        }, 201


@api.resource('/<rule_id>')
class RuleAlteration(BaseResource):
    @auth_required(AdminModel)
    @json_required('name', 'pointType', 'minPoint', 'maxPoint')
    @swag_from(RULE_ALTERATION_PATCH)
    def patch(self, rule_id):
        """
        상벌점 규칙 내용 수정
        """
        name = request.json['name']
        point_type = request.json['pointType']
        min_point = request.json['minPoint']
        max_point = request.json['maxPoint']

        if len(rule_id) != 24:
            return Response('', 204)

        rule = PointRuleModel.objects(id=rule_id).first()

        if not rule:
            return Response('', 204)

        updated = rule.update(
            name=name,
            point_type=point_type,
            min_point=min_point,
            max_point=max_point
        )

        if updated:
            return Response('', 200)
        else:
            abort(500)

    @auth_required(AdminModel)
    @swag_from(RULE_ALTERATION_DELETE)
    def delete(self, rule_id):
        """
        상벌점 규칙 삭제
        """
        if len(rule_id) != 24:
            return Response('', 204)

        rule = PointRuleModel.objects(id=rule_id).first()

        if not rule:
            return Response('', 204)

        rule.delete()

        return Response('', 200)
