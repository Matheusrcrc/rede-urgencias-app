import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Análise da Rede de Urgências - Bahia",
    page_icon="🏥",
    layout="wide"
)

# Função para carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv('dados_rede_urgencias.csv')
    return df

# Carregando os dados
df = load_data()

# Título principal
st.title('Análise da Rede de Urgências no Estado da Bahia')
st.markdown('### Avaliação da efetividade no atendimento ao Infarto Agudo do Miocárdio')

# Sidebar para filtros
st.sidebar.header('Filtros')
selected_region = st.sidebar.multiselect(
    'Selecione as Regiões',
    options=df['regiao'].unique(),
    default=df['regiao'].unique()
)

selected_years = st.sidebar.slider(
    'Selecione o Período',
    min_value=int(df['ano'].min()),
    max_value=int(df['ano'].max()),
    value=(int(df['ano'].min()), int(df['ano'].max()))
)

# Filtrando dados
mask = (df['regiao'].isin(selected_region)) & (df['ano'].between(selected_years[0], selected_years[1]))
filtered_df = df[mask]

# Layout em três colunas para métricas principais
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "População Total (Última estimativa)",
        f"{filtered_df[filtered_df['ano'] == filtered_df['ano'].max()]['populacao_estimada'].sum():,.0f}"
    )

with col2:
    st.metric(
        "Cobertura Média SAMU",
        f"{filtered_df['cobertura_samu'].mean():.1f}%"
    )

with col3:
    st.metric(
        "Taxa Média de Mortalidade IAM",
        f"{filtered_df['taxa_mortalidade_iam'].mean():.1f}"
    )

# Gráficos
st.markdown('### Análise Temporal dos Indicadores')

# Gráfico 1: Taxa de Mortalidade por IAM
fig_mortality = px.line(
    filtered_df,
    x='ano',
    y='taxa_mortalidade_iam',
    color='regiao',
    title='Taxa de Mortalidade por IAM ao longo do tempo'
)
st.plotly_chart(fig_mortality, use_container_width=True)

# Duas colunas para mais gráficos
col1, col2 = st.columns(2)

with col1:
    # Gráfico de Cobertura do SAMU
    fig_samu = px.line(
        filtered_df,
        x='ano',
        y='cobertura_samu',
        color='regiao',
        title='Cobertura do SAMU (%)'
    )
    st.plotly_chart(fig_samu, use_container_width=True)

with col2:
    # Gráfico de Cobertura da Atenção Básica
    fig_ab = px.line(
        filtered_df,
        x='ano',
        y='cobertura_atencao_basica',
        color='regiao',
        title='Cobertura da Atenção Básica (%)'
    )
    st.plotly_chart(fig_ab, use_container_width=True)

# Mapa da estrutura
st.markdown('### Estrutura da Rede de Urgências')

# Criar gráfico de barras para estrutura
latest_year = filtered_df['ano'].max()
latest_data = filtered_df[filtered_df['ano'] == latest_year]

estrutura_cols = ['n_usb', 'n_usa', 'n_upa', 'n_pa']
estrutura_data = latest_data.melt(
    id_vars=['regiao'],
    value_vars=estrutura_cols,
    var_name='tipo_unidade',
    value_name='quantidade'
)

fig_estrutura = px.bar(
    estrutura_data,
    x='regiao',
    y='quantidade',
    color='tipo_unidade',
    title=f'Estrutura da Rede de Urgências por Região (Ano: {latest_year})',
    barmode='group'
)
st.plotly_chart(fig_estrutura, use_container_width=True)

# Correlação entre indicadores
st.markdown('### Correlação entre Indicadores')

# Selecionando colunas numéricas para correlação
numeric_cols = ['cobertura_atencao_basica', 'cobertura_samu', 'taxa_leitos_uti', 'taxa_mortalidade_iam']
corr_matrix = filtered_df[numeric_cols].corr()

fig_corr = px.imshow(
    corr_matrix,
    title='Matriz de Correlação entre Indicadores',
    color_continuous_scale='RdBu'
)
st.plotly_chart(fig_corr, use_container_width=True)

# Análise detalhada
st.markdown('### Análise Detalhada dos Dados')
if st.checkbox('Mostrar dados brutos'):
    st.write(filtered_df)

# Download dos dados
st.markdown('### Download dos Dados')
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Download dados em CSV",
    data=csv,
    file_name="dados_rede_urgencias_filtrados.csv",
    mime="text/csv",
)
