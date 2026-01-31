from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.html import format_html
from django import forms

from .models import User


class CustomUserChangeForm(forms.ModelForm):
	class Meta:
		model = User
		fields = '__all__'


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
	form = CustomUserChangeForm
	model = User
	list_display = ('email', 'firstName', 'lastName', 'typeUser', 'is_staff', 'profile_image_tag')
	list_filter = ('typeUser', 'is_staff', 'is_superuser')
	search_fields = ('email', 'firstName', 'lastName')
	ordering = ('email',)
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Pessoal', {'fields': ('firstName', 'lastName', 'profile_picture')}),
		('Permissões', {'fields': ('typeUser', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
		('Datas', {'fields': ('last_login',)}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'firstName', 'lastName', 'password1', 'password2'),
		}),
	)
	readonly_fields = ('profile_image_tag', 'last_login')

	def profile_image_tag(self, obj):
		if obj.profile_picture:
			return format_html('<img src="{}" style="max-height:60px; border-radius:6px;" />', obj.profile_picture.url)
		return '-'

	profile_image_tag.short_description = 'Foto'

	def get_readonly_fields(self, request, obj=None):
		ro = list(super().get_readonly_fields(request, obj))
		if not request.user.is_superuser:
			ro.append('typeUser')
		return ro
