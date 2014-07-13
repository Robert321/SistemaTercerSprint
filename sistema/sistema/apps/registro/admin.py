from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Estudiante)
admin.site.register(Docente)
admin.site.register(Carrera)
admin.site.register(Materia)
admin.site.register(Notas)
admin.site.register(rel_car_mat)
admin.site.register(rel_estudiante_carrera)
admin.site.register(rel_estudiante_materia)
admin.site.register(Document)
admin.site.register(rel_docente_carrera)
