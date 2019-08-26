from django.contrib import admin

from .models import Citizen, Import, Relationship


class RelationshipInline(admin.StackedInline):
    model = Relationship
    fk_name = 'to_citizen'


class CitizenAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]


admin.site.register(Citizen, CitizenAdmin)
admin.site.register(Import)
