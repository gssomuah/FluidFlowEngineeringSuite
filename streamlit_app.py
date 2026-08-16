import streamlit as st

st.set_page_config(
    page_title="Fluid Flow & Heat Transfer Engineering Suite",
    page_icon="⚙️",
    layout="wide",
)

st.title("⚙️ Fluid Flow & Heat Transfer Engineering Suite")

st.write(
    "Welcome to the engineering analysis suite. "
    "Use the pages in the left sidebar to perform calculations "
    "and analyse engineering data."
)

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🔧 Module A")
    st.write("Pipe Flow Analyser")
    st.write(
        "Calculate velocity, Reynolds number, "
        "friction factor and pressure drop."
    )

with col2:
    st.subheader("🌡️ Module B")
    st.write("Heat Transfer Calculator")
    st.write(
        "Calculate conduction heat transfer "
        "and Newton cooling."
    )

with col3:
    st.subheader("📊 Module C")
    st.write("Rock & Fluid Data Dashboard")
    st.write(
        "Upload CSV data, filter it and create "
        "interactive engineering plots."
    )

st.success(
    "Application successfully loaded. "
    "Select a module from the sidebar."
)