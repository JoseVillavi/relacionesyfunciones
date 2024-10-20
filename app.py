from flask import Flask, render_template, request, jsonify
import random
import string
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import io
import base64
import numpy as np

app = Flask(__name__)

# Variables globales para almacenar el estatus de la funcion
es_reflexiva_actual = False
es_irreflexiva_actual = False
es_simetrica_actual = False
es_antisimetrica_actual = False
es_transitiva_actual = False
es_intransitiva_actual = False


def generar_conjunto(n):
    """
    Genera un conjunto con n numero de elementos.

    """
    conjunto = set(random.sample(string.ascii_lowercase, n))
    return conjunto

# Funciones reflexivas
def generar_relacion_reflexiva(conjunto):
    """
    Genera una relacion reflexiva en base a el conjunto dado que se genera.

    """
    elementos = list(conjunto)
    relacion = set()
    
    for elemento in elementos:
        relacion.add((elemento, elemento))
    
    for _ in range(random.randint(0, len(elementos)**2 - len(elementos))):
        a = random.choice(elementos)
        b = random.choice(elementos)
        relacion.add((a, b))
    
    return relacion

def generar_relacion_no_reflexiva(conjunto):
    """
    Genera una relación no reflexiva sobre un conjunto dado.

    """
    elementos = list(conjunto)
    relacion = set()

    for elemento in elementos:
        if random.random() > 0.5:
            relacion.add((elemento, elemento))
    
    for _ in range(random.randint(1, len(elementos)**2)):
        a = random.choice(elementos)
        b = random.choice(elementos)
        relacion.add((a, b))
    
    for elemento in elementos:
        if (elemento, elemento) not in relacion:
            break
    else:
        relacion.remove(random.choice([r for r in relacion if r[0] == r[1]]))
    
    return relacion

@app.route('/generar', methods=['POST'])
def generar():
    """
    Genera a traves de esta funcion una relacion reflexiva o no y genera su imagen.

    """
    n = int(request.form['n'])
    conjunto = generar_conjunto(n)
    
    if random.random() < 0.5:
        relacion = generar_relacion_reflexiva(conjunto)
        global es_reflexiva_actual
        es_reflexiva_actual = True
    else:
        relacion = generar_relacion_no_reflexiva(conjunto)
        es_reflexiva_actual = False
    
    imagen = generar_imagen(conjunto, relacion)
    
    return jsonify({
        'conjunto': list(conjunto),
        'relacion': list(relacion),
        'imagen': imagen
    })

@app.route('/evaluar', methods=['POST'])
def evaluar():
    """
    Evalua la funcion para determinar si se trata de una relacion reflexiva o no y ademas proporciona la retroalimentacion.

    """
    respuesta_usuario = request.json['respuesta']
    correcto = respuesta_usuario == es_reflexiva_actual
    mensaje = "¡Correcto!, buen trabajo" if correcto else "Incorrecto. Recuerda que, una relación reflexiva contiene todos los pares del conjunto tipo (x,x), (y,y), (z,z), etc.."
    
    return jsonify({
        'correcto': correcto,
        'mensaje': mensaje
    })

# Relaciones irreflexivas
def generar_relacion_irreflexiva(conjunto):
    """
    Genera una relacion irreflexiva en base a el conjunto dado que se genera.

    """
    elementos = list(conjunto)
    relacion = set()

    for _ in range(random.randint(1, len(elementos)**2)):
        a = random.choice(elementos)
        b = random.choice(elementos)
        if a != b:
            relacion.add((a, b))

    return relacion

def es_irreflexiva(relacion, conjunto):
    """
    Verifica si la relación es irreflexiva o no
    
    """
    for elemento in conjunto:
        if (elemento, elemento) in relacion:
            return False
    return True

@app.route('/generar_irreflexiva', methods=['POST'])
def generar_irreflexiva():
    """
    Genera a traves de esta funcion una relacion irreflexiva o no y genera su imagen.

    """
    global es_irreflexiva_actual
    n = int(request.form['n'])
    conjunto = generar_conjunto(n)
    
    if random.random() < 0.5:
        relacion = generar_relacion_reflexiva(conjunto)
        es_irreflexiva_actual = False
    else:
        relacion = generar_relacion_irreflexiva(conjunto)
        es_irreflexiva_actual = True
    
    imagen = generar_imagen(conjunto, relacion)
    
    return jsonify({
        'conjunto': list(conjunto),
        'relacion': list(relacion),
        'imagen': imagen
    })

@app.route('/evaluar_irreflexiva', methods=['POST'])
def evaluar_irreflexiva():
    """
    Evalua la funcion para determinar si se trata de una relacion irreflexiva o no y ademas proporciona la retroalimentacion.

    """
    respuesta_usuario = request.json['respuesta']
    correcto = respuesta_usuario == es_irreflexiva_actual
    mensaje = "¡Correcto!, buen trabajo" if correcto else "Incorrecto. Recuerda que, una relación irreflexiva no contiene ni un par del conjunto, no debe contener (x,x), (y,y), (z,z), etc..."
    
    return jsonify({
        'correcto': correcto,
        'mensaje': mensaje
    })

# Relaciones simetricas
def generar_relacion_simetrica(conjunto):
    """
    Genera una relación simétrica sobre un conjunto dado
    
    """
    elementos = list(conjunto)
    relacion = set()

    for _ in range(random.randint(1, len(elementos)**2)):
        a = random.choice(elementos)
        b = random.choice(elementos)
        relacion.add((a, b))
        relacion.add((b, a))

    return relacion

def generar_relacion_no_simetrica(conjunto):
    """
    Genera una relación no simetrica sobre un conjunto dado.

    """
    elementos = list(conjunto)
    relacion = set()

    for _ in range(random.randint(1, len(elementos)**2)):
        a = random.choice(elementos)
        b = random.choice(elementos)
        relacion.add((a, b))

    return relacion

@app.route('/generar_simetrica', methods=['POST'])
def generar_simetrica():
    """
    Genera a traves de esta funcion una relacion simetrica o no y genera su imagen.

    """
    global es_simetrica_actual
    n = int(request.form['n'])
    conjunto = generar_conjunto(n)

    if random.random() < 0.5:
        relacion = generar_relacion_simetrica(conjunto)
        es_simetrica_actual = True
    else:
        relacion = generar_relacion_no_simetrica(conjunto)
        es_simetrica_actual = False

    imagen = generar_imagen(conjunto, relacion)

    return jsonify({
        'conjunto': list(conjunto),
        'relacion': list(relacion),
        'imagen': imagen
    })

@app.route('/evaluar_simetrica', methods=['POST'])
def evaluar_simetrica():
    """
    Evalua la funcion para determinar si se trata de una relacion simetrica o no y ademas proporciona la retroalimentacion.

    """
    respuesta_usuario = request.json['respuesta']
    tipo_actual = "simétrica" if es_simetrica_actual else "no simétrica"
    correcto = respuesta_usuario == (tipo_actual == "simétrica")
    mensaje = "¡Correcto!, buen trabajo" if correcto else "Incorrecto. Recuerda, para que una relación sea simétrica necesita tener el par opuesto siempre, por ejemplo si tenemos (a,b), necesitamos de (b,a)"
    
    return jsonify({
        'correcto': correcto,
        'mensaje': mensaje
    })

# Relaciones antisimétricas
def generar_relacion_antisimetrica(conjunto):
    """
    Genera una relación antisimétrica sobre un conjunto dado, asegurando que no existan pares (a, b) y (b, a) si a ≠ b.

    """
    elementos = list(conjunto)
    relacion = set()

    for _ in range(random.randint(1, len(elementos)**2)):
        a = random.choice(elementos)
        b = random.choice(elementos)

        if (b, a) not in relacion:
            if a != b:
                relacion.add((a, b))  
            relacion.add((a, a))

    return relacion


def generar_relacion_no_antisimetrica(conjunto):
    """
    Genera una relación no antisimétrica sobre un conjunto dado, donde para algún par (a, b) también existe (b, a).

    """
    elementos = list(conjunto)
    relacion = set()

    for _ in range(random.randint(1, len(elementos)**2)):
        a = random.choice(elementos)
        b = random.choice(elementos)
        
        relacion.add((a, b))
        relacion.add((b, a))

    return relacion


@app.route('/generar_antisimetrica', methods=['POST'])
def generar_antisimetrica():
    """
    Genera a través de esta función una relación antisimétrica o no antisimétrica y genera su imagen.

    """
    global es_antisimetrica_actual
    n = int(request.form['n'])
    conjunto = generar_conjunto(n)

    if random.random() < 0.5:
        relacion = generar_relacion_antisimetrica(conjunto)
        es_antisimetrica_actual = True
    else:
        relacion = generar_relacion_no_antisimetrica(conjunto)
        es_antisimetrica_actual = False

    imagen = generar_imagen(conjunto, relacion)

    return jsonify({
        'conjunto': list(conjunto),
        'relacion': list(relacion),
        'imagen': imagen
    })


@app.route('/evaluar_antisimetrica', methods=['POST'])
def evaluar_antisimetrica():
    """
    Evalúa la relación para determinar si es antisimétrica o no y proporciona retroalimentación.

    """
    respuesta_usuario = request.json['respuesta']
    correcto = respuesta_usuario == es_antisimetrica_actual
    mensaje = "¡Correcto! Buen trabajo." if correcto else "Incorrecto. Recuerda, una relación antisimétrica no puede tener ambos pares (a, b) y (b, a) si a ≠ b."

    return jsonify({
        'correcto': correcto,
        'mensaje': mensaje
    })

# Relaciones transitivas
def es_transitiva(relacion):
    """
    Verifica si una relación es transitiva.
    Si (a, b) y (b, c) están en la relación, entonces (a, c) debe estar en la relación.

    """
    for (a, b) in relacion:
        for (x, c) in relacion:
            if b == x and (a, c) not in relacion:
                return False
    return True

def generar_relacion_transitiva(conjunto):
    """
    Genera una relación 100% transitiva sobre un conjunto dado.

    """
    while True:
        elementos = list(conjunto)
        relacion = set()

        for _ in range(random.randint(1, len(elementos)**2)):
            a = random.choice(elementos)
            b = random.choice(elementos)
            relacion.add((a, b))

        for (a, b) in list(relacion):
            for (x, y) in list(relacion):
                if b == x:
                    relacion.add((a, y))

        if es_transitiva(relacion):
            return relacion

def generar_relacion_no_transitiva(conjunto):
    """
    Genera una relación 100% no transitiva sobre un conjunto dado.

    """
    while True:
        elementos = list(conjunto)
        relacion = set()

        for _ in range(random.randint(1, len(elementos)**2)):
            a = random.choice(elementos)
            b = random.choice(elementos)
            relacion.add((a, b))

        for (a, b) in list(relacion):
            for (x, y) in list(relacion):
                if b == x and (a, y) in relacion:
                    relacion.remove((a, y))

        if not es_transitiva(relacion):
            return relacion

@app.route('/generar_transitiva', methods=['POST'])
def generar_transitiva():
    """
    Genera a través de esta función una relación 100% transitiva o no transitiva y genera su imagen.

    """
    global es_transitiva_actual
    n = int(request.form['n'])
    conjunto = generar_conjunto(n)

    if random.random() < 0.5:
        relacion = generar_relacion_transitiva(conjunto)
        es_transitiva_actual = True
    else:
        relacion = generar_relacion_no_transitiva(conjunto)
        es_transitiva_actual = False

    imagen = generar_imagen(conjunto, relacion)

    return jsonify({
        'conjunto': list(conjunto),
        'relacion': list(relacion),
        'imagen': imagen
    })

@app.route('/evaluar_transitiva', methods=['POST'])
def evaluar_transitiva():
    """
    Evalúa la relación para determinar si es transitiva o no y proporciona retroalimentación.

    """
    respuesta_usuario = request.json['respuesta']
    tipo_actual = "transitiva" if es_transitiva_actual else "no transitiva"
    correcto = respuesta_usuario == (tipo_actual == "transitiva")
    mensaje = "¡Correcto! Buen trabajo." if correcto else "Incorrecto. Recuerda que, en una relación transitiva si tenemos: (a,b), (b,c), es necesario que tengamos (a,c)."

    return jsonify({
        'correcto': correcto,
        'mensaje': mensaje
    })

# Relaciones intransitivas
def generar_relacion_intransitiva(conjunto):
    """
    Genera una relación intransitiva sobre un conjunto dado.
    
    """
    elementos = list(conjunto)
    relacion = set()

    for _ in range(random.randint(1, len(elementos)**2)):
        a = random.choice(elementos)
        b = random.choice(elementos)
        if a != b:
            relacion.add((a, b))
            if (b, a) not in relacion:
                relacion.add((b, a))
    
    return relacion

def generar_relacion_no_intransitiva(conjunto):
    """
    Genera una relación no intransitiva sobre un conjunto dado.

    """
    elementos = list(conjunto)
    relacion = set()

    for _ in range(random.randint(1, len(elementos)**2)):
        a = random.choice(elementos)
        b = random.choice(elementos)
        relacion.add((a, b))

        for (x, y) in list(relacion):
            if y == a and (x, b) not in relacion:
                relacion.add((x, b))

    return relacion

@app.route('/generar_intransitiva', methods=['POST'])
def generar_intransitiva():
    """
    Genera a traves de esta funcion una relacion intransitiva o no y genera su imagen.

    """
    global es_intransitiva_actual
    n = int(request.form['n'])
    conjunto = generar_conjunto(n)

    if random.random() < 0.5:
        relacion = generar_relacion_intransitiva(conjunto)
        es_intransitiva_actual = True
    else:
        relacion = generar_relacion_no_intransitiva(conjunto)
        es_intransitiva_actual = False

    imagen = generar_imagen(conjunto, relacion)

    return jsonify({
        'conjunto': list(conjunto),
        'relacion': list(relacion),
        'imagen': imagen
    })

@app.route('/evaluar_intransitiva', methods=['POST'])
def evaluar_intransitiva():
    """
    Evalua la funcion para determinar si se trata de una relacion intransitiva o no y ademas proporciona la retroalimentacion.

    """
    respuesta_usuario = request.json['respuesta']
    tipo_actual = "intransitiva" if es_intransitiva_actual else "transitiva"
    correcto = respuesta_usuario == (tipo_actual == "intransitiva")
    mensaje = "¡Correcto! Buen trabajo." if correcto else "Incorrecto. Recuerda, para que una relación sea intransitiva, las relaciones no tendran pares tipo: (a,b), (b,c), (a,c)."
    
    return jsonify({
        'correcto': correcto,
        'mensaje': mensaje
    })

# Funcion inyectiva
def generar_funcion_inyectiva():
    """
    Genera una función inyectiva con un dominio y un codominio de tamaños variables.
    La relación será inyectiva (1-1), pero puede que no todos los elementos del dominio estén relacionados.

    """
    tamaño_dom = random.randint(4, 6)
    tamaño_cod = random.randint(4, 6)

    conjunto_dom = list(random.sample(string.ascii_lowercase, tamaño_dom))
    conjunto_cod = list(random.sample(string.ascii_lowercase, tamaño_cod))

    subconjunto_cod = random.sample(conjunto_cod, min(tamaño_dom, tamaño_cod))
    relacion = list(zip(conjunto_dom, subconjunto_cod))

    descripcion = f"Dominio: {conjunto_dom} Codominio: {conjunto_cod}"
    es_inyectiva = True

    return relacion, descripcion, es_inyectiva


def generar_funcion_no_inyectiva():
    """
    Genera una función no inyectiva con un dominio y un codominio de tamaños variables.

    """
    tamaño_dom = random.randint(4, 6)
    tamaño_cod = random.randint(4, 6)

    conjunto_dom = list(random.sample(string.ascii_lowercase, tamaño_dom))
    conjunto_cod = list(random.sample(string.ascii_lowercase, tamaño_cod))

    relacion = [(conjunto_dom[0], conjunto_cod[0]), (conjunto_dom[1], conjunto_cod[0])]
    for i in range(2, len(conjunto_dom)):
        relacion.append((conjunto_dom[i], conjunto_cod[i % len(conjunto_cod)]))

    descripcion = f"Dominio: {conjunto_dom} Codominio: {conjunto_cod}"
    es_inyectiva = False

    return relacion, descripcion, es_inyectiva


@app.route('/generar_inyectiva', methods=['POST'])
def generar_inyectiva():
    """
    Genera una función inyectiva o no inyectiva y devuelve su representación y gráfico.

    """
    if random.random() < 0.5:
        relacion, descripcion, es_inyectiva = generar_funcion_inyectiva()
    else:
        relacion, descripcion, es_inyectiva = generar_funcion_no_inyectiva()

    global es_inyectiva_actual
    es_inyectiva_actual = es_inyectiva

    imagen = generar_imagen_dominio_codonimo(relacion)

    relaciones_texto = ', '.join([f'({a} → {b})' for a, b in relacion])

    return jsonify({
        'descripcion': descripcion,
        'relacion_texto': relaciones_texto,
        'imagen': imagen,
        'es_inyectiva': es_inyectiva
    })


@app.route('/evaluar_inyectiva', methods=['POST'])
def evaluar_inyectiva():
    """
    Evalúa si la respuesta del usuario sobre la inyectividad es correcta y proporciona retroalimentación.
    """
    respuesta_usuario = request.json['respuesta']
    tipo_actual = "inyectiva" if es_inyectiva_actual else "no inyectiva"
    correcto = respuesta_usuario == (tipo_actual == "inyectiva")

    if correcto:
        mensaje = f"¡Correcto! La función es {tipo_actual}. "
        if tipo_actual == "inyectiva":
            mensaje += "Una función es inyectiva si cada valor del dominio tiene una imagen única en el codominio."
        else:
            mensaje += "Esta función no es inyectiva porque dos valores del dominio tienen la misma imagen en el codominio."
    else:
        mensaje = f"Incorrecto. La función es {tipo_actual}. "
        if tipo_actual == "inyectiva":
            mensaje += "Recuerda que en una función inyectiva, no hay dos valores diferentes del dominio que tengan la misma imagen."
        else:
            mensaje += "En una función no inyectiva, dos o más elementos del dominio pueden tener la misma imagen en el codominio."

    return jsonify({
        'correcto': correcto,
        'mensaje': mensaje
    })

# Funcion sobreyectiva
def generar_funcion_sobreyectiva():
    """
    Genera una función sobreyectiva con un dominio y un codominio de tamaños variables.
    En este caso, todos los elementos del codominio tendrán al menos una relación con el dominio.

    """
    tamaño_dom = random.randint(4, 6)
    tamaño_cod = random.randint(4, 6)

    conjunto_dom = list(random.sample(string.ascii_lowercase, tamaño_dom))
    conjunto_cod = list(random.sample(string.ascii_lowercase, tamaño_cod))

    subconjunto_dom = random.choices(conjunto_dom, k=tamaño_cod)
    relacion = list(zip(subconjunto_dom, conjunto_cod))

    descripcion = f"Dominio: {conjunto_dom} Codominio: {conjunto_cod}"
    es_sobreyectiva = True

    return relacion, descripcion, es_sobreyectiva


def generar_funcion_no_sobreyectiva():
    """
    Genera una función no sobreyectiva con un dominio y un codominio de tamaños variables.
    En este caso, no todos los elementos del codominio tendrán una relación con el dominio.

    """
    tamaño_dom = random.randint(4, 6)
    tamaño_cod = random.randint(4, 6)

    conjunto_dom = list(random.sample(string.ascii_lowercase, tamaño_dom))
    conjunto_cod = list(random.sample(string.ascii_lowercase, tamaño_cod))

    subconjunto_cod = random.sample(conjunto_cod, random.randint(1, tamaño_cod - 1))
    subconjunto_dom = random.choices(conjunto_dom, k=len(subconjunto_cod))
    relacion = list(zip(subconjunto_dom, subconjunto_cod))

    descripcion = f"Dominio: {conjunto_dom} Codominio: {conjunto_cod}"
    es_sobreyectiva = False

    return relacion, descripcion, es_sobreyectiva


@app.route('/generar_sobreyectiva', methods=['POST'])
def generar_sobreyectiva():
    """
    Genera una función sobreyectiva o no sobreyectiva y devuelve su representación y gráfico.

    """
    if random.random() < 0.5:
        relacion, descripcion, es_sobreyectiva = generar_funcion_sobreyectiva()
    else:
        relacion, descripcion, es_sobreyectiva = generar_funcion_no_sobreyectiva()

    global es_sobreyectiva_actual
    es_sobreyectiva_actual = es_sobreyectiva

    imagen = generar_imagen_dominio_codonimo(relacion)

    relaciones_texto = ', '.join([f'({a} → {b})' for a, b in relacion])

    return jsonify({
        'descripcion': descripcion,
        'relacion_texto': relaciones_texto,
        'imagen': imagen,
        'es_sobreyectiva': es_sobreyectiva
    })


@app.route('/evaluar_sobreyectiva', methods=['POST'])
def evaluar_sobreyectiva():
    """
    Evalúa si la respuesta del usuario sobre la sobreyectividad es correcta y proporciona retroalimentación.
    """
    respuesta_usuario = request.json['respuesta']
    tipo_actual = "sobreyectiva" if es_sobreyectiva_actual else "no sobreyectiva"
    correcto = respuesta_usuario == (tipo_actual == "sobreyectiva")

    if correcto:
        mensaje = f"¡Correcto! La función es {tipo_actual}. "
        if tipo_actual == "sobreyectiva":
            mensaje += "Una función es sobreyectiva si cada elemento del codominio tiene al menos una preimagen en el dominio."
        else:
            mensaje += "Esta función no es sobreyectiva porque no cubre todo el codominio."
    else:
        mensaje = f"Incorrecto. La función es {tipo_actual}. "
        if tipo_actual == "sobreyectiva":
            mensaje += "Recuerda que en una función sobreyectiva, cada elemento del codominio tiene al menos una preimagen."
        else:
            mensaje += "En una función no sobreyectiva, algunos elementos del codominio no tienen preimagen en el dominio."

    return jsonify({
        'correcto': correcto,
        'mensaje': mensaje
    })

# Funcion biyectiva
def generar_funcion_biyectiva():
    """
    Genera una funcion biyectiva, mediante su dominio y codominio.
    
    """
    conjunto_dom = list(random.sample(string.ascii_lowercase, 5))
    conjunto_cod = list(random.sample(string.ascii_lowercase, 5))

    relacion = list(zip(conjunto_dom, conjunto_cod))
    descripcion = f"Dominio: {conjunto_dom} Codominio: {conjunto_cod}"
    es_biyectiva = True

    return relacion, descripcion, es_biyectiva

def generar_funcion_no_biyectiva():
    """
    Genera una funcion biyectiva, mediante su dominio y codominio.

    """
    conjunto_dom = list(random.sample(string.ascii_lowercase, 5))
    conjunto_cod = list(random.sample(string.ascii_lowercase, 5))

    relacion = [(conjunto_dom[0], conjunto_cod[0]), (conjunto_dom[1], conjunto_cod[0])]
    for i in range(2, len(conjunto_dom)):
        relacion.append((conjunto_dom[i], conjunto_cod[i]))
    
    descripcion = f"Dominio: {conjunto_dom} Codominio: {conjunto_cod}"
    es_biyectiva = False

    return relacion, descripcion, es_biyectiva

@app.route('/generar_biyectiva', methods=['POST'])
def generar_biyectiva():
    """
    Genera a traves de esta funcion una funcion biyectiva o no y genera su imagen.

    """
    if random.random() < 0.5:
        relacion, descripcion, es_biyectiva = generar_funcion_biyectiva()
    else:
        relacion, descripcion, es_biyectiva = generar_funcion_no_biyectiva()

    global es_biyectiva_actual
    es_biyectiva_actual = es_biyectiva

    imagen = generar_imagen_dominio_codonimo(relacion)

    relaciones_texto = ', '.join([f'({a} → {b})' for a, b in relacion])

    return jsonify({
        'descripcion': descripcion,
        'relacion_texto': relaciones_texto,
        'imagen': imagen,
        'es_biyectiva': es_biyectiva
    })


@app.route('/evaluar_biyectiva', methods=['POST'])
def evaluar_biyectiva():
    """
    Evalua la funcion para determinar si se trata de una funcion biyectiva o no y ademas proporciona la retroalimentacion.

    """
    respuesta_usuario = request.json['respuesta']
    tipo_actual = "biyectiva" if es_biyectiva_actual else "no biyectiva"
    correcto = respuesta_usuario == (tipo_actual == "biyectiva")

    if correcto:
        mensaje = f"¡Correcto! La función es {tipo_actual}. "
        if tipo_actual == "biyectiva":
            mensaje += "Una función es biyectiva si es tanto inyectiva como sobreyectiva. Cada elemento del dominio tiene una imagen única en el codominio y cubre todo el codominio."
        else:
            mensaje += "Esta función no es biyectiva porque o no es inyectiva (algunos elementos del dominio apuntan al mismo del codominio) o no es sobreyectiva (no cubre todo el codominio)."
    else:
        mensaje = f"Incorrecto. La función es {tipo_actual}. "
        if tipo_actual == "biyectiva":
            mensaje += "Recuerda, una función biyectiva cubre todo el codominio y no repite valores para diferentes elementos del dominio."
        else:
            mensaje += "En una función no biyectiva, podría haber elementos del dominio que compartan la misma imagen o no cubrir todo el codominio."

    return jsonify({
        'correcto': correcto,
        'mensaje': mensaje
    })

# imagenes
def generar_imagen(conjunto, relacion):
    """
    Funcion para decidir si la grafica que se genera en las relaciones será un plano cartesiano o un grafo.
    
    """
    if random.random() < 0.5:
        return generar_grafo(conjunto, relacion)
    else:
        return generar_plano_cartesiano(conjunto, relacion)

def generar_grafo(conjunto, relacion):
    """
    Funcion que genera un grafo, solo en caso de las relaciones.

    """
    G = nx.DiGraph()
    G.add_nodes_from(conjunto)
    G.add_edges_from(relacion)
    
    plt.figure(figsize=(6, 5))
    
    pos = nx.spring_layout(G, k=0.5)
    
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    reflexive_edges = [(a, b) for a, b in relacion if a == b]
    non_reflexive_edges = [(a, b) for a, b in relacion if a != b]
    
    nx.draw_networkx_edges(G, pos, edgelist=non_reflexive_edges, arrowsize=10, connectionstyle='arc3,rad=0.1', 
                           min_source_margin=15, min_target_margin=15)
    
    nx.draw_networkx_edges(G, pos, edgelist=reflexive_edges, arrowsize=10, connectionstyle='arc3,rad=1.5', 
                           min_source_margin=15, min_target_margin=15, width=2)
    
    return guardar_imagen()

def generar_plano_cartesiano(conjunto, relacion):
    """
    Funcion que genera un plano cartesiano, solo en caso de las relaciones.
    
    """
    plt.figure(figsize=(10, 6))
    
    letras_relacionadas = set(b for a, b in relacion).union(set(a for a, b in relacion))
    
    conjunto_ordenado = sorted(conjunto)
    relacionadas_ordenadas = sorted(letras_relacionadas)
    
    indices_x = {letra: idx for idx, letra in enumerate(conjunto_ordenado)}
    indices_y = {letra: idx for idx, letra in enumerate(relacionadas_ordenadas)}
    
    plt.xlim(-1, len(conjunto_ordenado))
    plt.ylim(-1, len(relacionadas_ordenadas))
    
    plt.xticks(range(len(conjunto_ordenado)), conjunto_ordenado)
    plt.yticks(range(len(relacionadas_ordenadas)), relacionadas_ordenadas)
    
    for (a, b) in relacion:
        plt.plot([indices_x[a], indices_x[a]], [indices_y[b], indices_y[b]], 'ro-')

    plt.grid(True)
    return guardar_imagen()

def generar_imagen_dominio_codonimo(relacion):
    """
    Generar plano cartesiado del dominio y codominio, con sus puntos en las relaciones. Funcion solo para funciones.

    """
    import matplotlib.pyplot as plt

    dominio = [r[0] for r in relacion]
    codominio = [r[1] for r in relacion]

    conjunto_dom = sorted(set(dominio))
    conjunto_cod = sorted(set(codominio))

    indices_dom = {letra: idx for idx, letra in enumerate(conjunto_dom)}
    indices_cod = {letra: idx for idx, letra in enumerate(conjunto_cod)}

    plt.figure(figsize=(10, 6))

    for (a, b) in relacion:
        plt.plot([indices_dom[a], indices_dom[a]], [indices_cod[b], indices_cod[b]], 'ro-')

    plt.xlim(-1, len(conjunto_dom))
    plt.ylim(-1, len(conjunto_cod))

    plt.xticks(range(len(conjunto_dom)), conjunto_dom)
    plt.yticks(range(len(conjunto_cod)), conjunto_cod)

    plt.grid(True)

    return guardar_imagen()

def guardar_imagen():
    """
    Guarda la imagen generada, ya sea de plano cartesiano o de grafo, para poder mostrarla en la pantalla, esta se usa en las relaciones y en las funciones.
    
    """
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    return f"data:image/png;base64,{base64.b64encode(img.getvalue()).decode()}"

#Rutas a cada una de las paginas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pagina1')
def pagina1():
    return render_template('pagina1.html')

@app.route('/pagina2')
def pagina2():
    return render_template('pagina2.html')

@app.route('/pagina3')
def pagina3():
    return render_template('pagina3.html')

@app.route('/pagina4')
def pagina4():
    return render_template('pagina4.html')

@app.route('/pagina5')
def pagina5():
    return render_template('pagina5.html')

@app.route('/pagina6')
def pagina6():
    return render_template('pagina6.html')

@app.route('/pagina7')
def pagina7():
    return render_template('pagina7.html')

@app.route('/pagina8')
def pagina8():
    return render_template('pagina8.html')

@app.route('/pagina9')
def pagina9():
    return render_template('pagina9.html')

if __name__ == '__main__':
    app.run(debug=True)
