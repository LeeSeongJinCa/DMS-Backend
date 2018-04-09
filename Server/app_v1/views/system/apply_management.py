from datetime import datetime

from flask import Blueprint, Response, request
from flask_restful import Api, abort

from app_v1.views import BaseResource
from app_v1.views import system_only

from app_v1.models.account import StudentModel
from app_v1.models.apply import ExtensionApplyModel, GoingoutApplyModel, StayApplyModel

api = Api(Blueprint('api', __name__))
api.prefix = '/system'


@api.resource('/apply/extension/11')
class Extension11(BaseResource):
    @system_only
    def delete(self):
        """
        11시 연장신청 정보 제거
        """
        for student in StudentModel.objects:
            student.update(extension_apply_11=None)

        return Response('', 200)


@api.resource('/apply/extension/11/<int:number>')
class Extension11EachStudent(BaseResource):
    @system_only
    def post(self, number):
        """
        특정 학생의 11시 연장신청
        """
        if not request.is_json:
            abort(400)

        student = StudentModel.objects(number=number).first()

        if not student:
            return Response('', 204)

        class_ = request.json['class_num']
        seat = request.json['seat']

        student.update(extension_apply_11=ExtensionApplyModel(class_=class_, seat=seat, apply_date=datetime.now()))

        return Response('', 201)

    @system_only
    def delete(self, number):
        """
        특정 학생의 11시 연장신청 정보 제거
        """
        student = StudentModel.objects(number=number).first()

        if not student:
            return Response('', 204)

        student.update(extension_apply_11=None)

        return Response('', 200)


@api.resource('/apply/extension/12')
class Extension12(BaseResource):
    @system_only
    def delete(self):
        """
        12시 연장신청 정보 제거
        """
        for student in StudentModel.objects:
            student.update(extension_apply_12=None)

        return Response('', 200)


@api.resource('/apply/extension/12/<int:number>')
class Extension12EachStudent(BaseResource):
    @system_only
    def post(self, number):
        """
        특정 학생의 12시 연장신청
        """
        if not request.is_json:
            abort(400)

        student = StudentModel.objects(number=number).first()

        if not student:
            return Response('', 204)

        class_ = request.json['class_num']
        seat = request.json['seat']

        student.update(extension_apply_12=ExtensionApplyModel(class_=class_, seat=seat, apply_date=datetime.now()))

        return Response('', 201)

    @system_only
    def delete(self, number):
        """
        특정 학생의 12시 연장신청 정보 제거
        """
        student = StudentModel.objects(number=number).first()

        if not student:
            return Response('', 204)

        student.update(extension_apply_12=None)

        return Response('', 200)


@api.resource('/apply/goingout')
class Goingout(BaseResource):
    @system_only
    def delete(self):
        """
        모든 학생의 외출신청 정보 초기화
        """
        for student in StudentModel.objects:
            student.update(goingout_apply=GoingoutApplyModel(apply_date=datetime.now()))

        return Response('', 200)


@api.resource('/apply/goingout/<int:number>')
class GoingoutEachStudent(BaseResource):
    @system_only
    def post(self, number):
        """
        특정 학생의 외출신청
        """
        if not request.is_json:
            abort(400)

        student = StudentModel.objects(number=number).first()

        if not student:
            return Response('', 204)

        sat = request.json['sat']
        sun = request.json['sun']

        student.update(goingout_apply=GoingoutApplyModel(on_saturday=sat, on_sunday=sun, apply_date=datetime.now()))

        return Response('', 201)

    @system_only
    def delete(self, number):
        """
        특정 학생의 외출신청 정보 초기화
        """
        student = StudentModel.objects(number=number).first()

        if not student:
            return Response('', 204)

        student.update(goingout_apply=GoingoutApplyModel(apply_date=datetime.now()))

        return Response('', 200)


@api.resource('/apply/stay/<int:number>')
class Stay(BaseResource):
    @system_only
    def post(self, number):
        """
        특정 학생의 잔류신청
        """
        if not request.is_json:
            abort(400)

        student = StudentModel.objects(number=number).first()

        if not student:
            return Response('', 204)

        value = request.json['value']

        student.update(stay_apply=StayApplyModel(value=value, apply_date=datetime.now()))

        return Response('', 201)