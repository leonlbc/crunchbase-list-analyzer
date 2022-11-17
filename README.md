# Crunchbase List Analyzer 

Este projeto tem a função de modelar os dados provindos da API interna da Crunchbase para persistir as listas do site de forma automática.

Os scripts atualmente funcionam com a lista "Hot Tech Companies Globally", e armazenam os dados das top 100 empresas de tech, de acordo com as métricas da Crunchbase, afim de gerar graficos e visualizacoes para um futuro WebApp.

## Run

```bash
  cd scraping-crunchbase
  pip install requirements.txt
  py scrape.py hotTechCompanies
```
    
