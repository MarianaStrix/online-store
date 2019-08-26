from itertools import groupby
import collections

from django.db.models import Count
from django.db.models.expressions import RawSQL
from django.db.transaction import atomic

from rest_framework import generics, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from numpy import percentile

from .functions import get_combined_id
from .models import Import, Citizen, Relationship
from .serializers import (CitizenCreateSerializers, CitizenUpdateSerializers,
                          CitizenGetListSerializers)


class ImportCreateView(generics.CreateAPIView):
    """
    Create a new import
    """
    serializer_class = CitizenCreateSerializers

    @staticmethod
    def valid_relatives(serializer):
        data = {}
        for citizen in serializer.validated_data:
            relatives = citizen.pop('relatives', ())
            citizen_id = citizen['citizen_id']
            import_id = citizen['import_id_id']
            data[get_combined_id(import_id, citizen_id)] = relatives

        for citizen_id, relatives in data.items():
            for relation in relatives:
                if relation not in data or citizen_id not in data[relation]:
                    raise ValidationError(
                        detail={'detail': 'Relationships are incorrect'}
                    )

    def pre_validate_unique_citizen_ids(self):
        """
        To avoid Import creation in some obvious cases.
        """
        citizens = self.request.data.get('citizens')
        if citizens is not None:
            if citizens in ([], [{}]):
                raise ValidationError(
                    detail={'detail': 'Citizens are empty'}
                )
            else:
                list_ids = [citizen['citizen_id'] for citizen in citizens]
                if len(set(list_ids)) != len(list_ids):
                    raise ValidationError(
                        detail={'detail': 'Citizen_id are not unique'}
                    )

    @atomic
    def create(self, request, *args, **kwargs):
        self.pre_validate_unique_citizen_ids()
        import_obj = Import.objects.create()
        serializer = self.get_serializer(
            data=request.data.get('citizens'),
            many=True,
        )
        serializer.context['import_id'] = import_obj.pk
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        self.valid_relatives(serializer)
        return Response(
            {'data': {'import_id': import_obj.pk}},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class CitizenUpdateView(mixins.UpdateModelMixin,
                        generics.GenericAPIView):
    serializer_class = CitizenUpdateSerializers

    @staticmethod
    def create_or_delete_relatives(new_relatives, old_relatives, citizen_id):
        set_new_relatives = set(new_relatives)

        # Checking for the existence
        # of all Citizen from new_relatives
        if Citizen.objects.filter(
                id__in=set_new_relatives
        ).count() != len(set_new_relatives):
            raise ValidationError(
                detail={'detail': 'Relationships are incorrect'}
            )

        set_old_relatives = set(old_relatives)
        add_relatives = set_new_relatives.difference(set_old_relatives)
        delete_relatives = set_old_relatives.difference(set_new_relatives)

        Relationship.objects.bulk_create(
            Relationship(
                from_citizen_id=new_relation,
                to_citizen_id=citizen_id,
            ) for new_relation in add_relatives
        )
        Relationship.objects.filter(
            from_citizen_id__in=delete_relatives,
            to_citizen_id=citizen_id,
        ).delete()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['import_id'] = self.kwargs.get('import_id')
        context['citizen_id'] = self.kwargs.get('citizen_id')
        return context

    @atomic
    def perform_update(self, serializer):
        """
        If the field came relatives then it is necessary
        to update new and old relatives
        """
        if 'relatives' in self.request.data:
            old_relation = serializer.instance.relatives.values_list('pk', flat=True,)
            new_relation = serializer.validated_data['relatives']
            self.create_or_delete_relatives(
                new_relation, old_relation,
                serializer.validated_data['id'],
            )

        serializer.save()

    def get_object(self):
        return get_object_or_404(Citizen.objects.filter(
            import_id=self.kwargs['import_id'],
            citizen_id=self.kwargs['citizen_id'],
        ))

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ImportGetListView(generics.ListAPIView):
    """
    Returns a list of citizens in an import
    """
    serializer_class = CitizenGetListSerializers

    def get_queryset(self):
        import_obj = get_object_or_404(
            Import.objects.all(), import_id=self.kwargs['pk'],
        )
        return import_obj.citizens.prefetch_related('relatives')


class ImportBirthdaysView(generics.GenericAPIView):
    queryset = Import.objects.all()

    def get(self, request, *args, **kwargs):
        import_obj = self.get_object()
        list_citizen = import_obj.citizens.all()
        data = list_citizen.annotate(
            presents=Count('relatives__pk'),
        ).values('citizen_id', 'relatives__birth_date__month', 'presents', )
        grouped_data = groupby(data, key=lambda x: x.pop('relatives__birth_date__month'))
        data = collections.defaultdict(list)
        [data[key].extend(group) for key, group in grouped_data]
        response_data = {month: data.get(month, []) for month in range(1, 13)}
        return Response(data={'data': response_data})


class ImportPercentileView(generics.GenericAPIView):
    queryset = Import.objects.all()

    @staticmethod
    def count_percentile_city(city_and_age):
        data = []
        for city, age in city_and_age.items():
            percentiles = percentile(age, (50, 75, 99), interpolation='linear')
            data.append({
                'town': city,
                'p50': round(percentiles[0], 2),
                'p75': round(percentiles[1], 2),
                'p99': round(percentiles[2], 2),
            })
        return data

    def get(self, request, *args, **kwargs):
        import_obj = self.get_object()
        list_citizen = import_obj.citizens.all()
        queryset = list_citizen.annotate(
            age=RawSQL('EXTRACT(year FROM AGE(birth_date))', [])
        ).order_by(
            'town',  # because of itertools.groupby() implementation
        ).values('town', 'age')

        grouped_data = groupby(queryset, key=lambda x: x.pop('town'))
        data = {
            key: [age['age'] for age in group] for key, group in grouped_data
        }
        response_data = self.count_percentile_city(data)
        return Response(data={'data': response_data})
