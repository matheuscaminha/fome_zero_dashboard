import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image
import inflection

st.set_page_config(page_title='Países', page_icon='🌎', layout='wide')

df = pd.read_csv("dataset/zomato.csv")

# ---------------------------------------------- #
#### LIMPEZA DE DADOS ####
# ---------------------------------------------- #
paises = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

df['Country Code'] = df['Country Code'].replace(paises)

cor = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}

df['Rating color'] = df['Rating color'].replace(cor)

preço = {
1: "cheap",
2: "normal",
3: "expansive",
4: "gourmet",
}

df['Price range'] = df['Price range'].replace(preço)

title = lambda x: inflection.titleize(x)
snakecase = lambda x: inflection.underscore(x)
spaces = lambda x: x.replace(" ", "")
cols_old = list(df.columns)
cols_old = list(map(title, cols_old))
cols_old = list(map(spaces, cols_old))
cols_new = list(map(snakecase, cols_old))
df.columns = cols_new

df['cuisines'] = df['cuisines'].astype( str )
df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

df.drop(385, inplace=True)
df.dropna(inplace=True)

# ---------------------------------------------- #
#### CONSTRUÇÃO DA SIDEBAR ####
# ---------------------------------------------- #

image = Image.open("logo-no-background.png")
st.sidebar.image(image, width=300)
st.sidebar.markdown("""---""")

# ---------------------------------------------- #
#### CONSTRUÇÃO DOS FILTROS ####
# ---------------------------------------------- #

st.sidebar.markdown('## Selecione o(s) país(es) desejados:')
filtro = st.sidebar.multiselect('Seleção atual:', 
                                     df['country_code'].unique(),
                                     default=df['country_code'].unique())
st.sidebar.markdown("""---""")

linhas_selecionadas = df['country_code'].isin(filtro)
df = df.loc[linhas_selecionadas, :]

# ---------------------------------------------- #
#### CONTEÚDO DA PAGINA ####
# ---------------------------------------------- #

st.write('# 🌎 Países')
st.markdown("#")
st.markdown("#")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        df_aux = df.loc[:, ['country_code', 'restaurant_id']].groupby('country_code').nunique().reset_index()
        df_aux.sort_values('restaurant_id', inplace=True, ascending=False)
        fig = px.bar(df_aux, x='country_code', y='restaurant_id', 
                     labels={'country_code': 'País', 'restaurant_id': 'Quantidade de restaurantes'},
                     color_discrete_sequence=px.colors.qualitative.Plotly,
                     template='plotly_dark', text='restaurant_id')
        fig.update_layout(title_text='Quantidade de Restaurantes', title_x= 0.35)
        fig.update_traces(textangle=0)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        df_aux = df.loc[:, ['country_code', 'city']].groupby('country_code').nunique().reset_index()
        df_aux.sort_values('city', inplace=True, ascending=False)
        fig = px.bar(df_aux, x='country_code', y='city', 
                     labels={'country_code': 'País', 'city': 'Quantidade de cidades'},
                     color_discrete_sequence=px.colors.qualitative.Plotly,
                     template='plotly_dark', text='city')
        fig.update_layout(title_text='Quantidade de Cidades', title_x= 0.35)
        fig.update_traces(textangle=0)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("#")
st.markdown("#")

with st.container():
    df_aux = df.loc[:, ['country_code', 'votes']].groupby('country_code').mean().reset_index()
    df_aux.sort_values('votes', inplace=True, ascending=False)
    fig = px.bar(df_aux, x='country_code', y='votes', 
                labels={'country_code': 'País', 'votes': 'Avaliações'},
                color_discrete_sequence=px.colors.qualitative.Plotly,
                template='plotly_dark', text='votes')
    fig.update_layout(title_text='Quantidade Média de Avaliações por Restaurante', title_x= 0.3)
    fig.update_traces(texttemplate='%{text:.2s}', textangle=0)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("#")
st.markdown("#")

with st.container():
    df_aux = df.loc[:, ['country_code', 'average_cost_for_two']].groupby('country_code').mean().reset_index()
    df_aux2 = df.loc[:, ['country_code', 'currency']]
    df_aux2.drop_duplicates(inplace=True)
    df_aux3 = pd.merge(df_aux, df_aux2, on='country_code', how='left')
    df_aux3.sort_values('average_cost_for_two', inplace=True, ascending=False)
    fig = px.bar(df_aux3, x='country_code', y='average_cost_for_two', 
                    labels={'country_code': 'País', 'average_cost_for_two': 'Preço'},
                    color_discrete_sequence=px.colors.qualitative.Plotly,
                    template='plotly_dark', text='average_cost_for_two',
                    hover_data='currency', color='currency')
    fig.update_layout(title_text='Preço Médio para Duas Pessoas', title_x= 0.4)
    fig.update_traces(texttemplate='%{text:.2s}', textangle=0)
    st.plotly_chart(fig, use_container_width=True)
