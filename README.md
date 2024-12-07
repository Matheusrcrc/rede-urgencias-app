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
