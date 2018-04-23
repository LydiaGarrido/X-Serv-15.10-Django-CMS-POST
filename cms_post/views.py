from django.shortcuts import render

# Create your views here.

from cms_post.models import Pages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


FORMULARIO = """
    <form method = 'POST'>
    <b>Contenido de la pagina: </b><br>
    <input type='text' name='page'><br>
    <input type='submit' value='Enviar'></form>
"""


def barra(request):
    content = Pages.objects.all()
    if request.user.is_authenticated():
        respuesta = "Logged in as " + request.user.username
        respuesta += ". <b><a href='logout'>Logout</a></b><br>"
    else:
        respuesta = "Not logged in. <b><a href='login'>Login</a></b><br>"
    respuesta += "<br>Páginas almacenadas:<br>"
    for pagina in content:
        respuesta += "<ul><li>" + pagina.name + " / " + pagina.page
        respuesta += "</ul></li>"
    return HttpResponse(respuesta)

@csrf_exempt
def edit(request, resource):
    if request.method == 'GET':
        try:
            pagina = Pages.objects.get(name=resource)
            respuesta = pagina.page + "<br>"
            if request.user.is_authenticated():
                respuesta += "<br>Rellene el formulario si se desea editar la pagina:<br>"
                respuesta += FORMULARIO
                return HttpResponse(respuesta)
            else:
                respuesta += "Es necesario hacer login para editar una pagina ya existente"
                return HttpResponse(respuesta)
        except Pages.DoesNotExist:
            if request.user.is_authenticated():
                respuesta = "La página no existe<br>"
                respuesta += "Rellene el formulario para crear una nueva pagina:<br>"
                respuesta += FORMULARIO
                return HttpResponse(respuesta)
            else:
                volver = '<a href="http://localhost:8000/">Inicio</a>'
                respuesta = "La página no existe. Es necesario"
                respuesta += "iniciar sesión para crear una nueva página. "
                return HttpResponse(respuesta + volver)

    if request.method == 'POST':
        try:
            if request.user.is_authenticated():
                page = request.POST['page']
                nueva_pag = Pages(name=resource, page=page)
                nueva_pag.save()
                nueva_pag.save(force_update=True)
                respuesta = "Pagina guardada<br>"
                respuesta += "Rellene el formulario si desea editar la pagina:<br>"
                respuesta += FORMULARIO
            else:
                volver = '<a href="http://localhost:8000/">Inicio</a>'
                respuesta = "No se ha podido actualizar la pagina. Es necesario iniciar sesión. "
                return HttpResponse(respuesta + volver)
        except Pages.DoesNotExist:
            if request.user.is_authenticated():
                page = request.POST['page']
                nueva_pag = Pages(name=resource, page=page)
                nueva_pag.save()
                respuesta = "Pagina guardada<br>"
                respuesta += "Rellene el formulario si desea editar la pagina:<br>"
                respuesta += FORMULARIO
            else:
                volver = '<a href="http://localhost:8000/">Inicio</a>'
                respuesta = "No se ha podido actualizar la pagina. Es necesario iniciar sesión. "
                return HttpResponse(respuesta + volver)
    else:
        respuesta = "Method not allowed"
    return HttpResponse(respuesta)

def error(request):
    volver = '<a href="http://localhost:8000/">Inicio</a>'
    respuesta = "Ha ocurrido un error: la pagina no esta disponible. "
    return HttpResponse(respuesta + volver)
        
