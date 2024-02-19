from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from .models import Restaurantes, Direcciones, Contactos
from django.shortcuts import get_object_or_404, get_list_or_404
import json
from django.db.models import F
from django.db import transaction

# Create your views here.
#para conectar pg admin correctamente con db de render: https://stackoverflow.com/questions/75470743/connect-render-db-to-pgadmin

def hogar(request):
    return HttpResponse('Bienvenido a la API de restaurantes')

@csrf_exempt
def restaurantes_path(request):
    if request.method == 'GET':
        return get_restaurantes(request)
    elif request.method == 'POST':
        return post_restaurante(request)
    else:
        return JsonResponse({'Error ':'Asegurate de hacer las peticiones correctas a este url'},status=501)

@csrf_exempt
def restaurante_path(request, pk):
    if request.method == 'GET':
        return get_restaurante(request, pk)
    elif request.method == 'PUT':
        return put_restaurante(request, pk)
    elif request.method == 'DELETE':
        return delete_restaurante(request, pk)
    else:
        return JsonResponse(status=501)
    

    
def get_restaurantes(request):
    # Obtener todos los restaurantes con sus datos relacionados
    restaurantes = Restaurantes.objects.all().values('id',
        'rating', 'imagen', 'nombre',  # Campos del modelo Restaurantes
        'direcciones__calle', 'direcciones__ciudad', 'direcciones__estado',  # Campos del modelo Direcciones
        'direcciones__latitud', 'direcciones__longitud',
        'contactos__sitio_web', 'contactos__email', 'contactos__telefono'  # Campos del modelo Contactos
    )

    # Formatear los datos en el formato deseado
    # aqqui uso notacion de corchetes porque es un queryset En el caso de la vista get_restaurantes, estás usando el método values() de la consulta de Django. Este método devuelve un diccionario para cada objeto en el queryset, donde las claves son los nombres de los campos que seleccionaste en la consulta. Por lo tanto, cuando iteras sobre los resultados, puedes acceder a los valores de cada campo utilizando la notación de corchetes (resultado['rating'], resultado['imagen'], etc.).
    resultados = []
    for restaurante in restaurantes:
        resultado = {
            "id": restaurante['id'],
            "rating": restaurante['rating'],
            "imagen": restaurante['imagen'],
            "name": restaurante['nombre'],
            "contact": {
                "site": restaurante['contactos__sitio_web'],
                "email": restaurante['contactos__email'],
                "phone": restaurante['contactos__telefono']
            },
            "address": {
                "street": restaurante['direcciones__calle'],
                "city": restaurante['direcciones__ciudad'],
                "state": restaurante['direcciones__estado'],
                "location": {
                    "lat": float(restaurante['direcciones__latitud']),
                    "lng": float(restaurante['direcciones__longitud'])
                }
            }
        }
        resultados.append(resultado)

    # Retornar la respuesta JSON con los resultados formateados
    return JsonResponse(resultados, safe=False)

#La decoración @transaction.atomic asegura que todas las operaciones de base de datos realizadas dentro de la vista se ejecuten como una sola transacción. Si ocurre algún error durante la ejecución de la vista, todas las operaciones realizadas hasta ese punto se revertirán, evitando que se produzcan inconsistencias en la base de datos.
@transaction.atomic
def post_restaurante(request):
    try:
        datos = json.loads(request.body)
        id = datos.get('id')
        if id:
            return JsonResponse({'Error': 'El restaurante a crear no debe contener un id'}, status=400)

        # Crear el nuevo restaurante
        nuevo_restaurante = Restaurantes.objects.create(
            rating=datos['rating'],
            imagen=datos['imagen'],
            nombre=datos['nombre']
        )

        # Crear una instancia de Direcciones con los datos de direcciones
        direccion_data = datos.pop('direcciones')
        direccion = Direcciones.objects.create(
            restaurante=nuevo_restaurante,
            **direccion_data
        )

        # Crear una instancia de Contactos con los datos de contactos enviados
        contacto_data = datos.pop('contactos')
        contacto = Contactos.objects.create(
            restaurante=nuevo_restaurante,
            **contacto_data
        )

        restaurante_data = {
            'id': str(nuevo_restaurante.id),
            'rating': nuevo_restaurante.rating,
            'imagen': nuevo_restaurante.imagen,
            'name': nuevo_restaurante.nombre,
            'contact': {
                'site': contacto.sitio_web,
                'email': contacto.email,
                'phone': contacto.telefono
            },
            'address': {
                'street': direccion.calle,
                'city': direccion.ciudad,
                'state': direccion.estado,
                'location': {
                    'lat': float(direccion.latitud),
                    'lng': float(direccion.longitud)
                }
            }
        }

    except Exception as e:
    # Manejo de la excepción
        HttpResponse("Se produjo un error:", e)

    #Recordemos que lo debemos recibir el body de la siguiente forma con post en el postman, ejemplo:
#     {
#     "rating": 5,
#     "imagen": "https://www.e-architect.com/wp-content/uploads/2021/12/ling-ling-restaurant-by-hakkasan-lighting-u071221-m5.jpg",
#     "nombre": "Ling Ling by Hakkasan",
#     "contactos": {
#         "sitio_web": "https://linktr.ee/linglingmx",
#         "email": "https://linktr.ee/linglingmx",
#         "telefono": "+525532799204"
#     },
#     "direcciones": {
#         "calle": "Av. P.º de la Reforma 509-Piso 56, Cuauhtémoc, 06500 , CDMX",
#         "ciudad": "Ciudad de México",
#         "estado": "CDMX",
#         "latitud": 19.424603873103642,
#         "longitud": -99.17583958214234
#     }
# }

    return JsonResponse(restaurante_data, status=201, safe=False)

def get_restaurante(request, pk):
    restaurante = get_object_or_404(Restaurantes, pk=pk)
    # print(restaurante)
    
    # Crea un diccionario con los datos del restaurante que deseo mostrar ya que recordemos que get_object_or_404 no es serializable y es un objeto
    restaurante_data = {
        "id": restaurante.id,
        "rating": restaurante.rating,
        "imagen": restaurante.imagen,
        "name": restaurante.nombre,
        "contact": {
            "site": restaurante.contactos.sitio_web,
            "email": restaurante.contactos.email,
            "phone": restaurante.contactos.telefono
        },
        "address": {
            "street": restaurante.direcciones.calle,
            "city": restaurante.direcciones.ciudad,
            "state": restaurante.direcciones.estado,
            "location": {
                "lat": float(restaurante.direcciones.latitud),
                "lng": float(restaurante.direcciones.longitud)
            }
        }
    }

    return JsonResponse(restaurante_data, safe=False)


@transaction.atomic
def put_restaurante(request, pk):
    # Convertimos el cuerpo de la solicitud a un diccionario Python
    datos = json.loads(request.body)
    
    # Verificamos si se proporciona un 'id', lo cual no debería permitirse en una actualización
    if 'id' in datos:
        return JsonResponse({'Error': 'No puedes modificar el id del restaurante'}, status=400)

    # Obtenemos el restaurante a actualizar o generamos un error 404 si no existe
    restaurante = get_object_or_404(Restaurantes, pk=pk)

    # Actualizamos la información básica del restaurante si se proporciona en los datos
    restaurante.rating = datos.get('rating', restaurante.rating)
    restaurante.imagen = datos.get('imagen', restaurante.imagen)
    restaurante.nombre = datos.get('nombre', restaurante.nombre)
    
    # Procesamos la información de dirección si está presente en los datos
    direccion_data = datos.pop('direcciones', None)
    if direccion_data:
        if restaurante.direcciones:  # Si ya existe una dirección, la actualizamos
            direccion = restaurante.direcciones
            for key, value in direccion_data.items():
                setattr(direccion, key, value)
            direccion.save()
        else:  # Si no existe una dirección, la creamos y la asociamos con el restaurante
            direccion = Direcciones.objects.create(restaurante=restaurante, **direccion_data)
    
    # Procesamos la información de contacto si está presente en los datos
    contacto_data = datos.pop('contactos', None)
    if contacto_data:
        if restaurante.contactos:  # Si ya existe un contacto, lo actualizamos
            contacto = restaurante.contactos
            for key, value in contacto_data.items():
                setattr(contacto, key, value)
            contacto.save()
        else:  # Si no existe un contacto, lo creamos y lo asociamos con el restaurante
            contacto = Contactos.objects.create(restaurante=restaurante, **contacto_data)

    # Guardamos los cambios en el restaurante
    restaurante.save()

    # Devolvemos una respuesta HTTP 200 OK
    return HttpResponse(status=200)

def delete_restaurante(request, pk):
    restaurante = get_object_or_404(Restaurantes, pk=pk) #Verificamos que exista sino mandamos un 404
    restaurante.delete() #La eliminamos porque ese objeto tiene el metodo delete
    return HttpResponse(status=204)