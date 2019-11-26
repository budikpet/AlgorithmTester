# -N	počet instancí
# -n	počet věcí
# -m	poměr kapacity batohu k sumární váze
# -W	max. hmotnost věci
# -w	převaha věcí lehkých/těžkých/balanc [bal|light|heavy]
# -C	max. cena věci
# -c	korelace s hmotností žádná/menší/silná [uni|corr|strong]
# -k	granularita (pouze pokud je -w light|heavy)

../kg2 -N 250 -n 20 -m 0.8 -W 50 -w bal -C 100 -c uni -k 1 \
>../../../data/MaxWeight/MaxWeight50_inst.dat

../kg2 -N 250 -n 20 -m 0.8 -W 100 -w bal -C 100 -c uni -k 1 \
>../../../data/MaxWeight/MaxWeight100_inst.dat

../kg2 -N 250 -n 20 -m 0.8 -W 150 -w bal -C 100 -c uni -k 1 \
>../../../data/MaxWeight/MaxWeight150_inst.dat

../kg2 -N 250 -n 20 -m 0.8 -W 200 -w bal -C 100 -c uni -k 1 \
>../../../data/MaxWeight/MaxWeight200_inst.dat

../kg2 -N 250 -n 20 -m 0.8 -W 250 -w bal -C 100 -c uni -k 1 \
>../../../data/MaxWeight/MaxWeight250_inst.dat
