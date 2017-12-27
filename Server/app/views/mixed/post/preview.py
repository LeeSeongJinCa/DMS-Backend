import json

from flasgger import swag_from
from flask import Response
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from app.docs.mixed.post.preview import *
from app.models.account import AdminModel, StudentModel
from app.models.post import FAQModel, NoticeModel, RuleModel


class FAQPreview(Resource):
    @swag_from(FAQ_PREVIEW_GET)
    @jwt_required
    def get(self):
        """
        FAQ 프리뷰 조회
        """
        admin = AdminModel.objects(id=get_jwt_identity()).first()
        student = StudentModel.objects(id=get_jwt_identity()).first()
        if not any((admin, student)):
            return Response('', 403)

        faq = FAQModel.objects(pinned=True).first()
        if not faq:
            faq = FAQModel.objects().first()
            if not faq:
                return Response('', 204)

        response = {
            'write_time': str(faq.write_time)[:-7],
            'author': faq.author.name,
            'title': faq.title,
            'content': faq.content,
            'pinned': faq.pinned
        }

        return Response(json.dumps(response, ensure_ascii=False), 200, content_type='application/json; charset=utf8')


class NoticePreview(Resource):
    @swag_from(NOTICE_PREVIEW_GET)
    @jwt_required
    def get(self):
        """
        공지사항 프리뷰 조회
        """
        admin = AdminModel.objects(id=get_jwt_identity()).first()
        student = StudentModel.objects(id=get_jwt_identity()).first()
        if not any((admin, student)):
            return Response('', 403)

        notice = NoticeModel.objects(pinned=True).first()
        if not notice:
            notice = NoticeModel.objects().first()
            if not notice:
                return Response('', 204)

        response ={
            'write_time': str(notice.write_time)[:-7],
            'author': notice.author.name,
            'title': notice.title,
            'content': notice.content,
            'pinned': notice.pinned
        }

        return Response(json.dumps(response, ensure_ascii=False), 200, content_type='application/json; charset=utf8')


class RulePreview(Resource):
    @swag_from(RULE_PREVIEW_GET)
    @jwt_required
    def get(self):
        """
        기숙사규정 프리뷰 조회
        """
        admin = AdminModel.objects(id=get_jwt_identity()).first()
        student = StudentModel.objects(id=get_jwt_identity()).first()
        if not any((admin, student)):
            return Response('', 403)

        rule = RuleModel.objects(pinned=True).first()
        if not rule:
            rule = RuleModel.objects().first()
            if not rule:
                return Response('', 204)

        response = {
            'write_time': str(rule.write_time)[:-7],
            'author': rule.author.name,
            'title': rule.title,
            'content': rule.content,
            'pinned': rule.pinned
        }

        return Response(json.dumps(response, ensure_ascii=False), 200, content_type='application/json; charset=utf8')
