import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image
import inflection

st.set_page_config(page_title='Cozinhas', page_icon='🍽️', layout='wide')

df = pd.read_csv('\dataset\zomato.csv')

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

image = Image.open('logo-no-background.png')
st.sidebar.image(image, width=300)
st.sidebar.markdown("""---""")

# ---------------------------------------------- #
#### CONSTRUÇÃO DOS FILTROS ####
# ---------------------------------------------- #

with st.sidebar.expander('Selecione o(s) país(es) desejados:'):
    filtro_pais = st.multiselect('Seleção atual:', 
                                        df['country_code'].unique(),
                                        default=df['country_code'].unique())

with st.sidebar.expander('Selecione o(s) tipo(s) de cunlinária desejados:'):
    filtro_cozinhas = st.multiselect('Seleção atual:', 
                                        df['cuisines'].unique(),
                                        default=df['cuisines'].unique())
st.sidebar.markdown("""---""")

linhas_selecionadas = df['country_code'].isin(filtro_pais)
df = df.loc[linhas_selecionadas, :]

linhas_selecionadas = df['cuisines'].isin(filtro_cozinhas)
df = df.loc[linhas_selecionadas, :]

if df['restaurant_id'].nunique() < 100:
    num_restaurantes = df['restaurant_id'].nunique()
else:
    num_restaurantes = 100

filtro_restaurantes = st.sidebar.slider('Selecione quantos restaurantes deseja vizualizar:',
                                        1, num_restaurantes, 10)

# ---------------------------------------------- #
#### CONTEÚDO DA PAGINA ####
# ---------------------------------------------- #

st.write('# 🍽️Cozinhas')
st.markdown("## Melhor restaurante para cada um dos tipos de culinária mais populares:")

with st.container():
    df_pop = df.loc[:, ['cuisines', 'restaurant_id']].groupby('cuisines').nunique().reset_index()
    df_pop.sort_values('restaurant_id', ascending=False, inplace=True)
    df_pop = df_pop.iloc[:5]

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        linhas = df['cuisines'] == df_pop.iloc[0, 0]
        df_aux = df.loc[linhas, :]
        df_aux.sort_values(by=['aggregate_rating', 'votes'], inplace=True, ascending=False)
        col1.metric(f'{df_pop.iloc[0, 0]}: {df_aux.iloc[0, 1]}', f'{df_aux.iloc[0, 17]}/5.0',
                    help=f'País: {df_aux.iloc[0, 2]} \n\n'+ 
                         f'Cidade: {df_aux.iloc[0, 3]} \n\n' +
                         f'Média de Prato Para Dois: {df_aux.iloc[0, 10]} ({df_aux.iloc[0, 11]})')

    with col2:
        linhas = df['cuisines'] == df_pop.iloc[1, 0]
        df_aux = df.loc[linhas, :]
        df_aux.sort_values(by=['aggregate_rating', 'votes'], inplace=True, ascending=False)
        col2.metric(f'{df_pop.iloc[1, 0]}: {df_aux.iloc[0, 1]}', f'{df_aux.iloc[0, 17]}/5.0',
                    help=f'País: {df_aux.iloc[0, 2]} \n\n'+ 
                         f'Cidade: {df_aux.iloc[0, 3]} \n\n' +
                         f'Média de Prato Para Dois: {df_aux.iloc[0, 10]} ({df_aux.iloc[0, 11]})')

    with col3:
        linhas = df['cuisines'] == df_pop.iloc[2, 0]
        df_aux = df.loc[linhas, :]
        df_aux.sort_values(by=['aggregate_rating', 'votes'], inplace=True, ascending=False)
        col3.metric(f'{df_pop.iloc[2, 0]}: {df_aux.iloc[0, 1]}', f'{df_aux.iloc[0, 17]}/5.0',
                    help=f'País: {df_aux.iloc[0, 2]} \n\n'+ 
                         f'Cidade: {df_aux.iloc[0, 3]} \n\n' +
                         f'Média de Prato Para Dois: {df_aux.iloc[0, 10]} ({df_aux.iloc[0, 11]})')

    with col4:
        linhas = df['cuisines'] == df_pop.iloc[3, 0]
        df_aux = df.loc[linhas, :]
        df_aux.sort_values(by=['aggregate_rating', 'votes'], inplace=True, ascending=False)
        col4.metric(f'{df_pop.iloc[3, 0]}: {df_aux.iloc[0, 1]}', f'{df_aux.iloc[0, 17]}/5.0',
                    help=f'País: {df_aux.iloc[0, 2]} \n\n'+ 
                         f'Cidade: {df_aux.iloc[0, 3]} \n\n' +
                         f'Média de Prato Para Dois: {df_aux.iloc[0, 10]} ({df_aux.iloc[0, 11]})')

    with col5:
        linhas = df['cuisines'] == df_pop.iloc[4, 0]
        df_aux = df.loc[linhas, :]
        df_aux.sort_values(by=['aggregate_rating', 'votes'], inplace=True, ascending=False)
        col5.metric(f'{df_pop.iloc[4, 0]}: {df_aux.iloc[0, 1]}', f'{df_aux.iloc[0, 17]}/5.0',
                    help=f'País: {df_aux.iloc[0, 2]} \n\n'+ 
                         f'Cidade: {df_aux.iloc[0, 3]} \n\n' +
                         f'Média de Prato Para Dois: {df_aux.iloc[0, 10]} ({df_aux.iloc[0, 11]})')

with st.container():
    st.markdown(f'## Top {filtro_restaurantes} Restaurantes:')
    df.sort_values('aggregate_rating', inplace=True, ascending=False)
    st.dataframe(df.iloc[:filtro_restaurantes, [1, 2, 3, 4, 9,10, 11, 17, 20]],
                            use_container_width=True, hide_index=True, column_config={
                                'restaurant_name': 'Nome do restaurante',
                                'country_code': 'País',
                                'city': 'Cidade',
                                'address': 'Endereço',
                                'cuisines': 'Tipo de cozinha',
                                'average_cost_for_two': 'Preço médio para duas pessoas',
                                'currency': 'Moeda',
                                'aggregate_rating': st.column_config.NumberColumn('Avaliação média', format='%.2f ⭐'),
                                'votes': 'Avaliações'
                            })

st.markdown("#")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        df_aux = df.loc[:, ['cuisines', 'aggregate_rating']].groupby('cuisines').mean().reset_index()
        df_aux.sort_values('aggregate_rating', inplace=True, ascending=False)
        df_aux2 = df_aux.head(filtro_restaurantes)
        fig = px.bar(df_aux2, x='cuisines', y='aggregate_rating', 
                    labels={'cuisines': 'Culinária', 'aggregate_rating': 'Avaliação Média'},
                    color_discrete_sequence=px.colors.qualitative.Plotly,
                    template='plotly_dark', text='aggregate_rating')
        fig.update_layout(title_text=f'Top {filtro_restaurantes} Melhores tipos Culinários', title_x= 0.30)
        fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
        fig.update_traces(texttemplate='%{text:.2f}')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        df_min = df.loc[:, ['cuisines', 'aggregate_rating']].groupby('cuisines').mean().reset_index()
        df_min.sort_values('aggregate_rating', inplace=True, ascending=True)
        linhas_vazias = df_min['aggregate_rating'] != 0
        df_min2 = df_min.loc[linhas_vazias, :]
        df_min3 = df_min2.head(filtro_restaurantes)
        fig = px.bar(df_min3, x='cuisines', y='aggregate_rating', 
                    labels={'cuisines': 'Culinária', 'aggregate_rating': 'Avaliação Média'},
                    color_discrete_sequence=px.colors.qualitative.Plotly,
                    template='plotly_dark', text='aggregate_rating')
        fig.update_layout(title_text=f'Top {filtro_restaurantes} Piores tipos Culinários', title_x= 0.30)
        fig.update_layout(barmode='stack', xaxis={'categoryorder':'total ascending'})
        fig.update_traces(texttemplate='%{text:.2f}')
        st.plotly_chart(fig, use_container_width=True)