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
