from django.contrib import admin

# core/admin.py
from base.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'birthday', 'rg', 'cpf')
    search_fields = (
        'user__first_name',
        'user__last_name',
        'user__email',
        'birthday',
        'rg',
        'cpf'
    )