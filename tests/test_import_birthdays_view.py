from django.urls import reverse

import pytest

from apps.citizens.functions import get_combined_id
from apps.citizens.models import Citizen, Import


pytestmark = pytest.mark.django_db


class TestImport:

    @pytest.fixture(autouse=True)
    def setup(self):
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
            birth_date='1984-11-23', gender='female',
            import_id_id=import_obj.pk, id=get_combined_id(import_obj.pk, 3)
        )
        citizen_4 = Citizen.objects.create(
            citizen_id=4, town='Керчь', street='Иосифа Бродского', building='2',
            apartment=11, name='Романов Николай Сергеевич',
            birth_date='1988-12-23', gender='male',
            import_id_id=import_obj.pk, id=get_combined_id(import_obj.pk, 4)
        )
        citizen_5 = Citizen.objects.create(
            citizen_id=5, town='Красноярск', street='проспект Мира', building='92',
            apartment=568, name='Смирнов Вячеслав Анатольевич',
            birth_date='1990-01-06', gender='male',
            import_id_id=import_obj.pk, id=get_combined_id(import_obj.pk, 5)
        )
        citizen_6 = Citizen.objects.create(
            citizen_id=6, town='Красноярск', street='проспект Мира', building='92',
            apartment=564, name='Стасенко Александр Васильевич',
            birth_date='1992-04-23', gender='male',
            import_id_id=import_obj.pk, id=get_combined_id(import_obj.pk, 6)
        )
        Citizen.objects.create(
            citizen_id=7, town='Владивосток', street='Набережная', building='1',
            apartment=9, name='Петров Иван Игоревич',
            birth_date='1999-03-31', gender='male',
            import_id_id=import_obj.pk, id=get_combined_id(import_obj.pk, 7)
        )
        citizen_1.relatives.add(citizen_2)
        citizen_1.relatives.add(citizen_3)
        citizen_2.relatives.add(citizen_1)
        citizen_3.relatives.add(citizen_1)
        citizen_3.relatives.add(citizen_4)
        citizen_4.relatives.add(citizen_3)
        citizen_5.relatives.add(citizen_6)
        citizen_6.relatives.add(citizen_5)

    def test_import_birthdays_valid(self, api_client):
        url = reverse(
            'citizens:import_birthdays',
            kwargs={'pk': Import.objects.get().pk},
        )
        response = api_client.get(url)
        assert response.status_code == 200, response.content

    def test_import_birthdays_valid_get(self, api_client):
        url = reverse(
            'citizens:import_birthdays',
            kwargs={'pk': Import.objects.get().pk},
        )
        response = api_client.get(url)
        assert response.json() == {
            "data": {
                "1": [{"citizen_id": 6, "presents": 1}],
                "2": [],
                "3": [],
                "4": [
                    {"citizen_id": 1, "presents": 1},
                    {"citizen_id": 5, "presents": 1}
                ],
                "5": [],
                "6": [],
                "7": [],
                "8": [],
                "9": [],
                "10": [],
                "11": [
                    {"citizen_id": 1, "presents": 1},
                    {"citizen_id": 4, "presents": 1}
                ],
                "12": [
                    {"citizen_id": 2, "presents": 1},
                    {"citizen_id": 3, "presents": 2
                     }
                ]
            }
        }

    def test_import_birthdays_import_id_not_exist(self, api_client):
        url = reverse(
            'citizens:import_birthdays',
            kwargs={'pk': Import.objects.get().pk+1}
        )
        response = api_client.get(url)
        assert response.status_code == 404, response.content
