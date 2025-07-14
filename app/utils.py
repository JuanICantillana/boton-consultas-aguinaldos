import os
import pandas as pd

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


def buscar_datos_por_rut(rut_usuario: str):
    """
    Busca en 'data/aguinaldos.xlsx' por el RUT exacto.
    Retorna un dict con los datos si existe, o None.
    """
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
