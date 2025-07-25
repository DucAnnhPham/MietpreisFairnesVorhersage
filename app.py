import streamlit as st
import pandas as pd
import joblib
import json
import numpy as np

# Modelle laden
model = joblib.load("model/bestes_fairness_model.joblib")
scaler = joblib.load("model/scaler.joblib")
encoder = joblib.load("model/label_encoder.joblib")
with open("model/feature_columns.json", "r") as f:
    feature_columns = json.load(f)

# Bezirke aus Features extrahieren
bezirke = [col.replace("Bezirk_", "") for col in feature_columns if col.startswith("Bezirk_")]

# Streamlit App Überschrift und Layout
st.title("🏡 Wohnungs-Fairness Vorhersage")
# Nutzereingaben
preis = st.number_input("Mietpreis (€)", min_value=100, max_value=10000, step=10)
flaeche = st.number_input("Wohnfläche (m²)", min_value=10, max_value=300, step=1)
zimmer = st.slider("Zimmeranzahl", 1, 10, 2)
bezirk = st.selectbox("Bezirk", bezirke)

# Ausstattungseingaben(Checkboxen)
st.markdown("### Ausstattung")
möbliert = st.checkbox("Möbliert")
balkon = st.checkbox("Balkon / Terrasse / Garten")
keller = st.checkbox("Keller")
aufzug = st.checkbox("Aufzug")
stellplatz = st.checkbox("Stellplatz")

# Ausstattungsgrad als Summe der "Ja"-Checkboxen (0-5)
ausstattungsgrad = sum([möbliert, balkon, keller, aufzug, stellplatz])

# Ausstattung-Faktoren definieren wie im Modelltraining
# Diese Faktoren wurden im Modelltraining verwendet, um den Preis pro qm anzupassen
AUSSTATTUNGS_FAKTOREN = {
    0: 0.90,
    1: 1.00,
    2: 1.10
}

# Gruppierung der Ausstattung in Gruppen 0,1,2 (0=gering, 1=mittel, 2=hoch) wie im Modelltraining
def gruppiere_ausstattungsgrad(grad):
    if grad <= 1:
        return 0
    elif grad <= 3:
        return 1
    else:
        return 2

# Ausstattungsgrad in Gruppen 0, 1, 2 umwandeln
ausstattungsgrad_gruppe = gruppiere_ausstattungsgrad(ausstattungsgrad)

# Input DataFrame erzeugen
def create_input_df(preis, flaeche, zimmer, ausstattungsgrad_gruppe, bezirk, feature_columns, bezirke):
    preis_pro_qm = preis / flaeche
    
    # Angepasster Preis pro qm (geteilt durch Ausstattung-Faktor)
    preis_pro_qm_angepasst = preis_pro_qm / AUSSTATTUNGS_FAKTOREN[ausstattungsgrad_gruppe]

    # Erstellen des DataFrames mit den erforderlichen Spalten
    data = {
        "Preis pro qm in euro": [preis_pro_qm_angepasst],  # angepasster Preis pro qm
        "Wohnfläche": [flaeche],
        "Zimmer": [zimmer],
        "Ausstattungsgrad_gruppe": [ausstattungsgrad_gruppe]
    }
    # Bezirks-Spalten hinzufügen
    input_df = pd.DataFrame(data)
    for b in bezirke:
        input_df[f"Bezirk_{b}"] = 1 if b == bezirk else 0
    for col in feature_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[feature_columns]
    return input_df


# Session State für Vorhersage-Status
if "vorhersage_gestartet" not in st.session_state:
    st.session_state["vorhersage_gestartet"] = False

if st.button("Vorhersage starten"):
    st.session_state["vorhersage_gestartet"] = True

if st.button("Zurücksetzen"):
    st.session_state["vorhersage_gestartet"] = False

# Vorhersage durchführen, wenn der Button geklickt wurde
if st.session_state["vorhersage_gestartet"]:
    # Eingabedaten vorbereiten
    input_data = create_input_df(preis, flaeche, zimmer, ausstattungsgrad_gruppe, bezirk, feature_columns, bezirke)
    numerische_features = ["Preis pro qm in euro", "Wohnfläche", "Zimmer", "Ausstattungsgrad_gruppe"]

    input_data_scaled = input_data.copy()
    input_data_scaled[numerische_features] = scaler.transform(input_data_scaled[numerische_features])

    # Vorhersage durchführen
    prediction_encoded = model.predict(input_data_scaled)[0]
    prediction = encoder.inverse_transform([prediction_encoded])[0]

    # Vorhersage anzeigen
    st.markdown("### Vorhersage:")
    if prediction == "Fair":
        st.success("✅ Die Wohnung hat einen **fairen Preis**.")
    elif prediction == "Günstig":
        st.info("💰 Die Wohnung ist **günstig für den Bezirk und deren Ausstattung**.")
    elif prediction == "Zu teuer":
        st.warning("⚠️ Die Wohnung ist **zu teuer** für den Bezirk und deren Ausstattung.")
    elif prediction == "Scam-Verdacht":
        st.error("🚨 **Scam-Verdacht** – Vorsicht beim Angebot! Der Preis ist verdächtig günstig.")

    # Feature-Importances anzeigen
    fi = model.feature_importances_
    importance_df = pd.DataFrame({
        "Feature": feature_columns,
        "Importance": fi
    }).sort_values(by="Importance", ascending=False)

    st.dataframe(importance_df)
