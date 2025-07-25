# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 11:51:12 2025

@author: jahop
"""


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# --------------------------
# CONFIGURACIÓN INICIAL
# --------------------------
st.set_page_config(
    page_title="PORTFOLIO ADMINISTRATIVO - OIL & GAS",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------
# DATOS SIMULADOS (DEMO)
# --------------------------
@st.cache_data
def cargar_datos():
    np.random.seed(42)
    meses = 24
    data = {
        'Fecha': pd.date_range(start='2023-01-01', periods=meses, freq='M'),
        'Sucursal': np.random.choice(['Cd. del Carmen', 'Paraíso', 'Dos Bocas'], meses),
        'Gastos_Operación': np.random.randint(20000, 60000, meses),
        'Gastos_Logística': np.random.randint(5000, 15000, meses),
        'Ingresos_Producción': np.random.randint(70000, 120000, meses),
        'Ingresos_Servicios': np.random.randint(20000, 50000, meses),
        'Horas_Productivas': np.random.randint(160, 250, meses)
    }
    df = pd.DataFrame(data)
    df['Utilidad_Neta'] = df['Ingresos_Producción'] + df['Ingresos_Servicios'] - df['Gastos_Operación'] - df['Gastos_Logística']
    df['Eficiencia'] = (df['Utilidad_Neta'] / (df['Gastos_Operación'] + df['Gastos_Logística'])) * 100
    return df

df = cargar_datos()

# --------------------------
# BARRA LATERAL (FILTROS)
# --------------------------
with st.sidebar:
    #st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Oil_platform_icon.svg/1200px-Oil_platform_icon.svg.png", width=100)
    st.title("Panel de Control")
    st.markdown("**Filtros Operativos**")
    
    # Filtro de sucursales (con lógica mejorada)
    sucursales = st.multiselect(
        "🔹 Sucursales",
        options=df['Sucursal'].unique(),
        default=df['Sucursal'].unique()[0]  # Solo una seleccionada por defecto
    )
    
    # Filtro de fechas mejorado
    fecha_min, fecha_max = st.slider(
        "📅 Rango de Periodo",
        min_value=df['Fecha'].min().to_pydatetime(),
        max_value=df['Fecha'].max().to_pydatetime(),
        value=(df['Fecha'].min().to_pydatetime(), df['Fecha'].max().to_pydatetime()),
        format="MM/YYYY"
    )
    
    st.markdown("---")
    st.markdown("**Candidato:** Javier Horacio Pérez Ricárdez")
    st.markdown("**Vacante:** Auxiliar Administrativo Oil & Gas")
    st.markdown("**Disponibilidad:** Inmediata + Reubicación")

# --------------------------
# APLICACIÓN DE FILTROS
# --------------------------
df_filtrado = df[
    (df['Sucursal'].isin(sucursales if sucursales else df['Sucursal'].unique())) &
    (df['Fecha'] >= pd.to_datetime(fecha_min)) &
    (df['Fecha'] <= pd.to_datetime(fecha_max))
]

# --------------------------
# SECCIÓN PRINCIPAL
# --------------------------
st.title("📈 DASHBOARD ADMINISTRATIVO - SECTOR HIDROCARBUROS")
st.markdown("**Análisis de Rentabilidad y Eficiencia Operativa** | *Herramienta desarrollada como demostración de competencias*")

# KPI's EN GRID
st.subheader("🔍 Indicadores Clave de Desempeño")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric("Utilidad Neta", f"${df_filtrado['Utilidad_Neta'].sum():,.0f}", delta="5.2% vs periodo anterior")
with kpi2:
    st.metric("Eficiencia Operativa", f"{df_filtrado['Eficiencia'].mean():.1f}%", delta="1.8%")
with kpi3:
    st.metric("Horas Productivas", f"{df_filtrado['Horas_Productivas'].sum():,.0f}h", "Eficiencia laboral")
with kpi4:
    st.metric("Margen Neto", f"{(df_filtrado['Utilidad_Neta'].sum() / (df_filtrado['Ingresos_Producción'].sum() + df_filtrado['Ingresos_Servicios'].sum()))*100:.1f}%")

# GRÁFICOS PROFESIONALES
col1, col2 = st.columns(2)
with col1:
    fig = px.line(
        df_filtrado,
        x='Fecha',
        y='Utilidad_Neta',
        color='Sucursal',
        title='<b>Tendencia de Utilidad Neta</b>',
        labels={'Utilidad_Neta': 'USD', 'Fecha': 'Periodo'},
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        df_filtrado.groupby('Sucursal').agg({'Utilidad_Neta': 'sum'}).reset_index(),
        x='Sucursal',
        y='Utilidad_Neta',
        title='<b>Utilidad por Sucursal (Acumulado)</b>',
        color='Sucursal',
        labels={'Utilidad_Neta': 'USD'},
        text_auto='.2s'
    )
    st.plotly_chart(fig, use_container_width=True)

# TABLA DINÁMICA AVANZADA
st.subheader("📊 Tablero Analítico Detallado")
pivot = pd.pivot_table(
    df_filtrado,
    values=['Utilidad_Neta', 'Eficiencia', 'Horas_Productivas'],
    index=['Fecha'],
    columns=['Sucursal'],
    aggfunc={'Utilidad_Neta': np.sum, 'Eficiencia': np.mean, 'Horas_Productivas': np.sum}
)
st.dataframe(pivot.style.format("{:,.0f}").highlight_max(axis=1, color='#d4f1d4'), use_container_width=True)

# --------------------------
# SECCIÓN DE PERFIL
# --------------------------
st.markdown("---")
st.subheader("🧑‍💼 PERFIL PROFESIONAL PARA LA VACANTE")

col_perfil1, col_perfil2 = st.columns(2)
with col_perfil1:
    st.markdown("""
    **Habilidades demostradas en este dashboard:**
    - ✔️ Análisis contable avanzado
    - ✔️ Automatización con Python
    - ✔️ Dominio de tablas dinámicas
    - ✔️ Visualización profesional de datos
    - ✔️ Creación de KPI's estratégicos
    """)

with col_perfil2:
    st.markdown("""
    **Competencias para el puesto:**
    - 🚀 Facilidad para interpretar datos financieros
    - 🚀 Comunicación efectiva de resultados
    - 🚀 Enfoque en eficiencia operativa
    - 🚀 Adaptabilidad a diferentes sucursales
    - 🚀 Precisión en reportes administrativos
    """)

# --------------------------
# FOOTER IMPACTANTE
# --------------------------
st.markdown("---")
st.markdown("""
<div style="background-color:#0E1117;padding:20px;border-radius:10px">
<h4 style="color:white;text-align:center;">🚀 LISTO PARA CONTRIBUIR EN SU EQUIPO ADMINISTRATIVO</h4>
<p style="color:white;text-align:center;">Disponibilidad inmediata | Flexibilidad geográfica | Aprendizaje continuo</p>
<p style="color:white;text-align:center;">📧 <strong>jahoperi@gmail.com</strong> | 📞 +52 56 1056 4095</p>
</div>
""", unsafe_allow_html=True)