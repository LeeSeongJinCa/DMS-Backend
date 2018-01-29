from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Api, abort, request
from flasgger import swag_from

from app.docs.student.report.bug_report import *
from app.models.account import StudentModel
from app.models.report import BugReportModel
from app.views import BaseResource

api = Api(Blueprint('student-bug-report-api', __name__))


@api.resource('/report/bug')
class BugReport(BaseResource):
    @swag_from(BUG_REPORT_POST)
    @jwt_required
    def post(self):
        """
        버그 신고
        """
        student = StudentModel.objects(id=get_jwt_identity()).first()
        if not student:
            abort(403)

        title = request.form['title']
        content = request.form['content']

        report = BugReportModel(author=student.name, title=title, content=content).save()

        return {
            'id': str(report.id)
        }, 201
