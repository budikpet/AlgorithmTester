# -N	počet instancí
# -n	počet věcí
# -m	poměr kapacity batohu k sumární váze
# -W	max. hmotnost věci
# -w	převaha věcí lehkých/těžkých/balanc [bal|light|heavy]
# -C	max. cena věci
# -c	korelace s hmotností žádná/menší/silná [uni|corr|strong]
# -k	granularita (pouze pokud je -w light|heavy)

path="../../data/DataAnalysis"
name="MaxWeight"

mkdir -p "$path"/"$name"

../gen/kg2 -N 250 -n 15 -m 0.8 -W 100 -w bal -C 250 -c uni -k 1.0 \
>$path/$name/"$name"_100_inst.dat

../gen/kg2 -N 250 -n 15 -m 0.8 -W 200 -w bal -C 250 -c uni -k 1.0 \
>$path/$name/"$name"_200_inst.dat

../gen/kg2 -N 250 -n 15 -m 0.8 -W 300 -w bal -C 250 -c uni -k 1.0 \
>$path/$name/"$name"_300_inst.dat

../gen/kg2 -N 250 -n 15 -m 0.8 -W 400 -w bal -C 250 -c uni -k 1.0 \
>$path/$name/"$name"_400_inst.dat

../gen/kg2 -N 250 -n 15 -m 0.8 -W 500 -w bal -C 250 -c uni -k 1.0 \
>$path/$name/"$name"_500_inst.dat