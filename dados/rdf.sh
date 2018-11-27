#!/bin/bash

#############################
## Para iniciar o servidor ##
#java -server -Xmx4g -jar blazegraph.jar &

################
## gera o RDF ##
python rdf_gen.py

#################################
## envia o RDF para o servidor ##
_rdf="test.ttl"
_rdf_formato="Content-Type:text/Turtle"
_servidor="http://localhost:9999/blazegraph/sparql"
curl -X POST -H $_rdf_formato --data-binary '@'$_rdf $_servidor