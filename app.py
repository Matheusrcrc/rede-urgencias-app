
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
    df = pd.read_csv('dados_rede_urgencias_bahia.csv')
    return df

# Carregando os dados
df = load_data()

# Título principal
st.title('Análise da Rede de Urgências no Estado da Bahia')
st.markdown('### Dashboard de Monitoramento e Avaliação')

# Sidebar para filtros
st.sidebar.header('Filtros')

# Agrupamento por macrorregião
macrorregioes = {
    'NORTE': ['JUAZEIRO', 'PAULO AFONSO'],
    'CENTRO-NORTE': ['JACOBINA', 'IRECÊ', 'SEABRA'],
    'NORDESTE': ['ALAGOINHAS', 'RIBEIRA DO POMBAL', 'SERRINHA'],
    'LESTE': ['SALVADOR', 'CAMAÇARI', 'CRUZ DAS ALMAS', 'SANTO ANTÔNIO DE JESUS'],
    'CENTRO-LESTE': ['FEIRA DE SANTANA'],
    'SUDOESTE': ['VITÓRIA DA CONQUISTA', 'BRUMADO', 'GUANAMBI', 'ITAPETINGA'],
    'SUL': ['ILHÉUS', 'ITABUNA', 'TEIXEIRA DE FREITAS', 'VALENÇA', 'PORTO SEGURO'],
    'OESTE': ['BARREIRAS', 'SANTA MARIA DA VITÓRIA', 'IBOTIRAMA', 'BOM JESUS DA LAPA']
}

# Criar seletor de macrorregião
selected_macro = st.sidebar.multiselect(
    'Selecione as Macrorregiões',
    options=list(macrorregioes.keys()),
    default=list(macrorregioes.keys())[0]
)

# Criar lista de regiões baseada nas macrorregiões selecionadas
selected_regions = []
for macro in selected_macro:
    selected_regions.extend(macrorregioes[macro])

# Filtro de período
selected_years = st.sidebar.slider(
    'Selecione o Período',
    min_value=int(df['ano'].min()),
    max_value=int(df['ano'].max()),
    value=(int(df['ano'].min()), int(df['ano'].max()))
)

# Filtrando dados
mask = (df['regiao'].isin(selected_regions)) & (df['ano'].between(selected_years[0], selected_years[1]))
filtered_df = df[mask]

# Layout em três colunas para métricas principais
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "População Total",
        f"{filtered_df[filtered_df['ano'] == filtered_df['ano'].max()]['populacao_estimada'].sum():,.0f}"
    )

with col2:
    st.metric(
        "Cobertura SAMU",
        f"{filtered_df['cobertura_samu'].mean():.1f}%"
    )

with col3:
    st.metric(
        "Cobertura Atenção Básica",
        f"{filtered_df['cobertura_atencao_basica'].mean():.1f}%"
    )

with col4:
    st.metric(
        "Taxa Média de Mortalidade IAM",
        f"{filtered_df['taxa_mortalidade_iam'].mean():.1f}"
    )

# Tabs para diferentes análises
tab1, tab2, tab3 = st.tabs(["Indicadores Temporais", "Estrutura da Rede", "Análise Regional"])

with tab1:
    # Gráfico 1: Taxa de Mortalidade por IAM
    st.subheader('Evolução Temporal dos Indicadores')
    
    # Seletor de indicador
    indicador = st.selectbox(
        'Selecione o Indicador',
        ['taxa_mortalidade_iam', 'cobertura_samu', 'cobertura_atencao_basica', 'taxa_leitos_uti']
    )
    
    nomes_indicadores = {
        'taxa_mortalidade_iam': 'Taxa de Mortalidade por IAM',
        'cobertura_samu': 'Cobertura SAMU (%)',
        'cobertura_atencao_basica': 'Cobertura da Atenção Básica (%)',
        'taxa_leitos_uti': 'Taxa de Leitos UTI'
    }
    
    fig = px.line(
        filtered_df,
        x='ano',
        y=indicador,
        color='regiao',
        title=f'Evolução do Indicador: {nomes_indicadores[indicador]}'
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader('Estrutura da Rede de Urgências')
    
    # Criar gráfico de barras para estrutura
    latest_year = filtered_df['ano'].max()
    latest_data = filtered_df[filtered_df['ano'] == latest_year]

    # Seletor de tipo de unidade
    unit_type = st.selectbox(
        'Tipo de Unidade',
        ['Todas', 'USB', 'USA', 'UPA', 'PA']
    )

    if unit_type == 'Todas':
        estrutura_cols = ['n_usb', 'n_usa', 'n_upa', 'n_pa']
        estrutura_data = latest_data.melt(
            id_vars=['regiao'],
            value_vars=estrutura_cols,
            var_name='tipo_unidade',
            value_name='quantidade'
        )
        
        fig = px.bar(
            estrutura_data,
            x='regiao',
            y='quantidade',
            color='tipo_unidade',
            title=f'Estrutura da Rede de Urgências por Região (Ano: {latest_year})',
            barmode='group'
        )
    else:
        col_map = {'USB': 'n_usb', 'USA': 'n_usa', 'UPA': 'n_upa', 'PA': 'n_pa'}
        fig = px.bar(
            latest_data,
            x='regiao',
            y=col_map[unit_type],
            title=f'Quantidade de {unit_type} por Região (Ano: {latest_year})'
        )
    
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader('Análise Comparativa Regional')
    
    # Seletor de indicadores para comparação
    indicador_x = st.selectbox(
        'Indicador Eixo X',
        ['cobertura_samu', 'cobertura_atencao_basica', 'taxa_leitos_uti', 'taxa_mortalidade_iam'],
        key='ind_x'
    )
    
    indicador_y = st.selectbox(
        'Indicador Eixo Y',
        ['taxa_mortalidade_iam', 'cobertura_samu', 'cobertura_atencao_basica', 'taxa_leitos_uti'],
        key='ind_y'
    )
    
    # Criar scatter plot
    latest_data = filtered_df[filtered_df['ano'] == latest_year]
    fig = px.scatter(
        latest_data,
        x=indicador_x,
        y=indicador_y,
        color='regiao',
        title=f'Correlação entre {nomes_indicadores[indicador_x]} e {nomes_indicadores[indicador_y]}',
        hover_data=['populacao_estimada']
    )
    st.plotly_chart(fig, use_container_width=True)

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

# Adicionar footer com informações
st.markdown('---')
st.markdown('''
    #### Notas:
    - Os dados apresentados são atualizados anualmente
    - A taxa de mortalidade por IAM é calculada por 100.000 habitantes
    - A cobertura do SAMU e da Atenção Básica é apresentada em percentual
    - USB: Unidade de Suporte Básico
    - USA: Unidade de Suporte Avançado
    - UPA: Unidade de Pronto Atendimento
    - PA: Pronto Atendimento
''')
