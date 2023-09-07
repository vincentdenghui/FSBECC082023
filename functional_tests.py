import requests
import unittest
import os
from dotenv import load_dotenv, find_dotenv
from requests.auth import HTTPBasicAuth
from rest_framework import status

load_dotenv(find_dotenv())

class RequestsClientTest(unittest.TestCase):

    def setUp(self):
        self.djang_user = os.environ['DJANGO_USER']
        self.djang_user_password = os.environ['DJANGO_USER_PASSWORD']
        self.basic_authentication_object = HTTPBasicAuth(self.djang_user, self.djang_user_password)
        self.test_users = []


        #user for readonly checks
        self.test_ro_lender_code = 'TRO'
        self.test_ro_lender_name = 'SampleName'
        self.test_ro_lender_active = True
    def tearDown(self):
        ...#remove TRO user

    def get_url(self,route):
        return f'http://localhost:8000{route}'

    #FRi1. can visit the home page
    def test_can_visit_the_default_home_page(self):
        response = requests.get(self.get_url('/'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('lenders' in response.json())



    def test_user_can_create_lender_for_read_only_check(self):
        requests.post(self.get_url('/lenders/'),
                      auth=self.basic_authentication_object,
                      json={'name':self.test_ro_lender_name,
                            'code': self.test_ro_lender_code,
                            'upfront_commission_rate': 100,
                            'trial_commission_rate': 200,
                            'active': self.test_ro_lender_active})
        self.assertEqual(requests.get(self.get_url(f'/lenders/{self.test_ro_lender_code}')).json()['name'],
                         self.test_ro_lender_name)


    # FR1. Create a new Lender
    def test_user_can_create_lender(self):
        test_code = 'TGP'
        test_name = 'tgf7qh8o3y45'
        res = requests.post(self.get_url('/lenders/'),
                      auth=self.basic_authentication_object,
                      json={'name':test_name,
                            'code': test_code,
                            'upfront_commission_rate': 100,
                            'trial_commission_rate': 200,
                            'active': False})
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        self.assertEqual(requests.get(self.get_url(f'/lenders/{test_code}')).json()['name'],test_name)

    def test_user_can_get_lender(self):
        self.assertEqual(
            requests.get(
                self.get_url(f'/lenders/{self.test_ro_lender_code}'),
                auth=self.basic_authentication_object
            ).json()['name'],
            self.test_ro_lender_name
        )

    def test_visitors_cannot_create_lender(self):
        test_code = 'TGQ'
        test_name = 'tgf7qh8o3y46'
        res = requests.post(self.get_url('/lenders/'),
                      json={'name':test_name,
                            'code': test_code,
                            'upfront_commission_rate': 100,
                            'trial_commission_rate': 200,
                            'active': False})
        self.assertNotEqual(res.status_code,status.HTTP_201_CREATED)
        self.assertEqual(requests.get(self.get_url(f'/lenders/{test_code}')).status_code,status.HTTP_404_NOT_FOUND)

    # FR2. List all Lenders (five per page)
    def test_user_can_see_pagination(self):
        #create 6 lenders
        for i in range(65,72):
            character = chr(i).upper()
            requests.post(self.get_url('/lenders/'),
                            auth=self.basic_authentication_object,
                            json={'name': f'pagination_test_{character}',
                                  'code': f'PT{character}',
                                  'upfront_commission_rate': 100,
                                  'trial_commission_rate': 200,
                                  'active': True})
        self.assertEqual(len(requests.get(self.get_url('/lenders/')).json()['results']), 5)



        ...
    # FR1. List active lenders
    def test_filter_active_lenders(self):
        #create 4 lenders, 2 active 2 inactive
        for i in range(65,69):
            character = chr(i).upper()
            requests.post(self.get_url('/lenders/'),
                            auth=self.basic_authentication_object,
                            json={'name': f'active_filter_test_{character}',
                                  'code': f'FL{character}',
                                  'upfront_commission_rate': 100,
                                  'trial_commission_rate': 200,
                                  'active': i%2 == 0})

        url = self.get_url(f'/lenders/?active=True')
        all_active = True
        while True:
            response = requests.get(url).json()
            for each in response['results']:
                if not each['active']:
                    all_active = False
                    break
            if not response['next']:
                break
            else:
                url = response['next']
        self.assertTrue(all_active)


    # FR3. Get a specific Lender
    def test_can_get_a_specific_lender_by_code(self):
        requests.post(self.get_url('/lenders/'),
                      auth=self.basic_authentication_object,
                      json={'name': f'get_specific_by_code_test',
                            'code': f'FSC',
                            'upfront_commission_rate': 100,
                            'trial_commission_rate': 200,
                            'active': True})
        self.assertEqual(requests.get(self.get_url(f'/lenders/?code=FSC')).json()['results'][0]['name'],
                         'get_specific_by_code_test')

    # FR4. Update a specific Lender
    def test_user_can_update_a_specific_lender_by_code(self):
        requests.post(self.get_url('/lenders/'),
                      auth=self.basic_authentication_object,
                      json={'name': f'update_specific_by_code_test',
                            'code': f'FSU',
                            'upfront_commission_rate': 100,
                            'trial_commission_rate': 200,
                            'active': False})
        requests.put(self.get_url('/lenders/FSU/'),
                      auth=self.basic_authentication_object,
                      data={'name': f'update_specific_by_code_test',
                            'code': f'FSU',
                            'upfront_commission_rate': 100,
                            'trial_commission_rate': 200,
                            'active': True})
        self.assertTrue(requests.get(self.get_url(f'/lenders/FSU/')).json()['active'])

    def test_visitor_cannot_update_a_specific_lender_by_code(self):
        requests.post(self.get_url('/lenders/'),
                      auth=self.basic_authentication_object,
                      json={'name': f'visitor_update_specific_by_code_test',
                            'code': f'FSV',
                            'upfront_commission_rate': 100,
                            'trial_commission_rate': 200,
                            'active': False})
        requests.put(self.get_url('/lenders/FSV/'),
                      data={'name': f'visitor_update_specific_by_code_test',
                            'code': f'FSV',
                            'upfront_commission_rate': 100,
                            'trial_commission_rate': 200,
                            'active': True})
        self.assertFalse(requests.get(self.get_url(f'/lenders/FSV/')).json()['active'])
    # FR5. Delete a specific Lender

        # test user can

        # test visito cannot

    # FR6. Bulk upload Lenders in CSV format

    # FR7. Download Lenders in CSV format





if __name__ == '__main__':
    unittest.main()






