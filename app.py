
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
#**********************************************************************************************************    
#**********************************************Menu Gastos*************************************************
#**********************************************************************************************************  

elif menu == "Gastos":
    st.markdown("<h2>💸 Registro de Gastos</h2>", unsafe_allow_html=True)

    GASTOS_FILE = "gastos_olivar.xlsx"
    HOJA_GASTOS = "Gastos"

    # 🗂️ Cargar o inicializar datos de gastos
    if HOJA_GASTOS not in st.session_state:
        if os.path.exists(GASTOS_FILE):
            df_gastos = pd.read_excel(GASTOS_FILE, sheet_name=HOJA_GASTOS)
        else:
            df_gastos = pd.DataFrame(columns=["Finca", "Fecha", "Categoría", "Descripción", "Importe (€)"])
        st.session_state[HOJA_GASTOS] = df_gastos
    else:
        df_gastos = st.session_state[HOJA_GASTOS]

    categorias = [
        "GASÓLEOS Y ACEITES", "TALLERES / REPARACIONES", "MANTENIMIENTOS MAQUINARIA",
        "PRODUCTOS FITOSANITARIOS", "SEGUROS VEHÍCULOS", "IMPUESTOS HACIENDA",
        "SEGUROS SOCIALES", "RIEGO", "JORNALES MANTENIMIENTO FINCA",
        "JORNALES RECOGIDA ACEITUNA", "GASTOS EN RECOGIDA", "OTROS"
    ]

    # 📜 Mostrar historial de gastos con filtro
    st.markdown("### 🧾 Historial de gastos")

    if df_gastos.empty:
        st.info("ℹ️ No hay gastos registrados aún.")
    else:
        fincas_disponibles = sorted(df_gastos["Finca"].dropna().unique().tolist())
        finca_seleccionada = st.selectbox(
            "🏡 Selecciona la finca para ver sus gastos",
            options=["Todas las fincas"] + fincas_disponibles
        )

        # Filtrar según finca seleccionada
        if finca_seleccionada != "Todas las fincas":
            df_filtrado = df_gastos[df_gastos["Finca"] == finca_seleccionada]
        else:
            df_filtrado = df_gastos.copy()

        # Mostrar tabla
        df_mostrar = df_filtrado.copy()
        df_mostrar["Fecha"] = pd.to_datetime(df_mostrar["Fecha"], errors="coerce").dt.strftime("%d/%m/%Y")
        df_mostrar = df_mostrar[["Finca", "Fecha", "Categoría", "Descripción", "Importe (€)"]]
        st.dataframe(df_mostrar, use_container_width=True)

       # Total por finca o total global con mensaje personalizado
        total = pd.to_numeric(df_filtrado["Importe (€)"], errors="coerce").sum()
        
        if finca_seleccionada == "Todas las fincas":
            st.markdown(f"<h4>💰 Total de gastos: <b>{total:.2f} €</b></h4>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h4>💰 Total de gastos en la finca <i>{finca_seleccionada}</i>: <b>{total:.2f} €</b></h4>", unsafe_allow_html=True)
            
    st.divider()

    # ➕ Añadir nuevo gasto
    st.markdown("### ➕ Añadir nuevo gasto")

    with st.form("form_nuevo_gasto"):
        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("📅 Fecha")
        with col2:
            finca_referida = st.selectbox("🏡 Finca", df_finca["Nombre"].unique().tolist())

        categoria = st.selectbox("📂 Categoría", categorias)
        descripcion = st.text_input("📝 Descripción (opcional)")
        importe = st.number_input("💶 Importe (€)", min_value=0.0, step=1.0)

        guardar = st.form_submit_button("💾 Guardar gasto")

    if guardar:
        nuevo_gasto = pd.DataFrame([{
            "Finca": finca_referida,
            "Fecha": fecha,
            "Categoría": categoria,
            "Descripción": descripcion,
            "Importe (€)": importe
        }])
        st.session_state[HOJA_GASTOS] = pd.concat([df_gastos, nuevo_gasto], ignore_index=True)
        st.success("✅ Gasto guardado correctamente.")
        st.rerun()

    st.divider()

    # ✏️ Modificar gasto
    st.markdown("### ✏️ Modificar un gasto existente")

    if not df_gastos.empty:
        opciones_edit = [
            f"{i} - {row['Finca']} / {row['Categoría']} / {row['Descripción']}"
            for i, row in df_gastos.iterrows()
        ]
        seleccion = st.selectbox("🔎 Selecciona el gasto a modificar", opciones_edit)

        index = int(seleccion.split(" - ")[0])
        gasto = df_gastos.loc[index]

        with st.form("form_editar"):
            col1, col2 = st.columns(2)
            with col1:
                nueva_fecha = st.date_input("📅 Nueva fecha", value=pd.to_datetime(gasto["Fecha"]), key="edit_fecha")
            with col2:
                nueva_finca = st.selectbox("🏡 Nueva finca", df_finca["Nombre"].unique().tolist(),
                                           index=df_finca["Nombre"].tolist().index(gasto["Finca"]), key="edit_finca")

            nueva_cat = st.selectbox("📂 Nueva categoría", categorias,
                                     index=categorias.index(gasto["Categoría"]), key="edit_cat")
            nueva_desc = st.text_input("📝 Nueva descripción", value=gasto["Descripción"], key="edit_desc")
            nuevo_imp = st.number_input("💶 Nuevo importe (€)", min_value=0.0, step=1.0,
                                        value=float(gasto["Importe (€)"]), key="edit_imp")

            modificar = st.form_submit_button("✅ Guardar cambios")

        if modificar:
            df_gastos.at[index, "Fecha"] = nueva_fecha
            df_gastos.at[index, "Finca"] = nueva_finca
            df_gastos.at[index, "Categoría"] = nueva_cat
            df_gastos.at[index, "Descripción"] = nueva_desc
            df_gastos.at[index, "Importe (€)"] = nuevo_imp
            st.success("✅ Gasto modificado.")
            st.rerun()
    else:
        st.info("ℹ️ No hay gastos para modificar.")

    st.divider()

    # ❌ Borrar gasto
    st.markdown("### ❌ Eliminar un gasto")

    if not df_gastos.empty:
        st.markdown("Selecciona el gasto que deseas eliminar:")

        # Mostrar opciones de forma visual y clara
        opciones_borrar = [
            f"{i} - 🏡 {row['Finca']} / 📅 {row['Fecha']} / 📂 {row['Categoría']} / 📝 {row['Descripción']} / 💶 {row['Importe (€)']}"
            for i, row in df_gastos.iterrows()
        ]
        seleccion_borrar = st.selectbox("🗑️ Gasto a eliminar", opciones_borrar)

        index_borrar = int(seleccion_borrar.split(" - ")[0])
        gasto = df_gastos.loc[index_borrar]

        # Mostrar los detalles en un recuadro bien visible
        st.markdown("### 👀 Detalles del gasto seleccionado")
        st.info(
            f"**🏡 Finca:** {gasto['Finca']}\n\n"
            f"**📅 Fecha:** {gasto['Fecha']}\n\n"
            f"**📂 Categoría:** {gasto['Categoría']}\n\n"
            f"**📝 Descripción:** {gasto['Descripción']}\n\n"
            f"**💶 Importe:** {gasto['Importe (€)']} €"
        )

        confirmar = st.checkbox("☑️ Confirmo que deseo eliminar este gasto")

        if confirmar:
            if st.button("❌ Borrar definitivamente"):
                st.session_state[HOJA_GASTOS] = df_gastos.drop(index=index_borrar).reset_index(drop=True)
                st.success("✅ Gasto eliminado correctamente.")
                st.rerun()
        else:
            st.warning("Marca la casilla para poder borrar el gasto.")
    else:
        st.info("ℹ️ No hay gastos para eliminar.")


    # 💾 Guardar el archivo Excel limpio
    st.session_state[HOJA_GASTOS].to_excel(GASTOS_FILE, sheet_name=HOJA_GASTOS, index=False)


