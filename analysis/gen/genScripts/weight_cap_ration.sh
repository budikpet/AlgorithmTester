# -N	počet instancí
# -n	počet věcí
# -m	poměr kapacity batohu k sumární váze
# -W	max. hmotnost věci
# -w	převaha věcí lehkých/těžkých/balanc [bal|light|heavy]
# -C	max. cena věci
# -c	korelace s hmotností žádná/menší/silná [uni|corr|strong]
# -k	granularita (pouze pokud je -w light|heavy)

../kg2 -N 100 -n 10 -m 0.2 -W 100 -w bal -C 100 -c uni -k 1 \
>../../../data/Weight_Cap_Ration/Weight_Cap_Ration0,2_inst.dat

../kg2 -N 100 -n 10 -m 0.4 -W 100 -w bal -C 100 -c uni -k 1 \
>../../../data/Weight_Cap_Ration/Weight_Cap_Ration0,4_inst.dat

../kg2 -N 100 -n 10 -m 0.6 -W 100 -w bal -C 100 -c uni -k 1 \
>../../../data/Weight_Cap_Ration/Weight_Cap_Ration0,6_inst.dat

../kg2 -N 100 -n 10 -m 0.8 -W 100 -w bal -C 100 -c uni -k 1 \
>../../../data/Weight_Cap_Ration/Weight_Cap_Ration0,8_inst.dat

../kg2 -N 100 -n 10 -m 1.0 -W 100 -w bal -C 100 -c uni -k 1 \
>../../../data/Weight_Cap_Ration/Weight_Cap_Ration1,0_inst.dat