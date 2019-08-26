from django.urls import reverse

import pytest

from apps.citizens.functions import get_combined_id
from apps.citizens.models import Citizen, Import

pytestmark = pytest.mark.django_db


class TestCitizen:

    def get_url(self, import_pk):
        return reverse(
            'citizens:citizen_patch',
            kwargs={'import_id': import_pk, 'citizen_id': 2}
        )

    @pytest.fixture(autouse=True)
    def setup(self, testing_general_data):
        import_obj = Import.objects.create()
        citizen_1 = Citizen.objects.create(
            citizen_id=1, town='Москва', street='Льва Толстого', building='16к7стр5',
            apartment=7, name='Иванов Иван Иванович',
            birth_date='1986-12-26', gender='male',
            import_id_id=import_obj.pk, id=get_combined_id(import_obj.pk, 1)
        )
        citizen_2 = Citizen.objects.create(
            citizen_id=2, town='Москва', street='Льва Толстого', building='16к7стр5',
            apartment=7, name='Иванов Сергей Иванович',
            birth_date='1997-04-17', gender='male',
            import_id_id=import_obj.pk, id=get_combined_id(import_obj.pk, 2)
        )
        citizen_3 = Citizen.objects.create(
            citizen_id=3, town='Керчь', street='Иосифа Бродского', building='2',
            apartment=11, name='Романова Мария Леонидовна',
            birth_date='1986-11-23', gender='female',
            import_id_id=import_obj.pk, id=get_combined_id(import_obj.pk, 3)
        )
        citizen_1.relatives.add(citizen_2)
        citizen_1.relatives.add(citizen_3)
        citizen_2.relatives.add(citizen_1)
        citizen_3.relatives.add(citizen_1)

    def make_test(self, api_client, data, expected_status):
        import_id = Import.objects.get().pk
        response = api_client.patch(self.get_url(import_id), data=data)
        assert response.status_code == expected_status, response.content
        return response

    def test_citizen_update_valid_data(self, api_client, testing_update_data_2):
        self.make_test(api_client, testing_update_data_2, 200)

    def test_citizen_update_valid_data_save(self, api_client, testing_update_data_2):
        response = self.make_test(api_client, testing_update_data_2, 200)
        for key in testing_update_data_2:
            if key != 'relatives':
                assert testing_update_data_2[key] == response.data[key], (
                    testing_update_data_2[key], response.data[key])
            else:
                assert set(testing_update_data_2[key]) == set(response.data[key]), (
                    testing_update_data_2[key], response.data[key]
                )

    def test_citizen_update_citizen_prohibition_of_change(self, api_client, testing_update_data_3):
        self.make_test(api_client, testing_update_data_3, 400)

    def test_citizen_update_town_not_valid_type_data(self, api_client, testing_update_data_4):
        self.make_test(api_client, testing_update_data_4, 400)

    def test_citizen_update_town_not_valid_len(self, api_client, testing_update_data_5):
        self.make_test(api_client, testing_update_data_5, 400)

    def test_citizen_update_town_empty(self, api_client, testing_update_data_6):
        self.make_test(api_client, testing_update_data_6, 400)

    def test_citizen_update_street_not_valid_type_data(self, api_client, testing_update_data_7):
        self.make_test(api_client, testing_update_data_7, 400)

    def test_citizen_update_street_not_valid_len(self, api_client, testing_update_data_8):
        self.make_test(api_client, testing_update_data_8, 400)

    def test_citizen_update_street_empty(self, api_client, testing_update_data_9):
        self.make_test(api_client, testing_update_data_9, 400)

    def test_citizen_update_building_not_valid_type_data(self, api_client, testing_update_data_10):
        self.make_test(api_client, testing_update_data_10, 400)

    def test_citizen_update_building_not_valid_len(self, api_client, testing_update_data_11):
        self.make_test(api_client, testing_update_data_11, 400)

    def test_citizen_update_building_empty(self, api_client, testing_update_data_12):
        self.make_test(api_client, testing_update_data_12, 400)

    def test_citizen_update_apartment_not_valid_type(self, api_client, testing_update_data_13):
        self.make_test(api_client, testing_update_data_13, 400)

    def test_citizen_update_apartment_not_valid_integer(self, api_client, testing_update_data_14):
        self.make_test(api_client, testing_update_data_14, 400)

    def test_citizen_update_apartment_empty(self, api_client, testing_update_data_15):
        self.make_test(api_client, testing_update_data_15, 400)

    def test_citizen_update_name_not_valid_len(self, api_client, testing_update_data_16):
        self.make_test(api_client, testing_update_data_16, 400)

    def test_citizen_update_name_empty(self, api_client, testing_update_data_17):
        self.make_test(api_client, testing_update_data_17, 400)

    def test_citizen_update_birth_date_not_valid_format(self, api_client, testing_update_data_18):
        self.make_test(api_client, testing_update_data_18, 400)

    def test_citizen_update_birth_date_not_valid_date(self, api_client, testing_update_data_19):
        self.make_test(api_client, testing_update_data_19, 400)

    def test_citizen_update_birth_date_future_date(self, api_client, testing_update_data_20):
        self.make_test(api_client, testing_update_data_20, 400)

    def test_citizen_update_birth_date_empty(self, api_client, testing_update_data_21):
        self.make_test(api_client, testing_update_data_21, 400)

    def test_citizen_update_gender_not_valid(self, api_client, testing_update_data_22):
        self.make_test(api_client, testing_update_data_22, 400)

    def test_citizen_update_gender_empty(self, api_client, testing_update_data_23):
        self.make_test(api_client, testing_update_data_23, 400)

    def test_citizen_update_two_way_relatives_valid(self, api_client, testing_update_data_24):
        response = self.make_test(api_client, testing_update_data_24, 200)
        import_id = Import.objects.get().pk
        list_citizen = Citizen.objects.filter(import_id=import_id)
        for citizen in list_citizen:
            if citizen.citizen_id in response.data['relatives']:
                assert 2 in [
                    relation.citizen_id for relation in citizen.relatives.all()
                ], (citizen.relatives.all())
            else:
                assert 2 not in [
                    relation.citizen_id for relation in citizen.relatives.all()
                ], (citizen.relatives.all())

    def test_citizen_update_relatives_not_valid_type(self, api_client, testing_update_data_25):
        self.make_test(api_client, testing_update_data_25, 400)

    def test_citizen_update_relatives_not_exist(self, api_client, testing_update_data_26):
        self.make_test(api_client, testing_update_data_26, 400)

    def test_citizen_update_nonexistent_field(self, api_client, testing_update_data_27):
        self.make_test(api_client, testing_update_data_27, 400)

    def test_citizen_update_empty_data(self, api_client, testing_update_data_28):
        self.make_test(api_client, testing_update_data_28, 400)

    def test_citizen_update_relatives_not_unique(self, api_client, testing_update_data_29):
        self.make_test(api_client, testing_update_data_29, 400)

    def test_citizen_update_update_of_nonexistent_citizen(self, api_client, testing_update_data_2):
        url = reverse(
            'citizens:citizen_patch',
            kwargs={'import_id': Import.objects.get().pk, 'citizen_id': 8}
        )
        response = api_client.patch(url, data=testing_update_data_2)
        assert response.status_code == 404, response.content

    def test_citizen_update_update_of_nonexistent_import(self, api_client, testing_update_data_2):
        url = reverse(
            'citizens:citizen_patch',
            kwargs={'import_id': Import.objects.get().pk+5, 'citizen_id': 8}
        )
        response = api_client.patch(url, data=testing_update_data_2)
        assert response.status_code == 404, response.content
