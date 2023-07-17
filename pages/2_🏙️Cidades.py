import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image
import inflection

st.set_page_config(page_title='Cidades', page_icon='🏙️', layout='wide')

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

st.write('# 🏙️ Cidades')
st.markdown("#")
st.markdown("#")

with st.container():
    df_aux = df.loc[:, ['city', 'restaurant_id']].groupby('city').nunique().reset_index()
    df_aux.sort_values('restaurant_id', inplace=True, ascending=False)
    df_aux2 = df_aux.head(10)
    df_aux3 = df.loc[:, ['country_code', 'city']]
    df_aux3.drop_duplicates(inplace=True)
    df_aux4 = pd.merge(df_aux2, df_aux3, on='city', how='left')

    fig = px.bar(df_aux4, x='city', y='restaurant_id', 
                labels={'city': 'Cidade', 'restaurant_id': 'Quantidade de restaurantes'},
                color_discrete_sequence=px.colors.qualitative.Plotly,
                template='plotly_dark', text='restaurant_id', color='country_code')
    fig.update_layout(title_text='Top 10 cidades com mais restaurantes', title_x= 0.35)
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig, use_container_width=True)

st.markdown("#")
st.markdown("#")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        linhas = df['aggregate_rating'] > 4.0
        df_filtro = df.loc[linhas, :]
        df_aux = df_filtro.loc[:, ['city', 'restaurant_id']].groupby('city').nunique().reset_index()
        df_aux.sort_values('restaurant_id', inplace=True, ascending=False)
        df_aux2 = df_aux.head(7)
        df_aux3 = df.loc[:, ['country_code', 'city']]
        df_aux3.drop_duplicates(inplace=True)
        df_aux4 = pd.merge(df_aux2, df_aux3, on='city', how='left')
        fig = px.bar(df_aux4, x='city', y='restaurant_id', 
                    labels={'city': 'Cidade', 'restaurant_id': 'Quantidade de restaurantes'},
                    color_discrete_sequence=px.colors.qualitative.Plotly,
                    template='plotly_dark', text='restaurant_id', color='country_code')
        fig.update_layout(title_text='Top 7 cidades com mais restaurantes com nota acima de 4', title_x= 0.0)
        fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        linhas = df['aggregate_rating'] < 2.5
        df_filtro = df.loc[linhas, :]
        df_aux = df_filtro.loc[:, ['city', 'restaurant_id']].groupby('city').nunique().reset_index()
        df_aux.sort_values('restaurant_id', inplace=True, ascending=False)
        df_aux2 = df_aux.head(7)
        df_aux3 = df.loc[:, ['country_code', 'city']]
        df_aux3.drop_duplicates(inplace=True)
        df_aux4 = pd.merge(df_aux2, df_aux3, on='city', how='left')
        fig = px.bar(df_aux4, x='city', y='restaurant_id', 
                    labels={'city': 'Cidade', 'restaurant_id': 'Quantidade de restaurantes'},
                    color_discrete_sequence=px.colors.qualitative.Plotly,
                    template='plotly_dark', text='restaurant_id', color='country_code')
        fig.update_layout(title_text='Top 7 cidades com mais restaurantes com nota abaixo de 2.5', title_x= 0.0)
        fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig, use_container_width=True)

st.markdown("#")
st.markdown("#")

with st.container():
    df_aux = df.loc[:, ['city', 'cuisines']].groupby('city').nunique().reset_index()
    df_aux.sort_values('cuisines', inplace=True, ascending=False)
    df_aux2 = df_aux.head(10)
    df_aux3 = df.loc[:, ['country_code', 'city']]
    df_aux3.drop_duplicates(inplace=True)
    df_aux4 = pd.merge(df_aux2, df_aux3, on='city', how='left')

    fig = px.bar(df_aux4, x='city', y='cuisines', 
                labels={'city': 'Cidade', 'cuisines': 'Quantidade de restaurantes'},
                color_discrete_sequence=px.colors.qualitative.Plotly,
                template='plotly_dark', text='cuisines', color='country_code')
    fig.update_layout(title_text='Top 10 cidades com mais tipos culinários distintos', title_x= 0.35)
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig, use_container_width=True)
