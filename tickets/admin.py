from django.contrib import admin
from .models import Ticket, Area, Problem


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
	list_display = ('name', 'area')
	list_filter = ('area',)
	search_fields = ('name',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
	list_display = ('problem', 'created_by', 'district', 'status', 'created_at')
	list_filter = ('district', 'status', 'created_at')
	search_fields = ('problem__name', 'address', 'created_by__email')
