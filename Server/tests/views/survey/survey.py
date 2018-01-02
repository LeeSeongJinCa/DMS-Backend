import json
import unittest2 as unittest

from tests.views import account_admin, account_student

from app.models.survey import SurveyModel
from server import app


class TestSurvey(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        account_admin.create_fake_account()
        account_student.create_fake_account()

        self.admin_access_token = account_admin.get_access_token(self.client)

    def tearDown(self):
        account_admin.remove_fake_account()
        account_student.remove_fake_account()
        SurveyModel.objects.delete()

    def testA_addSurvey(self):
        """
        TC about survey addition

        - Preparations
        None

        - Process
        Add survey data

        - Validation
        Check survey data length is 1
        """
        # -- Process --
        rv = self.client.post('/admin/survey', headers={'Authorization': self.admin_access_token}, data={
            'title': 'test',
            'description': 'test',
            'start_date': '2018-01-01',
            'end_date': '2018-12-31',
            'target': [1, 3]
        })
        self.assertEqual(rv.status_code, 201)
        # -- Process --

        # -- Validation --
        rv = self.client.get('/admin/survey', headers={'Authorization': self.admin_access_token})
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(len(json.loads(rv.data.decode())), 1)
        # -- Validation --

    def testB_deleteSurvey(self):
        """
        TC about survey deletion

        - Preparations
        Add sample survey data and take survey ID

        - Process
        Delete survey data

        - Validation
        Check survey data length is 0
        """
        # -- Preparations --
        self.client.post('/admin/survey', headers={'Authorization': self.admin_access_token}, data={
            'title': 'test',
            'description': 'test',
            'start_date': '2018-01-01',
            'end_date': '2018-12-31',
            'target': [1, 3]
        })

        rv = self.client.get('/admin/survey', headers={'Authorization': self.admin_access_token})
        survey_id = json.loads(rv.data.decode())[0]['id']
        # -- Preparations --

        # -- Process --
        rv = self.client.delete('/admin/survey', headers={'Authorization': self.admin_access_token}, data={'survey_id': survey_id})
        self.assertEqual(rv.status_code, 200)
        # -- Process --

        # -- Validation --
        rv = self.client.get('/admin/survey', headers={'Authorization': self.admin_access_token})
        self.assertEqual(len(json.loads(rv.data.decode())), 0)
        # -- Validation --

    def testC_addQuestion(self):
        """
        TC about survey question addition

        - Preparations
        Add sample survey data and take survey ID

        - Process
        Add question data

        - Validation
        Check question data length is 1
        """
        # -- Preparations --
        self.client.post('/admin/survey', headers={'Authorization': self.admin_access_token}, data={
            'title': 'test',
            'description': 'test',
            'start_date': '2018-01-01',
            'end_date': '2018-12-31',
            'target': [1, 3]
        })

        rv = self.client.get('/admin/survey', headers={'Authorization': self.admin_access_token})
        survey_id = json.loads(rv.data.decode())[0]['id']
        # -- Preparations --

        # -- Process --
        rv = self.client.post('/admin/survey/question', headers={'Authorization': self.admin_access_token}, data={
            'survey_id': survey_id,
            'title': 'test',
            'is_objective': True,
            'choice_paper': ['one', 'two', 'three']
        })
        self.assertEqual(rv.status_code, 201)
        # -- Process --

        # -- Validation --
        rv = self.client.get('/admin/survey/question', headers={'Authorization': self.admin_access_token}, query_string={'survey_id': survey_id})
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(len(json.loads(rv.data.decode())), 1)
        # -- Validation --

    def testD_answer(self):
        """
        TC about survey answer upload

        - Preparations
        Add sample survey, question data, and take question IDs

        - Process
        Add answer data

        - Validation
        Check answer data(API required)
        """