#!/bin/bash

#############################
## Para iniciar o servidor ##
#java -server -Xmx4g -jar blazegraph.jar &

################
## gera o RDF ##
_rdf="../dados/flaredown.ttl"
python rdf_gen.py >$_rdf

#################################
## envia o RDF para o servidor ##
_rdf_formato="Content-Type:text/Turtle"
_servidor="http://localhost:9999/blazegraph/sparql"
curl -X POST -H $_rdf_formato --data-binary '@'$_rdf $_servidor