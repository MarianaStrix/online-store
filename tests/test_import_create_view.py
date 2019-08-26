from django.urls import reverse

import pytest

from apps.citizens.models import Import

pytestmark = pytest.mark.django_db


class TestImport:
    url = reverse('citizens:import_create')

    def make_test(self, api_client, data, expected_status):
        response = api_client.post(self.url, data=data)
        assert response.status_code == expected_status, response.content

    def test_import_create_valid_data(self, api_client, testing_general_data):
        self.make_test(api_client, testing_general_data, 201)

    def test_import_create_citizen_id_not_unique(self, api_client, testing_create_data_2):
        self.make_test(api_client, testing_create_data_2, 400)

    def test_import_create_citizen_id_not_valid_type(self, api_client, testing_create_data_3):
        self.make_test(api_client, testing_create_data_3, 400)

    def test_import_create_citizen_id_not_valid_integer(self, api_client, testing_create_data_4):
        self.make_test(api_client, testing_create_data_4, 400)

    def test_import_create_citizen_id_empty(self, api_client, testing_create_data_5):
        self.make_test(api_client, testing_create_data_5, 400)

    def test_import_create_town_not_valid_type_data(self, api_client, testing_create_data_6):
        self.make_test(api_client, testing_create_data_6, 400)

    def test_import_create_town_not_valid_len(self, api_client, testing_create_data_7):
        self.make_test(api_client, testing_create_data_7, 400)

    def test_import_create_town_empty(self, api_client, testing_create_data_8):
        self.make_test(api_client, testing_create_data_8, 400)

    def test_import_create_street_not_valid_type_data(self, api_client, testing_create_data_9):
        self.make_test(api_client, testing_create_data_9, 400)

    def test_import_create_street_not_valid_len(self, api_client, testing_create_data_10):
        self.make_test(api_client, testing_create_data_10, 400)

    def test_import_create_street_empty(self, api_client, testing_create_data_11):
        self.make_test(api_client, testing_create_data_11, 400)

    def test_import_create_building_not_valid_data(self, api_client, testing_create_data_12):
        self.make_test(api_client, testing_create_data_12, 400)

    def test_import_create_building_not_valid_len(self, api_client, testing_create_data_13):
        self.make_test(api_client, testing_create_data_13, 400)

    def test_import_create_building_empty(self, api_client, testing_create_data_14):
        self.make_test(api_client, testing_create_data_14, 400)

    def test_import_create_apartment_not_valid_type(self, api_client, testing_create_data_15):
        self.make_test(api_client, testing_create_data_15, 400)

    def test_import_create_apartment_not_valid_integer(self, api_client, testing_create_data_16):
        self.make_test(api_client, testing_create_data_16, 400)

    def test_import_create_apartment_empty(self, api_client, testing_create_data_17):
        self.make_test(api_client, testing_create_data_17, 400)

    def test_import_create_name_empty(self, api_client, testing_create_data_18):
        self.make_test(api_client, testing_create_data_18, 400)

    def test_import_create_name_not_valid_len(self, api_client, testing_create_data_19):
        self.make_test(api_client, testing_create_data_19, 400)

    def test_import_create_birth_date_not_valid_format(self, api_client, testing_create_data_20):
        self.make_test(api_client, testing_create_data_20, 400)

    def test_import_create_birth_date_not_valid_date(self, api_client, testing_create_data_21):
        self.make_test(api_client, testing_create_data_21, 400)

    def test_import_create_birthday_future_date(self, api_client, testing_create_data_22):
        self.make_test(api_client, testing_create_data_22, 400)

    def test_import_create_birthday_empty(self, api_client, testing_create_data_23):
        self.make_test(api_client, testing_create_data_23, 400)

    def test_import_create_gender_not_valid_data(self, api_client, testing_create_data_24):
        self.make_test(api_client, testing_create_data_24, 400)

    def test_import_create_gender_empty(self, api_client, testing_create_data_25):
        self.make_test(api_client, testing_create_data_25, 400)

    def test_import_create_relation_not_valid(self, api_client, testing_create_data_26):
        self.make_test(api_client, testing_create_data_26, 400)

    def test_import_create_relation_not_exist_citizen_id(self, api_client, testing_create_data_27):
        self.make_test(api_client, testing_create_data_27, 400)

    def test_import_create_relation_with_oneself(self, api_client, testing_create_data_28):
        self.make_test(api_client, testing_create_data_28, 201)

    def test_import_create_relation_empty(self, api_client, testing_create_data_29):
        self.make_test(api_client, testing_create_data_29, 201)

    def test_import_create_additional_fields(self, api_client, testing_create_data_30):
        self.make_test(api_client, testing_create_data_30, 400)

    def test_import_create_no_fields(self, api_client, testing_create_data_31):
        self.make_test(api_client, testing_create_data_31, 400)

    def test_import_create_empty_citizens_list(self, api_client, testing_create_data_32):
        start = Import.objects.all()
        self.make_test(api_client, testing_create_data_32, 400)
        end = Import.objects.all()
        assert start != end, 'The number of Imports in the database has changed'

    def test_import_create_empty_data(self, api_client, testing_create_data_33):
        start = Import.objects.all()
        self.make_test(api_client, testing_create_data_33, 400)
        end = Import.objects.all()
        assert start != end, 'The number of Imports in the database has changed'

    def test_import_create_big_data(self, api_client, testing_big_date):
        self.make_test(api_client, testing_big_date, 201)

    def test_import_create_not_unique_relatives(self, api_client, testing_create_data_34):
        self.make_test(api_client, testing_create_data_34, 400)
