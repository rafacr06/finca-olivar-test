
import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import os

st.set_page_config(page_title="Gestión Finca de Olivar", layout="wide")
st.markdown("""
<style>
    .main {background-color: #f4f4f4; padding: 1rem;}
    .block-container {padding: 2rem 2rem;}
    h1 {color: #2E7D32;}
    .stButton>button {background-color: #4CAF50; color: white; border-radius: 8px; height: 2.5em;}
</style>
""", unsafe_allow_html=True)

st.title("🌿 Aplicación sencilla para gestionar tu finca de olivar")
st.caption("Diseñada para ser fácil, clara y útil para agricultores")

EXCEL_FILE = "finca_olivar_datos.xlsx"

def cargar_datos():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE, sheet_name=None)
    else:
        return {
            "Finca": pd.DataFrame(columns=["ID Parcela", "Nombre", "Variedad", "Hectáreas", "Marco", "Riego"]),
            "Labores": pd.DataFrame(columns=["Fecha", "Parcela", "Tipo", "Descripción", "Operario", "Horas", "Costo (€)"]),
            "Costes": pd.DataFrame(columns=["Fecha", "Categoría", "Descripción", "Importe (€)", "Relacionado con"]),
            "Ingresos": pd.DataFrame(columns=["Fecha", "Concepto", "Descripción", "Importe (€)", "Tipo"]),
            "Inventario": pd.DataFrame(columns=["Producto", "Inicial", "Entrada", "Salida", "Stock", "Unidad"]),
            "Rentabilidad": pd.DataFrame(columns=["Parcela", "Campaña", "Ingresos (€)", "Costes (€)", "Margen (€)", "Margen €/ha"])
        }

def guardar_datos(xls):
    with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl") as writer:
        for sheet, df in xls.items():
            df.to_excel(writer, sheet_name=sheet, index=False)

if "guardado" not in st.session_state:
    st.session_state["guardado"] = False

datos = cargar_datos()

menu = st.sidebar.selectbox("📘 ¿Qué quieres gestionar?", list(datos.keys()) + ["Ver resumen de todo"])

def mostrar_editor(nombre_hoja):
    st.subheader(f"📋 Gestión de {nombre_hoja}")
    df = datos[nombre_hoja]

    if st.session_state["guardado"]:
        datos = cargar_datos()
        df = datos[nombre_hoja]
        st.session_state["guardado"] = False

    if df.empty:
        st.info("No hay datos registrados todavía.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### ➕ Añadir un nuevo dato")
    columnas = df.columns.tolist()
    nuevo = {}
    cols = st.columns(2)
    for i, col in enumerate(columnas):
        nuevo[col] = cols[i % 2].text_input(col, key=f"{nombre_hoja}_{col}")

    if st.button(f"Guardar en {nombre_hoja}", key=f"guardar_{nombre_hoja}"):
        datos[nombre_hoja] = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
        guardar_datos(datos)
        st.success("✅ Guardado correctamente.")
        st.session_state["guardado"] = True
        st.experimental_rerun()

if menu == "Ver resumen de todo":
    st.header("📊 Resumen general de la finca")
    for hoja, df in datos.items():
        with st.expander(f"📁 {hoja} ({len(df)} registros)"):
            if df.empty:
                st.write("No hay datos todavía.")
            else:
                st.dataframe(df, use_container_width=True, hide_index=True)
else:
    mostrar_editor(menu)
