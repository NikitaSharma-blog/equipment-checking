from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from api.forms import UserCreationForm

# Register your models here.

class UsersAdmin(UserAdmin):
    add_form = UserCreationForm
    list_display = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'employee_supervisor', 'roles', 'device_token')}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'name', 'employee_supervisor', 'roles', 'device_token', 'is_superuser', 'is_staff', 'is_active')}
            ),
        )

    filter_horizontal = ()

class EquipmentsAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')

class SelectedEquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id')


admin.site.register(Equipments, EquipmentsAdmin)
admin.site.register(User, UsersAdmin)
admin.site.register(SelectedEquipments, SelectedEquipmentAdmin)