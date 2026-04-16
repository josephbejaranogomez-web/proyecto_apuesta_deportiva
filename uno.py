from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# 🔹 Base de datos simulada
usuarios = []

eventos = [
    {"id": 1, "equipos": "Barcelona vs Madrid"},
    {"id": 2, "equipos": "PSG vs Bayern"},
    {"id": 3, "equipos": "Liverpool vs Chelsea"}
]

# 🔹 LOGIN
@app.route('/')
def inicio():
    return render_template_string('''
    <html>
    <head>
        <title>Login</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>

    <body class="bg-dark text-white">
    <div class="container mt-5">
        <div class="card p-4 mx-auto shadow" style="max-width:400px;">
            <h3 class="text-center">⚽ Predictor Deportivo</h3>

            <form action="/login" method="post">
                <input class="form-control mb-3" type="text" name="correo" placeholder="Correo">
                <input class="form-control mb-3" type="password" name="password" placeholder="Contraseña">
                <button class="btn btn-primary w-100">Ingresar</button>
            </form>

            <a href="/registro" class="mt-3 text-center">Registrarse</a>
        </div>
    </div>
    </body>
    </html>
    ''')

# 🔹 REGISTRO
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        usuarios.append({"correo": correo, "password": password})
        return redirect(url_for('inicio'))

    return render_template_string('''
    <html>
    <head>
        <title>Registro</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>

    <body class="bg-light">
    <div class="container mt-5">
        <div class="card p-4 mx-auto shadow" style="max-width:400px;">
            <h3 class="text-center">Registro</h3>

            <form method="post">
                <input class="form-control mb-3" type="text" name="correo" placeholder="Correo">
                <input class="form-control mb-3" type="password" name="password" placeholder="Contraseña">
                <button class="btn btn-success w-100">Registrar</button>
            </form>
        </div>
    </div>
    </body>
    </html>
    ''')

# 🔹 LOGIN PROCESO
@app.route('/login', methods=['POST'])
def login():
    correo = request.form['correo']
    password = request.form['password']

    for u in usuarios:
        if u['correo'] == correo and u['password'] == password:
            return redirect(url_for('dashboard'))

    return "<h3>❌ Error en login</h3>"

# 🔹 DASHBOARD
@app.route('/dashboard')
def dashboard():
    return render_template_string('''
    <html>
    <head>
        <title>Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>

    <body class="bg-light">
    <div class="container mt-5">
        <h2 class="mb-4">⚽ Eventos Deportivos</h2>

        <div class="row">
        {% for evento in eventos %}
            <div class="col-md-4">
                <div class="card p-3 mb-3 shadow">
                    <h5>{{ evento.equipos }}</h5>
                    <a href="/prediccion/{{ evento.id }}" class="btn btn-success mt-2">Ver predicción</a>
                </div>
            </div>
        {% endfor %}
        </div>

        <a href="/simulador" class="btn btn-dark">Ir al simulador</a>
    </div>
    </body>
    </html>
    ''', eventos=eventos)

# 🔹 PREDICCIÓN
@app.route('/prediccion/<int:id>')
def prediccion(id):
    resultado = {
        "gana_local": 65,
        "empate": 20,
        "gana_visitante": 15
    }

    return render_template_string('''
    <html>
    <head>
        <title>Predicción</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>

    <body class="bg-light">
    <div class="container mt-5">
        <div class="card p-4 shadow">
            <h3>📊 Predicción del Partido</h3>

            <p>Gana local: <b>{{ r.gana_local }}%</b></p>
            <p>Empate: <b>{{ r.empate }}%</b></p>
            <p>Gana visitante: <b>{{ r.gana_visitante }}%</b></p>

            <a href="/dashboard" class="btn btn-secondary">Volver</a>
        </div>
    </div>
    </body>
    </html>
    ''', r=resultado)

# 🔹 SIMULADOR
@app.route('/simulador', methods=['GET', 'POST'])
def simulador():
    ganancia = None

    if request.method == 'POST':
        apuesta = int(request.form['apuesta'])
        ganancia = apuesta * 1.65

    return render_template_string('''
    <html>
    <head>
        <title>Simulador</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>

    <body class="bg-light">
    <div class="container mt-5">
        <div class="card p-4 shadow">
            <h3>💰 Simulador de Apuestas</h3>

            <form method="post">
                <input class="form-control mb-3" type="number" name="apuesta" placeholder="Ingrese apuesta">
                <button class="btn btn-primary">Calcular</button>
            </form>

            {% if ganancia %}
                <div class="alert alert-success mt-3">
                    Ganancia estimada: {{ ganancia }}
                </div>
            {% endif %}

            <a href="/dashboard" class="btn btn-secondary">Volver</a>
        </div>
    </div>
    </body>
    </html>
    ''', ganancia=ganancia)

# 🔹 EJECUCIÓN
if __name__ == '__main__':
    app.run(debug=True)