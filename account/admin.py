from django.contrib import admin

from .models import Relation


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'datetime_created',]
    raw_id_fields = ['from_user', 'to_user',]