# Pasos 01 a 08 – Proyecto Botón de Consultas de Aguinaldos

## 🧩 Objetivo del proyecto

Construir una aplicación web Flask que permita consultar datos por RUT desde un archivo Excel (`aguinaldos.xlsx`), con validación real del RUT chileno.

---

## ✅ Paso 01 – Estructura base del proyecto

boton_consultas_aguinaldos/
├── app/
│ ├── init.py
│ ├── routes.py
│ ├── forms.py
│ ├── utils.py
│ └── templates/
│ └── consulta.html
├── data/
│ └── aguinaldos.xlsx
├── run.py
├── .env
└── requirements.txt

yaml
Copiar
Editar

---

## ✅ Paso 02 – Archivo principal `run.py`

```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

✅ Paso 03 – Inicialización de la app en __init__.py
python
Copiar
Editar
from flask import Flask
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'clave-secreta-segura'
    csrf.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    return app

✅ Paso 04 – Rutas principales en routes.py

from flask import Blueprint, render_template
from app.forms import ConsultaForm
from app.utils import buscar_datos_por_rut

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def home():
    form = ConsultaForm()
    resultado = None

    if form.validate_on_submit():
        rut = form.rut.data
        resultado = buscar_datos_por_rut(rut)

    return render_template('consulta.html', form=form, resultado=resultado)

✅ Paso 05 – Formulario en forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.utils import validar_rut

class ConsultaForm(FlaskForm):
    rut = StringField('Ingrese su RUT', validators=[DataRequired()])
    submit = SubmitField('Consultar')

    def validate_rut(self, field):
        if not validar_rut(field.data):
            raise ValidationError('RUT inválido. Verifique el dígito verificador.')

✅ Paso 06 – Plantilla HTML consulta.html

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Consulta de Aguinaldos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f2f5;
            padding: 40px;
        }
        .container {
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .error { color: red; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Consulta de Aguinaldos</h2>
        <form method="POST">
            {{ form.hidden_tag() }}
            <p>
                {{ form.rut.label }}<br>
                {{ form.rut(size=40) }}
                {% for error in form.rut.errors %}
                    <div class="error">{{ error }}</div>
                {% endfor %}
            </p>
            <p>{{ form.submit(class="btn") }}</p>
        </form>

        {% if resultado %}
            <hr>
            <p><strong>Nombre:</strong> {{ resultado['Nombre'] }}</p>
            <p><strong>Monto Aguinaldo:</strong> ${{ "{:,.0f}".format(resultado['Monto']) }}</p>
        {% elif form.rut.data %}
            <hr>
            <p style="color: red;">No se encontró información para el RUT ingresado.</p>
        {% endif %}
    </div>
</body>
</html>

✅ Paso 07 – Validación de RUT en utils.py
python
Copiar
Editar
def validar_rut(rut: str) -> bool:
    rut = rut.upper().replace("-", "").replace(".", "")
    if not rut[:-1].isdigit():
        return False

    cuerpo = rut[:-1]
    dv = rut[-1]

    suma = 0
    factores = [2, 3, 4, 5, 6, 7]
    factor_index = 0

    for c in reversed(cuerpo):
        suma += int(c) * factores[factor_index]
        factor_index = (factor_index + 1) % len(factores)

    resto = suma % 11
    digito = 11 - resto

    if digito == 11:
        dv_esperado = '0'
    elif digito == 10:
        dv_esperado = 'K'
    else:
        dv_esperado = str(digito)

    return dv == dv_esperado

✅ Paso 08 – Búsqueda de datos por RUT en utils.py
python
Copiar
Editar
import os
import pandas as pd

def buscar_datos_por_rut(rut_usuario: str):
    ruta = os.path.join('data', 'aguinaldos.xlsx')
    if not os.path.exists(ruta):
        print("⚠️ Archivo Excel no encontrado")
        return None

    try:
        df = pd.read_excel(ruta)
        df['RUT'] = df['RUT'].astype(str).str.upper().str.replace(".", "", regex=False)

        rut_usuario = rut_usuario.upper().replace(".", "")
        resultado = df[df['RUT'] == rut_usuario]

        if not resultado.empty:
            return resultado.iloc[0].to_dict()
        else:
            return None
    except Exception as e:
        print(f"❌ Error leyendo archivo: {e}")
        return None






