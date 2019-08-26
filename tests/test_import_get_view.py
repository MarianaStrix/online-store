from django.urls import reverse

import pytest

from apps.citizens.functions import get_combined_id
from apps.citizens.models import Citizen, Import


pytestmark = pytest.mark.django_db


class TestImport:

    def get_url(self, import_pk):
        return reverse(
            'citizens:import_get',
            kwargs={'pk': import_pk}
        )

    @pytest.fixture(autouse=True)
    def setup(self,):
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

    def test_import_get_valid(self, api_client):
        import_id = Import.objects.get().pk
        response = api_client.get(self.get_url(import_id))
        assert response.status_code == 200, response.content

    def test_import_get_import_id_not_exist(self, api_client):
        import_id = Import.objects.get().pk+1
        response = api_client.get(self.get_url(import_id))
        assert response.status_code == 404, response.content

    def test_import_get_valid_data(self, api_client, testing_general_data):
        import_id = Import.objects.get().pk
        response = api_client.get(self.get_url(import_id))
        expected_data = {'data': testing_general_data['citizens']}
        assert set(
            [citizen['citizen_id'] for citizen in expected_data['data']]
        ) == set(
            [citizen['citizen_id'] for citizen in response.json()['data']]
        )
        for response_citizen in response.json()['data']:
            for citizen in expected_data['data']:
                if response_citizen['citizen_id'] == citizen['citizen_id']:
                    if response_citizen != citizen:
                        assert set(response_citizen['relatives']) == set(citizen['relatives'])
