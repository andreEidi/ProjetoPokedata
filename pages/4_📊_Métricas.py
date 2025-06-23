import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go

# Set the page configuration
st.set_page_config(
    page_title="PokeStats",
    page_icon="datasets/Poké_Ball_icon.png",
    layout="wide"
)

# Check if the session state already has the data
if "data" not in st.session_state:
    df_data = pd.read_csv("datasets/All_Pokemon.csv")
    df_data["Generation"] = df_data["Generation"].astype(int)
    df_data = df_data[df_data['Generation'] <= 6]
    df_data["Type 1"].fillna("Nenhum", inplace=True)
    df_data["Type 2"].fillna("Nenhum", inplace=True)
    df_data = df_data.sort_values(by="Number")
    st.session_state["data"] = df_data
else:
    df_data = st.session_state["data"]

# Filter values by generation
gene_df = df_data["Generation"].value_counts().sort_index().index.tolist()
gen_options = ["Todos"] + [str(g) for g in gene_df]
gen_selected = st.sidebar.selectbox("Geração", gen_options)

if gen_selected == "Todos":
    df_filtered = df_data
else:
    df_filtered = df_data[df_data["Generation"] == int(gen_selected)]

# Title for the page
st.markdown(f"## Visões Gerais e Métricas Agregadas")
st.divider()

# Bar chart: Quantidade de Pokémon por Type 1
st.subheader(f"Quantidade de Pokémon por Tipo Principal")
# Contar e ordenar os valores da coluna "Type 1"
type1_counts = df_filtered["Type 1"].value_counts().sort_values(ascending=False)
data = pd.DataFrame({
    "Tipo": type1_counts.index,
    "Quantidade": type1_counts.values
})

st.write(alt.Chart(data).mark_bar().encode(
    x=alt.X('Tipo', sort=None),
    y='Quantidade',
))

# Gráficos de barras para cada Type 1 mostrando a quantidade de Type 2
st.subheader("Distribuição do Tipo Secundário para cada Tipo Principal")
type1_list = data["Tipo"].tolist()

# Adiciona um botão para escolher o Type 1 e mostrar a distribuição de Type 2
selected_type1 = st.selectbox("Escolha o Tipo Principal Para Ver a Distribuição do Tipo Secundário:", type1_list)

if st.button("Mostrar distribuição do Tipo secundário para o Tipo Principal selecionado"):
    sub_df = df_filtered[df_filtered["Type 1"] == selected_type1]
    type2_counts = sub_df["Type 2"].value_counts().sort_values(ascending=False)
    type2_data = pd.DataFrame({
        "Tipo Secundário": type2_counts.index,
        "Quantidade": type2_counts.values
    })
    st.markdown(f"**{selected_type1}**")
    st.write(alt.Chart(type2_data).mark_bar().encode(
        x=alt.X('Tipo Secundário', sort=None),
        y='Quantidade',
    ))

st.divider()
#diplay statistics 
st.subheader("Média de Atributos e Delta em Relação a Média Geral")

hp, att, deff, spa, spd, spe, qtde = st.columns(7)
qtde.metric(label="Qtde. de Pokémons", value=f"{df_filtered['Number'].nunique()}")
hp.metric(label="Pontos de Vida Base", value=f"{df_filtered['HP'].mean():.2f}", delta=f"{df_filtered['HP'].mean() - df_data['HP'].mean():.2f}")
att.metric(label="Ataque Base", value=f"{df_filtered['Att'].mean():.2f}", delta=f"{df_filtered['Att'].mean() - df_data['Att'].mean():.2f}")
deff.metric(label="Defesa Base", value=f"{df_filtered['Def'].mean():.2f}", delta=f"{df_filtered['Def'].mean() - df_data['Def'].mean():.2f}")
spa.metric(label="Ataque Especial Base", value=f"{df_filtered['Spa'].mean():.2f}", delta=f"{df_filtered['Spa'].mean() - df_data['Spa'].mean():.2f}")
spd.metric(label="Defesa Especial Base", value=f"{df_filtered['Spd'].mean():.2f}", delta=f"{df_filtered['Spd'].mean() - df_data['Spd'].mean():.2f}")
spe.metric(label="Velocidade Base", value=f"{df_filtered['Spe'].mean():.2f}", delta=f"{df_filtered['Spe'].mean() - df_data['Spe'].mean():.2f}")


st.divider()
