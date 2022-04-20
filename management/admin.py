from django.contrib import admin
from .models import EmployeeDocuments, Employee, Branch, Position
# Register your models here.


class EmployeeDocsAdmin(admin.StackedInline):
    model = EmployeeDocuments


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'position', 'status', 'phone_number')
    list_editable = ['status', 'position']
    inlines = [EmployeeDocsAdmin]


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('city', 'name', 'supervisor')


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('office', 'name')
