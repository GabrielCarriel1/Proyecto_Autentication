from django.urls import path
from core import views
 
app_name='core' # define un espacio de nombre para la aplicacion
urlpatterns = [
   # urls de vistas
   path('product_list/', views.product_List,name='product_list'),
   path('product_create/', views.product_create,name='product_create'),
   path('product_update/<int:id>/', views.product_update,name='product_update'),
   path('product_delete/<int:id>/', views.product_delete,name='product_delete'),
   # urls de marcas
   path('brand_list/', views.brand_List,name='brand_list'),
   # urls de proveedores
   path('supplier_list/', views.supplier_List,name='supplier_list'),
   path('signup/', views.signup,name='signup'),
   path('login/', views.iniciar_sesion,name='login'),
   path('logout/', views.cerrar_sesion,name='logout'),
]