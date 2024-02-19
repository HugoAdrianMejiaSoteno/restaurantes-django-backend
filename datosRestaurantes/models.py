import uuid
from django.db import models

# Create your models here.
from django.db import models

class Restaurantes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rating = models.IntegerField()
    imagen = models.TextField()
    nombre = models.TextField()
    class Meta:
        db_table = 'restaurantes'


class Direcciones(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurante = models.OneToOneField(Restaurantes, on_delete=models.CASCADE, null=True)
    calle = models.TextField()
    ciudad = models.TextField()
    estado = models.TextField()
    latitud = models.DecimalField(max_digits=20, decimal_places=20)
    longitud = models.DecimalField(max_digits=20, decimal_places=20)
    class Meta:
        db_table = 'direcciones'


class Contactos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurante = models.OneToOneField(Restaurantes, on_delete=models.CASCADE, null=True)
    sitio_web = models.TextField()
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    class Meta:
        db_table = 'contactos'

