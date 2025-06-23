import streamlit as st
import pandas as pd

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
# gene_df = df_data["Generation"].value_counts().sort_index().index
# gen = st.sidebar.selectbox("Geração", gene_df)

# df_filtered = df_data[(df_data["Generation"] == gen)]
# df_filtered.reset_index(names = "NºPokedex", inplace=True)

gene_df = df_data["Generation"].value_counts().sort_index().index.tolist()
gen_options = ["Todos"] + [str(g) for g in gene_df]
gen_selected = st.sidebar.selectbox("Geração", gen_options)

if gen_selected == "Todos":
    df_filtered = df_data.copy()
else:
    df_filtered = df_data[df_data["Generation"] == int(gen_selected)].copy()
    # df_filtered.reset_index(names = "NºPokedex", inplace=True)

df_filtered = df_filtered.sort_values(by="Number")

st.markdown(f"## {gen_selected}º Gen - Pokémon Stats")

# Drop alolan and galarian forms
df_filtered.drop(["Alolan Form" ,"Galarian Form"], axis=1, inplace=True)

# Rename columns to pt-br
columns = [
    "NºPokedex", "Nome", "Tipo 1", "Tipo 2", "Habilidades", "HP", "Ataque", "Defesa", "Ataque Esp.", "Defesa Esp.", "Velocidade", "Soma das Métricas",
    "Média das Métricas", "Desvio Padrão", "Geração", "Tipo de Experiência", "Experiência até nível 100", "Evolução Final",
    "Taxa de Captura", "Lendário", "Mega Evolução", "Contra Normal", "Contra Fogo",
    "Contra Água", "Contra Elétrico", "Contra Planta", "Contra Gelo", "Contra Lutador", "Contra Venenoso",
    "Contra Terrestre", "Contra Voador", "Contra Psíquico", "Contra Inseto", "Contra Pedra", "Contra Fantasma",
    "Contra Dragão", "Contra Sombrio", "Contra Aço", "Contra Fada", "Altura", "Peso", "IMC"
]

df_filtered.columns = columns

# Convert columns to native Python types to avoid JSON serialization errors
df_filtered = df_filtered.applymap(lambda x: x.item() if hasattr(x, "item") else x)

# Formatar a coluna "Habilidades" para exibir como string separada por vírgulas
df_filtered["Habilidades"] = df_filtered["Habilidades"].apply(
    lambda x: ", ".join(eval(x)) if isinstance(x, str) and x.startswith("[") else str(x)
)

st.dataframe(
    df_filtered,
    hide_index=True,
    column_config={
        "Média das Métricas": st.column_config.ProgressColumn(
            "Média das Métricas",
            format="%.2f",
            min_value=0,
            max_value=float(df_filtered["Média das Métricas"].max()),
        )
    }
)