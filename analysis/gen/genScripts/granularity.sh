# -N	počet instancí
# -n	počet věcí
# -m	poměr kapacity batohu k sumární váze
# -W	max. hmotnost věci
# -w	převaha věcí lehkých/těžkých/balanc [bal|light|heavy]
# -C	max. cena věci
# -c	korelace s hmotností žádná/menší/silná [uni|corr|strong]
# -k	granularita (pouze pokud je -w light|heavy)

path="../../../data"
name="GranularityLight"

mkdir -p "$path"/"$name"

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w light -C 250 -c uni -k 0.25 \
>$path/$name/"$name"_0,25_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w light -C 250 -c uni -k 0.5 \
>$path/$name/"$name"_0,5_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w light -C 250 -c uni -k 0.75 \
>$path/$name/"$name"_0,75_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w light -C 250 -c uni -k 1.0 \
>$path/$name/"$name"_1,0_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w light -C 250 -c uni -k 1.25 \
>$path/$name/"$name"_1,25_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w light -C 250 -c uni -k 1.5 \
>$path/$name/"$name"_1,5_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w light -C 250 -c uni -k 1.75 \
>$path/$name/"$name"_1,75_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w light -C 250 -c uni -k 2.0 \
>$path/$name/"$name"_2,0_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w light -C 250 -c uni -k 2.25 \
>$path/$name/"$name"_2,25_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w light -C 250 -c uni -k 2.5 \
>$path/$name/"$name"_2,5_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w light -C 250 -c uni -k 2.75 \
>$path/$name/"$name"_2,75_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w light -C 250 -c uni -k 3.0 \
>$path/$name/"$name"_3,0_inst.dat

name="GranularityHeavy"

mkdir -p "$path"/"$name"

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w heavy -C 250 -c uni -k 0.25 \
>$path/$name/"$name"_0,25_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w heavy -C 250 -c uni -k 0.5 \
>$path/$name/"$name"_0,5_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w heavy -C 250 -c uni -k 0.75 \
>$path/$name/"$name"_0,75_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w heavy -C 250 -c uni -k 1.0 \
>$path/$name/"$name"_1,0_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w heavy -C 250 -c uni -k 1.25 \
>$path/$name/"$name"_1,25_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w heavy -C 250 -c uni -k 1.5 \
>$path/$name/"$name"_1,5_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w heavy -C 250 -c uni -k 1.75 \
>$path/$name/"$name"_1,75_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w heavy -C 250 -c uni -k 2.0 \
>$path/$name/"$name"_2,0_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w heavy -C 250 -c uni -k 2.25 \
>$path/$name/"$name"_2,25_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w heavy -C 250 -c uni -k 2.5 \
>$path/$name/"$name"_2,5_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w heavy -C 250 -c uni -k 2.75 \
>$path/$name/"$name"_2,75_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 250 -w heavy -C 250 -c uni -k 3.0 \
>$path/$name/"$name"_3,0_inst.dat