import streamlit as st
import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Pokémon Explorer", layout="wide")

st.header("Analise de Pokémons -TURMA CDN1 2024 - EFG-LUIZ RASSI APARECIDA DE GOIÂNIA")

# Função para obter a lista de Pokémons da API
@st.cache_data
def listar_pokemons(limit=1302):  # Pode mudar o limite para mais Pokémons
    url = f'https://pokeapi.co/api/v2/pokemon?limit={limit}'
    resposta = requests.get(url)
    if resposta.status_code == 200:
        resultados = resposta.json()['results']
        nomes = sorted(list({p['name'] for p in resultados}))  # remove duplicatas e ordena
        return nomes
        
    return []

# Função para obter dados detalhados de um Pokémon
def obter_dados_pokemon(nome_ou_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{nome_ou_id.lower()}"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        dados = resposta.json()
        stats = dados['stats']
        tipos = [tipo['type']['name'] for tipo in dados['types']]
        info = {
            "Nome": dados['name'].capitalize(),
            "ID": dados['id'],
            "Altura": dados['height'] / 10,  # altura em metros
            "Peso": dados['weight'] / 10,    # peso em kg
            "Tipos": tipos,
            "Sprite": dados['sprites']['front_default'],
            "Stats": {stat['stat']['name']: stat['base_stat'] for stat in stats}
        }
        return info
    else:
        return None

# Lista de pokémons para o selectbox
lista_pokemons = listar_pokemons()

# Selectbox para escolher o Pokémon
pokemon_input = st.selectbox("Selecione um Pokémon:", lista_pokemons)

    

if pokemon_input:
    info = obter_dados_pokemon(pokemon_input)
    
    if info:
        col1, col2 , col3 = st.columns([1, 2,3])
        
        with col1:
            st.image(info["Sprite"], width=300)
            st.markdown(f"**Nome:** {info['Nome']}")
            st.markdown(f"**ID:** {info['ID']}")
            st.markdown(f"**Altura:** {info['Altura']} m")
            st.markdown(f"**Peso:** {info['Peso']} kg")
            st.markdown(f"**Tipo(s):** {', '.join(info['Tipos'])}")
        
        with col2:
            df_stats = pd.DataFrame({
                'Atributo': list(info['Stats'].keys()),
                'Valor': list(info['Stats'].values())
            })

            st.markdown("### Atributos Base")
            sns.set_style("whitegrid")
            plt.figure(figsize=(7, 3))
            ax = sns.barplot(x="Atributo", y="Valor", data=df_stats, palette="viridis", hue="Atributo", dodge=False)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(plt.gcf())
            plt.clf()
        with col3:
            st.markdown("### Habilidades")
            habilidades = info['Stats']
            habilidades_df = pd.DataFrame({
                'Habilidade': list(habilidades.keys()),
                'Valor': list(habilidades.values())
            })
            st.dataframe(habilidades_df)    

    else:
        st.error("Pokémon não encontrado ou erro na API.")
 st.markdown(f"**Quatidade:** {limit}")


    
