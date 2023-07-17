import streamlit as st
import pandas as pd
import inflection
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from PIL import Image

st.set_page_config(page_title='Home', page_icon='🏠', layout='wide')

df = pd.read_csv('dataset\zomato.csv')


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

st.write('# Fome Zero!')
st.write('## The Best Place To Find Your Favorite Food!')
st.write('### Você encontrará os seguintes restaurantes na nossa plataforma:')

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        col1.metric('Nº de Restaurantes:', len(df['restaurant_id'].unique()))

    with col2:
        col2.metric('Nº de Países:', len(df['country_code'].unique()))

    with col3:
        col3.metric('Nº de Cidades:', len(df['city'].unique()))

    with col4:
        soma = df['votes'].sum()
        col4.metric('Nº de Avaliações:', '{:,}'.format(soma).replace(',','.'))

    with col5:
        col5.metric('Tipos de culinária:', len(df['cuisines'].unique()))

with st.container():
    df_aux = df.loc[:, ['restaurant_id', 'longitude', 'latitude', 'aggregate_rating', 
                    'average_cost_for_two']].groupby('restaurant_id').mean().reset_index()
    df_aux2 = df.loc[:, ['restaurant_id', 'restaurant_name', 'cuisines', 'currency', 'votes']]
    df_local = pd.merge(df_aux, df_aux2, on='restaurant_id', how='left')
    map = folium.Map(location=[30.514771, 28.989190], zoom_start=2)
    map_cluster = MarkerCluster().add_to(map)
    for index, row in df_local.iterrows():
        frame = folium.Popup('<b>' + row['restaurant_name'] + '</b> <br> <br>' + 'Preço: ' + str(row['average_cost_for_two']) +
                              '(' + row['currency'] + ') p\ dois <br>' + 'Tipo: ' + row['cuisines'] + '<br>' +
                              'Nota: ' + str(row['aggregate_rating']) + '/5.0 <br>' + 'Votos: ' + str(row['votes']), lazy=True,
                              min_widht=2000, max_width=2000)
        #pop = folium.Popup(frame, min_widht=1000, max_width=2000)
        folium.Marker(location=[row['latitude'], row['longitude']], popup=frame).add_to(map_cluster)
    folium_static(map, width= 1024, height= 600)
