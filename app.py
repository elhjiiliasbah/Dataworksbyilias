
import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="SmartSales AI", layout="wide")

st.title("SmartSales AI")
st.write("Welkom bij mijn eerste AI-analyseapp!")

bestand = st.file_uploader(
    "Upload je verkoopgegevens",
    type=["csv", "xlsx"]
)

if bestand is not None:

    if bestand.name.endswith(".csv"):
        df = pd.read_csv(bestand)
    else:
        df = pd.read_excel(bestand)
    
    st.success("Bestand succesvol geüpload!")

    st.subheader("Voorbeeld van je gegevens")
    st.dataframe(df.head())

    st.metric("Aantal rijen", len(df))


# Omzet per verkoopregel berekene
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# Alleen postieve verkopen selecteren
verkopen = df[
    (df["Quantity"] > 0) &
    (df["UnitPrice"] > 0)
]

# Totale omzet berekenen
totale_omzet = verkopen["Revenue"].sum()

# Dashboard tonen
st.subheader("Verkoopdashboard")

st.metric(
    "Totale omzet",
    f"${totale_omzet:,.2f}"
)

# Top 10 producten op basis van omzet
top_producten = (
    verkopen.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# Interactieve grafiek maken
fig = px.bar(
    top_producten,
    x ="Revenue",
    y="Description",
    orientation="h",
    title="Top 10 producten op basis van omzet",
    labels={
        "Revenue": "Omzet ($)",
        "Description": "Product"
    }
)

# Grootse product bovenaan
fig.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

# Grafiek tonen in Streamlit app
st.plotly_chart(fig, use_container_width=True)


 # STAP 3.3 - Omzet per maand

# Datums omzetten naar datetime
verkopen = verkopen.copy()

verkopen["InvoiceDate"] = pd.to_datetime(
    verkopen["InvoiceDate"],
     errors="coerce"
)

# Rijen zonder geldige datum verwijderen
verkopen = verkopen.dropna(subset=["InvoiceDate"])

# Jaar en maand uit de datum halen
verkopen["Maand"] = verkopen["InvoiceDate"].dt.to_period("M")

# Omzet per maand berekenen
omzet_per_maand = (
    verkopen.groupby("Maand")["Revenue"]
    .sum()
    .reset_index()
)

# Maand omzetten voor Plotly
omzet_per_maand["Maand"] = (
    omzet_per_maand["Maand"].dt.to_timestamp()
)

# Lijngrafiek maken
fig_maand = px.line(
    omzet_per_maand,
     x="Maand",
    y="Revenue",
    title="Omzetontwikkeling per maand",
    markers=True,
    labels={
        "Maand": "Maand",
        "Revenue": "Omzet (£)"
    }
)

# Grafiek weergeven
st.plotly_chart(
    fig_maand,
    use_container_width=True
)
