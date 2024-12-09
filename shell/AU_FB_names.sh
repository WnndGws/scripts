#! /usr/bin/env sh
##

# Change League names
#
sed -i "s/England and Wales Cricket Board/ECB/g" UK_data.csv
sed -i 's/2022 - //g' UK_data.csv
sed -i 's/2023 - //g' UK_data.csv
sed -i 's/Koninklijke Nederlandse Cricket Bond/KNCB/g' UK_data.csv
sed -i 's/Cricket League/CL/g' UK_data.csv
sed -i 's/Berkshire, Chilterns/Berks&Chilterns/g' UK_data.csv
sed -i 's/Saturday XI/XI/g' UK_data.csv
sed -i 's/Sunday XI/XI/g' UK_data.csv
sed -i 's/Under /U/g' UK_data.csv
sed -i 's/Cricket Association/CA/g' UK_data.csv
sed -i 's/Cricket Union/CU/g' UK_data.csv
sed -i 's/Friendly XI//g' UK_data.csv
sed -i 's/ECB - Friendly/ECB Friendly/g' UK_data.csv
sed -i --regexp-extended 's/ \([0-9]+\)//g' UK_data.csv
sed -i 's/Twenty20/T20/g' UK_data.csv
sed -i 's/Sweet Streams SA - 2022\//Sweet Streams SA - /g' UK_data.csv
sed -i 's/Oxford UCCE Oxford UCCE/Oxford UCCE/g' UK_data.csv
sed -i 's/, Berks//g' UK_data.csv
sed -i 's/, Brighton//g' UK_data.csv
sed -i 's/, Bristol//g' UK_data.csv
sed -i 's/, Cheshire//g' UK_data.csv
sed -i 's/, Cornwall//g' UK_data.csv
sed -i 's/, Derbyshire//g' UK_data.csv
sed -i 's/, Durham//g' UK_data.csv
sed -i 's/, Essex//g' UK_data.csv
sed -i 's/, Glos"//g' UK_data.csv
sed -i 's/, Herts//g' UK_data.csv
sed -i 's/, Isle of Man//g' UK_data.csv
sed -i 's/, Kent//g' UK_data.csv
sed -i 's/, Lancashire//g' UK_data.csv
sed -i 's/, Lincs//g' UK_data.csv
sed -i 's/, Middlesex//g' UK_data.csv
sed -i 's/, Middx//g' UK_data.csv
sed -i 's/, North Yorkshire//g' UK_data.csv
sed -i 's/, Sheffield//g' UK_data.csv
sed -i 's/, Somerset//g' UK_data.csv
sed -i 's/, Staffordshire//g' UK_data.csv
sed -i 's/, Suffolk//g' UK_data.csv
sed -i 's/, Surrey//g' UK_data.csv
sed -i 's/, Sussex//g' UK_data.csv
sed -i 's/, Warks//g' UK_data.csv
sed -i 's/, Wilts//g' UK_data.csv
sed -i 's/, Worcester//g' UK_data.csv
sed -i 's/, Worcs//g' UK_data.csv
sed -i 's/, Yorks//g' UK_data.csv
sed -i 's/, QEA//g' UK_data.csv
