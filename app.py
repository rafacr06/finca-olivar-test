
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Gestión de Finca de Olivar", layout="wide")

EXCEL_FILE = "finca_olivar_datos.xlsx"
HOJA_FINCA = "Finca"

if HOJA_FINCA not in st.session_state:
    if os.path.exists(EXCEL_FILE):
        df_finca = pd.read_excel(EXCEL_FILE, sheet_name=HOJA_FINCA)
        if "Marco" in df_finca.columns:
            df_finca = df_finca.drop(columns=["Marco"])
    else:
        df_finca = pd.DataFrame(columns=["ID Parcela", "Nombre", "Variedad", "Hectáreas", "Número total de olivos", "Riego"])
    st.session_state[HOJA_FINCA] = df_finca
else:
    df_finca = st.session_state[HOJA_FINCA]

st.markdown("""
    <h1>🌿 Aplicación sencilla para gestionar tu finca de olivar</h1>
    <p style='color:gray;'>Diseñada para ser fácil, clara y útil para agricultores</p>
""", unsafe_allow_html=True)

menu = st.sidebar.radio("📋 ¿Qué quieres gestionar?", [
    "Finca", "Labores", "Costes", "Ingresos", "Inventario", "Rentabilidad", "Ver resumen de todo"
])

if menu == "Finca":
    st.subheader("📋 Gestión de Finca")

    selected_index = st.session_state.get("selected_index", None)

    def mostrar_tabla():
        st.dataframe(df_finca, use_container_width=True)

    mostrar_tabla()

    st.markdown("<hr><h3>➕Agregar nuevo registro</h3>", unsafe_allow_html=True)

    id_parcela = len(df_finca) + 1
    nombre = st.text_input("Nombre")

    # Lista de variedades ampliada
    variedades_base = ["Picual", "Arbequina", "Hojiblanca", "Cornicabra", "Manzanilla", "Verdial", "Empeltre", "Lechín", "Changlot Real", "Blanqueta", "Farga", "Royal", "Cuquillo"]
    variedades_existentes = df_finca["Variedad"].dropna().unique().tolist()
    variedades_disponibles = sorted(set(variedades_base + variedades_existentes))

    variedad = st.selectbox("Variedad", variedades_disponibles)
    hectareas = st.number_input("Hectáreas", min_value=0.0, step=0.1)
    numero_olivos = st.number_input("Número total de olivos", min_value=0, step=100)
    riego = st.selectbox("Riego", ["sí", "no"])

    if st.button("Guardar en Finca"):
        nuevo = pd.DataFrame([{
            "ID Parcela": id_parcela,
            "Nombre": nombre,
            "Variedad": variedad,
            "Hectáreas": hectareas,
            "Número total de olivos": numero_olivos,
            "Riego": riego
        }])
        st.session_state[HOJA_FINCA] = pd.concat([df_finca, nuevo], ignore_index=True)
        st.session_state.selected_index = None
        st.rerun()

    st.markdown("<hr><h3>Borrar un registro</h3>", unsafe_allow_html=True)

    if len(df_finca) > 0:
        nombres_fincas = df_finca["Nombre"].tolist()
        indices_fincas = df_finca.index.tolist()
        nombre_a_indice = {nombre: idx for nombre, idx in zip(nombres_fincas, indices_fincas)}

        selected_nombre = st.selectbox("Selecciona el nombre de la finca a borrar", nombres_fincas, key="nombre_borrar")

        confirmar = st.checkbox("Confirmo que deseo borrar este registro")

        if confirmar:
            if st.button("🗑️Borrar registro"):
                selected_index = nombre_a_indice[selected_nombre]
                st.session_state[HOJA_FINCA] = df_finca.drop(index=selected_index).reset_index(drop=True)
                st.success(f"Se ha borrado correctamente la finca: {selected_nombre}")
                st.session_state.selected_index = None
                st.rerun()
        else:
            st.info("Marca la casilla de confirmación antes de borrar.")
    else:
        st.info("No hay registros para borrar.")

    # Guardar Excel actualizado
    st.session_state[HOJA_FINCA].to_excel(EXCEL_FILE, sheet_name=HOJA_FINCA, index=False)

