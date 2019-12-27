# -N	počet instancí
# -n	počet věcí
# -m	poměr kapacity batohu k sumární váze
# -W	max. hmotnost věci
# -w	převaha věcí lehkých/těžkých/balanc [bal|light|heavy]
# -C	max. cena věci
# -c	korelace s hmotností žádná/menší/silná [uni|corr|strong]
# -k	granularita (pouze pokud je -w light|heavy)

path="../../data/DataAnalysis"
name="Things"

mkdir -p "$path"/"$name"

../gen/kg2 -N 100 -n 35 -m 0.8 -W 250 -w bal -C 250 -c uni -k 1.0 \
>$path/$name/"$name"_5_inst.dat

../gen/kg2 -N 100 -n 40 -m 0.8 -W 250 -w bal -C 250 -c uni -k 1.0 \
>$path/$name/"$name"_10_inst.dat

../gen/kg2 -N 100 -n 45 -m 0.8 -W 250 -w bal -C 250 -c uni -k 1.0 \
>$path/$name/"$name"_15_inst.dat

../gen/kg2 -N 100 -n 50 -m 0.8 -W 250 -w bal -C 250 -c uni -k 1.0 \
>$path/$name/"$name"_20_inst.dat

../gen/kg2 -N 100 -n 55 -m 0.8 -W 250 -w bal -C 250 -c uni -k 1.0 \
>$path/$name/"$name"_25_inst.dat

../gen/kg2 -N 100 -n 60 -m 0.8 -W 250 -w bal -C 250 -c uni -k 1.0 \
>$path/$name/"$name"_30_inst.dat
