from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm



class Estudiante(models.Model):
	username=models.OneToOneField(User, unique=True, related_name='estudiante')
	nombre=models.CharField(max_length=150)
	apellido=models.CharField(max_length=150)
	ci=models.CharField(max_length=20)
	email=models.EmailField()
	password=models.CharField(max_length=150)
	def __unicode__(self):
		return self.user.username




class Docente(models.Model):
	username=models.OneToOneField(User, unique=True, related_name='docente')
	nombre=models.CharField(max_length=150)
	apellido=models.CharField(max_length=150)
	ci=models.CharField(max_length=20)
	email=models.EmailField()
	password=models.CharField(max_length=150)
	def __unicode__(self):
		return	self.user.username


#carrera
class Carrera(models.Model):
	nombre=models.CharField(max_length=200)
	direccion=models.CharField(max_length=200)
	telefono=models.CharField(max_length=200)
	def __unicode__(self):
		return self.nombre


class Materia(models.Model):
	nombre=models.CharField(max_length=150)
	sigla=models.CharField(max_length=150)
	nivel=models.IntegerField()
	descripcion=models.TextField()
	notamin=models.IntegerField()
	notamax=models.IntegerField()
	notamindeaprovacion=models.IntegerField()
	class meta:
		ordering=['nombre',]

	def __str__(self):
		return self.nombre

class Notas(models.Model):
	poderacionparcial=models.IntegerField(default=0)
	poderacionpracticas=models.IntegerField(default=0)
	poderacionlaboratorio=models.IntegerField(default=0)
	poderacionexamenfinal=models.IntegerField(default=0)
	primerparcial=models.IntegerField(default=0)
	segundoparcial=models.IntegerField(default=0)
	tercerparcial=models.IntegerField(default=0)
	practicas=models.IntegerField(default=0)
	laboratorio=models.IntegerField(default=0)
	examenfinal=models.IntegerField(default=0)
	notafinal=models.IntegerField(default=0)
	id_Mat=models.ForeignKey(Materia)	
	def __unicode__(self):
		return self.id_Mat



class rel_car_mat(models.Model):
	id_Car =models.ForeignKey(Carrera)
	id_Mat =models.ForeignKey(Materia)
	def __unicode__(self):
		return"%s %s"%(self.id_Car.nombre,self.id_Mat.sigla)



class rel_estudiante_carrera(models.Model):
	idCarrera=models.ForeignKey(Carrera)
	idEstudiante=models.ForeignKey(Estudiante)
	def __unicode__(self):
		return"%s %s"%(self.idCarrera.nombre,self.idEstudiante.email)


class rel_estudiante_materia(models.Model):
	idEstudiante=models.ForeignKey(Estudiante)
	idMateria=models.ForeignKey(Materia)
	def __unicode__(self):
		return"%s %s"%(self.idEstudiante.email,self.idMateria.sigla)


class rel_docente_carrera(models.Model):
	idCarrera=models.ForeignKey(Carrera)
	idDocente=models.ForeignKey(Docente)
	def __unicode__(self):
		return"%s %s"%(self.idCarrera.nombre,self.idDocente.email)


class rel_docente_materia(models.Model):
	idDocente=models.ForeignKey(Docente)
	idMateria=models.ForeignKey(Materia)
	def __unicode__(self):
		return"%s %s"%(self.idDocente.email,self.idMateria.sigla)


class Autor(models.Model):
	nombre = models.CharField(max_length=200)
	apellido_pat = models.CharField(max_length=200)
	apellido_mat = models.CharField(max_length=200)
	def __unicode__(self):
		return"%s %s %s"%(self.nombre,self.apellido_pat,self.apellido_mat)


class Document(models.Model):
	nombre=models.CharField(max_length=200)
	imagen=models.FileField(upload_to='imagenes/%Y/%m/%d')
	docfile = models.FileField(upload_to='documents/%Y/%m/%d')
	autor=models.ForeignKey(Autor)
	def __unicode__(self):
		return self.nombre


