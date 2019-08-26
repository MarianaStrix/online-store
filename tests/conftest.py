import pytest
from rest_framework.test import APIClient

from .big_data import big_data


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def testing_general_data():
    return dict(
        citizens=
        [
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [2, 3]
            },
            {
                "citizen_id": 2,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Сергей Иванович",
                "birth_date": "17.04.1997",
                "gender": "male",
                "relatives": [1]
            },
            {
                "citizen_id": 3,
                "town": "Керчь",
                "street": "Иосифа Бродского",
                "building": "2",
                "apartment": 11,
                "name": "Романова Мария Леонидовна",
                "birth_date": "23.11.1986",
                "gender": "female",
                "relatives": [1]
            },
        ],
    )


@pytest.fixture
def testing_update_data_2():
    return dict(
        town="Санкт-Петербург",
        street="Пушкинская",
        building="18",
        apartment=79,
        name="Сергеев Никита Иванович",
        birth_date="17.04.1998",
        gender="male",
        relatives=[1, 3]
    )


@pytest.fixture
def testing_update_data_3():
    return dict(
        citizen_id=4
    )


@pytest.fixture
def testing_update_data_4():
    return dict(
        town=" - "
    )


@pytest.fixture
def testing_update_data_5():
    return dict(
        town="Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean "
             "commodo ligula eget dolor. Aenean massa. Cum sociis natoque "
             "penatibus et magnis dis parturient montes, nascetur ridiculus "
             "mus. Donec quam felis, ultricies nec, pellentesque eu, pretium "
             "quis, sem."
    )


@pytest.fixture
def testing_update_data_6():
    return dict(
        town=""
    )


@pytest.fixture
def testing_update_data_7():
    return dict(
        street="_"
    )


@pytest.fixture
def testing_update_data_8():
    return dict(
        street="Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean "
               "commodo ligula eget dolor. Aenean massa. Cum sociis natoque "
               "penatibus et magnis dis parturient montes, nascetur ridiculus "
               "mus. Donec quam felis, ultricies nec, pellentesque eu, pretium "
               "quis, sem."
    )


@pytest.fixture
def testing_update_data_9():
    return dict(
        street="-*"
    )


@pytest.fixture
def testing_update_data_10():
    return dict(
        building=" / "
    )


@pytest.fixture
def testing_update_data_11():
    return dict(
        building="Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean "
                 "commodo ligula eget dolor. Aenean massa. Cum sociis natoque "
                 "penatibus et magnis dis parturient montes, nascetur ridiculus "
                 "mus. Donec quam felis, ultricies nec, pellentesque eu, pretium "
                 "quis, sem."
    )


@pytest.fixture
def testing_update_data_12():
    return dict(
        building=""
    )


@pytest.fixture
def testing_update_data_13():
    return dict(
        apartment="lkv-"
    )


@pytest.fixture
def testing_update_data_14():
    return dict(
        apartment=-8
    )


@pytest.fixture
def testing_update_data_15():
    return dict(
        apartment=""
    )


@pytest.fixture
def testing_update_data_16():
    return dict(
        name="Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean "
             "commodo ligula eget dolor. Aenean massa. Cum sociis natoque "
             "penatibus et magnis dis parturient montes, nascetur ridiculus "
             "mus. Donec quam felis, ultricies nec, pellentesque eu, pretium "
             "quis, sem."
    )


@pytest.fixture
def testing_update_data_17():
    return dict(
        name="   "
    )


@pytest.fixture
def testing_update_data_18():
    return dict(
        birth_date="1997.12.12"
    )


@pytest.fixture
def testing_update_data_19():
    return dict(
        birth_date="32.09.1997"
    )


@pytest.fixture
def testing_update_data_20():
    return dict(
        birth_date="04.12.2030"
    )


@pytest.fixture
def testing_update_data_21():
    return dict(
        birth_date=""
    )


@pytest.fixture
def testing_update_data_22():
    return dict(
        gender="мужской"
    )


@pytest.fixture
def testing_update_data_23():
    return dict(
        gender=""
    )


@pytest.fixture
def testing_update_data_24():
    return dict(
        relatives=[1, 3]
    )


@pytest.fixture
def testing_update_data_25():
    return dict(
        relatives={1: '2', 3: 4}
    )


@pytest.fixture
def testing_update_data_26():
    return dict(
        relatives=[4]
    )


@pytest.fixture
def testing_update_data_27():
    return dict(
        auto='Ford'
    )


@pytest.fixture
def testing_update_data_28():
    return dict(
    )


@pytest.fixture
def testing_update_data_29():
    return dict(
        relatives=[1, 1]
    )


@pytest.fixture
def testing_create_data_2():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [1]
            },
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Сергей Иванович",
                "birth_date": "17.04.1997",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_3():
    return dict(
        citizens=[
            {
                "citizen_id": "kjvf",
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_4():
    return dict(
        citizens=[
            {
                "citizen_id": 0,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_5():
    return dict(
        citizens=[
            {
                "citizen_id": "",
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_6():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "{}",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_7():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean "
                        "commodo ligula eget dolor. Aenean massa. Cum sociis natoque "
                        "penatibus et magnis dis parturient montes, nascetur ridiculus "
                        "mus. Donec quam felis, ultricies nec, pellentesque eu, pretium "
                        "quis, sem.",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_8():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_9():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "-#",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_10():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean "
                          "commodo ligula eget dolor. Aenean massa. Cum sociis natoque "
                          "penatibus et magnis dis parturient montes, nascetur ridiculus "
                          "mus. Donec quam felis, ultricies nec, pellentesque eu, pretium "
                          "quis, sem.",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_11():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_12():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "- ",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_13():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean "
                            "commodo ligula eget dolor. Aenean massa. Cum sociis natoque "
                            "penatibus et magnis dis parturient montes, nascetur ridiculus "
                            "mus. Donec quam felis, ultricies nec, pellentesque eu, pretium "
                            "quis, sem.",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_14():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_15():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": "jhhj",
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_16():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": -8,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_17():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": "",
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_18():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_19():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean "
                        "commodo ligula eget dolor. Aenean massa. Cum sociis natoque "
                        "penatibus et magnis dis parturient montes, nascetur ridiculus "
                        "mus. Donec quam felis, ultricies nec, pellentesque eu, pretium "
                        "quis, sem.",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_20():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "1986.04.30",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_21():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "30.02.1986",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_22():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.2030",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_23():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_24():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "30.01.1986",
                "gender": "мужской",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_25():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "30.01.1986",
                "gender": "",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_26():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [2]
            },
            {
                "citizen_id": 2,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Сергей Иванович",
                "birth_date": "17.04.1997",
                "gender": "male",
                "relatives": []
            }
        ]
    )


@pytest.fixture
def testing_create_data_27():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [2]
            }
        ]
    )


@pytest.fixture
def testing_create_data_28():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [1]
            }
        ]
    )

@pytest.fixture
def testing_create_data_29():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": []
            }
        ]
    )

@pytest.fixture
def testing_create_data_30():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "auto": "yes",
                "relatives": [1]
            }
        ]
    )


@pytest.fixture
def testing_create_data_31():
    return dict(
        citizens=[
            {
            }
        ]
    )


@pytest.fixture
def testing_create_data_32():
    return dict(
        citizens=[
        ]
    )


@pytest.fixture
def testing_create_data_33():
    return dict(
    )


@pytest.fixture
def testing_create_data_34():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [1, 1]
            }
        ]
    )


@pytest.fixture
def testing_birthdays_data():
    return dict(
        citizens=[
            {
                "citizen_id": 1,
                "town": "Lorem",
                "street": "Lorem",
                "building": "Lorem",
                "apartment": 7,
                "name": "Lorem",
                "birth_date": "26.1.1992",
                "gender": "male",
                "relatives": [2, 3]
            },
            {
                "citizen_id": 2,
                "town": "Lorem",
                "street": "Lorem",
                "building": "Lorem",
                "apartment": 7,
                "name": "Lorem",
                "birth_date": "26.2.1992",
                "gender": "male",
                "relatives": [1]
            },
            {
                "citizen_id": 3,
                "town": "Lorem",
                "street": "Lorem",
                "building": "Lorem",
                "apartment": 7,
                "name": "Lorem",
                "birth_date": "26.1.1992",
                "gender": "male",
                "relatives": [4, 1]
            },
            {
                "citizen_id": 4,
                "town": "Lorem",
                "street": "Lorem",
                "building": "Lorem",
                "apartment": 7,
                "name": "Lorem",
                "birth_date": "26.2.1992",
                "gender": "male",
                "relatives": [3]
            },
            {
                "citizen_id": 5,
                "town": "Lorem",
                "street": "Lorem",
                "building": "Lorem",
                "apartment": 7,
                "name": "Lorem",
                "birth_date": "26.5.1992",
                "gender": "male",
                "relatives": [6]
            },
            {
                "citizen_id": 6,
                "town": "Lorem",
                "street": "Lorem",
                "building": "Lorem",
                "apartment": 7,
                "name": "Lorem",
                "birth_date": "26.7.1992",
                "gender": "male",
                "relatives": [5]
            }
        ]
    )


@pytest.fixture
def testing_big_date():
    return dict(
        citizens=big_data()
    )
