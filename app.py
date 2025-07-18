import streamlit as st
import pandas as pd
import os

# Ruta al archivo Excel
data_file = "finca_olivar_datos.xlsx"

# Inicializa el archivo si no existe
if not os.path.exists(data_file):
    with pd.ExcelWriter(data_file, engine='openpyxl') as writer:
        pd.DataFrame(columns=["ID Parcela", "Nombre", "Variedad", "Hectáreas", "Olivos", "Riego"]).to_excel(writer, sheet_name="Finca", index=False)

# Cargar los datos
def cargar_datos():
    return pd.read_excel(data_file, sheet_name="Finca")

# Guardar los datos
def guardar_datos(df):
    with pd.ExcelWriter(data_file, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, sheet_name="Finca", index=False)

# Borrar registro por índice
def borrar_registro(indice):
    df = cargar_datos()
    df = df.drop(index=indice).reset_index(drop=True)
    guardar_datos(df)
    st.success("Registro eliminado correctamente")

# Interfaz
st.set_page_config(page_title="Finca Olivar", layout="wide")
st.title("🌿 Aplicación sencilla para gestionar tu finca de olivar")
st.caption("Diseñada para ser fácil, clara y útil para agricultoresv.01")

# Secciones (no desplegable)
menu = st.sidebar.radio("📍 ¿Qué quieres gestionar?", ["Finca", "Labores", "Costes", "Ingresos", "Inventario", "Rentabilidad", "Ver resumen de todo"])

if menu == "Finca":
    st.header("📑 Gestión de Finca")

    df = cargar_datos()

    if not df.empty:
        st.dataframe(df, use_container_width=True)

        for i, row in df.iterrows():
            borrar = st.button(f"🗑️ Borrar fila {i+1}", key=f"borrar_{i}")
            if borrar:
                borrar_registro(i)
                st.experimental_rerun()
    else:
        st.info("No hay datos en la hoja de finca.")

    st.markdown("---")
    st.subheader("➕ Añadir nuevo registro")

    # Generar ID siguiente
    next_id = "ID1"
    if not df.empty:
        last_id = df["ID Parcela"].iloc[-1]
        try:
            num = int(''.join(filter(str.isdigit, str(last_id)))) + 1
            next_id = f"ID{num}"
        except:
            pass

    # Variedades disponibles
    variedades_disponibles = sorted(df["Variedad"].dropna().unique()) if not df.empty else []

    # Inputs
    col1, col2 = st.columns(2)
    with col1:
        id_parcela = st.text_input("ID Parcela", value=next_id, disabled=True)
        variedad = st.selectbox("Variedad", opciones := variedades_disponibles + ["Otra"] if "Otra" not in variedades_disponibles else variedades_disponibles)
        if variedad == "Otra":
            variedad = st.text_input("Escribe nueva variedad")
        olivos = st.text_input("Número total de olivos de la finca")
    with col2:
        nombre = st.text_input("Nombre")
        hectareas = st.number_input("Hectáreas", min_value=0.0, max_value=999.9, step=0.1, format="%.1f")
        riego = st.selectbox("Riego", ["sí", "no"])

    if st.button("💾 Guardar en Finca"):
        nuevo = pd.DataFrame({
            "ID Parcela": [id_parcela],
            "Nombre": [nombre],
            "Variedad": [variedad],
            "Hectáreas": [hectareas],
            "Olivos": [olivos],
            "Riego": [riego]
        })
        df = pd.concat([df, nuevo], ignore_index=True)
        guardar_datos(df)
        st.success("✅ Guardado correctamente")
        st.experimental_rerun()

else:
    st.info(f"La sección '{menu}' está en desarrollo.")

