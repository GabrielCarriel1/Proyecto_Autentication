from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.db.models import F
from proy_sales.utils import valida_ruc_o_cedula, valida_telefono_ecuador
from django.core.exceptions import ValidationError



class ActiveBrandManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(state=True)
   
 
class Brand(models.Model):
    description = models.CharField('Nombre de la Marca', max_length=100)
    logo = models.ImageField('Imagen Marca',upload_to='brands/',blank=True,null=True,default='brands/default.png')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.BooleanField('Activo', default=True)

    objects = models.Manager()  # Manager predeterminado


    objects = models.Manager()  # Manager predeterminado
    active_brands = ActiveBrandManager()
    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['description']
        indexes = [
            models.Index(fields=['description']),
        ]
        
    def __str__(self):
        return self.description

class Supplier(models.Model):
    foto = models.ImageField(upload_to='suplier/',blank=True,null=True,default='suppliers/default.png')
    name = models.CharField('nombre',max_length=100)
    ruc = models.CharField('*Ingrese Ruc/ C.I',max_length=13,validators=[valida_ruc_o_cedula])
    address = models.CharField('Direccion',max_length=500)
    phone = models.CharField('Nº Celular',max_length=20,validators=[valida_telefono_ecuador])
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.BooleanField('Activo', default = True)

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()


        if Supplier.objects.filter(ruc=self.ruc).exclude(id=self.id).exists():
            raise ValidationError('Ya existe un proveedor con este número de RUC o cédula.')

        if len(self.ruc) == 13:
            cedula = self.ruc[:10]
            if Supplier.objects.filter(ruc=cedula).exclude(id=self.id).exists():
                raise ValidationError('Ya existe un proveedor con un RUC que coincide con esta cédula.')

        if len(self.ruc) == 10:
            ruc = Supplier.objects.filter(ruc__startswith=self.ruc).exclude(id=self.id)
            if ruc.exists():
                raise ValidationError('Ya existe un proveedor con una cédula que coincide con los primeros 10 dígitos de un RUC.')

    def save(self, *args, **kwargs):
        self.clean()
        super(Supplier, self).save(*args, **kwargs)


class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(state=True)
    
class Product(models.Model):
    class Status(models.TextChoices):
        STORE = 'RS', 'Rio Store'
        FERRISARITO = 'FS', 'Ferrisariato'
        COMISARIATO = 'CS', 'Comisariato'
     
        
    description = models.CharField('Articulo',max_length=100)
    cost=models.DecimalField('Costo Producto',max_digits=10,decimal_places=2,default=Decimal('0.0'))
    price=models.DecimalField('Precio',max_digits=10,decimal_places=2,default=Decimal('0.0'))
    stock=models.IntegerField(default=100,help_text="Stock debe estar en 0 y 10000 unidades",verbose_name='Stock')
    iva = models.IntegerField(verbose_name='IVA', choices=((0,'0%'),(5,'5%'),(15,'15%')), default=15)
    expiration_date = models.DateTimeField('Fecha Caducidad',default=timezone.now()+timedelta(days=60))
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,related_name='product',verbose_name='Marca')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE,verbose_name='Proveedor')
    categories = models.ManyToManyField('Category',verbose_name='Categoria', related_name='productos')
    line = models.CharField('Linea',max_length=2,choices=Status.choices,default=Status.COMISARIATO)
    image = models.ImageField(upload_to='products/',blank=True,null=True,default='products/default.png')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.BooleanField('Activo', default = True)

    objects = models.Manager()  # Manager predeterminado
    active_products = ActiveProductManager()  #
     
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['description']
        indexes = [models.Index(fields=['description']),]
           
    def __str__(self):
        return self.description  
     
    @property
    def get_categories(self):
        return " - ".join([c.description for c in self.categories.all().order_by('description')]) 
    
  
    def reduce_stock(self,quantity):
        if quantity > self.stock:
            raise ValueError("No hay suficiente stock disponible.")
        self.stock -= quantity
        self.save()
        
    @staticmethod
    def update_stock(self,id,quantity):
         Product.objects.filter(pk=id).update(stock=F('stock') - quantity)
            
class Category(models.Model):
    description = models.CharField(verbose_name='Nombre Categoría', max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.BooleanField('Activo', default=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['description']
        indexes = [models.Index(fields=['description']),]

    def __str__(self):
        return f"{self.description}"
    
    @property
    def num_productos(self):
        return self.productos.count()
        
    def clean(self):
        super().clean()
        if Category.objects.filter(description=self.description).exclude(id=self.id).exists():
            raise ValidationError('Ya existe una categoría con este nombre.')


class Customer(models.Model):
    dni = models.CharField(verbose_name='Dni',max_length=13, unique=True, blank=True, null=True)
    first_name = models.CharField(verbose_name='Nombres',max_length=50)
    last_name = models.CharField(verbose_name='Apellidos',max_length=50)
    address = models.TextField(verbose_name='Dirección',blank=True, null=True)
    gender = models.CharField(verbose_name='Sexo',max_length=1, choices=(('M','Masculino'),('F','Femenino')), default='M')
    date_of_birth = models.DateField(verbose_name='Fecha Nacimiento',blank=True, null=True)
    phone = models.CharField(verbose_name='Telefono',max_length=50, blank=True, null=True)
    email = models.CharField(verbose_name='Correo',max_length=100, blank=True, null=True)
    image = models.ImageField(verbose_name='Foto',upload_to='customers/',blank=True,null=True,default='products/default.png')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.BooleanField(verbose_name='Activo', default = True)
 
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['last_name']
        indexes = [models.Index(fields=['last_name']),]

    def save(self, *args, **kwargs):
        if self.first_name:
            self.first_name = self.first_name.upper()
        if self.last_name:
            self.last_name = self.last_name.upper()
        super(Customer, self).save(*args, **kwargs)
    
    @property
    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class PaymentMethod(models.Model):
    description = models.CharField(verbose_name='Metodo Pago',max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.BooleanField('Activo', default = True)
 
    class Meta:
        verbose_name = 'Metodo de Pago'
        verbose_name_plural = 'Metodo de Pagos'
        ordering = ['description']
       
        
    def __str__(self):
        return self.description
    
class Invoice(models.Model):
    customer =  models.ForeignKey(Customer, on_delete=models.PROTECT,related_name='customer_invoices',verbose_name='Cliente')
    payment_method = models.ForeignKey(PaymentMethod,on_delete=models.PROTECT,related_name='payment_invoices',verbose_name='Metodo pago')
    issue_date = models.DateTimeField(verbose_name='Fecha Emision',default=timezone.now)
    subtotal = models.DecimalField(verbose_name='Subtotal',default=0, max_digits=16, decimal_places=2)
    iva = models.DecimalField(verbose_name='Iva',default=0, max_digits=16, decimal_places=2)
    discount = models.DecimalField(verbose_name='descuento',default=0, max_digits=16, decimal_places=2)
    total = models.DecimalField(verbose_name='Total',default=0, max_digits=16, decimal_places=2)
    payment = models.DecimalField(verbose_name='Pago',default=0, max_digits=16, decimal_places=2)
    change = models.DecimalField(verbose_name='Cambio',default=0, max_digits=16, decimal_places=2)
    status = models.CharField(verbose_name='Estado',max_length=1,choices=(('F','Factura'),('A','Anulada'),('D','Devolucion')),default='F')  
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.BooleanField('Activo', default = True)
 
    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ('-issue_date','customer',)
        indexes = [
            models.Index(fields=['issue_date']),
            models.Index(fields=['customer']),  
        ]
    
    
    def __str__(self):
        return f"{self.id} - {self.customer}"


class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE,related_name='detail',verbose_name='Factura')
    product = models.ForeignKey(Product, on_delete=models.PROTECT,related_name='Product',verbose_name='Producto')
    cost = models.DecimalField(default=0, max_digits=16, decimal_places=2, null=True, blank=True)
    quantity = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    price = models.DecimalField(default=0, max_digits=16, decimal_places=2)
    subtotal = models.DecimalField(default=0, max_digits=16, decimal_places=2)
    iva = models.DecimalField(default=0, max_digits=10, decimal_places=2)
  
    class Meta:
        verbose_name = "Factura Detalle"
        verbose_name_plural = "Factura Detalles"
        ordering = ('id',)
        indexes = [models.Index(fields=['id']),]
    
        
    def __str__(self):
        return f"{self.product}"