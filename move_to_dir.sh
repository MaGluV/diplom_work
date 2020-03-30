#!/bin/bash

echo "Input Directory:" && read directory

mv *.evt ../$directory
mv *.pha ../$directory
mv *.lc ../$directory
mv *.arf ../$directory
mv *.rmf ../$directory
mv *.fits ../$directory
mv *.hk ../$directory
mv *.dat ../$directory
mv *.ps ../$directory

