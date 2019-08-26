import datetime
import re

from django.conf import settings
from django.core.validators import RegexValidator

from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.serializers import ListSerializer

from .functions import get_combined_id
from .models import Citizen, Relationship


RE_ADDRESS_FIELD = re.compile(r"\b(?!_)[\w]+\b")


def valid_birth_date(value):
    if value >= datetime.date.today():
        raise serializers.ValidationError('Invalid birth date')


class BulkCreateListSerializer(ListSerializer):

    def get_instance(self, **attrs):
        relatives = attrs.pop('relatives', [])
        instance = Citizen(**attrs)
        relations = [
            Relationship(
                from_citizen_id=instance.id, to_citizen_id=item,
            ) for item in relatives
        ]
        return instance, relations

    def create(self, validated_data):
        citizens_bulk, relations_bulk = [], []
        for attrs in validated_data:
            instance, relations = self.get_instance(**attrs)
            citizens_bulk.append(instance)
            relations_bulk.extend(relations)
        result = Citizen.objects.bulk_create(citizens_bulk)
        Relationship.objects.bulk_create(relations_bulk)
        return result


class MainCitizenSerializers(serializers.ModelSerializer):
    citizen_id = serializers.IntegerField(
        min_value=1,
    )
    town = serializers.CharField(max_length=256, validators=[
        RegexValidator(
            regex=RE_ADDRESS_FIELD,
            message='Enter a valid town. Town must be at least 1 characters '
                    'long, also contain number or letter.',
        )], )
    street = serializers.CharField(max_length=256, validators=[
        RegexValidator(
            regex=RE_ADDRESS_FIELD,
            message='Enter a valid street. Street must be at least 1 '
                    'characters long, also contain number or letter.',
        )], )
    building = serializers.CharField(max_length=256, validators=[
        RegexValidator(
            regex=RE_ADDRESS_FIELD,
            message='Enter a valid building. Building must be at least 1 '
                    'characters long, also contain number or letter.',
        )], )
    apartment = serializers.IntegerField(
        min_value=1,
        required=True,
    )
    name = serializers.CharField(max_length=256, )
    birth_date = serializers.DateField(
        format='%d.%m.%Y',
        input_formats=settings.DATE_INPUT_FORMATS,
        validators=[valid_birth_date],
    )
    gender = serializers.ChoiceField(
        ['male', 'female'],
        required=True,
        error_messages={
            'invalid_choice': '"{input}" is not a valid choice. Possible '
                              'choices are male or female',
        }, )

    class Meta:
        model = Citizen
        fields = (
            'citizen_id', 'town', 'street', 'building', 'apartment',
            'name', 'birth_date', 'gender', 'relatives',
        )

    def validate_relatives(self, attrs):
        if len(set(attrs)) != len(attrs):
            raise serializers.ValidationError(
                detail={'detail': 'Relatives are not unique'}
            )
        return super().validate(attrs)


class CustomIDField(serializers.IntegerField):

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        return get_combined_id(self.context['import_id'], value)


class CitizenCreateSerializers(MainCitizenSerializers):
    relatives = serializers.ListField(child=CustomIDField())

    class Meta(MainCitizenSerializers.Meta):
        fields_set = set(MainCitizenSerializers.Meta.fields)
        list_serializer_class = BulkCreateListSerializer

    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        result['import_id_id'] = self.context['import_id']
        result['id'] = get_combined_id(
            self.context['import_id'],
            result['citizen_id']
        )
        return result

    def to_representation(self, data):
        return {}

    def run_validation(self, data=empty):
        if set(data.keys()) - self.Meta.fields_set:
            raise serializers.ValidationError(
                detail={'detail': 'Additional fields not allowed'}
            )
        return super().run_validation(data=data)


class CustomListField(serializers.ListField):

    def to_representation(self, value):
        """
        .all() allows us reuse prefetch_related cache and avoid additional
        DB queries, instead of .values_list('citizen_id')
        """
        return [item.citizen_id for item in value.instance.relatives.all()]


class CitizenUpdateSerializers(MainCitizenSerializers):
    citizen_id = serializers.IntegerField(read_only=True)
    relatives = CustomListField(child=CustomIDField())

    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        result['import_id_id'] = self.context['import_id']
        result['id'] = get_combined_id(
            self.context['import_id'],
            self.context['citizen_id']
        )
        return result

    def validate(self, attrs):
        attrs = super().validate(attrs)
        input_keys = set(self.initial_data.keys())
        if len(input_keys) == 0:
            raise serializers.ValidationError(
                detail={'detail': 'At least one field is specified'})

        # Check for excess field
        # Citizen_id is not trying to change
        if input_keys - (set(self.fields) - {'citizen_id'}):
            raise serializers.ValidationError(
                detail={'detail': 'Additional fields not allowed'}
            )

        return attrs


class RepresentDataListSerializer(ListSerializer):

    @property
    def data(self):
        return {'data': super().data}


class CitizenGetListSerializers(MainCitizenSerializers):
    relatives = CustomListField(child=serializers.IntegerField())

    class Meta(MainCitizenSerializers.Meta):
        list_serializer_class = RepresentDataListSerializer
