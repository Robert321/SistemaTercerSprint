from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User


class CarreraForm(ModelForm):
	nombre	= forms.CharField(label="Nombre de Carrera",widget=forms.TextInput())
	direccion	= forms.CharField(label="La Direccion",widget=forms.TextInput())
	telefono	= forms.CharField(label="El Telefono",widget=forms.TextInput())
	class Meta:
		model=Carrera
		fields=["nombre","direccion","telefono"] 


class ContactForm(ModelForm):
	class Meta:
		model=Carrera
		fields=["nombre","direccion","telefono"] 


class LoginEstudianteForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput())
	password = forms.CharField(widget=forms.PasswordInput(render_value=False))










class LoginDocenteForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput())
	password = forms.CharField(widget=forms.PasswordInput(render_value=False))





class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput())
	password = forms.CharField(widget=forms.PasswordInput(render_value=False))


class RegistrarEstudiante(forms.Form):
	username=forms.CharField(widget=forms.TextInput())
	apellido=forms.CharField(widget=forms.TextInput())
	ci=forms.CharField(widget=forms.TextInput())
	email=forms.EmailField(widget=forms.EmailInput())

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			u = User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('Nombre de usuario ya existe')

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			u = User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('Email ya registrado')


class UserForm(forms.ModelForm):
	class Meta:
		model=User
		fields = ('username', 'first_name', 'last_name', 'email')


class Registro_Estudiante(forms.ModelForm):
	class Meta:
		model=Estudiante


class Registro_Docente(forms.ModelForm):
	class Meta:
		model=Docente



class RegistrarDocente(forms.Form):
	username=forms.CharField(widget=forms.TextInput())
	apellido=forms.CharField(widget=forms.TextInput())
	ci=forms.CharField(widget=forms.TextInput())
	email=forms.EmailField(widget=forms.EmailInput())

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			u = User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('Nombre de usuario ya existe')

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			u = User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('Email ya registrado')

class RegisterForm(forms.Form):
	username = forms.CharField(label="Nombre de Usuario",widget=forms.TextInput())
	email    = forms.EmailField(label="Correo Electronico",widget=forms.TextInput())
	password_one = forms.CharField(label="Password",widget=forms.PasswordInput(render_value=False))
	password_two = forms.CharField(label="Confirmar password",widget=forms.PasswordInput(render_value=False))

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			u = User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('Nombre de usuario ya existe')

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			u = User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('Email ya registrado')

	def clean_password_two(self):
		password_one = self.cleaned_data['password_one']
		password_two = self.cleaned_data['password_two']
		if password_one == password_two:
			pass
		else:
			raise forms.ValidationError('Password no coinciden')

class RegistrarMateria(forms.ModelForm):
	class Meta():
		model=Materia
		fields=["nombre","sigla","nivel","descripcion","notamin","notamax","notamindeaprovacion"] 


class RegistrarNotas(forms.ModelForm):
	class Meta():
		model=Notas
		fields=["poderacionparcial","poderacionpracticas","poderacionlaboratorio","poderacionexamenfinal","primerparcial","segundoparcial","tercerparcial","practicas","laboratorio","examenfinal","notafinal","id_Mat"]


class RegistrarRelCarMat(forms.ModelForm):
	class Meta():
		model=rel_car_mat
		fields=["id_Car","id_Mat"]


class RegistrarRelEstCar(forms.ModelForm):
	class Meta():
		model=rel_estudiante_carrera
		fields=["idCarrera"]

class RegistrarRelEstMat(forms.ModelForm):
	class Meta():
		model=rel_estudiante_materia
		fields=["idEstudiante","idMateria"]


class AutorForm(ModelForm):
	class Meta:
		model=Autor
		fields=["nombre","apellido_pat","apellido_mat"] 

class DocumentForm(ModelForm):
	class Meta:
		model=Document
		fields=["nombre","imagen","docfile","autor"] 


class RegistrarRelCarDoc(forms.ModelForm):
	class Meta():
		model=rel_docente_carrera
		fields=["idCarrera","idDocente"]
class RegistrarRelDocMat(forms.ModelForm):
	class Meta():
		model=rel_docente_materia
		fields=["idDocente","idMateria"]