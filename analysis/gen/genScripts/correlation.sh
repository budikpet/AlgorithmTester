# -N	počet instancí
# -n	počet věcí
# -m	poměr kapacity batohu k sumární váze
# -W	max. hmotnost věci
# -w	převaha věcí lehkých/těžkých/balanc [bal|light|heavy] (Weight distribution)
# -C	max. cena věci
# -c	korelace s hmotností žádná/menší/silná [uni|corr|strong] (Cost distribution)
# -k	granularita (pouze pokud je -w light|heavy)

path="../../../data"
name="Correlation"

mkdir -p "$path"/"$name"

../kg2 -N 100 -n 10 -m 0.8 -W 250 -w bal -C 250 -c uni -k 1.0 \
>$path/$name/"$name"_Uni_inst.dat

../kg2 -N 100 -n 10 -m 0.8 -W 250 -w bal -C 250 -c corr -k 1.0 \
>$path/$name/"$name"_Corr_inst.dat

../kg2 -N 100 -n 10 -m 0.8 -W 250 -w bal -C 250 -c strong -k 1.0 \
>$path/$name/"$name"_Strong_inst.dat