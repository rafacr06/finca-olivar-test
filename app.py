
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
    <h1>🌿Gestion de fincas del olivar🌿</h1>
    <p style='color:gray;'>Diseñada para ser fácil, clara y útil para agricultores</p>
""", unsafe_allow_html=True)

menu = st.sidebar.radio("📋 ¿Qué quieres gestionar?", [
    "Finca", "Gastos", "Jornales", "Ingresos", "Abonos y Tratamientos", "Rentabilidad", "Ver resumen de todo"
])
# **********************************************Menu Finca*************************************************************
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

    st.markdown("<hr><h3>❌Borrar un registro</h3>", unsafe_allow_html=True)

    if len(df_finca) > 0:
        nombres_fincas = df_finca["Nombre"].tolist()
        indices_fincas = df_finca.index.tolist()
        nombre_a_indice = {nombre: idx for nombre, idx in zip(nombres_fincas, indices_fincas)}

        selected_nombre = st.selectbox("Selecciona el nombre de la finca a borrar", nombres_fincas, key="nombre_borrar")

        confirmar = st.checkbox("⚠️Confirmo que deseo borrar este registro")

        if confirmar:
            if st.button("❌Borrar registro"):
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
    
#**********************************************Menu Gastos*************************************************
elif menu == "Gastos":
    st.markdown("<h2>💸 Registro de Gastos de la Finca</h2>", unsafe_allow_html=True)

    GASTOS_FILE = "gastos_olivar.xlsx"
    HOJA_GASTOS = "Gastos"

    # Inicializar gastos
    if HOJA_GASTOS not in st.session_state:
        if os.path.exists(GASTOS_FILE):
            df_gastos = pd.read_excel(GASTOS_FILE, sheet_name=HOJA_GASTOS)
            # Limpiar columnas innecesarias
            if "Finca asociada" in df_gastos.columns:
                df_gastos.drop(columns=["Finca asociada"], inplace=True)
        else:
            df_gastos = pd.DataFrame(columns=["Finca", "Fecha", "Categoría", "Descripción", "Importe (€)"])

        st.session_state[HOJA_GASTOS] = df_gastos
    else:
        df_gastos = st.session_state[HOJA_GASTOS]

    # 🧾 Mostrar historial formateado
    st.markdown("### 🧾 Historial de gastos")

    df_mostrar = df_gastos.copy()
    df_mostrar["Fecha"] = pd.to_datetime(df_mostrar["Fecha"], errors="coerce").dt.strftime("%d/%m/%Y")
    columnas_ordenadas = ["Finca", "Fecha", "Categoría", "Descripción", "Importe (€)"]
    df_mostrar = df_mostrar[columnas_ordenadas]

    st.dataframe(df_mostrar, use_container_width=True)

    total = pd.to_numeric(df_gastos["Importe (€)"], errors="coerce").sum()
    st.markdown(f"💰 <b>Total acumulado de gastos: {total:.2f} €</b>", unsafe_allow_html=True)

    # ➕ Añadir gasto
    st.markdown("### ➕ Añadir nuevo gasto")
    fecha = st.date_input("📅 Fecha del gasto")
    categorias = [
        "GASÓLEOS Y ACEITES", "TALLERES / REPARACIONES", "MANTENIMIENTOS MAQUINARIA",
        "PRODUCTOS FITOSANITARIOS", "SEGUROS VEHÍCULOS", "IMPUESTOS HACIENDA",
        "SEGUROS SOCIALES", "RIEGO", "JORNALES MANTENIMIENTO FINCA",
        "JORNALES RECOGIDA ACEITUNA", "GASTOS EN RECOGIDA", "OTROS"
    ]
    categoria = st.selectbox("🗂️ Tipo de gasto", categorias)
    descripcion = st.text_input("📝 Descripción (opcional)")
    importe = st.number_input("💶 Importe (€)", min_value=0.0, step=1.0)
    finca_referida = st.selectbox("🏡 ¿A qué finca corresponde?", df_finca["Nombre"].unique().tolist())

    if st.button("💾 Guardar gasto"):
        if not finca_referida:
            st.warning("⚠️ Debes seleccionar una finca antes de guardar el gasto.")
        else:
            nuevo_gasto = pd.DataFrame([{
                "Finca": finca_referida,
                "Fecha": fecha,
                "Categoría": categoria,
                "Descripción": descripcion,
                "Importe (€)": importe
            }])
            st.session_state[HOJA_GASTOS] = pd.concat([df_gastos, nuevo_gasto], ignore_index=True)
            st.success("✅ Gasto registrado correctamente.")
            st.rerun()

    # ✏️ Modificar gasto
    st.markdown("### ✏️ Modificar gasto")
    if len(df_gastos) > 0:
        opciones_editables = {
            f"{i} - {row['Finca']} / {row['Categoría']} / {row['Descripción']}": i
            for i, row in df_gastos.iterrows()
        }
        selected_label_edit = st.selectbox("✍️ Selecciona el gasto a modificar", list(opciones_editables.keys()), key="editar_gasto")
        index_editar = opciones_editables[selected_label_edit]
        gasto = df_gastos.loc[index_editar]

        nueva_fecha = st.date_input("Nueva fecha", value=pd.to_datetime(gasto["Fecha"]), key="edit_fecha")
        nueva_categoria = st.selectbox("Nueva categoría", categorias, index=categorias.index(gasto["Categoría"]), key="edit_cat")
        nueva_desc = st.text_input("Nueva descripción", value=gasto["Descripción"], key="edit_desc")
        nuevo_importe = st.number_input("Nuevo importe (€)", min_value=0.0, step=1.0, value=float(gasto["Importe (€)"]), key="edit_imp")
        nueva_finca = st.selectbox("Nueva finca", df_finca["Nombre"].unique().tolist(), index=df_finca["Nombre"].tolist().index(gasto["Finca"]), key="edit_finca")

        if st.button("✅ Guardar cambios"):
            st.session_state[HOJA_GASTOS].at[index_editar, "Fecha"] = nueva_fecha
            st.session_state[HOJA_GASTOS].at[index_editar, "Categoría"] = nueva_categoria
            st.session_state[HOJA_GASTOS].at[index_editar, "Descripción"] = nueva_desc
            st.session_state[HOJA_GASTOS].at[index_editar, "Importe (€)"] = nuevo_importe
            st.session_state[HOJA_GASTOS].at[index_editar, "Finca"] = nueva_finca
            st.success("✅ Gasto actualizado.")
            st.rerun()
    else:
        st.info("ℹ️ No hay gastos para modificar.")

    # ❌ Borrar gasto
    st.markdown("### ❌ Borrar gasto")
    if len(df_gastos) > 0:
        opciones_borrables = {
            f"{i} - {row['Finca']} / {row['Categoría']} / {row['Descripción']}": i
            for i, row in df_gastos.iterrows()
        }
        selected_label_del = st.selectbox("🗑️ Selecciona el gasto a borrar", list(opciones_borrables.keys()), key="borrar_gasto")
        index_borrar = opciones_borrables[selected_label_del]

        confirmar = st.checkbox("⚠️ Confirmo que deseo borrar este gasto", key="conf_borrar")
        if confirmar:
            if st.button("❌ Borrar gasto"):
                st.session_state[HOJA_GASTOS] = df_gastos.drop(index=index_borrar).reset_index(drop=True)
                st.success("✅ Gasto eliminado correctamente.")
                st.rerun()
    else:
        st.info("ℹ️ No hay gastos para borrar.")

    # Guardar Excel limpio
    st.session_state[HOJA_GASTOS].to_excel(GAST]()_

