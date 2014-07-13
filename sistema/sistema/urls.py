from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import RedirectView

admin.autodiscover()
from sistema.apps.registro.views import *

urlpatterns = patterns('',
     url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),
)
urlpatterns += patterns(
    'sistema.apps.registro.views',
    # Examples:
    # url(r'^$', 'sistema.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
   	
    url(r'^$','index_view',name='vista_principal'),
    #url(r'^contacto/$','contacto_view',name='vista_contacto'),
    url(r'^vercontacto/$','VerContacto',name='ver_contacto'),
    url(r'^agregarestudiante/','addEstudiante',name='vista_estudiante'),
    url(r'^menuestudiante/(?P<id>\d+)/$','MenuEstudiante',name='vista_menuestudiante'),
    url(r'^menudocente/(?P<id>\d+)/$','MenuDocente',name='vista_menudocente'),
    url(r'^agregardocente/','addDocente',name='vista_docente'),
    url(r'^loginEstudiante/$','login_view_Estudiante',name='vista_login_estudiante'),
    url(r'^logoutEstudiante/$','logout_view_Estudiante',name='vista_logout_estudiante'),
    url(r'^loginDocente/$','login_view_Docente',name='vista_login_docente'),
    url(r'^logoutDocente/$','logout_view_Docente',name='vista_logout_docente'),

    url(r'^editarestudiante/(?P<id>\d+)/$',editar_estudiante),
    url(r'^editardocente/(?P<id>\d+)/$',editar_docente),

    url(r'^vermaterias/(?P<id>\d+)/$',VerMaterias),
    url(r'^agregarrelcarest/(?P<id>\d+)/$','addRelCarEst',name='vista_relcarest'),
    url(r'^agregarrelestmat/(?P<id>\d+)/$',addRelEstMat),
    url(r'^programacion/(?P<id>\d+)/$',programacion),
    url(r'^carrera/$','addCarrera',name='vista_carrera'),
    url(r'^agregarmateria/$',addMateria),
    url(r'^agregarnotas/$',addNotas),
    url(r'^agregarrelcarmat/$',addRelCarMat),  
    url(r'^registro/exito/$',exito),
    

    url(r'^ver/carreras/$','VerCarrera',name='vista_carrera2'),
    url(r'^autor/$',"addAutor",name='Autor'),

    url(r'^login/$','login_view',name='vista_login'),
    url(r'^registro/$','register_view',name='vista_registro'),
    url(r'^logout/$','logout_view',name='vista_logout'),
    url(r'^menudirector/$',"MenuDirector",name="vista_menu_director"),
    url(r'^agregarrelcardoc/$',AsignacionDocente), 
    url(r'^agregarreldocmat/$',AsignacionDocenteMateria),
    url(r'^nota/$',notas),  
    #url(r'^mapas/$',mapas),
    #url(r'^uploads/$','upload_file',name="uploads"),
    #url(r'^list/$','upload_file',name="uploads"),
)
urlpatterns += patterns('sistema.apps.registro.views',
    url(r'^list/$', 'list', name='list'),
    url(r'^libros/$', 'libros', name='libros'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
