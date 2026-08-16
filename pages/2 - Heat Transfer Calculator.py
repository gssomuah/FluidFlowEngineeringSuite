import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from engineering import HeatTransfer

st.title("🌡️ Heat Transfer Calculator")

st.write(
    "Calculate heat conduction through a flat wall "
    "and cooling time using Newton's law of cooling."
)

st.sidebar.header("Conduction Inputs")

k = st.sidebar.number_input(
    "Thermal conductivity k (W/m·K)",
    min_value=0.0001,
    value=45.0,
)

area = st.sidebar.number_input(
    "Wall area A (m²)",
    min_value=0.0001,
    value=2.0,
)

thickness = st.sidebar.number_input(
    "Wall thickness L (m)",
    min_value=0.0001,
    value=0.1,
)

hot_temperature = st.sidebar.number_input(
    "Hot-side temperature (°C)",
    value=150.0,
)

cold_temperature = st.sidebar.number_input(
    "Cold-side temperature (°C)",
    value=25.0,
)

st.sidebar.markdown("---")
st.sidebar.header("Newton Cooling Inputs")

density = st.sidebar.number_input(
    "Density ρ (kg/m³)",
    min_value=0.001,
    value=7800.0,
)

specific_heat = st.sidebar.number_input(
    "Specific heat Cp (J/kg·K)",
    min_value=0.001,
    value=500.0,
)

volume = st.sidebar.number_input(
    "Object volume V (m³)",
    min_value=0.000001,
    value=0.01,
)

heat_transfer_coefficient = st.sidebar.number_input(
    "Heat transfer coefficient h (W/m²·K)",
    min_value=0.001,
    value=25.0,
)

cooling_area = st.sidebar.number_input(
    "Cooling area A (m²)",
    min_value=0.0001,
    value=1.0,
)

initial_temperature = st.sidebar.number_input(
    "Initial temperature T₀ (°C)",
    value=200.0,
)

target_temperature = st.sidebar.number_input(
    "Target temperature (°C)",
    value=80.0,
)

ambient_temperature = st.sidebar.number_input(
    "Ambient temperature T∞ (°C)",
    value=25.0,
)

try:
    heat_rate = HeatTransfer.conduction_heat_rate(
        k,
        area,
        hot_temperature,
        cold_temperature,
        thickness,
    )

    cooling_time = HeatTransfer.cooling_time(
        density,
        specific_heat,
        volume,
        heat_transfer_coefficient,
        cooling_area,
        initial_temperature,
        target_temperature,
        ambient_temperature,
    )

    st.subheader("Calculation Results")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Conduction Heat Transfer",
            f"{heat_rate:,.2f} W",
        )

        st.latex(
            r"Q = \frac{kA(T_{hot}-T_{cold})}{L}"
        )

    with col2:
        st.metric(
            "Cooling Time",
            f"{cooling_time:,.2f} s",
        )

        st.metric(
            "Cooling Time",
            f"{cooling_time / 60:,.2f} min",
        )

        st.latex(
            r"t=-\frac{\rho C_p V}{hA}\ln\left(\frac{T-T_\infty}{T_0-T_\infty}\right)"
        )

    st.subheader("Newton Cooling Curve")

    time_values = np.linspace(
        0,
        max(cooling_time * 1.5, 1),
        150,
    )

    temperatures = []

    for time in time_values:
        temperature = HeatTransfer.cooling_temperature(
            time,
            density,
            specific_heat,
            volume,
            heat_transfer_coefficient,
            cooling_area,
            initial_temperature,
            ambient_temperature,
        )

        temperatures.append(temperature)

    chart_data = pd.DataFrame(
        {
            "Time (s)": time_values,
            "Temperature (°C)": temperatures,
        }
    )

    figure = px.line(
        chart_data,
        x="Time (s)",
        y="Temperature (°C)",
        title="Temperature vs Time",
    )

    st.plotly_chart(
        figure,
        use_container_width=True,
    )

except ValueError as error:
    st.error(f"Input error: {error}")

except Exception as error:
    st.error(f"Calculation error: {error}")