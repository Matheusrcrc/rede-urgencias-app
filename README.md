# Dashboard da Rede de Urgências da Bahia

## Sobre
Este dashboard apresenta uma análise completa da rede de urgências e emergências do estado da Bahia, incluindo todas as regiões de saúde.

## Funcionalidades
- Visualização de indicadores por macrorregião
- Análise temporal de indicadores chave
- Comparação entre regiões de saúde
- Mapeamento da estrutura da rede
- Download de dados filtrados

## Como executar
1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o aplicativo:
```bash
streamlit run app.py
```

## Estrutura de Dados
O dashboard utiliza dados das seguintes dimensões:
- Cobertura do SAMU
- Cobertura da Atenção Básica
- Taxa de Mortalidade por IAM
- Distribuição de unidades (USB, USA, UPA, PA)
- Taxa de leitos de UTI

## Macrorregiões de Saúde
- NORTE
- CENTRO-NORTE
- NORDESTE
- LESTE
- CENTRO-LESTE
- SUDOESTE
- SUL
- OESTE

## Notas
- Os dados são atualizados anualmente
- As taxas são calculadas por 100.000 habitantes
- As coberturas são apresentadas em percentual

## Visualizações no Mapa

O dashboard agora inclui um mapa interativo com três tipos de visualização:

### 1. Mapa Choropleth
- Visualização por cores graduadas dos indicadores
- Comparação entre regiões
- Tooltip com informações detalhadas

### 2. Mapa de Calor (Heatmap)
- Densidade de serviços e indicadores
- Identificação de áreas de concentração
- Análise de distribuição espacial

### 3. Mapa de Marcadores
- Localização específica das unidades
- Ícones diferenciados por tipo de unidade
- Informações detalhadas em popup

### Filtros Disponíveis
- Seleção do tipo de visualização
- Escolha do ano
- Seleção de indicadores
- Filtro por tipo de unidade

### Indicadores no Mapa
- Cobertura do SAMU
- Cobertura da Atenção Básica
- Taxa de Mortalidade por IAM
- Taxa de leitos de UTI
- Distribuição de unidades (USB, USA, UPA, PA)

### Como usar o mapa
1. Selecione o tipo de visualização desejada
2. Escolha o ano de referência
3. Selecione o indicador ou tipo de unidade
4. Interaja com o mapa usando zoom e pan
5. Clique nos elementos para mais informações
