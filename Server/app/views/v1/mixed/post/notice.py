
from flask import Blueprint
from flask_restful import Api

from app.views.v1 import auth_required


from app.models.post import NoticeModel
from app.views.v1.mixed.post import PostAPIResource

api = Api(Blueprint('notice-api', __name__))


@api.resource('/notice')
class NoticeList(PostAPIResource):

    @auth_required
    def get(self):
        """
        공지사항 리스트 조회
        """
        return self.get_list_as_response(NoticeModel)


@api.resource('/notice/<post_id>')
class NoticeItem(PostAPIResource):

    @auth_required
    def get(self, post_id):
        """
        공지사항 내용 조회
        """
        return self.get_item_as_response(NoticeModel, post_id)
