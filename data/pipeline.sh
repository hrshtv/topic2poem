#!/bin/bash

python3 clean_data.py -i kaggle_poem_dataset.csv -o dataset.csv
echo "Dataset cleaned"
echo ""

if [ $? -ne 0 ]; then
    echo "Error"
    exit $?
fi

python3 filter_length.py -i dataset.csv -o dataset_250.csv -m 50 -M 250
echo "Filtered by length"
echo ""

if [ $? -ne 0 ]; then
    echo "Error"
    exit $?
fi

python3 filter_authors.py -i dataset_250.csv -o dataset_250_top_authors.csv
echo "Filtered by authors"
echo ""

if [ $? -ne 0 ]; then
    echo "Error"
    exit $?
fi

python3 add_topics.py -i dataset_250_top_authors.csv -o topics_250_top_authors.csv -s stopwords/stopwords.txt
echo "Added topics column"
echo ""

if [ $? -ne 0 ]; then
    echo "Error"
    exit $?
fi