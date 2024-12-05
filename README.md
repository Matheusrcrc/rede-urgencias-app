
# Análise da Rede de Urgências - Bahia

## Sobre o Projeto
Aplicação para análise da efetividade da rede de atenção às urgências no atendimento ao Infarto Agudo do Miocárdio no estado da Bahia.

## Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Executando a aplicação

```bash
streamlit run app.py
```

## Funcionalidades

- Visualização temporal dos indicadores
- Análise comparativa entre regiões
- Correlação entre diferentes métricas
- Download dos dados filtrados
- Filtros por região e período

## Estrutura dos Dados

O aplicativo analisa os seguintes indicadores:
- População estimada
- Cobertura de atenção básica
- Cobertura SAMU
- Número de unidades (USB, USA, UPA, PA)
- Taxa de leitos UTI
- Taxa de mortalidade por IAM

## Regiões Analisadas

- Alagoinhas (código 290001)
- Ribeira do Pombal (código 29019)
