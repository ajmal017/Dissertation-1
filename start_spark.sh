#!/usr/bin/env bash
spark-submit --master "spark://student32-x1:7077" \
    --py-files dist/StockSimulator-0.1-py2.7.egg \
    --driver-memory	1g\
    --executor-memory 1g\
    StockSimulator/RegressionMethod/distributed_neural_network.py