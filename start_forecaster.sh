#!/usr/bin/env bash

WORKER_NUM=2
PACKAGE_NAME=stockforecaster-0.1-py2.7.egg

#spark-submit \
#    --master local[${WORKER_NUM}] \
#    --py-files dist/${PACKAGE_NAME} \
#    --driver-memory	1g \
#    --executor-memory 1g \
#    --conf "spark.driver.extraJavaOptions=-Dlog4j.configuration=file:./logs/log4j.properties" \
#    src/test_forecaster/test_all_method.py
spark-submit --py-files dist/${PACKAGE_NAME} \
    --conf "spark.driver.extraJavaOptions=-Dlog4j.configuration=file:./logs/log4j.properties" \
    src/test_forecaster/test_different_period.py