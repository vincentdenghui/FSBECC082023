import requests
import unittest
import os
from dotenv import load_dotenv, find_dotenv
from requests.auth import HTTPBasicAuth
from rest_framework import status
import secrets

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

    def delete_test_objects(self,codes):
        for code in codes:
            requests.delete(self.get_url(f'/lenders/{code}/'),auth=self.basic_authentication_object)

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

        self.delete_test_objects([self.test_ro_lender_code])

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

        self.delete_test_objects([test_code])

    def test_user_can_get_lender(self):
        requests.post(self.get_url('/lenders/'),
                      auth=self.basic_authentication_object,
                      json={'name': self.test_ro_lender_name,
                            'code': self.test_ro_lender_code,
                            'upfront_commission_rate': 100,
                            'trial_commission_rate': 200,
                            'active': self.test_ro_lender_active})
        self.assertEqual(
            requests.get(
                self.get_url(f'/lenders/{self.test_ro_lender_code}'),
                auth=self.basic_authentication_object
            ).json()['name'],
            self.test_ro_lender_name
        )

        self.delete_test_objects([self.test_ro_lender_code])

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

        self.delete_test_objects([test_code])

    # FR2. List all Lenders (five per page)
    def test_user_can_see_pagination(self):
        #create 6 lenders
        codes_created = []
        for i in range(65,72):
            character = chr(i).upper()
            code = f'PT{character}'
            codes_created.append(code)
            requests.post(self.get_url('/lenders/'),
                            auth=self.basic_authentication_object,
                            json={'name': f'pagination_test_{character}',
                                  'code': code,
                                  'upfront_commission_rate': 100,
                                  'trial_commission_rate': 200,
                                  'active': True})
        self.assertEqual(len(requests.get(self.get_url('/lenders/')).json()['results']), 5)

        self.delete_test_objects(codes_created)

    # FR1. List active lenders
    def test_filter_active_lenders(self):
        #create 4 lenders, 2 active 2 inactive
        codes_created = []
        for i in range(65,69):
            character = chr(i).upper()
            code = f'FL{character}'
            codes_created.append(code)
            requests.post(self.get_url('/lenders/'),
                            auth=self.basic_authentication_object,
                            json={'name': f'active_filter_test_{character}',
                                  'code': code,
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

        self.delete_test_objects(codes_created)

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

        self.delete_test_objects(['FSC'])

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

        self.delete_test_objects(['FSU'])

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

        self.delete_test_objects(['FSV'])


    #FR5. Delete a specific Lender
    def test_user_can_delete_a_lender(self):
        requests.post(self.get_url('/lenders/'),
                      auth=self.basic_authentication_object,
                      json={'name': f'visitor_update_specific_by_code_test',
                            'code': f'FSW',
                            'upfront_commission_rate': 100,
                            'trial_commission_rate': 200,
                            'active': False})
        requests.delete(self.get_url('/lenders/FSW/'),auth=self.basic_authentication_object,)
        self.assertEqual(requests.get(self.get_url('/lenders/FSW/')).status_code,status.HTTP_404_NOT_FOUND)

        self.delete_test_objects(['FSW'])
    def test_visitor_cannot_delete_a_lender(self):
        requests.post(self.get_url('/lenders/'),
                      auth=self.basic_authentication_object,
                      json={'name': f'visitor_update_specific_by_code_test',
                            'code': f'FSX',
                            'upfront_commission_rate': 100,
                            'trial_commission_rate': 200,
                            'active': False})
        requests.delete(self.get_url('/lenders/FSX/'))
        self.assertNotEqual(requests.get(self.get_url('/lenders/FSX/')).status_code,status.HTTP_404_NOT_FOUND)

        self.delete_test_objects(['FSX'])

    # FR6. Bulk upload Lenders in CSV format
    def test_visitor_cannot_bulk_upload(self):
        csv = """id,name,code,upfront_commission_rate,trial_commission_rate,active
        1,csv_upload_test_A,CSA,100.0,200.0,True
"""
        post_response = requests.post(self.get_url('/csv-in-bulk/'),
                            data=csv.encode('utf-8'))
        get_response = requests.get(self.get_url('/lenders/CSD/'))
        self.assertEqual(post_response.status_code,status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_upload_empty_file_handled(self):
        csv = ''
        post_response = requests.post(self.get_url('/csv-in-bulk/'),
                            auth=self.basic_authentication_object,
                            data=csv.encode('utf-8'))
        self.assertTrue('No columns to parse from file' in post_response.json()['csv_parsing_errors'][0]['exception'])
        self.assertEqual(post_response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertFalse(post_response.json()['items_added'])
        self.assertFalse(post_response.json()['items_not_added'])


    def test_user_cannot_upload_malformed_csv(self):
        malformed_bytes =b'\x00' + secrets.token_bytes(1024) + b'\x00'
        post_response = requests.post(self.get_url('/csv-in-bulk/'),
                                      auth=self.basic_authentication_object,
                                      data=malformed_bytes)
        self.assertTrue('codec can\'t decode byte' , post_response.json()['csv_parsing_errors'][0]['exception'])
        self.assertEqual(post_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_upload_csv(self):
        csv = """id,name,code,upfront_commission_rate,trial_commission_rate,active
        1,csv_upload_test_B,CSB,100.0,200.0,True
"""
        post_response = requests.post(self.get_url('/csv-in-bulk/'),
                            auth=self.basic_authentication_object,
                            data=csv.encode('utf-8'))
        get_response = requests.get(self.get_url('/lenders/CSB/'))
        self.assertEqual(post_response.status_code,status.HTTP_200_OK)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

        self.delete_test_objects(['CSB'])

    def test_user_upload_duplicated_entries_will_not_be_overwritten_but_reported_in_the_response(self):
        csv = """id,name,code,upfront_commission_rate,trial_commission_rate,active
        1,csv_upload_test_C,CSC,100.0,200.0,True
        2,csv_upload_test_D,CSD,100.0,200.0,True
"""
        post_response = requests.post(self.get_url('/csv-in-bulk/'),
                            auth=self.basic_authentication_object,
                            data=csv.encode('utf-8'))
        self.assertEqual(post_response.status_code,status.HTTP_200_OK)

        second_post_response = requests.post(self.get_url('/csv-in-bulk/'),
                            auth=self.basic_authentication_object,
                            data=csv.encode('utf-8'))
        self.assertEqual(second_post_response.status_code, status.HTTP_207_MULTI_STATUS)
        self.assertEqual(len(second_post_response.json()['items_not_added']), 2)

        self.delete_test_objects(['CSC','CSD'])


    #FR7. Download Lenders in CSV format
    def test_visitor_can_not_bulk_download(self):
        get_response = requests.get(self.get_url('/csv-in-bulk/'))
        self.assertEqual(get_response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_user_can_bulk_download(self):
        csv = """id,name,code,upfront_commission_rate,trial_commission_rate,active
        1,csv_upload_test_F,CSF,100.0,200.0,True
        2,csv_upload_test_G,CSG,100.0,200.0,True
"""
        requests.post(self.get_url('/csv-in-bulk/'),
                            auth=self.basic_authentication_object,
                            data=csv.encode('utf-8'))

        get_response = requests.get(self.get_url('/csv-in-bulk/'),
                            auth=self.basic_authentication_object,
                            data=csv.encode('utf-8'))
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(requests.get(self.get_url('/lenders/CSF/')).status_code,status.HTTP_200_OK)
        self.assertEqual(requests.get(self.get_url('/lenders/CSG/')).status_code, status.HTTP_200_OK)

        self.delete_test_objects(['CSF','CSG'])



if __name__ == '__main__':
    unittest.main()







