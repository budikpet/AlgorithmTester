# -N	počet instancí
# -n	počet věcí
# -m	poměr kapacity batohu k sumární váze
# -W	max. hmotnost věci
# -w	převaha věcí lehkých/těžkých/balanc [bal|light|heavy]
# -C	max. cena věci
# -c	korelace s hmotností žádná/menší/silná [uni|corr|strong]
# -k	granularita (pouze pokud je -w light|heavy)

../kg2 -N 250 -n 5 -m 0.8 -W 100 -w bal -C 100 -c uni -k 1 \
>../../../data/Things/Thing5_inst.dat

../kg2 -N 250 -n 10 -m 0.8 -W 100 -w bal -C 100 -c uni -k 1 \
>../../../data/Things/Thing10_inst.dat

../kg2 -N 250 -n 15 -m 0.8 -W 100 -w bal -C 100 -c uni -k 1 \
>../../../data/Things/Thing15_inst.dat

../kg2 -N 250 -n 20 -m 0.8 -W 100 -w bal -C 100 -c uni -k 1 \
>../../../data/Things/Thing20_inst.dat

../kg2 -N 250 -n 25 -m 0.8 -W 100 -w bal -C 100 -c uni -k 1 \
>../../../data/Things/Thing25_inst.dat
