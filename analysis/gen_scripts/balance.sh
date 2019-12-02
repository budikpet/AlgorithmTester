# -N	počet instancí
# -n	počet věcí
# -m	poměr kapacity batohu k sumární váze
# -W	max. hmotnost věci
# -w	převaha věcí lehkých/těžkých/balanc [bal|light|heavy]
# -C	max. cena věci
# -c	korelace s hmotností žádná/menší/silná [uni|corr|strong]
# -k	granularita (pouze pokud je -w light|heavy)

path="../../data"
name="Balance"

mkdir -p "$path"/"$name"

../gen/kg2 -N 100 -n 15 -m 0.8 -W 250 -w bal -C 250 -c uni -k 1.0 \
>$path/$name/"$name"_Bal_inst.dat

../gen/kg2 -N 100 -n 15 -m 0.8 -W 250 -w light -C 250 -c uni -k 1.0 \
>$path/$name/"$name"_Light_inst.dat

../gen/kg2 -N 100 -n 15 -m 0.8 -W 250 -w heavy -C 250 -c uni -k 1.0 \
>$path/$name/"$name"_Heavy_inst.dat