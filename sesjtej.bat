#!/bin/bash

sestevek=0

for file in ./csv/*.csv; do
    echo $file
    wc -l $file
    echo $dolzina
    sestevek=$sestevek+$dolzina
done

echo $sestevek
exit 42