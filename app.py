import streamlit as st
import pandas as pd
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

def guardar_datos(datos):
    with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl") as writer:
        for nombre, df in datos.items():
            df.to_excel(writer, sheet_name=nombre, index=False)

# Cargar o inicializar datos
if "datos" not in st.session_state:
    st.session_state["datos"] = cargar_datos()

datos = st.session_state["datos"]

# Menú lateral
menu = st.sidebar.selectbox("📘 ¿Qué quieres gestionar?", list(datos.keys()) + ["Ver resumen de todo"])

# Editor por sección
def editor(nombre_hoja):
    st.subheader(f"📋 Gestión de {nombre_hoja}")
    df = datos[nombre_hoja]

    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No hay datos registrados todavía.")

    st.markdown("---")
    st.markdown("### ➕ Añadir nuevo registro")
    columnas = df.columns.tolist()
    nuevo = {}
    columnas_ui = st.columns(2)
    for i, col in enumerate(columnas):
        nuevo[col] = columnas_ui[i % 2].text_input(col, key=f"{nombre_hoja}_{col}")

    if st.button(f"Guardar en {nombre_hoja}"):
        nuevo_df = pd.DataFrame([nuevo])
        datos[nombre_hoja] = pd.concat([df, nuevo_df], ignore_index=True)
        guardar_datos(datos)
        st.success("✅ Guardado correctamente.")
        st.rerun()

# Vista
if menu == "Ver resumen de todo":
    st.header("📊 Resumen general de la finca")
    for nombre_hoja, df in datos.items():
        with st.expander(f"📁 {nombre_hoja} ({len(df)} registros)"):
            if df.empty:
                st.write("No hay datos todavía.")
            else:
                st.dataframe(df, use_container_width=True, hide_index=True)
else:
    editor(menu)
