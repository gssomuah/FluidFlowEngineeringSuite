import pandas as pd
import plotly.express as px
import streamlit as st


st.title("📊 Rock & Fluid Data Dashboard")

st.write(
    "Upload a CSV file containing rock and fluid data, "
    "explore the dataset, filter values, and create interactive plots."
)

st.sidebar.header("Data Input")

uploaded_file = st.file_uploader(
    "Upload CSV file",
    type=["csv"],
)

if uploaded_file is None:
    st.info(
        "Upload a CSV file to begin. "
        "You can also use the sample dataset below."
    )

    sample_data = pd.DataFrame(
        {
            "Depth_m": [1000, 1100, 1200, 1300, 1400],
            "Porosity": [0.22, 0.19, 0.17, 0.15, 0.13],
            "Permeability_mD": [450, 320, 210, 150, 95],
            "Pressure_MPa": [12.1, 13.4, 14.8, 16.2, 17.7],
            "Temperature_C": [48, 52, 57, 61, 66],
        }
    )

    st.subheader("Sample Engineering Dataset")

    st.dataframe(
        sample_data,
        use_container_width=True,
    )

    data = sample_data

else:
    try:
        data = pd.read_csv(uploaded_file)

        st.success(
            f"Loaded {len(data):,} rows and "
            f"{len(data.columns):,} columns."
        )

    except Exception as error:
        st.error(f"Could not read CSV: {error}")
        st.stop()


st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Rows", f"{len(data):,}")

with col2:
    st.metric("Columns", f"{len(data.columns):,}")

with col3:
    st.metric(
        "Missing Values",
        f"{int(data.isna().sum().sum()):,}",
    )


st.dataframe(
    data,
    use_container_width=True,
)


numeric_columns = data.select_dtypes(
    include="number"
).columns.tolist()


if numeric_columns:

    st.sidebar.markdown("---")
    st.sidebar.header("Plot Controls")

    x_column = st.sidebar.selectbox(
        "X-axis",
        numeric_columns,
        index=0,
    )

    y_column = st.sidebar.selectbox(
        "Y-axis",
        numeric_columns,
        index=min(1, len(numeric_columns) - 1),
    )

    chart_type = st.sidebar.selectbox(
        "Chart type",
        [
            "Scatter",
            "Line",
            "Histogram",
        ],
    )

    st.subheader("Interactive Engineering Plot")

    if chart_type == "Scatter":

        figure = px.scatter(
            data,
            x=x_column,
            y=y_column,
            title=f"{y_column} vs {x_column}",
        )

    elif chart_type == "Line":

        figure = px.line(
            data,
            x=x_column,
            y=y_column,
            title=f"{y_column} vs {x_column}",
        )

    else:

        figure = px.histogram(
            data,
            x=x_column,
            title=f"Distribution of {x_column}",
        )

    st.plotly_chart(
        figure,
        use_container_width=True,
    )

else:

    st.warning(
        "No numeric columns were found in the dataset."
    )


st.subheader("Statistics")

if numeric_columns:

    st.dataframe(
        data[numeric_columns].describe(),
        use_container_width=True,
    )


csv_output = data.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "⬇️ Download Dataset",
    data=csv_output,
    file_name="engineering_dataset.csv",
    mime="text/csv",
)