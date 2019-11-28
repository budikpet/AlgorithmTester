# Pro každou instanci načtenou ze standardního vstupu vytvoří -N permutací.
# -d	id instance vždy inkrementováno o danou hodnotu
# -N	počet vygenerovaných instancí

SMALL="1 10 84 4 9 18 39 7 38 9 20 5 12 20 11 7 45 24 27 8 32 3 49"
LARGE="1 20 205 4 9 18 39 7 38 9 20 5 12 20 11 7 45 24 27 8 32 3 49 25 33 16 42 16 37 11 24 22 33 13 24 9 30 9 18 25 10 6 17"

path="../../../data"
name="Robust"

mkdir -p "$path"/"$name"

echo $SMALL | ../kg_perm -d 1 -N 1025 \
> $path/$name/"$name"_10_inst.dat

echo $LARGE | ../kg_perm -d 1 -N 32768 \
> $path/$name/"$name"_15_inst.dat