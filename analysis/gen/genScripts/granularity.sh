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

../kg2 -N 100 -n 10 -m 0.8 -W 250 -w light -C 250 -c uni -k 0.5 \
>$path/$name/"$name"0,5_inst.dat

../kg2 -N 100 -n 10 -m 0.8 -W 250 -w light -C 250 -c uni -k 1.0 \
>$path/$name/"$name"1,0_inst.dat

../kg2 -N 100 -n 10 -m 0.8 -W 250 -w light -C 250 -c uni -k 1.5 \
>$path/$name/"$name"1,5_inst.dat

../kg2 -N 100 -n 10 -m 0.8 -W 250 -w light -C 250 -c uni -k 2.0 \
>$path/$name/"$name"2,0_inst.dat

../kg2 -N 100 -n 10 -m 0.8 -W 250 -w light -C 250 -c uni -k 2.5 \
>$path/$name/"$name"2,5_inst.dat

name="GranularityHeavy"

mkdir -p "$path"/"$name"

../kg2 -N 100 -n 10 -m 0.8 -W 250 -w light -C 250 -c uni -k 0.5 \
>$path/$name/"$name"0,5_inst.dat

../kg2 -N 100 -n 10 -m 0.8 -W 250 -w light -C 250 -c uni -k 1.0 \
>$path/$name/"$name"1,0_inst.dat

../kg2 -N 100 -n 10 -m 0.8 -W 250 -w light -C 250 -c uni -k 1.5 \
>$path/$name/"$name"1,5_inst.dat

../kg2 -N 100 -n 10 -m 0.8 -W 250 -w light -C 250 -c uni -k 2.0 \
>$path/$name/"$name"2,0_inst.dat

../kg2 -N 100 -n 10 -m 0.8 -W 250 -w light -C 250 -c uni -k 2.5 \
>$path/$name/"$name"2,5_inst.dat