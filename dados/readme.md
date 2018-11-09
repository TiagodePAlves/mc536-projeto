# Dados

Todos os dados são do aplicativo [Flaredown](http://flaredown.com/), em que os usuários rastreiam suas doenças crônicas ao longo do tempo, com os sintomas, os tratamentos e outros dados relevantes. Esses dados foram publicados na plataforma [Kaggle](https://www.kaggle.com/) e podem ser recuperados por lá.

## Fonte

- [Publicação dos dados no Kaggle](https://www.kaggle.com/flaredown/flaredown-autoimmune-symptom-tracker)

## Arquivos

Os dados originais, extraídos diretamente da fonte, se encontram em `flaredown-completo.csv`, retirados em outubro de 2018. O arquivo `flaredown.csv` é só uma amostragem aleatória de 10 mil dos valores originais, para os testes.

## Processamento

O _script_ `dados.sh` for feito para baixar os dados originais (com a [API do Kaggle](https://github.com/Kaggle/kaggle-api)), extrair e ajustá-los. Além disso, é gerado também a amostra de 10 mil registros aleatórios (ou qualquer outro valor que pode ser passado como argumento para o _script_).
