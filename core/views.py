
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from core.forms import ProductForm
from core.models import Product
from django.db import IntegrityError
import re


def signup(request):
    if request.method == 'GET':
        return render(request, "core/authentication/signup.html", {'form': UserCreationForm()})
    else:
        form = UserCreationForm(request.POST)
        
        # Validación de contraseña
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if len(password1) < 8 or not re.search(r'[!@#$%^&*()<>?/\|}{~:]', password1):
            return render(request, "core/authentication/signup.html", {'form': form, 'error': 'La contraseña debe tener al menos 8 caracteres y al menos un carácter especial.'})
        
        if form.is_valid():
            username = form.cleaned_data['username']
            
            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    return render(request, "core/authentication/signup.html", {'form': UserCreationForm(), 'error': 'El nombre de usuario ya está en uso.'})
                else:
                    user = User.objects.create_user(username=username, password=password1)
                    user.save()
                    login(request, user)
                    return redirect('core:login')
            else:
                return render(request, "core/authentication/signup.html", {'form': form, 'error': 'Las contraseñas no coinciden.'})
        else:
            return render(request, "core/authentication/signup.html", {'form': form, 'error': 'Por favor corrija los errores en el formulario.'})

def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request, 'core/login/login.html', {'form': AuthenticationForm()})
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'core/login/login.html', {'form': AuthenticationForm(), 'error': "Usuario o contraseña incorrectos"})
        else:
            return render(request, 'core/login/login.html', {'form': form, 'error': "Datos de inicio de sesión inválidos"})



def cerrar_sesion(request):
    logout(request)
    return redirect ('home')  


def home(request):
   
   return render(request,'core/home.html')

  #  return HttpResponse(f"<h1>{data['title2']}<h1>\
  #                        <h2>Le da la Bienvenida  a su selecta clientela</h2>")
  #  products = ["aceite","coca cola","embutido"]
  #  prods_obj=[{'nombre': producto} for producto in products] # json.dumps()
  #  return JsonResponse({'mensaje2': data,'productos':prods_obj})

 
  #  return HttpResponse(f"<h1>{data['title2']}<h1>\
  #                      <h2>Le da la Bienvenida  a su selecta clientela</h2>")
# vistas de productos: listar productos 
def product_List(request):
    data = {
        "title1": "Productos",
        "title2": "Consulta De Productos"
    }
    products = Product.objects.all() # select * from Product
    data["products"]=products
    return render(request,"core/products/list.html",data)
# crear un producto
def product_create(request):
    
    
    
    
    data = {"title1": "Productos","title2": "Ingreso De Productos"}
   
    if request.method == "POST":
        #print(request.POST)
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect("core:product_list")

    else:
        data["form"] = ProductForm() # controles formulario sin datos

    return render(request, "core/products/form.html", data)

# editar un producto
def product_update(request,id):
    data = {"title1": "Productos","title2": ">Edicion De Productos"}
    product = Product.objects.get(pk=id)
    if request.method == "POST":
      form = ProductForm(request.POST,request.FILES, instance=product)
      if form.is_valid():
            form.save()
            return redirect("core:product_list")
    else:
        form = ProductForm(instance=product)
        data["form"]=form
    return render(request, "core/products/form.html", data)


# eliminar un producto
def product_delete(request,id):
    product = Product.objects.get(pk=id)
    data = {"title1":"Eliminar","title2":"Eliminar Un Producto","product":product}
    if request.method == "POST":
        product.delete()
        return redirect("core:product_list")
 
    return render(request, "core/products/delete.html", data)

# vistas de marcas: Listar marcas
def brand_List(request):
    data = {
        "title1": "Marcas",
        "title2": "Consulta De Marcas De Productos"
    }
    return render(request,"core/brands/list.html",data)

def supplier_List(request):
    data = {
        "title1": "Proveedores",
        "title2": "Consulta De proveedores"
    }
    return render(request,"core/suppliers/list.html",data)
  