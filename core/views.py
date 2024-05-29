
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from core.forms import ProductForm, BrandForm, SupplierForm,CategoryForm
from core.models import Product, Brand, Supplier, Category
from django.db import IntegrityError
import re
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache 

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'GET':
        return render(request, "core/authentication/signup.html", {'form': UserCreationForm()})
    else:
        form = UserCreationForm(request.POST)
        
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
    if request.user.is_authenticated:
        return redirect('home')
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
    response = redirect('home')
    response.delete_cookie('sessionid')
    return response


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
@never_cache
@login_required
def product_List(request):
    data = {
        "title1": "Productos",
        "title2": "Consulta De Productos"
    }
    products = Product.objects.all() # select * from Product
    data["products"]=products
    return render(request,"core/products/list.html",data)
# crear un producto
@login_required
@never_cache
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
@never_cache
@login_required
def product_update(request,id):
    data = {"title1": "Productos","title2": "Edicion De Productos"}
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

@login_required
@never_cache
def brand_update(request,id):
    data = {"title1": "Productos","title2": "Edicion De Productos"}
    brand = Brand.objects.get(pk=id)
    if request.method == "POST":
      form = BrandForm(request.POST,request.FILES, instance=brand)
      if form.is_valid():
            form.save()
            return redirect("core:brand_list")
    else:
        form = BrandForm(instance=brand)
        data["form"]=form
    return render(request, "core/brands/form.html", data)

@login_required
@never_cache
def supplier_update(request,id):
    data = {"title1": "Productos","title2": "Edicion De Proveedores"}
    supplier = Supplier.objects.get(pk=id)
    if request.method == "POST":
      form = SupplierForm(request.POST,request.FILES, instance=supplier)
      if form.is_valid():
            form.save()
            return redirect("core:supplier_list")
    else:
        form = SupplierForm(instance=supplier)
        data["form"]=form
    return render(request, "core/suppliers/form.html", data)

@never_cache
@login_required
def category_update(request,id):
    data = {"title1": "Categoría","title2": "Edicion De categoría"}
    category = Category.objects.get(pk=id)
    if request.method == "POST":
      form = CategoryForm(request.POST,request.FILES, instance=category)
      if form.is_valid():
            form.save()
            return redirect("core:category_list")
    else:
        form = CategoryForm(instance=category)
        data["form"]=form
    return render(request, "core/categorys/form.html", data)


# eliminar un producto
@login_required
@never_cache
def product_delete(request,id):
    product = Product.objects.get(pk=id)
    data = {"title1":"Eliminar","title2":"Eliminar Un Producto","product":product}
    if request.method == "POST":
        product.delete()
        return redirect("core:product_list")
 
    return render(request, "core/products/delete.html", data)

@login_required
@never_cache
def supplier_delete(request,id):
    supplier = Supplier.objects.get(pk=id)
    data = {"title1":"Eliminar","title2":"Eliminar Un Proveedor","supplier":supplier}
    if request.method == "POST":
        supplier.delete()
        return redirect("core:supplier_list")
 
    return render(request, "core/suppliers/delete.html", data)

@login_required
@never_cache
def brand_delete(request,id):
    brand = Brand.objects.get(pk=id)
    data = {"title1":"Eliminar","title2":"Eliminar una Marca","brand":brand}
    if request.method == "POST":
        brand.delete()
        return redirect("core:brand_list")
    return render(request, "core/brands/delete.html", data)

@login_required
@never_cache
def category_delete(request,id):
    category = Category.objects.get(pk=id)
    data = {"title1":"Eliminar","title2":"Eliminar una categoría","category": category}
    if request.method == "POST":
        category.delete()
        return redirect("core:category_list")
 
    return render(request, "core/categorys/delete.html", data)
    
# vistas de marcas: Listar marcas
@never_cache
@login_required
def brand_List(request):
    data = {
        "title1": "Marcas",
        "title2": "Consulta De Marcas De Productos"
    }
    brands = Brand.objects.all()  # Obtener todas las marcas
    data["brands"] = brands
    return render(request, "core/brands/list.html", data)
#crear las marcas 
@never_cache
@login_required
def brand_create(request):
    data = {
        "title1": "Crear Marcas",
        "title2": "Ingreso de Marcas"
    }

    if request.method == "POST":
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            brand = form.save(commit=False)
            brand.user = request.user
            brand.save()
            return redirect("core:brand_list")
    else:
        form = BrandForm()

    data["form"] = form
    return render(request, "core/brands/form.html", data)

# Listar proveedores
@never_cache
@login_required
def supplier_List(request):
    data = {
        "title1": "Proveedores",
        "title2": "Consulta De Proveedores"
    }
    suppliers = Supplier.objects.all()  # Obtener todos los proveedores
    data["suppliers"] = suppliers
    return render(request, "core/suppliers/list.html", data)

#listar categoría
@never_cache
@login_required
def category_List(request):
    data = {
        "title1": "Categoría",
        "title2": "Consulta De Categoría"
    }
    categorys = Category.objects.all()  # Obtener todos los proveedores
    data["categorys"] = categorys
    return render(request, "core/categorys/list.html", data)


@never_cache
@login_required
def category_create(request):
    data = {
        "title1": "Crear Categoría",
        "title2": "Ingreso de Categorías"
    }

    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect("core:category_list")
    else:
        form = CategoryForm()

    data["form"] = form
    return render(request, "core/categorys/form.html", data)


@never_cache
@login_required
def supplier_create(request):
    data = {
        "title1": "Crear Proveedor",
        "title2": "Ingresar Proveedor"
    }

    if request.method == "POST":
        form = SupplierForm(request.POST, request.FILES)
        if form.is_valid():
            Supplier = form.save(commit=False)
            Supplier.user = request.user
            Supplier.save()

            return redirect("core:supplier_list")
    else:
        form = SupplierForm()
    data["form"] = form
    return render(request, "core/suppliers/form.html", data)