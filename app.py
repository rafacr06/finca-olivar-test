
import streamlit as st
import pandas as pd
from openai import OpenAI
from openpyxl import load_workbook
from io import BytesIO
import os

# Configuraci贸n de la app
st.set_page_config(page_title="Gesti贸n Finca de Olivar", layout="wide")
st.title("馃尶 Gesti贸n Integral de Finca de Olivar")

# Cargar clave API de OpenAI
api_key = st.sidebar.text_input("馃攽 Clave API de OpenAI", type="password")

# Nombre del archivo Excel
EXCEL_FILE = "finca_olivar_datos.xlsx"

# Funci贸n para cargar o crear archivo Excel
def cargar_datos():
    if os.path.exists(EXCEL_FILE):
        xls = pd.read_excel(EXCEL_FILE, sheet_name=None)
    else:
        xls = {
            "Finca": pd.DataFrame(columns=["ID Parcela", "Nombre", "Variedad", "Hect谩reas", "Marco", "Riego"]),
            "Labores": pd.DataFrame(columns=["Fecha", "Parcela", "Tipo", "Descripci贸n", "Operario", "Horas", "Costo (鈧?"]),
            "Costes": pd.DataFrame(columns=["Fecha", "Categor铆a", "Descripci贸n", "Importe (鈧?", "Relacionado con"]),
            "Ingresos": pd.DataFrame(columns=["Fecha", "Concepto", "Descripci贸n", "Importe (鈧?", "Tipo"]),
            "Inventario": pd.DataFrame(columns=["Producto", "Inicial", "Entrada", "Salida", "Stock", "Unidad"]),
            "Rentabilidad": pd.DataFrame(columns=["Parcela", "Campa帽a", "Ingresos (鈧?", "Costes (鈧?", "Margen (鈧?", "Margen 鈧?ha"])
        }
    return xls

def guardar_datos(xls):
    with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl") as writer:
        for sheet, df in xls.items():
            df.to_excel(writer, sheet_name=sheet, index=False)

# Cargar datos actuales
datos = cargar_datos()

# Tabs principales
menu = st.sidebar.radio("Men煤", list(datos.keys()) + ["GPT Analista"])

# Interfaz para cada hoja
def mostrar_editor(nombre_hoja):
    df = datos[nombre_hoja]
    st.subheader(f"馃搵 {nombre_hoja}")
    st.dataframe(df, use_container_width=True)

    with st.expander("鉃?Agregar nuevo registro"):
        columnas = df.columns.tolist()
        nuevo = {}
        for col in columnas:
            nuevo[col] = st.text_input(f"{col}", key=f"{nombre_hoja}_{col}")
        if st.button(f"Guardar en {nombre_hoja}", key=f"guardar_{nombre_hoja}"):
            datos[nombre_hoja] = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            guardar_datos(datos)
            st.success("Registro guardado correctamente.")
            st.experimental_rerun()

# GPT
if menu == "GPT Analista":
    st.subheader("馃 Consulta a GPT tus datos agr铆colas")
    if not api_key:
        st.warning("Introduce tu clave API de OpenAI en la barra lateral.")
    else:
        pregunta = st.text_area("Haz tu pregunta sobre la finca, costes, rentabilidad, etc.")
        if st.button("Preguntar") and pregunta:
            resumen = ""
            for hoja, df in datos.items():
                resumen += f"\n\n[{hoja}]\n{df.to_string(index=False)}"
            prompt = f"""
Eres un asesor agr铆cola que trabaja con los siguientes datos de una finca olivarera:
{resumen}

Responde a esta pregunta de forma clara y profesional:
{pregunta}
"""
            try:
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Eres un experto en gesti贸n contable y agron贸mica de fincas."},
                        {"role": "user", "content": prompt}
                    ]
                )
                st.success("Respuesta de GPT:")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {str(e)}")
else:
    mostrar_editor(menu)
