from datetime import datetime

from flask import Blueprint, g, request
from flask_restful import Api, abort


from app.views.v1 import BaseResource
from app.views.v1 import student_only


from app.models.report import FacilityReportModel

api = Api(Blueprint('student-facility-report-api', __name__))


@api.resource('/report/facility')
class FacilityReport(BaseResource):

    @student_only
    def post(self):
        """
        시설고장 신고
        """
        student = g.user

        content = request.form['content']
        room = int(request.form['room'])

        if not 200 <= room < 519:
            abort(400)

        report = FacilityReportModel(author=student.name, content=content, room=room, report_time=datetime.now()).save()

        return self.unicode_safe_json_response({
            'id': str(report.id)
        }, 201)
