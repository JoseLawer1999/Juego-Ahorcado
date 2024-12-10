from django.shortcuts import render, redirect
from .models import Categoria, Palabra, Jugador
import random

# Create your views here.


def index(request):  # Definicion de una funcion, el parametro request representa una solicitud HTTP
    # Como resultado me renderiza la solicitud y carga en el navegador la pagina html
    return render(request, 'index.html')


def ayuda(request):
    return render(request, 'ayuda.html')

# Logica del Juego ahorcado en vistas

# Inicializar el juego con eleccion de categoria, palabra y configuracion de sesion


def iniciar_juego(request):
    categorias = Categoria.objects.all()  # Obtiene todas las categorias disponibles
    # Comprueba si el tipo de solicitud es post(lo cual indica que el usuario ha enviado datos)
    if request.method == 'POST':
        # Obtiene el valor de nickname del formulario enviado por el usuario en la solicitud POST.
        nickname = request.POST.get('nickname')
        # Crea o recupera el jugador // Busca en la base de datos un jugador con el nickname dado.
        jugador, created = Jugador.objects.get_or_create(nickname=nickname)
        # Sino lo encuentra, lo crea. La variable created es true si el jugador fue creado y false si ya existia.

        # Seleccion de categoria y palabra
        # Obtiene el ID de la categoria seleccionada por el jugador desde el formulario enviado en la solicitud POST.
        categoria_id = request.POST.get('categoria')
        # Busca en la base de datos la instancia de categoria que corresponde al id proporcionado por el jugador
        categoria = Categoria.objects.get(id=categoria_id)
        # Filtra las palabras en la base de datos que pertenecen a la categoria seleccionada por el jugador y las almacena en la variable palabras.
        palabras = Palabra.objects.filter(categoria=categoria)
        # Selecciona aleatoriamente una palabra de la lista palabras y convierte su texto a mayusculas. Esta palabra sera el desafio que el jugador tendra que adivinar.
        palabra = random.choice(palabras).texto.upper()

        # Configuracion inicial de variables de sesion
        # La palabra que el jugador debe adivinar
        request.session['palabra'] = palabra
        request.session['letras_adivinadas'] = []
        # El numero de intentos disponibles para adivinar.
        request.session['intentos'] = 8

        request.session['score'] = 0  # El puntaje inicial
        request.session['palabra_mostrada'] = " "
        request.session['nickname'] = nickname
        request.session['categoria_nombre'] = categoria.nombre
        request.session['totalpuntos'] = 0
        request.session['nivelcompletado'] = True

        # Redirige al juego despues de inicializarlo // Redirige al jugador a la vista jugar despues de inicializarlo
        return redirect(jugar)

    return render(request, 'iniciar_juego.html', {  # Si la solicitud no es de tipo POST, renderiza iniciar_juego.html y le pasa la lista de categorias para seleccionar una.
        'categorias': categorias
    })


def jugar(request):  # Este es una funcion de vista en Django
    if request.method == 'POST':  # Verifica si el metodo de la solicitud es POST, lo que indica que el usuario envio datos de un formulario en la pagina
        letra = request.POST.get('letra').upper()
        palabra = request.session.get('palabra')
        score = request.session.get('score')
        intentos = request.session.get('intentos')
        letras_adivinadas = request.session.get('letras_adivinadas')
        palabra_mostrada = request.session.get('palabra_mostrada')

        if letra and letra not in request.session['letras_adivinadas']:
            letras_adivinadas += letra

            if letra in request.session['palabra']:
                score += 2
            else:
                intentos -= 1
                score -= 2 if score >= 2 else 0

        # Actualizar sesión
        # Actualiza el puntaje en la sesión del usuario.
        request.session['score'] = score
        # Actualiza el número de intentos en la sesión.
        request.session['intentos'] = intentos
        request.session['letras_adivinadas'] = letras_adivinadas
        palabra_mostrada = ''.join(
            [letra if letra in letras_adivinadas else '_ ' for letra in palabra])
        request.session['palabra_mostrada'] = palabra_mostrada

        # Condicion si pierdo
        if intentos == 0:

            return redirect(perder)
        elif '_' not in palabra_mostrada:
            return redirect(ganar)

    # Determinar la imagen del ahorcado segun los intentos restantes
    imagen_ahorcado = f"images/intentos/{8 -
                                         request.session.get('intentos', 0)}.png"

    return render(request, 'jugar.html', {
        'intentos': request.session.get('intentos'),
        'score': request.session.get('score'),
        'totalpuntos': request.session.get('totalpuntos'),
        'palabra': request.session.get('palabra'),
        'letras_adivinadas': request.session.get('letras_adivinadas'),
        'palabra_mostrada': request.session.get('palabra_mostrada'),
        'nickname': request.session.get('nickname'),
        'imagen_ahorcado': imagen_ahorcado,


    })


def reiniciar(request):
    # Recuperar la categoria seleccionada previamente
    categoria_nombre = request.session.get('categoria_nombre')
    categoria = Categoria.objects.get(nombre=categoria_nombre)

    # Obtener una nueva palabra aleatoria de la categoria seleccionada
    palabras = Palabra.objects.filter(categoria=categoria)
    nueva_palabra = random.choice(palabras).texto.upper()

    request.session['palabra'] = nueva_palabra  # Asignar la nueva palabra
    request.session['intentos'] = 8
    request.session['letras_adivinadas'] = []
    request.session['score'] = 0
    request.session['palabra_mostrada'] = " "
    request.session['nivelcompletado'] = False

    return redirect(jugar)


def perder(request):
    score = request.session.get('score', 0)  # Puntaje actual del jugador
    nickname = request.session.get('nickname')
    # Obtener el jugador de la base de datos
    jugador = Jugador.objects.get(nickname=nickname)
    totalpuntos = request.session.get('totalpuntos')
    # Valor booleano para evitar acumulacion
    nivelcompletado = request.session.get('nivelcompletado')

    # Inicializar el puntaje total desde la base de datos o desde la sesion
    totalpuntos = request.session.get('totalpuntos', 0)

    if nivelcompletado and totalpuntos == 0:
        totalpuntos += score
        request.session['totalpuntos'] = totalpuntos  # Guardar en la sesion
    elif not nivelcompletado and totalpuntos != 0:
        totalpuntos += score
        request.session['totalpuntos'] = totalpuntos

    # Verificar si el puntaje acumulado supera el maximo historico del jugador
    if totalpuntos > jugador.score:
        jugador.score = totalpuntos
        jugador.save()

    # Marcar el nivel como completado para evitar acumulacion
    request.session['nivelcompletado'] = True

    # Imagen cuando pierda
    imagen_ahorcado = f"images/perder/HangMan.gif"

    return render(request, 'perdiste.html', {
        'palabra': request.session.get('palabra'),
        'nickname': request.session.get('nickname'),
        'categoria_nombre': request.session.get('categoria_nombre'),
        'score': score,
        'totalpuntos': totalpuntos,
        'imagen_ahorcado': imagen_ahorcado,
    })


def ganar(request):
    score = request.session.get('score', 0)  # Puntaje actual del jugador
    nickname = request.session.get('nickname')
    # Obtener el jugador de la base de datos
    jugador = Jugador.objects.get(nickname=nickname)
    # Valor booleano para evitar acumulacion
    nivelcompletado = request.session.get('nivelcompletado', False)

    # Inicializar el puntaje total desde la base de datos o desde la sesion
    totalpuntos = request.session.get('totalpuntos', 0)

    # Solo sumar el puntaje actual si no se ha procesado aun el nivel
    if nivelcompletado and totalpuntos == 0:
        totalpuntos += score
        request.session['totalpuntos'] = totalpuntos  # Guardar en la sesion
    elif not nivelcompletado and totalpuntos != 0:
        totalpuntos += score
        request.session['totalpuntos'] = totalpuntos

    # Verificar si el puntaje acumulado supera el maximo historico del jugador
    if totalpuntos > jugador.score:
        jugador.score = totalpuntos
        jugador.save()

    # Marcar el nivel como completado para evitar acumulacion
    request.session['nivelcompletado'] = True

    # Imagen cuando gane
    imagen_ahorcado = f"images/intentos/winner.png"

    return render(request, 'ganaste.html', {
        'cagegoria': request.session.get('categoria'),
        'nickname': nickname,
        'score': score,
        'totalpuntos': totalpuntos,
        'imagen_ahorcado': imagen_ahorcado,
    })


def record(request):
    jugadores = Jugador.objects.all()

    return render(request, 'record.html', {
        'jugadores': jugadores,
    })

#def borrar(request, nickname):
#    jugador = Jugador.objects.get(pk=nickname)
#    jugador.delete()

#    return render(request, 'record.html')
