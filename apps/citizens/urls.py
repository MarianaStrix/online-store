from django.urls import path

from .views import (CitizenUpdateView, ImportBirthdaysView, ImportCreateView,
                    ImportGetListView, ImportPercentileView)

app_name = 'citizens'
urlpatterns = [
    path('imports',
         ImportCreateView.as_view(),
         name='import_create',
         ),
    path('imports/<int:import_id>/citizens/<int:citizen_id>',
         CitizenUpdateView.as_view(),
         name='citizen_patch',
         ),
    path('imports/<int:pk>/citizens',
         ImportGetListView.as_view(),
         name='import_get',
         ),
    path('imports/<int:pk>/citizens/birthdays',
         ImportBirthdaysView.as_view(),
         name='import_birthdays',
         ),
    path('imports/<int:pk>/towns/stat/percentile/age',
         ImportPercentileView.as_view(),
         name='import_percentile',
         )
]
