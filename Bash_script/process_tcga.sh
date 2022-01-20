#!/bin/bash
(($# == 3)) || { echo -e "\nUsage: $0 <Directory to download>\n\n"; exit; }

d="$1"
link="$2"
output="$3"
# Check conditions and downloads
[ -d "${d}" ] &&  echo "Directory $d found." || { echo -e "Not exist $d, automatically create";mkdir -p $d;}
wget $link
for i in  `find *tar.gz*`;do echo k=`basename $i .tar.gz`;tar -xvzf $i ;done
mv */*data* $d/$output
rm -rf gdac* 
# Split by chromosome
cat $d/$output| sed "1,2d" |awk -v d=$d 'OFS="\t" {print $0 > d"/chr"$4".tsv"}'
head -2 $d/$output > $d/header.txt
for k in `find $d/chr*.tsv`;do echo $k;cat $d/header.txt > mediator.tsv; cat $k >> mediator.tsv; mv mediator.tsv $k; done
# Process to spling smaller files
python3 process.py $d
head -1 $d/chr1.tsv > $d/$output
rm $d/header.txt
for i in `find *$d/chr*`
do
echo $i
cat $i >>$d/$output
rm $i
done

bash split_columns_keep1.sh $d/$output 50
rm $d/$output
