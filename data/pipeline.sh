#!/bin/bash

# Description: Creates the dataset used for finetuning
# Author: Harshit Varma


# Constants: Modify them according to your own needs

# All poems with length in [MIN_LENGTH, MAX_LENGTH] will be kept, rest will be discarded
MIN_LENGTH=50
MAX_LENGTH=250

STOPWORDS_PATH="stopwords/stopwords.txt"

ORIG_DATA="kaggle_poem_dataset.csv"
CLEANED_DATA="cleaned_dataset.csv"
LENGTH_FILTERED_DATA="filtered_length_${MIN_LENGTH}_${MAX_LENGTH}.csv"
AUTHOR_FILTERED_DATA="filtered_authors.csv"
FINAL_DATA="final_dataset.csv" # Path where the final dataset will be saved

KEEP_INTERMEDIATE=0 # Set to 1 if intermediate CSV files are needed


# Step 1:
python3 clean_data.py -i $ORIG_DATA -o $CLEANED_DATA

if [ $? -ne 0 ]
then
    echo "Error while cleaning the dataset"
    exit $?
else
    echo "Dataset cleaned"
    echo ""
fi


# Step 2:
python3 filter_length.py -i $CLEANED_DATA -o $LENGTH_FILTERED_DATA -m $MIN_LENGTH -M $MAX_LENGTH

if [ $? -ne 0 ]
then
    echo "Error while filtering by length"
    exit $?
else
    echo "Filtered by length"
    echo ""
fi


# Step 3:
python3 filter_authors.py -i $LENGTH_FILTERED_DATA -o $AUTHOR_FILTERED_DATA

if [ $? -ne 0 ]
then
    echo "Error while filtering by authors"
    exit $?
else
    echo "Filtered by authors"
    echo ""
fi


# Step 4:
python3 add_topics.py -i $AUTHOR_FILTERED_DATA -o $FINAL_DATA -s $STOPWORDS_PATH

if [ $? -ne 0 ]
then
    echo "Error while adding the topics column"
    exit $?
else
    echo "Added topics column"
    echo ""
fi


# Clean up
if [ $KEEP_INTERMEDIATE -ne 1 ]
then
    rm $CLEANED_DATA
    rm $LENGTH_FILTERED_DATA
    rm $AUTHOR_FILTERED_DATA
fi