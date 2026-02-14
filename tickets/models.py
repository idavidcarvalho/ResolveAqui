from django.db import models
from django.conf import settings


class Area(models.Model):
	name = models.CharField(max_length=120, unique=True)

	class Meta:
		verbose_name = 'Área'
		verbose_name_plural = 'Áreas'

	def __str__(self):
		return self.name


class Problem(models.Model):
	area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='problems')
	name = models.CharField(max_length=150)

	class Meta:
		unique_together = ('area', 'name')
		verbose_name = 'Problema'
		verbose_name_plural = 'Problemas'

	def __str__(self):
		return self.name


class Ticket(models.Model):
	DISTRICT_CHOICES = (
		('Pipa', 'Pipa'),
		('Tibau do Sul', 'Tibau do Sul'),
		('Sibaúma', 'Sibaúma'),
		('Pernambuquinho', 'Pernambuquinho'),
		('Cabeceiras', 'Cabeceiras'),
		('Munim', 'Munim'),
		('Manibú', 'Manibú'),
		('Bela Vista', 'Bela Vista'),
		('Piau', 'Piau'),
		('Umari', 'Umari'),
	)

	STATUS_CHOICES = (
		('Aberto', 'Aberto'),
		('Em andamento', 'Em andamento'),
		('Finalizado', 'Finalizado'),
	)

	problem = models.ForeignKey(Problem, on_delete=models.SET_NULL, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	photo = models.ImageField(upload_to='tickets/photos/', null=False, blank=False)
	district = models.CharField(max_length=32, choices=DISTRICT_CHOICES)
	address = models.CharField(max_length=300)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Aberto')
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		label = self.problem.name if self.problem else '(Sem problema pré-cadastrado)'
		return f"{label} — {self.district}"
