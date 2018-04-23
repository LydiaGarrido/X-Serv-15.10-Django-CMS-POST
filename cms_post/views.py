from django.shortcuts import render

# Create your views here.

from cms_post.models import Pages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


FORMULARIO = """
    <form method = 'POST'>
    <b><br>Contenido de la pagina: </b><br>
    <input type='text' name='page'><br>
    <input type='submit' value='Enviar'></form>
"""

VOLVER = """
    <a href="http://localhost:8000/">
    Volver a la pagina principal</a>
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
                respuesta += "<br>Rellene el formulario si se "
                respuesta += "desea editar la pagina:<br>"
                respuesta += FORMULARIO
            else:
                respuesta += "Es necesario hacer login para "
                respuesta += "editar una pagina ya existente. "
                return HttpResponse(respuesta + VOLVER)
        except Pages.DoesNotExist:
            if request.user.is_authenticated():
                respuesta = "La página no existe<br>"
                respuesta += "<br>Rellene el formulario para "
                respuesta += "crear una nueva pagina:<br>"
                respuesta += FORMULARIO
            else:
                respuesta = "La página no existe. Es necesario "
                respuesta += "iniciar sesión para crear una nueva página. "
                return HttpResponse(respuesta + VOLVER)

    elif request.method == 'POST':
        if request.user.is_authenticated():
            try:
                page = request.POST['page']
                pag = Pages.objects.get(name=resource)
                pag.page = page
                pag.save()
            except Pages.DoesNotExist:
                page = request.POST['page']
                pag_nueva = Pages(name=resource, page=page)
                pag_nueva.save()
            respuesta = "Pagina guardada<br>"
            respuesta += "<br>Rellene el formulario si "
            respuesta += "desea editar la pagina:<br>"
            respuesta += FORMULARIO
        else:
            respuesta = "No se ha podido guardar la pagina. "
            respuesta += "Es necesario iniciar sesión. "
            return HttpResponse(respuesta + VOLVER)
    else:
        respuesta = "Method not allowed"
    return HttpResponse(respuesta)


def error(request):
    respuesta = "Ha ocurrido un error: la pagina no esta disponible. "
    return HttpResponse(respuesta + VOLVER)
