#!/bin/bash

# Simple script, just generates python
cd ui
files=(*)
cd ../

mkdir -p ui_py

for file in "${files[@]}"; do
	pyuic5 -x ui/$file -o ui_py/${file%.ui}.py
	echo "Generated ui_py/${file%.ui}.py"
done

