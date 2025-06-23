import streamlit as st
import pandas as pd
import re

#function to check if the text is a Mega Evolution form
def is_mega_form(text):
    pattern = r'^Mega\s+([A-Za-z]+(?:\s[A-Za-z]+)*)(?:\s+([A-Za-z]))?$'
    match = re.match(pattern, text, re.IGNORECASE)
    if match:
        letra = None
        if len(match.group().split(" ")) > 2:
            letra = match.group().split(" ")[-1].upper()
        return True, letra
    return False, None

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



# filter values by generation
geracoes = df_data["Generation"].value_counts().sort_index().index
gen = st.sidebar.selectbox("Geração", geracoes)

#filter values by type 1
df_gen = df_data[(df_data["Generation"] == gen)]
tipos1 = df_gen["Type 1"].value_counts().sort_index().index
tipo1 = st.sidebar.selectbox("Tipo 1", tipos1)

#filter values by type 2
df_tipo1 = df_gen[(df_gen["Type 1"] == tipo1)]
tipos2 = df_tipo1["Type 2"].value_counts().sort_index().index
tipo2 = st.sidebar.selectbox("Tipo 2", tipos2)

# filter values by name
df_players = df_tipo1[(df_tipo1["Type 2"] == tipo2)]
pokemons = df_players["Name"].value_counts().sort_index().index
pk = st.sidebar.selectbox("Pokemon", pokemons)

pk_stats = df_data[df_data["Name"] == pk].iloc[0]

# Display player information (name and image)
mega, letter = is_mega_form(pk_stats["Name"])
if mega:
    if letter:
        st.image(f"datasets/img/pokemon/{pk_stats['Number']}-mega-{letter}.png")
    else:
        st.image(f"datasets/img/pokemon/{pk_stats['Number']}-mega.png")
else:
    st.image(f"datasets/img/pokemon/{pk_stats["Number"]}.png")
st.title(pk_stats["Name"])

# Display badges based on pokemon statistics
badges = []
if pk_stats["Legendary"] > 0:
    badges.append(("Lendário", ":material/check:", "green"))
if pk_stats["Mega Evolution"] > 0:
    badges.append(("Mega Evolução", ":material/check:", "green"))
if pk_stats["Alolan Form"] > 0:
    badges.append(("Alola Form", ":material/check:", "green"))
if pk_stats["Galarian Form"] > 0:
    badges.append(("Galarian Form", ":material/check:", "green"))

if badges:
    cols = st.columns(4)
    for col, (label, icon, color) in zip(cols, badges):
        col.badge(label, icon=icon, color=color)

# Display player statistics
col1, col2, catchRate, _ = st.columns(4)
col1.markdown(f"**Tipo 1:** {pk_stats['Type 1']}")
col2.markdown(f"**Tipo 2:** {pk_stats['Type 2']}")
catchRate.markdown(f"**Taxa de Captura:** {pk_stats['Catch Rate']}")

col3, col4, col5, col6 = st.columns(4)
col3.markdown(f"**Geração:** {pk_stats['Generation']}º")
col4.markdown(f"**Nº Pokedex:** {pk_stats['Number']}")
col5.markdown(f"**Altura:** {pk_stats['Height']} m")
col6.markdown(f"**Peso:** {pk_stats['Weight']} Kg")
st.divider()

# Display pokemon abilities
st.subheader("Habilidades")
lista_habilidades = [h.split("'")[1] for h in pk_stats["Abilities"].split(", ") if "'" in h]

if lista_habilidades:
    cols = st.columns(len(lista_habilidades))
    for col, label in zip(cols, lista_habilidades):
        col.markdown(f"{label}")

st.divider()

st.subheader(f"Média das Métricas {pk_stats['Mean']:.2f}")
max_mean = df_data["Mean"].max()
percent = (pk_stats["Mean"] / max_mean) * 100
st.progress(int(percent))
st.caption(f"{percent:.2f}% do valor máximo de média ({max_mean:.2f})")

st.subheader("Comparativo das Métricas Base com a Média Geral dos Pokémons")
hp, att, deff, spa, spd, spe = st.columns(6)
hp.metric(label="Pontos de Vida Base", value=f"{pk_stats['HP']}", delta=f"{pk_stats['HP'] - df_data['HP'].mean():.2f}")
att.metric(label="Ataque Base", value=f"{pk_stats['Att']}", delta=f"{pk_stats['Att'] - df_data['Att'].mean():.2f}")
deff.metric(label="Defesa Base", value=f"{pk_stats['Def']}", delta=f"{pk_stats['Def'] - df_data['Def'].mean():.2f}")
spa.metric(label="Ataque Especial Base", value=f"{pk_stats['Spa']}", delta=f"{pk_stats['Spa'] - df_data['Spa'].mean():.2f}")
spd.metric(label="Defesa Especial Base", value=f"{pk_stats['Spd']}", delta=f"{pk_stats['Spd'] - df_data['Spd'].mean():.2f}")
spe.metric(label="Velocidade Base", value=f"{pk_stats['Spe']}", delta=f"{pk_stats['Spe'] - df_data['Spe'].mean():.2f}")

st.divider()
st.subheader("Vantangens e Desvantagens")

# Mapeamento dos tipos para português
tipo_ptbr = {
    "Normal": "Normal",
    "Fire": "Fogo",
    "Water": "Água",
    "Electric": "Elétrico",
    "Grass": "Grama",
    "Ice": "Gelo",
    "Fighting": "Lutador",
    "Poison": "Venenoso",
    "Ground": "Terrestre",
    "Flying": "Voador",
    "Psychic": "Psíquico",
    "Bug": "Inseto",
    "Rock": "Pedra",
    "Ghost": "Fantasma",
    "Dragon": "Dragão",
    "Dark": "Sombrio",
    "Steel": "Aço",
    "Fairy": "Fada"
}


# Encontrar o(s) tipo(s) com maior vantagem e maior desvantagem

against_columns = [col for col in df_data.columns if col.startswith("Against")]
df_against = df_data.loc[df_data["Name"] == pk, against_columns]

max_adv = df_against.max(axis=1).values[0]
min_adv = df_against.min(axis=1).values[0]

tipos_vantagem = [tipo_ptbr[col.replace("Against ", "")] for col in df_against.columns if df_against[col].values[0] == max_adv]
tipos_desvantagem = [tipo_ptbr[col.replace("Against ", "")] for col in df_against.columns if df_against[col].values[0] == min_adv]

max, min = st.columns(2)
max.markdown(f"**Maior vantagem ({max_adv}x):** {', '.join(tipos_vantagem)}")
min.markdown(f"**Maior desvantagem ({min_adv}x):** {', '.join(tipos_desvantagem)}")


against = (
    df_against.T
    .rename(columns={df_against.index[0]: "Multiplicador"})
    .reset_index(names="Tipo")
    .sort_values(by="Multiplicador", ascending=False)
)
against["Tipo"] = against["Tipo"].str.replace("Against ", "").map(tipo_ptbr)

st.data_editor(
    against,
    column_config={
        "Multiplicador": st.column_config.ProgressColumn(
            "Multiplicador",
            help="Multiplicador de dano que o Pokémon causa com base no tipo",
            format="%f",
            min_value=against["Multiplicador"].min(),
            max_value=against["Multiplicador"].max(),
        ),
    },
    hide_index=True,
)