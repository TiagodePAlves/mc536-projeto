#!/bin/bash
#####################
## DADOS COMPLETOS ##

# baixando os dados completos
kaggle datasets download -d flaredown/flaredown-autoimmune-symptom-tracker

# extraindo e renomeando
unzip flaredown-autoimmune-symptom-tracker.zip
rm flaredown-autoimmune-symptom-tracker.zip
mv fd-export.csv flaredown-completo.csv

######################
## DADOS DE AMOSTRA ##

# cabeçalho dos dados
head -n 1 flaredown-completo.csv > flaredown.csv

# número de amostras
if [ -n "$1" ]
then
    _num=$1
else
    _num=10000
fi

# montagem das amostras
tail -n +2 flaredown-completo.csv | shuf | shuf -n $_num | sed '/"/d' >> flaredown.csv
