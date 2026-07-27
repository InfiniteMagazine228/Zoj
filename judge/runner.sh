#!/bin/bash

# $1: language (python/cpp)
# $2: input_file
# $3: timeout_seconds

LANG=$1
INPUT_FILE=$2
TIMEOUT=$3

if [ "$LANG" == "python" ]; then
    timeout $TIMEOUT python3 main.py < $INPUT_FILE
elif [ "$LANG" == "cpp" ]; then
    g++ -std=c++20 main.cpp -o main 2> compile_err.txt
    if [ $? -ne 0 ]; then
        echo "COMPILE_ERROR"
        cat compile_err.txt
        exit 1
    fi
    timeout $TIMEOUT ./main < $INPUT_FILE
else
    echo "UNSUPPORTED_LANGUAGE"
    exit 1
fi
