
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import folium
from folium import plugins
from streamlit_folium import folium_static
import json
import branca.colormap as cm
import geopandas as gpd

# Configuração da página
st.set_page_config(
    page_title="Análise da Rede de Urgências - Bahia",
    page_icon="🏥",
    layout="wide"
)

# Função para carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv('dados_rede_urgencias_bahia.csv')
    return df

@st.cache_data
def load_geojson():
    with open('bahia_regioes_saude.geojson') as f:
        return json.load(f)

# Função para criar mapa base
def create_base_map(center_lat=-12.5, center_lon=-41.7, zoom=6):
    return folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles='cartodbpositron'
    )

# Função para criar mapa com choropleth
def create_choropleth_map(df, geojson_data, indicator, year):
    # Filtrar dados para o ano selecionado
    df_year = df[df['ano'] == year]
    
    # Criar mapa base
    m = create_base_map()
    
    # Criar escala de cores
    colormap = cm.LinearColormap(
        colors=['#fee5d9', '#fcae91', '#fb6a4a', '#de2d26', '#a50f15'],
        vmin=df_year[indicator].min(),
        vmax=df_year[indicator].max()
    )
    
    # Adicionar choropleth
    folium.Choropleth(
        geo_data=geojson_data,
        name='choropleth',
        data=df_year,
        columns=['codigo_regiao', indicator],
        key_on='feature.properties.id',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=indicator
    ).add_to(m)
    
    # Adicionar tooltips
    folium.GeoJsonTooltip(
        fields=['regiao', indicator],
        aliases=['Região:', indicator + ':'],
        style=('background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;')
    ).add_to(m)
    
    # Adicionar legenda
    colormap.add_to(m)
    
    return m

# Função para criar mapa de calor
def create_heatmap(df, indicator, year):
    df_year = df[df['ano'] == year]
    
    m = create_base_map()
    
    # Adicionar heatmap
    heat_data = [[row['lat'], row['lon'], row[indicator]] 
                 for index, row in df_year.iterrows()]
    
    plugins.HeatMap(heat_data).add_to(m)
    
    return m

# Função para criar mapa de marcadores
def create_marker_map(df, year, unit_type):
    df_year = df[df['ano'] == year]
    
    m = create_base_map()
    
    # Dicionário de ícones para cada tipo de unidade
    icons = {
        'USB': 'ambulance',
        'USA': 'plus-square',
        'UPA': 'hospital-o',
        'PA': 'medkit'
    }
    
    # Adicionar marcadores
    for idx, row in df_year.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f"{row['regiao']} - {unit_type}: {row[f'n_{unit_type.lower()}']}",
            icon=folium.Icon(color='red', icon=icons.get(unit_type, 'info-sign'))
        ).add_to(m)
    
    return m

# Carregar dados
df = load_data()
geojson_data = load_geojson()

# Título principal
st.title('Análise da Rede de Urgências no Estado da Bahia')
st.markdown('### Dashboard de Monitoramento e Avaliação com Visualização Geográfica')

# Sidebar para filtros
st.sidebar.header('Filtros do Mapa')

# Seleção do tipo de mapa
map_type = st.sidebar.selectbox(
    'Tipo de Visualização',
    ['Choropleth', 'Heatmap', 'Marcadores']
)

# Seleção do ano
selected_year = st.sidebar.slider(
    'Ano',
    min_value=int(df['ano'].min()),
    max_value=int(df['ano'].max()),
    value=int(df['ano'].max())
)

# Filtros específicos baseados no tipo de mapa
if map_type == 'Choropleth':
    selected_indicator = st.sidebar.selectbox(
        'Indicador',
        ['cobertura_samu', 'cobertura_atencao_basica', 'taxa_mortalidade_iam', 'taxa_leitos_uti']
    )
    m = create_choropleth_map(df, geojson_data, selected_indicator, selected_year)
    
elif map_type == 'Heatmap':
    selected_indicator = st.sidebar.selectbox(
        'Indicador',
        ['cobertura_samu', 'cobertura_atencao_basica', 'taxa_mortalidade_iam', 'taxa_leitos_uti']
    )
    m = create_heatmap(df, selected_indicator, selected_year)
    
else:  # Marcadores
    unit_type = st.sidebar.selectbox(
        'Tipo de Unidade',
        ['USB', 'USA', 'UPA', 'PA']
    )
    m = create_marker_map(df, selected_year, unit_type)

# Exibir mapa
st.subheader('Mapa Interativo')
folium_static(m)

# Métricas complementares
st.subheader('Métricas Complementares')
col1, col2, col3 = st.columns(3)

df_year = df[df['ano'] == selected_year]

with col1:
    st.metric(
        "Total de Unidades",
        f"{df_year[['n_usb', 'n_usa', 'n_upa', 'n_pa']].sum().sum():,.0f}"
    )

with col2:
    st.metric(
        "Cobertura Média SAMU",
        f"{df_year['cobertura_samu'].mean():.1f}%"
    )

with col3:
    st.metric(
        "Taxa Média de Mortalidade",
        f"{df_year['taxa_mortalidade_iam'].mean():.1f}"
    )

# Análise detalhada
st.markdown('### Análise Detalhada dos Dados')
if st.checkbox('Mostrar dados do ano selecionado'):
    st.write(df_year)

# Download dos dados
st.markdown('### Download dos Dados')
csv = df_year.to_csv(index=False)
st.download_button(
    label="Download dados em CSV",
    data=csv,
    file_name=f"dados_rede_urgencias_{selected_year}.csv",
    mime="text/csv",
)

# Adicionar footer com informações
st.markdown('---')
st.markdown('''
    #### Tipos de Visualização:
    - **Choropleth**: Mapa com cores graduadas mostrando a intensidade dos indicadores por região
    - **Heatmap**: Mapa de calor mostrando concentração de serviços/indicadores
    - **Marcadores**: Localização específica das unidades de saúde
    
    #### Indicadores Disponíveis:
    - Cobertura do SAMU (%)
    - Cobertura da Atenção Básica (%)
    - Taxa de Mortalidade por IAM
    - Taxa de Leitos UTI
    - Distribuição de Unidades (USB, USA, UPA, PA)
''')
