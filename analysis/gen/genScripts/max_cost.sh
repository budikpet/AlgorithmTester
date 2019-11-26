# -N	počet instancí
# -n	počet věcí
# -m	poměr kapacity batohu k sumární váze
# -W	max. hmotnost věci
# -w	převaha věcí lehkých/těžkých/balanc [bal|light|heavy]
# -C	max. cena věci
# -c	korelace s hmotností žádná/menší/silná [uni|corr|strong]
# -k	granularita (pouze pokud je -w light|heavy)

../kg2 -N 250 -n 10 -m 0.8 -W 100 -w bal -C 100 -c uni -k 1 \
>../../../data/MaxCost/MaxCost100_inst.dat

../kg2 -N 250 -n 10 -m 0.8 -W 100 -w bal -C 150 -c uni -k 1 \
>../../../data/MaxCost/MaxCost150_inst.dat

../kg2 -N 250 -n 10 -m 0.8 -W 100 -w bal -C 200 -c uni -k 1 \
>../../../data/MaxCost/MaxCost200_inst.dat

../kg2 -N 250 -n 10 -m 0.8 -W 100 -w bal -C 250 -c uni -k 1 \
>../../../data/MaxCost/MaxCost250_inst.dat

../kg2 -N 250 -n 10 -m 0.8 -W 100 -w bal -C 300 -c uni -k 1 \
>../../../data/MaxCost/MaxCost300_inst.dat