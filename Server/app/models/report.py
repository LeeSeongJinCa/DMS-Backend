from datetime import datetime

from app.models.account import StudentModel
from app.models import *


class ReportBase(Document):
    """
    Report document base
    """
    meta = {
        'collection': 'report_base',
        'allow_inheritance': True
    }

    report_time = DateTimeField(
        required=True,
        default=datetime.now()
    )

    informant = ReferenceField(
        document_type=StudentModel,
        required=True
    )

    title = StringField(
        required=True
    )

    content = StringField(
        required=True
    )


class BugReportModel(ReportBase):
    """
    Bug report document
    """


class FacilityReportModel(ReportBase):
    """
    Facility report document
    """
    room = IntField(
        required=True,
        min_value=200,
        max_value=599
    )