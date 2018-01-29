import json
import unittest

from tests.views import account_admin, account_student

from server import app


class TestAccountControl(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        account_admin.create_fake_account()
        account_student.create_fake_account()
        self.admin_access_token = account_admin.get_access_token(self.client)
        self.student_access_token = account_student.get_access_token(self.client)

    def tearDown(self):
        account_admin.remove_fake_account()
        account_student.remove_fake_account()

    def testA_deleteAccount(self):
        """
        TC about existing student account deletion

        - Preparations
        Test auth with existing student data

        - Exception Tests
        Non-existing student number
        Forbidden with student access token

        - Process
        Take UUID with student account deletion

        - Validation
        Test student auth
        """
        # -- Preparations --
        rv = self.client.post('/auth', data={'id': 'fake_student', 'pw': 'fake'})
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(rv.data)
        # -- Preparations --

        # -- Exception Tests --
        rv = self.client.post('/admin/account-control', headers={'Authorization': self.admin_access_token}, data={'number': 0000})
        self.assertEqual(rv.status_code, 204)

        rv = self.client.post('/admin/account-control', headers={'Authorization': self.student_access_token})
        self.assertEqual(rv.status_code, 403)
        # -- Exception Tests --

        # -- Process --
        rv = self.client.post('/admin/account-control', headers={'Authorization': self.admin_access_token}, data={'number': 1111})
        self.assertEqual(rv.status_code, 201)
        # -- Process --

        # -- Validation --
        rv = self.client.post('/auth', data={'id': 'fake_student', 'pw': 'fake'})
        self.assertEqual(rv.status_code, 401)
        # -- Validation --

    def testB_findUUID(self):
        """
        TC about find UUID after student account initialize

        - Preparations
        Initialize student account

        - Exception Tests
        None

        - Process
        Get UUID with student number

        - Validation
        Verify UUID
        """
        # -- Preparations --
        rv = self.client.post('/admin/account-control', headers={'Authorization': self.admin_access_token}, data={'number': 1111})
        self.assertEqual(rv.status_code, 201)
        # -- Preparations --

        # -- Exception Tests --
        # -- Exception Tests --

        # -- Process --
        rv = self.client.post('/admin/account-control', headers={'Authorization': self.admin_access_token}, data={'number': 1111})
        self.assertEqual(rv.status_code, 201)
        uuid = json.loads(rv.data.decode())['uuid']
        # -- Process --

        # -- Validation --
        rv = self.client.post('/verify/uuid', data={'uuid': uuid})
        self.assertEqual(rv.status_code, 200)
        # -- Validation --
