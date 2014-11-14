#!/bin/bash
TOA_BIN_PATH=$2
TOA_FLOW_PATH=$1
FILE=`date --date="10 minutes ago" "+/$TOA_FLOW_PATH/%Y/%Y-%m/%Y-%m-%d/ft-v05.%Y-%m-%d.%H%M**-0400"`
python $TOA_BIN_PATH/flows-db-update.py $FILE 
python $TOA_BIN_PATH/flowsgrapher.py 
python $TOA_BIN_PATH/p2p_graphic.py
