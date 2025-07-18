
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Gestión Olivar", layout="wide")

archivo = "finca.xlsx"
hoja = "Finca"

def cargar_datos():
    if os.path.exists(archivo):
        df = pd.read_excel(archivo, sheet_name=hoja)
    else:
        df = pd.DataFrame(columns=["ID Parcela", "Nombre", "Variedad", "Hectáreas", "Marco", "Riego"])
    return df

def guardar_datos(df):
    with pd.ExcelWriter(archivo, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, sheet_name=hoja, index=False)

st.title("🌿 Aplicación sencilla para gestionar tu finca de olivar")
st.caption("Diseñada para ser fácil, clara y útil para agricultores2")

st.header("📋 Gestión de Finca")

df = cargar_datos()
st.dataframe(df, use_container_width=True)

st.divider()

st.subheader("➕ Añadir un nuevo dato")
col1, col2 = st.columns(2)
with col1:
    id_parcela = st.text_input("ID Parcela")
    variedad = st.text_input("Variedad")
    marco = st.text_input("Marco")
with col2:
    nombre = st.text_input("Nombre")
    hectareas = st.number_input("Hectáreas", min_value=0.0, step=0.1)
    riego = st.selectbox("Riego", ["sí", "no"])

if st.button("💾 Guardar en Finca"):
    nuevo_dato = {
        "ID Parcela": id_parcela,
        "Nombre": nombre,
        "Variedad": variedad,
        "Hectáreas": hectareas,
        "Marco": marco,
        "Riego": riego
    }
    df = pd.concat([df, pd.DataFrame([nuevo_dato])], ignore_index=True)
    guardar_datos(df)
    st.success("✅ Guardado correctamente.")
    st.experimental_set_query_params(_="refresh")
    st.rerun()
