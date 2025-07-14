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
