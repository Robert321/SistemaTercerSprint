from django.shortcuts import render,render_to_response,redirect
from django.template import RequestContext,loader
from django.views.generic import CreateView,TemplateView,ListView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login,logout,authenticate 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from sistema.settings import RUTA_PROYECTO
#from sistema.settings import URL_LOGIN
from .models import *
from .forms import *
import datetime
import MySQLdb
import os
from django.template.loader import render_to_string
from django.http import HttpResponse


# Create your views here.
def index_view(request):
	return render_to_response("index.html",{},RequestContext(request))


@login_required
def MenuEstudiante(request,id):
	idest=int(id)
	registro=Estudiante.objects.get(id=idest)
	return render_to_response("menuestudiante.html",{"dato":registro},RequestContext(request))

@login_required
def MenuDocente(request,id):
	iddoc=int(id)
	registro=Docente.objects.get(id=iddoc)
	return render_to_response("menudocente.html",{"dato":registro},RequestContext(request))


def login_view(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == "POST":
			form = LoginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				usuario = authenticate(username=username,password=password)
				if usuario is not None and usuario.is_active:
					login(request,usuario)
					return HttpResponseRedirect("/agregarcarrera/")
		form = LoginForm()
		ctx = {'form':form}
		return render_to_response('login.html',ctx,context_instance=RequestContext(request))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')


def register_view(request):
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			usuario = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password_one = form.cleaned_data['password_one']
			password_two = form.cleaned_data['password_two']
			u = User.objects.create_user(username=usuario,email=email,password=password_one)
			u.save() # Guardar el objeto
			return HttpResponse("Director Registrado")
		else:
			ctx = {'form':form}
			return 	render_to_response('register.html',ctx,context_instance=RequestContext(request))
	ctx = {'form':form}
	return render_to_response('register.html',ctx,context_instance=RequestContext(request))




import pdb
def login_view_Estudiante(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
	else:
		if request.method == "POST":
			form = LoginEstudianteForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				usuario = authenticate(username=username,password=password)
				if usuario is not None and usuario.is_active:
					login(request,usuario)
					e=Estudiante.objects.get(nombre=username,password=password)
					if e:
						elid=int(e.id)
						return HttpResponseRedirect("/menuestudiante/"+str(elid)+"/")
					else:
						return HttpResponse("mal los datos")
				
				else:
					return HttpResponse("Error datos")
		form = LoginEstudianteForm()
		ctx = {'form':form}
		return render_to_response('loginEstudiante.html',ctx,context_instance=RequestContext(request))
import pdb 


def addEstudiante(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
	else:
		formulario = RegistrarEstudiante()
		if request.method=="POST":
			formulario=RegistrarEstudiante(request.POST)
			if formulario.is_valid():
				username=formulario.cleaned_data["username"]
				apellido=formulario.cleaned_data["apellido"]
				ci=formulario.cleaned_data["ci"]
				email=formulario.cleaned_data["email"]
				password=formulario.cleaned_data["username"]+formulario.cleaned_data["ci"]
				u = User.objects.create_user(username=username,email=email,password=password)
				u.save()
				p=Estudiante(
					username=User.objects.get(username=username),
					nombre=User.objects.get(username=username),
					apellido=apellido,
					ci=ci,
					email=email,	
					password=formulario.cleaned_data["username"]+formulario.cleaned_data["ci"],		
					)	
				p.save()
				url=str(p.id)
				username = User.objects.get(username=username)
				password = password
				usuario = authenticate(username=username,password=password)
				if usuario is not None and usuario.is_active:
					login(request,usuario)
					e=Estudiante.objects.get(nombre=username,password=password)
					if e:
						elid=int(e.id)
						return HttpResponseRedirect("/menuestudiante/"+str(elid)+"/")
				#return HttpResponseRedirect("/menuestudiante/"+url+"/")
		else:
			formulario=RegistrarEstudiante()
		return render_to_response("estudiante.html",{"form":formulario},RequestContext(request))





#def programacion(request,id):
#	idcarrera=int(id)
#	carrera=Carrera.objects.get(id=idcarrera)
#	return HttpResponse("carrera")
import pdb
@login_required
def editar_estudiante(request, id):
	if request.method == 'POST':
        # formulario enviado
		user_form = UserForm(request.POST, instance=request.user)
		perfil_form = Registro_Estudiante(request.POST, instance=request.user.estudiante)
		if user_form.is_valid() and perfil_form.is_valid():
			# formulario validado correctamente
			user_form.save()
			perfil_form.save()
			return HttpResponse('guardado')
	else:
		# formulario inicial
		user_form = UserForm(instance=request.user)
		perfil_form = Registro_Estudiante(instance=request.user.estudiante)
	return render_to_response('modificarestudiante.html', { 'user_form': user_form,  'perfil_form': perfil_form }, context_instance=RequestContext(request))
@login_required
def addRelCarEst(request,id):
	elid=int(id)
    #consulta=Estudiante.objects.get(id=elid)
	if request.method=="POST":
		formulario=RegistrarRelEstCar(request.POST)
		if formulario.is_valid():
			p=rel_estudiante_carrera(
				idCarrera=formulario.cleaned_data["idCarrera"],
				idEstudiante=Estudiante.objects.get(pk=elid),
			)
			p.save()
			return HttpResponseRedirect("agregarrelcarest/"+str(elid)+"/")
	else:
		formulario=RegistrarRelEstCar()
	ctx={"form":formulario}
	return render_to_response("relestudiantecarrera.html",ctx,RequestContext(request))

@login_required
def addRelEstMat(request,id):
	elid=int(id)
	if request.method=="POST":
		formulario=RegistrarRelEstMat(request.POST)
		if formulario.is_valid():
			p=rel_estudiante_materia(
				idMateria=formulario.cleaned_data["idMateria"],
				idEstudiante=Estudiante.objects.get(pk=elid),
			)
			p.save()
			return HttpResponseRedirect("/agregarrelestmat/"+str(elid)+"/")
	else:
		formulario=RegistrarRelEstMat()
	ctx={"form":formulario}
	return render_to_response("relestudiantemateria.html",ctx,RequestContext(request))
@login_required
def programacion(request,id):
	idrel=int(id)
	registro=rel_estudiante_materia.objects.filter(idMateria__in=idrel)
	pdb.set_trace()
	return render_to_response("programacion.html",{"dato":registro},RequestContext(request))


@login_required
def logout_view_Estudiante(request):
	logout(request)
	return HttpResponseRedirect('/')



def login_view_Docente(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
	else:
		if request.method == "POST":
			form = LoginDocenteForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				usuario = authenticate(username=username,password=password)
				if usuario is not None and usuario.is_active:
					login(request,usuario)
					e=Docente.objects.get(nombre=username,password=password)
					if e:
						elid=int(e.id)
						return HttpResponseRedirect("/menudocente/"+str(elid)+"/")
					else:
						return HttpResponse("mal los datos")
				
				else:
					return HttpResponse("Error datos")
		form = LoginDocenteForm()
		ctx = {'form':form}
		return render_to_response('loginDocente.html',ctx,context_instance=RequestContext(request))

@login_required
def logout_view_Docente(request):
	logout(request)
	return HttpResponseRedirect('/')



def addDocente(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
	else:
		formulario = RegistrarDocente()
		if request.method=="POST":
			formulario=RegistrarDocente(request.POST)
			if formulario.is_valid():
				username=formulario.cleaned_data["username"]
				apellido=formulario.cleaned_data["apellido"]
				ci=formulario.cleaned_data["ci"]
				email=formulario.cleaned_data["email"]
				password=formulario.cleaned_data["username"]+formulario.cleaned_data["ci"]
				u = User.objects.create_user(username=username,email=email,password=password)
				u.save()
				p=Docente(
					username=User.objects.get(username=username),
					nombre=User.objects.get(username=username),
					apellido=apellido,
					ci=ci,
					email=email,	
					password=formulario.cleaned_data["username"]+formulario.cleaned_data["ci"],		
					)	
				p.save()
				url=str(p.id)
				username = User.objects.get(username=username)
				password = password
				usuario = authenticate(username=username,password=password)
				if usuario is not None and usuario.is_active:
					login(request,usuario)
					e=Docente.objects.get(nombre=username,password=password)
					if e:
						elid=int(e.id)
						return HttpResponseRedirect("/menudocente/"+str(elid)+"/")
				#return HttpResponseRedirect("/menuestudiante/"+url+"/")
		else:
			formulario=RegistrarDocente()
		return render_to_response("docente.html",{"form":formulario},RequestContext(request))




@login_required
def editar_docente(request, id):
	if request.method == 'POST':
        # formulario enviado
		user_form = UserForm(request.POST, instance=request.user)
		perfil_form = Registro_Docente(request.POST, instance=request.user.docente)
		if user_form.is_valid() and perfil_form.is_valid():
			# formulario validado correctamente
			user_form.save()
			perfil_form.save()
			return HttpResponse('guardado')
	else:
		# formulario inicial
		user_form = UserForm(instance=request.user)
		perfil_form = Registro_Docente(instance=request.user.docente)
	return render_to_response('modificardocente.html', { 'user_form': user_form,  'perfil_form': perfil_form }, context_instance=RequestContext(request))


def exito(request):
	return render_to_response("exito.html",{},RequestContext(request))


def addCarrera(request):
	if request.method == "POST":
		formulario = CarreraForm(request.POST)
		if formulario.is_valid():
			p=Carrera(
				nombre = formulario.cleaned_data["nombre"],
				direccion = formulario.cleaned_data["direccion"],
				telefono = formulario.cleaned_data["telefono"],
			)
			p.save()
			return HttpResponseRedirect("/agregarmateria/")
	else:
		formulario = CarreraForm()
	return render_to_response("carrera.html",{"form":formulario},RequestContext(request))



def addMateria(request):
	if request.method=="POST":
		formulario=RegistrarMateria(request.POST)
		if formulario.is_valid():
			p=Materia(
				nombre=formulario.cleaned_data["nombre"],
				sigla=formulario.cleaned_data["sigla"],
				nivel=formulario.cleaned_data["nivel"],
				descripcion=formulario.cleaned_data["descripcion"],
				notamin=formulario.cleaned_data["notamin"],
				notamax=formulario.cleaned_data["notamax"],
				notamindeaprovacion=formulario.cleaned_data["notamindeaprovacion"],
				)
			p.save()
			return HttpResponseRedirect("/agregarmateria/")
	else:
		formulario=RegistrarMateria()
	return render_to_response("materias.html",{"form":formulario},RequestContext(request))



def addNotas(request):
	if request.method=="POST":
		formulario=RegistrarNotas(request.POST)
		if formulario.is_valid():
			p=Notas(
				poderacionparcial=formulario.cleaned_data["poderacionparcial"],
				poderacionpracticas=formulario.cleaned_data["poderacionpracticas"],
				poderacionlaboratorio=formulario.cleaned_data["poderacionlaboratorio"],
				poderacionexamenfinal=formulario.cleaned_data["poderacionexamenfinal"],
				primerparcial=formulario.cleaned_data["primerparcial"],
				segundoparcial=formulario.cleaned_data["segundoparcial"],
				tercerparcial=formulario.cleaned_data["tercerparcial"],
				practicas=formulario.cleaned_data["practicas"],
				laboratorio=formulario.cleaned_data["laboratorio"],
				examenfinal=formulario.cleaned_data["examenfinal"],
				notafinal=formulario.cleaned_data["notafinal"],
				id_Mat=formulario.cleaned_data["id_Mat"],
				)
			p.save()
			return HttpResponseRedirect("/agregarnotas/")
	else:
		formulario=RegistrarNotas()
	return render_to_response("notas.html",{"form":formulario},RequestContext(request))

def addRelCarMat(request):
	if request.method=="POST":
		formulario=RegistrarRelCarMat(request.POST)
		if formulario.is_valid():
			p=rel_car_mat(
				id_Car=formulario.cleaned_data["id_Car"],
				id_Mat=formulario.cleaned_data["id_Mat"],
				)
			p.save()
			return HttpResponseRedirect("/agregarrelcarmat/")
	else:
		formulario=RegistrarRelCarMat()
	return render_to_response("relcarmat.html",{"form":formulario},RequestContext(request))


def VerContacto(request):
	lista=Carrera.objects.all()
	return render_to_response("vercontacto.html",{"dato":lista},RequestContext(request))

def VerCarrera(request):
	lista=Carrera.objects.all()
	return render_to_response("vercarrera.html",{"dato":lista},RequestContext(request))
def VerMaterias(request,id):
	idcarrera=int(id)
	carrera=Carrera.objects.get(id=idcarrera)
	id_materia=rel_car_mat.objects.filter(id_Car=carrera)
	materia=Materia.objects.filter(id__in=id_materia).order_by("nivel")
	#nivel2=Semestre.objects.all()
	#return HttpResponse(materia)
	#d = rel_car_mat.objects.get(id_Car=idcarrera)

	#c = Comentarios.objects.filter(tema=t.id)
	#c = Comentarios.objects.filter(tema=1)
	#rel=carrera.rel_car_mat_set.all()

	#materia=Materia.objects.all()
	#db = MySQLdb.connect(user='root',db='sistema',passwd='',host='localhost')
   	#cursor = db.cursor()
   	#cursor.execute('SELECT c.nombre,m.nombre,m.sigla,s.nivel FROM registro_semestre as s,registro_carrera as c,registro_materia as m,registro_rel_car_mat as cm where c.id=cm.id_car_id and m.id=cm.id_mat_id and m.id=s.id_Mat_id order by s.nivel,c.nombre asc')
   	#names = cursor.fetchall()
   	#db.close()
   	#lista=list(names)
   	#pdb.set_trace()
	return render_to_response("vermaterias.html",{"materia":materia},RequestContext(request))

def mapas(request):
	return render_to_response('mapas.html',RequestContext(request))




def addAutor(request):
	if request.method=="POST":
		formulario=AutorForm(request.POST)
		r=formulario.is_valid()
		if formulario.is_valid():
			p=Autor(
				nombre=formulario.cleaned_data["nombre"],
				apellido_pat=formulario.cleaned_data["apellido_pat"],
				apellido_mat=formulario.cleaned_data["apellido_mat"],
				)
			p.save()
			return HttpResponseRedirect("/list/")
	else:
		formulario=AutorForm()
	return render_to_response("autor.html",{"form":formulario},RequestContext(request))



def list(request):
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			nombre2=request.POST['nombre']
			imagen2=request.FILES['imagen']
			docfile2=request.FILES['docfile']
			autor2=request.POST['autor']
			newdoc = Document(
				nombre = nombre2,
				imagen = imagen2,
				docfile = docfile2,
				autor = Autor.objects.get(pk=autor2),
				)
			newdoc.save()
			return HttpResponseRedirect("/libros/")
	else:
		form = DocumentForm() 
	return render_to_response('list.html',{'form': form},context_instance=RequestContext(request))

def libros(request):
	documents = Document.objects.all()
	return render_to_response("libro_pdf.html",{"documents":documents},RequestContext(request))



def login_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == "POST":
			form = LoginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				usuario = authenticate(username=username,password=password)
				if usuario is not None and usuario.is_active:
					login(request,usuario)
					return HttpResponseRedirect("/menudirector/")
				else:
					mensaje = "usuario y/o password incorrecto"
		form = LoginForm()
		ctx = {'form':form,'mensaje':mensaje}
		return render_to_response('login.html',ctx,context_instance=RequestContext(request))





def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')


def MenuDirector(request):
	return render_to_response("menudirector.html",{},RequestContext(request))

def AsignacionDocente(request):
	if request.method=="POST":
		formulario=RegistrarRelCarDoc(request.POST)
		if formulario.is_valid():
			p=rel_docente_carrera(
				idCarrera=formulario.cleaned_data["idCarrera"],
				idDocente=formulario.cleaned_data["idDocente"],
				)
			p.save()
			return HttpResponseRedirect("/agregarrelcardoc/")
	else:
		formulario=RegistrarRelCarDoc()
	return render_to_response("asignacionDocente.html",{"form":formulario},RequestContext(request))


def AsignacionDocenteMateria(request):
	if request.method=="POST":
		formulario=RegistrarRelDocMat(request.POST)
		if formulario.is_valid():
			p=rel_docente_materia(
				idDocente=formulario.cleaned_data["idDocente"],
				idMateria=formulario.cleaned_data["idMateria"],
				)
			p.save()
			return HttpResponseRedirect("/agregarreldocmat/")
	else:
		formulario=RegistrarRelDocMat()
	return render_to_response("asignacionDocenteMateria.html",{"form":formulario},RequestContext(request))




def notas(request):
	est=Estudiante.objects.get(id=2)
	mat=rel_estudiante_materia.objects.filter(idEstudiante=est)
	materias=Materia.objects.filter(id__in=mat)
	nt=Notas.objects.filter(id_Mat=materias)
	pdb.set_trace()
	return HttpResponse(nt)