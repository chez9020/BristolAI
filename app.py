from flask import Flask, render_template, request, session, redirect, url_for, Response
from openai import OpenAI
import os, requests

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY')
)

#client.images.
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/genero", methods=["POST"])
def genero():
    genero = request.form.get("genero")
    session['genero'] = genero
    return redirect(url_for("nombre"))

@app.route('/nombre', methods=["GET", "POST"])
def nombre():
    if request.method == 'POST':
        nombre = request.form.get("nombre")
        if not nombre:  # Verificar si el nombre está vacío
            # Mostrar un mensaje de error al usuario
            return render_template('nombre.html', error="Por favor, ingresa un nombre para el robot.") 
        
        nombre = nombre.capitalize()  # Formatear el nombre
        session['nombre'] = nombre  # Guardar el nombre en la sesión
        return redirect(url_for('personalidad')) 

    return render_template('nombre.html')

@app.route('/personalidad', methods=["GET", "POST"])
def personalidad():
    if request.method == 'POST':
        personalidad = request.form.get("personalidad")
        session['personalidad'] = personalidad
        return redirect(url_for('estilo'))  # Redirigir a la siguiente página
    return render_template('personalidad.html')

@app.route('/estilo', methods=["GET", "POST"])
def estilo():
    if request.method == 'POST':
        estilo = request.form.get("estilo")
        session['estilo'] = estilo
        return redirect(url_for('evento'))  # Redirigir a la siguiente página
    return render_template('estilo.html')

@app.route('/evento', methods=["GET", "POST"])
def evento():
    if request.method == 'POST':
        evento = request.form.get("evento")
        session['evento'] = evento
        return redirect(url_for('expertise'))  # Redirigir a la siguiente página
    return render_template('evento.html')

@app.route('/expertise', methods=["GET", "POST"])
def expertise():
    if request.method == 'POST':
        expertise = request.form.get("expertise")
        session['expertise'] = expertise
        return redirect(url_for('super_poder'))  # Redirigir a la siguiente página
    return render_template('expertise.html')

@app.route('/super_poder', methods=["GET", "POST"])
def super_poder():
    if request.method == 'POST':
        super_poder = request.form.get("super_poder")
        session['super_poder'] = super_poder
        return redirect(url_for('generar_imagen'))  # Redirigir a la siguiente página
    return render_template('super_poder.html')

@app.route("/generar_imagen", methods=["GET", "POST"])
def generar_imagen():
    imagen_url = None
    genero = session.get('genero')
    personalidad = session.get('personalidad')
    estilo = session.get('estilo')
    nombre = session.get('nombre')
    evento = session.get('evento')
    expertise = session.get('expertise')
    super_poder = session.get('super_poder')

    prompt_completo = f"Un androide futurista con rostro humanoide, manos con cinco dedos y una postura bípeda, de genero {genero}, con una actitud {personalidad}, con un estilo {estilo}, que le encante {evento}, haciendo {super_poder}, en un ambiente cosmos rosa concéntrate en los detalles visuales, no incluir ningún elemento textual"
    #    prompt_completo = f"Un robot futurista con rasgos humanos cyberpunk de genero {genero}, con una actitud {personalidad}, con un estilo {estilo}, que le encante {evento}, que sea experto en {expertise}, que tenga la habilidad de {super_poder} en un ambiente cosmos rosa"
    response = client.images.generate(
        model="dall-e-3",  # Modelo a utilizar
        prompt=prompt_completo,  # Usar el prompt completo con el género
        n=1,  # Número de imágenes a generar
        size="1024x1024"  # Tamaño de la imagen
    )

    imagen_url = response.data[0].url # Obtener la URL de la imagen

    return render_template("generar_imagen.html", imagen_url=imagen_url, nombre=nombre)

@app.route('/descargar_imagen', methods=['GET'])
def descargar_imagen():
    nombre = session.get('nombre')
    imagen_url = request.args.get('imagen_url')  # Obtener la URL de la imagen de la petición
    
    # Obtener la imagen desde la URL
    response = requests.get(imagen_url, stream=True)
    response.raise_for_status()  # Verificar si la petición fue exitosa

    # Devolver la imagen como respuesta con las cabeceras correctas
    return Response(
        response.iter_content(chunk_size=1024),
        mimetype=response.headers['Content-Type'],
        headers={'Content-Disposition': f'attachment; filename="{nombre}.png"'} 
    )

# if __name__ == "__main__":
#     app.run(debug=True)