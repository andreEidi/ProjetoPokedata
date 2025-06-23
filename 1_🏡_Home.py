import streamlit as st
import pandas as pd
from datetime import datetime

# Check if the session state already has the data
if "data" not in st.session_state:
    df_data = pd.read_csv("datasets/All_Pokemon.csv")
    df_data["Generation"] = df_data["Generation"].astype(int)
    df_data = df_data[df_data['Generation'] <= 6]
    df_data["Type 1"].fillna("Nenhum", inplace=True)
    df_data["Type 2"].fillna("Nenhum", inplace=True)
    df_data = df_data.sort_values(by="Generation")
    st.session_state["data"] = df_data

# Set the page configuration
st.set_page_config(
    page_title="Pokemon Data Explorer",
    page_icon="datasets/Poké_Ball_icon.png", 
    layout="wide",
)

# Place the text and image at the top of the page
st.image('datasets/Poké_Ball_icon.png', width=50)
st.markdown("# The world of PokeData!")

# Sidebar for navigation and information
st.sidebar.markdown("Dados Disponíveis em [Kaggle](https://www.kaggle.com/datasets/maca11/all-pokemon-dataset)")
st.sidebar.markdown("Imagens Disponíveis em [Kaggle](https://www.kaggle.com/datasets/kvpratama/pokemon-images-dataset?resource=download)")
st.sidebar.markdown("Desenvolvido por [Andre Eidi Maeda](https://www.linkedin.com/in/andre-eidi-maeda/)")


# Display the project description
st.markdown(
    """
    Este projeto tem como objetivo criar uma visualização interativa de todos os Pokémons disponíveis no conjunto de dados. 
    Através desta aplicação, você poderá explorar informações detalhadas sobre cada Pokémon, como seus atributos, tipos, estatísticas e muito mais. 
    A ferramenta foi desenvolvida para facilitar a análise, comparação e descoberta de padrões entre os diferentes Pokémons, tornando o processo de exploração de dados mais intuitivo e acessível para fãs, pesquisadores e entusiastas do universo Pokémon.
    A base de dados possui informações sobre os Pokémons, como número, nome, tipo, geração, altura, peso e outras características relevantes até a 6ª geração, com 801 registros contando formas alternativas.
    """
)

st.video("https://youtu.be/BoZ0Zwab6Oc?si=w7_2y2LxQBw5j7Rd", loop=True, autoplay=False, muted=False, width="stretch")

