from datetime import datetime

from mongoengine import *


class SignupWaitingModel(Document):
    """
    학생 회원가입을 위한 UUID-학생 정보 매핑 collection
    """
    meta = {
        'collection': 'signup_waiting'
    }

    uuid = StringField(
        primary_key=True,
        min_length=4,
        max_length=4
    )
    # 회원가입 시 사용할 UUID

    name = StringField(
        required=True
    )
    # 학생 이름

    number = IntField(
        required=True
    )
    # 학번


class AccountBase(Document):
    """
    계정에 대한 상위 collection
    """
    meta = {
        'abstract': True,
        'allow_inheritance': True
    }

    signup_time = DateTimeField(
        default=datetime.now
    )
    # 회원가입 시간

    id = StringField(
        primary_key=True
    )
    pw = StringField(
        required=True
    )
    name = StringField(
        required=True
    )


class StudentModel(AccountBase):
    """
    학생 계정
    """
    meta = {
        'collection': 'account_student'
    }

    number = IntField(
        required=True
    )

    good_point = IntField(
        default=0
    )
    # 상점

    bad_point = IntField(
        default=0
    )
    # 벌점

    point_histories = EmbeddedDocumentListField(
        document_type='PointHistoryModel'
    )
    # 상벌점 내역

    penalty_training_status = BooleanField(
        default=False
    )
    # 벌점 교육 중인지의 여부

    penalty_level = IntField(
        default=0
    )
    # 벌점 교육 단계


class AdminModel(AccountBase):
    """
    관리자 계정
    """
    meta = {
        'collection': 'account_admin'
    }
