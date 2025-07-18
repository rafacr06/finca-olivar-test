import streamlit as st
import pandas as pd
import os
from io import BytesIO
import openpyxl

st.set_page_config(page_title="Gestión de Finca de Olivar", layout="wide")

ARCHIVO_EXCEL = "finca_olivar_datos.xlsx"

SECCIONES = ["Finca", "Labores", "Costes", "Ingresos", "Inventario", "Rentabilidad", "Resumen"]

# Leer hoja desde Excel
def cargar_hoja(nombre_hoja):
    if os.path.exists(ARCHIVO_EXCEL):
        df = pd.read_excel(ARCHIVO_EXCEL, sheet_name=nombre_hoja)
        return df
    else:
        return pd.DataFrame()

# Guardar hoja en Excel
def guardar_hoja(nombre_hoja, df):
    with pd.ExcelWriter(ARCHIVO_EXCEL, mode="a" if os.path.exists(ARCHIVO_EXCEL) else "w", engine="openpyxl", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name=nombre_hoja, index=False)

# Inicializar variedades conocidas
VARIEDADES_CONOCIDAS = ["Picual", "Arbequina", "Hojiblanca", "Cornicabra", "Manzanilla"]

# Gestión de finca
def gestion_finca():
    st.markdown("## 📋 Gestión de Finca")

    df = cargar_hoja("Finca")

    st.markdown("### 📄 Datos actuales")
    if not df.empty:
        selected_idx = st.selectbox("Selecciona un registro para borrar:", df.index, format_func=lambda x: f"ID {df.loc[x, 'ID Parcela']} - {df.loc[x, 'Nombre']}")
        if st.button("🗑️ Borrar registro seleccionado"):
            df = df.drop(selected_idx)
            guardar_hoja("Finca", df)
            st.success("Registro eliminado correctamente")
            st.experimental_rerun()

        st.dataframe(df, use_container_width=True)
    else:
        st.info("No hay datos registrados aún.")

    st.markdown("---")
    st.markdown("### ➕ Añadir nuevo registro")

    # ID automático
    nuevo_id = (df["ID Parcela"].astype(str).str.extract(r'(\d+)').dropna().astype(int).max()[0] + 1) if not df.empty else 1

    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre")
    with col2:
        variedad = st.selectbox("Variedad", VARIEDADES_CONOCIDAS + ["Otra"])

    col3, col4 = st.columns(2)
    with col3:
        hectareas = st.number_input("Hectáreas", min_value=0.0, step=0.1)
    with col4:
        riego = st.selectbox("Riego", ["sí", "no"])

    num_olivos = st.text_input("Número total de olivos")

    if st.button("💾 Guardar en Finca"):
        nuevo_registro = pd.DataFrame({
            "ID Parcela": [nuevo_id],
            "Nombre": [nombre],
            "Variedad": [variedad],
            "Hectáreas": [hectareas],
            "Marco": [num_olivos],
            "Riego": [riego]
        })
        df = pd.concat([df, nuevo_registro], ignore_index=True)
        guardar_hoja("Finca", df)
        st.success("Guardado correctamente.")
        st.experimental_rerun()

# Interfaz principal
st.title("🌿 Aplicación sencilla para gestionar tu finca de olivar")
st.caption("Diseñada para ser fácil, clara y útil para agricultores")

menu = st.sidebar.radio("📌 ¿Qué quieres gestionar?", SECCIONES)

if menu == "Finca":
    gestion_finca()
else:
    st.info(f"Funcionalidad '{menu}' en desarrollo.")


