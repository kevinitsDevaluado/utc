import os
from datetime import datetime

from django.db import models
from django.forms import model_to_dict

from config import settings
from core.homepage.models import Mainpage
from core.user.models import User
from core.barrios.choices import *
from autoslug import AutoSlugField


class Country(models.Model):
    code = models.CharField(max_length=10, verbose_name='Código', unique=True)
    name = models.CharField(max_length=50, verbose_name='Nombre', unique=True)
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Paises'
        ordering = ['-id']


class Province(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='País')
    name = models.CharField(max_length=50, verbose_name='Nombre', unique=True)
    code = models.CharField(max_length=10, verbose_name='Código', unique=True)
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return 'País: {} / Provincia: {}'.format(self.country.name, self.name)

    def toJSON(self):
        item = model_to_dict(self)
        item['country'] = self.country.toJSON()
        return item

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        ordering = ['-id']


class Canton(models.Model):
    province = models.ForeignKey(Province, on_delete=models.PROTECT, verbose_name='Provincia')
    name = models.CharField(max_length=50, verbose_name='Nombre')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return '{} / Cantón: {}'.format(self.province.__str__(), self.name)

    def toJSON(self):
        item = model_to_dict(self)
        item['province'] = self.province.toJSON()
        return item

    class Meta:
        verbose_name = 'Cantón'
        verbose_name_plural = 'Cantones'
        ordering = ['-id']


class Parish(models.Model):
    canton = models.ForeignKey(Canton, on_delete=models.PROTECT, verbose_name='Cantón')
    name = models.CharField(max_length=100, verbose_name='Nombre')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return '{} / Parroquia: {}'.format(self.canton.__str__(), self.name)

    def toJSON(self):
        item = model_to_dict(self)
        item['canton'] = self.canton.toJSON()
        return item

    class Meta:
        verbose_name = 'Parroquia'
        verbose_name_plural = 'Parroquias'
        ordering = ['-id']

class District(models.Model):
    parroquia = models.ForeignKey(Parish, on_delete=models.PROTECT, verbose_name='Parroquia')
    name = models.CharField(max_length=100, verbose_name='Nombre')
    image = models.ImageField(upload_to='district/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    state = models.BooleanField(default=True, verbose_name='Estado')
    

    def __str__(self):
        return '{} / Barrios: {}'.format(self.parroquia.__str__(), self.name)

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def remove_image(self):
        try:
            if self.image:
                os.remove(self.image.path)
        except:
            pass

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(User, self).delete()


    def toJSON(self):
        item = model_to_dict(self)
        item['parroquia'] = self.parroquia.toJSON()
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Barrios'
        verbose_name_plural = 'Barrios'
        ordering = ['-id']


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    gender = models.CharField(max_length=10, choices=gender_person, default=gender_person[0][0], verbose_name='Sexo')
    mobile = models.CharField(max_length=10, verbose_name='Teléfono celular')
    phone = models.CharField(max_length=10, null=True, blank=True, verbose_name='Teléfono convencional')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Barrios')
    code = models.CharField(max_length=10, verbose_name='code',null=True, blank=True, default='')

    def __str__(self):
        return '{} / {}'.format(self.user.get_full_name(), self.user.dni)

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['district'] = {} if self.district is None else self.district.toJSON()
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-id']


class PresidentDistrict(models.Model):
    district = models.ForeignKey(District, on_delete=models.PROTECT, verbose_name='Barrio')
    user = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='Usuario')
    period = models.CharField(max_length=100, verbose_name='Periodo')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return '{} / User: {}'.format(self.user.user.last_name.__str__(), self.user.user.first_name)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Presidente'
        verbose_name_plural = 'Presidentes'
        ordering = ['-id']


class Meeting(models.Model):
    subject = models.CharField(max_length=500, null=True, blank=True, verbose_name='Asunto')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    date = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Barrios')

    def __str__(self):
        return '{} / {}'.format(self.subject, self.district.name)

    def toJSON(self):
        item = model_to_dict(self)
        item['date'] = self.birthdate.strftime('%Y-%m-%d')
        item['district'] = self.district.toJSON()
        return item

    class Meta:
        verbose_name = 'Reunion'
        verbose_name_plural = 'Reuniones'
        ordering = ['-id']




class RollCall(models.Model):
    user = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='Usuario')    
    meeting = models.ForeignKey(Meeting, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Reunión')

    def __str__(self):
        return '{} / {}'.format(self.user.get_full_name(), self.user.dni)

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['meeting'] = self.meeting.toJSON()
        return item

    class Meta:
        verbose_name = 'Pasar Lista'
        verbose_name_plural = 'Pasar lista'
        ordering = ['-id']





class FamilyResponsibilities(models.Model):
    user = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='Usuario')
    dni = models.CharField(max_length=13, unique=True, verbose_name='Cédula o RUC')
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Nombres')
    last_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Apellidos')        
    gender = models.CharField(max_length=10, choices=gender_person, default=gender_person[0][0], verbose_name='Sexo')
    mobile = models.CharField(max_length=10, verbose_name='Teléfono celular')
    phone = models.CharField(max_length=10, null=True, blank=True, verbose_name='Teléfono convencional')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')

    def __str__(self):
        return '{} / {}'.format(self.name, self.last_name)

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        return item

    class Meta:
        verbose_name = 'Carga Familiar'
        verbose_name_plural = 'Cargas Familiares'
        ordering = ['-id']

class Fees(models.Model):
    cuota = models.CharField(max_length=50, null=True, blank=True, verbose_name='Motivo de la Cuota')
    monto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Monto')
    date = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Barrios')

    def __str__(self):
        return '{} / {}'.format(self.user.get_full_name(), self.user.dni)

    def toJSON(self):
        item = model_to_dict(self)
        item['date'] = self.birthdate.strftime('%Y-%m-%d')
        item['district'] = self.district.toJSON()
        return item

    class Meta:
        verbose_name = 'Cuota'
        verbose_name_plural = 'Cuotas'
        ordering = ['-id']


class Debt(models.Model):
    fees = models.ForeignKey(Fees, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Cuota')
    user = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='Usuario')
    state = models.BooleanField(default=True, verbose_name='Estado')
    monto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Monto')


    def __str__(self):
        return '{} / {}'.format(self.user.get_full_name(), self.user.dni)

    def toJSON(self):
        item = model_to_dict(self)
        item['date'] = self.birthdate.strftime('%Y-%m-%d')
        item['fees'] = self.fees.toJSON()
        item['user'] = self.user.toJSON()
        return item

    class Meta:
        verbose_name = 'Deuda'
        verbose_name_plural = 'Deudas'
        ordering = ['-id']



class Payments(models.Model):
    debt = models.ForeignKey(Debt, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Cuota')
    monto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Monto')
    user = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='Usuario')
    date = models.DateField(default=datetime.now, verbose_name='Fecha de registro')

    def __str__(self):
        return '{} / {}'.format(self.user.get_full_name(), self.user.dni)

    def toJSON(self):
        item = model_to_dict(self)
        item['debt'] = self.debt.toJSON()
        item['date'] = self.birthdate.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pago'
        ordering = ['-id']



class Company(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=2000, blank=True, null=True)
    user = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='Usuario')
    proprietor = models.CharField(verbose_name='Propietario', max_length=100)
    desc = models.CharField(verbose_name='Descripción', max_length=2000, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Barrios')
    with_us = models.CharField(verbose_name='¿Porque estar con nosotros?', max_length=2000, blank=True, null=True)
    mission = models.CharField(verbose_name='Misión', max_length=1000, blank=True, null=True)
    vision = models.CharField(verbose_name='Visión', max_length=1000, blank=True, null=True)
    about_us = models.CharField(verbose_name='Quienes Somos', max_length=1000, blank=True, null=True)
    icon_image = models.ImageField(verbose_name='Logo', upload_to='mainpage/%Y/%m/%d', null=True, blank=True)
    phone = models.CharField(verbose_name='Teléfono Convencional', max_length=9, unique=True, blank=True, null=True)
    mobile = models.CharField(verbose_name='Teléfono Celular', max_length=10, unique=True, blank=True, null=True)
    email = models.EmailField(verbose_name='Correo Electrónico', max_length=50, unique=True, blank=True, null=True)
    address = models.CharField(verbose_name='Dirección', max_length=255, blank=True, null=True)
    horary = models.CharField(verbose_name='Horario', max_length=50, blank=True, null=True)
    coordinates = models.CharField(verbose_name='Coordenadas', max_length=50, blank=True, null=True)
    about_youtube = models.CharField(verbose_name='Video de Youtube', max_length=250, blank=True, null=True)
    

    def __str__(self):
        return self.name

    def get_latitude(self):
        return self.coordinates.split(',')[0].replace(',', '.')

    def get_longitude(self):
        return self.coordinates.split(',')[1].replace(',', '.')

    def get_icon_image(self):
        if self.icon_image:
            return '{}{}'.format(settings.MEDIA_URL, self.icon_image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def remove_icon_image(self):
        try:
            if self.icon_image:
                os.remove(self.icon_image.path)
        except:
            pass

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['-id']


class Category(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name='Empresa')
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    image = models.ImageField(upload_to='category/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    inventoried = models.BooleanField(default=True, verbose_name='¿Es inventariado?')
    slug = AutoSlugField(populate_from='name')
    activo = models.BooleanField(default=True, verbose_name='Activo')

    def remove_image(self):
        try:
            if self.image:
                os.remove(self.image.path)
        except:
            pass
        finally:
            self.image = None

    def __str__(self):
        return '{} / {}'.format(self.name, self.get_inventoried())

    def get_inventoried(self):
        if self.inventoried:
            return 'Inventariado'
        return 'No inventariado'

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item
        
    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['-id']



 
class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name='Empresa')
    cod_barra = models.CharField(max_length=150, verbose_name='Código de Barra', null=True, blank=True)
    name = models.CharField(max_length=150, verbose_name='Nombre')
    stock = models.IntegerField(default=0, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Categoría', null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Precio de Compra', null=True, blank=True)
    pvp = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Precio de Venta', null=True, blank=True)
    image = models.ImageField(upload_to='product/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    iva = models.CharField(default='Si', verbose_name="Cobranza Iva", choices=iva, max_length=10, null=True, blank=True)
    activo = models.BooleanField(default=True, verbose_name='Activo')
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name

    def remove_image(self):
        try:
            if self.image:
                os.remove(self.image.path)
        except:
            pass
        finally:
            self.image = None

    def toJSON(self):
        item = model_to_dict(self)
        item['category'] = self.category.toJSON()
        item['price'] = format(self.price, '.2f')
        item['price_promotion'] = format(self.get_price_promotion(), '.2f')
        item['price_current'] = format(self.get_price_current(), '.2f')
        item['pvp'] = format(self.pvp, '.2f')
        item['image'] = self.get_image()
        return item

    def price_discount(self):
        promotions = self.promotionsdetail_set.filter(promotion__state=True)
        if promotions.exists():
            return promotions[0].dscto
        return 0.00

    def get_price_promotion(self):
        promotions = self.promotionsdetail_set.filter(promotion__state=True)
        if promotions.exists():
            return promotions[0].price_final
        return 0.00
    
    def get_price_current(self):
        price_promotion = self.get_price_promotion()
        if price_promotion > 0:
            return price_promotion
        return self.pvp
 
    @property
    def get_discount(self):
        discount = 0
        price_promotion = self.price_discount()
        if price_promotion > 0:
            return price_promotion
        return discount

    @property
    def get_price_discount(self):
        price_promotion = self.get_price_promotion()
        if price_promotion > 0:
            return price_promotion
        return self.pvp

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Product, self).delete()

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-name']


