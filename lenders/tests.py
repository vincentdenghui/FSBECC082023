from django.test import TestCase
from lenders.models import Lender
from django.db.utils import DataError
from django.core.exceptions import ValidationError

class LenderTestCase(TestCase):
    def setUp(self):
        Lender.objects.create(  name = 'Commonwealth Bank',
                                code = 'CBA',
                                upfront_commission_rate = 12,
                                trial_commission_rate = 23,
                                active = True)
        Lender.objects.create(  name = 'Westpac',
                                code = 'WBC',
                                upfront_commission_rate = 11,
                                trial_commission_rate = 13,
                                active = True)
        Lender.objects.create(  name = 'Silicon Valley Bank',
                                code = 'SVB',
                                upfront_commission_rate = 100,
                                trial_commission_rate = 200,
                                active = False)

    def test_lenders_can_be_created(self):
        """Lenders can be correctly stored"""
        cba = Lender.objects.get(code="CBA")
        wbc = Lender.objects.get(code="WBC")
        svb = Lender.objects.get(code="SVB")

        self.assertEqual(cba.name,'Commonwealth Bank')
        self.assertEqual(wbc.name, 'Westpac')
        self.assertEqual(svb.name, 'Silicon Valley Bank')

        self.assertEqual(cba.upfront_commission_rate, 12)
        self.assertEqual(wbc.upfront_commission_rate, 11)
        self.assertEqual(svb.upfront_commission_rate, 100)

        self.assertEqual(cba.trial_commission_rate,23)
        self.assertEqual(wbc.trial_commission_rate, 13)
        self.assertEqual(svb.trial_commission_rate, 200)

        self.assertEqual(cba.active, True)
        self.assertEqual(wbc.active, True)
        self.assertEqual(svb.active, False)

    def test_empty_name_not_allowed(self):
        with self.assertRaises(ValidationError) as context:
            test_object = Lender.objects.create(name='',
                                  code='TAA',
                                  upfront_commission_rate=100,
                                  trial_commission_rate=200,
                                  active=False)
            test_object.full_clean()
        self.assertTrue('This field cannot be blank' in str(context.exception))

    def test_max_name_length_allowed(self):
        test_object = Lender.objects.create(name='A'*1024,
                              code='TAB',
                              upfront_commission_rate=100,
                              trial_commission_rate=200,
                              active=False)
        test_object.full_clean()
        self.assertEqual(test_object.name, 'A'*1024)

    def test_over_length_name_not_allowed(self):
        with self.assertRaises(DataError) as context:
            test_object = Lender.objects.create(name='A'*2025,
                                  code='TAC',
                                  upfront_commission_rate=100,
                                  trial_commission_rate=200,
                                  active=False)
            test_object.full_clean()
        self.assertTrue('Data too long' in str(context.exception))

    def test_three_only_three_uppercase_alphebets_allowed_in_code(self):
        test_object = Lender.objects.create(name='Blah',
                              code='TAD',
                              upfront_commission_rate=100,
                              trial_commission_rate=200,
                              active=False)
        test_object.full_clean()
        self.assertEqual(test_object.code, 'TAD')

    def test_empty_code_not_allowed_for_a_lender_code(self):
        with self.assertRaises(ValidationError) as context:
            test_object = Lender.objects.create(name='Blah',
                                  code='',
                                  upfront_commission_rate=100,
                                  trial_commission_rate=200,
                                  active=False)
            test_object.full_clean()
        self.assertTrue('This field cannot be blank' in str(context.exception))

    def test_number_not_allowed_for_a_lender_code(self):
        with self.assertRaises(ValidationError) as context:
            test_object = Lender.objects.create(name='Blah',
                                                code='TA3',
                                                upfront_commission_rate=100,
                                                trial_commission_rate=200,
                                                active=False)
            test_object.full_clean()
        self.assertTrue('only capital alphabets [A-Z] are allowed' in str(context.exception))

    def test_punctuations_not_allowed_for_a_lender_code(self):
        with self.assertRaises(ValidationError) as context:
            test_object = Lender.objects.create(name='Blah',
                                                code='TA@',
                                                upfront_commission_rate=100,
                                                trial_commission_rate=200,
                                                active=False)
            test_object.full_clean()
        self.assertTrue('only capital alphabets [A-Z] are allowed' in str(context.exception))

    def test_lower_case_letters_not_allowed_for_a_lender_code(self):
        with self.assertRaises(ValidationError) as context:
            test_object = Lender.objects.create(name='Blah',
                                                code='taf',
                                                upfront_commission_rate=100,
                                                trial_commission_rate=200,
                                                active=False)
            test_object.full_clean()
        self.assertTrue('only capital alphabets [A-Z] are allowed' in str(context.exception))

    def test_no_more_than_three_characters_allowed_for_a_lender_code(self):
        with self.assertRaises(DataError) as context:
            test_object = Lender.objects.create(name='Blah',
                                                code='TAFF',
                                                upfront_commission_rate=100,
                                                trial_commission_rate=200,
                                                active=False)
            test_object.full_clean()
        self.assertTrue('Data too long for column' in str(context.exception))

    def test_upfront_commission_rate_can_only_be_numerical(self):
        with self.assertRaises(ValueError) as context:
            test_object = Lender.objects.create(name='Blah',
                                            code='TAG',
                                            upfront_commission_rate='A',
                                            trial_commission_rate=10,
                                            active=False)
            test_object.full_clean()
        self.assertTrue('expected a number but got' in str(context.exception))

    def test_upfront_commission_rate_can_not_be_negative(self):
        with self.assertRaises(ValidationError) as context:
            test_object = Lender.objects.create(name='Blah',
                                            code='TAH',
                                            upfront_commission_rate=-0.1,
                                            trial_commission_rate=200,
                                            active=False)
            test_object.full_clean()
        self.assertTrue('Ensure this value is greater than or equal to 0.0' in str(context.exception))

    def test_upfront_commission_rate_can_be_zero(self):
        test_object = Lender.objects.create(name='Blah',
                                            code='TAI',
                                            upfront_commission_rate=0.0,
                                            trial_commission_rate=200,
                                            active=False)
        test_object.full_clean()
        self.assertEqual(test_object.upfront_commission_rate,0)

    def test_upfront_commission_rate_can_not_be_a_large_number(self):
        with self.assertRaises(ValidationError) as context:
            test_object = Lender.objects.create(name='Blah',
                                                code='TAJ',
                                                upfront_commission_rate=1000.0,
                                                trial_commission_rate=200,
                                                active=False)
            test_object.full_clean()
        self.assertTrue('Ensure this value is less than or equal to' in str(context.exception))

    def test_trial_commission_rate_can_only_be_numerical(self):
        with self.assertRaises(ValueError) as context:
            test_object = Lender.objects.create(name='Blah',
                                                code='TAK',
                                                upfront_commission_rate=10,
                                                trial_commission_rate='A',
                                                active=False)
            test_object.full_clean()
        self.assertTrue('expected a number but got' in str(context.exception))

    def test_trial_commission_rate_can_not_be_negative(self):
        with self.assertRaises(ValidationError) as context:
            test_object = Lender.objects.create(name='Blah',
                                            code='TAL',
                                            upfront_commission_rate=10,
                                            trial_commission_rate=-0.1,
                                            active=False)
            test_object.full_clean()
        self.assertTrue('Ensure this value is greater than or equal to 0.0' in str(context.exception))

    def test_trial_commission_rate_can_be_zero(self):
        test_object = Lender.objects.create(name='Blah',
                                            code='TAM',
                                            upfront_commission_rate=10,
                                            trial_commission_rate=0.0,
                                            active=False)
        test_object.full_clean()
        self.assertEqual(test_object.trial_commission_rate,0)

    def test_trial_commission_rate_can_not_be_a_large_number(self):
        with self.assertRaises(ValidationError) as context:
            test_object = Lender.objects.create(name='Blah',
                                                code='TAN',
                                                upfront_commission_rate=10,
                                                trial_commission_rate=1000,
                                                active=False)
            test_object.full_clean()
        self.assertTrue('Ensure this value is less than or equal to' in str(context.exception))

    def test_active_can_only_be_boolean(self):
        with self.assertRaises(ValidationError) as context:
            test_object = Lender.objects.create(name='Blah',
                                                code='TAO',
                                                upfront_commission_rate=10,
                                                trial_commission_rate=1000,
                                                active='A')
            test_object.full_clean()
        self.assertTrue('value must be either True or False' in str(context.exception))