#!/bin/bash

for p_table in ../force-matching/Pair*.table; do
    table_name=$(echo $p_table | cut -d "_" -f2 )
    table_name=$(echo $table_name | cut -d "." -f1)
    a1=$(echo $table_name | cut -d "-" -f1)
    a2=$(echo $table_name | cut -d "-" -f2)
    python pair_tables.py -t $p_table -o table_"$a1"_"$a2".xvg
done

mv table_C1_C1s.xvg table.xvg

echo "Bond table key:" > table_keys.txt
echo " " >> table_keys.txt

i=0
for b_table in ../force-matching/Bond*.table; do
    echo "$b_table --> table_b$i.xvg" >> table_keys.txt
    python bond_tables.py -t $b_table -o table_b$i.xvg
    i=$((i+1))
done

echo " " >> table_keys.txt
echo "Angle table key:" >> table_keys.txt
echo " " >> table_keys.txt

i=0
for a_table in ../force-matching/Angle*.table; do
    echo "$a_table --> table_a$i.xvg" >> table_keys.txt
    python bond_tables.py -t $a_table -o table_a$i.xvg
    i=$((i+1))
done

mkdir tables
mv table*.xvg tables