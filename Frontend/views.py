from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from Fincas.models import InfoUser
from Proveedor.models import Proveedor
from Fincas.models import Bodegas,Lotes,Finca, arbol
from django.contrib.auth import logout
from django.shortcuts import redirect, reverse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken
from django.db.models import Q

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # Suponiendo que "nombre_de_tu_vista" es el nombre de la URL de la vista a la que quieres redirigir
            return redirect(reverse('home'))
        else:
            # Aquí puedes agregar un mensaje de error si lo deseas
            context = {"error": "Credenciales incorrectas"}
            return render(request, 'html/app/auth-sign-in.html', context)
    else:
        return render(request, 'html/app/auth-sign-in.html')

def logout_view(request):
    auth_logout(request)
    return redirect(reverse('login'))

@login_required
def test_view(request):
    return redirect(reverse('add_user'))

@login_required
def add_user(request,user_id=None):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    if user_id:
        user_instance = get_object_or_404(User, id=user_id)
        return render(request,"html/app/add-usuario.html",{'userId': user_instance.pk,'token':token,'grupos_usuario': grupos_usuario})
        
    else:
        return render(request,"html/app/add-usuario.html",{'token':token,'grupos_usuario': grupos_usuario})

@login_required    
def list_users(request):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    context = {"token":token,'grupos_usuario': grupos_usuario}
    return render(request,"html/app/list-usuarios.html",context) 
@login_required
def add_proveedor(request,prov_id=None):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    if prov_id:
        prov_instance = get_object_or_404(Proveedor,id=prov_id)
        return render(request,"html/app/add-proveedor.html",{'providerId': prov_instance.pk,'token':token,'grupos_usuario': grupos_usuario})
    else:
        return render(request,"html/app/add-proveedor.html",{'token':token,'grupos_usuario': grupos_usuario})
@login_required
def list_proveedor(request):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    proveedores = Proveedor.objects.all()
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))

    return render(request,"html/app/list-proveedor.html",{'token':token,'proveedores':proveedores,'user':user,'grupos_usuario': grupos_usuario}) 



@login_required
def list_fincas(request):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    fincas = Finca.objects.all()
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    return render(request,"html/app/list-fincas.html",{'fincas':fincas,'token':token,'grupos_usuario': grupos_usuario})

@login_required
def add_fincas(request,fincas_id=None):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    if fincas_id:
        fincas_instance = get_object_or_404(Finca,pk=fincas_id)
        return render(request,"html/app/add-fincas.html",{'fincas_id': fincas_instance.pk,'finca':fincas_instance,'token':token,'grupos_usuario': grupos_usuario})
    else:
        return render(request,"html/app/add-fincas.html",{'token':token,'grupos_usuario': grupos_usuario})

@login_required
def list_lotes(request):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    lotes = Lotes.objects.all()
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    return render(request,"html/app/list-lotes.html",{'lotes':lotes,'token':token,'grupos_usuario': grupos_usuario})

@login_required
def add_lotes(request,lotes_id=None):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    fincas = Finca.objects.all()
    estructura = arbol(user)
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    context = {'fincas':fincas,'estructura':estructura,'token':token,'grupos_usuario': grupos_usuario}

    if lotes_id:
        lotes_instance = get_object_or_404(Lotes,pk=lotes_id)
        context["lotes_id"] = lotes_instance.pk
        context["lote_edit"] = lotes_instance
        context["finca_preseleccionada"] = lotes_instance.finca.pk

    return render(request,"html/app/add-lotes.html",context)

@login_required
def list_bodegas(request):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    bodegas = Bodegas.objects.all()
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    return render(request,"html/app/list-bodegas.html",{'bodegas':bodegas,'token':token,'grupos_usuario': grupos_usuario})

@login_required
def add_bodegas(request,bodegas_id=None):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    bodegas = Bodegas.objects.all()
    usuarios = User.objects.all()
    estructura = arbol(user)
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    context = {'bodegas':bodegas,'estructura': estructura,'usuarios':usuarios,'token':token,'grupos_usuario': grupos_usuario}

    if bodegas_id:
        bodega_instance = get_object_or_404(Bodegas,pk=bodegas_id)
        context["bodegas_id"] = bodega_instance.pk
        context["bodega_edit"] = bodega_instance
        context["lote_preseleccionado"] = bodega_instance.lote.pk
        context["finca_preseleccionada"] = bodega_instance.lote.finca.pk
        context["usuarios_preseleccionados"] = list(bodega_instance.usuario.all().values_list('pk',flat=True))
        

    return render(request,"html/app/add-bodegas.html",context)

