import streamlit as st
import random
import json
import os

DB_FILE = "base_datos.json"

def cargar_bd():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def guardar_bd(bd):
    with open(DB_FILE, "w") as f:
        json.dump(bd, f)

def normalizar_fila(numeros):
    return sorted(list(set(numeros)))

st.title("📊 Comparador de Combinaciones (0 al 45)")
st.write("Genera una fila automática, ingresa la tuya y compáralas con la base de datos.")

bd = cargar_bd()
st.info(f"Registros totales en la base de datos: {len(bd)}")

# --- PASO 1: Generar fila automática ---
if st.button("🎲 Generar Fila Automática"):
    fila_gen = random.sample(range(0, 46), 6)
    st.session_state['fila_gen'] = normalizar_fila(fila_gen)

if 'fila_gen' in st.session_state:
    st.success(f"**Fila Generada por la App:** {st.session_state['fila_gen']}")

# --- PASO 2: Ingresar fila del usuario ---
st.subheader("Ingresa tu propia fila (6 números entre 0 y 45, separados por comas):")
usuario_input = st.text_input("Ejemplo: 5, 12, 23, 34, 40, 45", "")

# --- PASO 3: Comparar y Guardar ---
if st.button("🔍 Comparar Ambas Filas con la Base de Datos"):
    if 'fila_gen' not in st.session_state:
        st.warning("⚠️ Primero presiona 'Generar Fila Automática' antes de comparar.")
    else:
        try:
            fila_user = [int(n.strip()) for n in usuario_input.split(",")]
            
            if len(fila_user) != 6 or any(n < 0 or n > 45 for n in fila_user) or len(set(fila_user)) != 6:
                st.error("Error: Debes ingresar exactamente 6 números únicos entre 0 y 45, separados por comas.")
            else:
                fila_user = normalizar_fila(fila_user)
                fila_generada = st.session_state['fila_gen']
                st.write(f"**Tu Fila Procesada:** {fila_user}")
                
                gen_existe = fila_generada in bd
                user_existe = fila_user in bd
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Fila Generada")
                    if gen_existe:
                        st.warning("⚠️ ¡Ya existe en la base de datos!")
                    else:
                        st.info("✨ Es una combinación NUEVA.")
                        if fila_generada not in bd:
                            bd.append(fila_generada)
                
                with col2:
                    st.markdown("### Tu Fila")
                    if user_existe:
                        st.warning("⚠️ ¡Ya existe en la base de datos!")
                    else:
                        st.info("✨ Es una combinación NUEVA.")
                        if fila_user not in bd:
                            bd.append(fila_user)
                
                guardar_bd(bd)
                st.success("Base de datos actualizada correctamente.")
                
        except ValueError:
            st.error("Por favor, ingresa solo números válidos separados por comas.")
