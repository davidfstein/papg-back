#!/bin/sh
VCF=$1
SNPS=$2
UUID=$3
echo "starting"
zgrep -wE 'rs4341|rs12594956|rs2306604|rs324420|rs4950|rs2576037|rs5993883|rs362584|rs5759037|rs2164273|rs1426371|rs7498702|rs6481128|rs6981523|rs9611519|rs3814424|rs150812083|rs139315125|rs4680|rs10952668|rs1402494|rs802047|rs802028|rs802030|rs802026|rs802036|rs802025|rs802024|rs802032|rs802049|rs802051|rs12936442|rs894664|rs6502671|rs7216028|rs7510759|rs7510924|rs7290560|rs8136107|rs3783337|rs7158754|rs3783332|rs2181102|rs7159195|rs11160570|rs941898' $VCF > "${UUID}project.out"
cut -f3,4,5,10 "${UUID}project.out" | sed 's/[:].*//' > "${UUID}projectGenotype.out"
cut -f3 "${UUID}project.out" > "${UUID}myProjectSNPs.out"
awk 'NR==FNR{a[$0];next}!($0 in a)' "${UUID}myProjectSNPs.out" $SNPS > "${UUID}onlyRefProjectSNPs.txt"
cat "${UUID}onlyRefProjectSNPs.txt" | grep rs | awk '{print $0, "\t", "0/0"}'> "${UUID}refProjectGenotype.out"
cat "${UUID}projectGenotype.out" "${UUID}refProjectGenotype.out" | sed 's/[|]/\//g' > "${UUID}results.txt"
echo "done"



