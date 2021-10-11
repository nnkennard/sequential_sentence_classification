for label in rev_coarse rev_fine rev_asp rev_pol reb_coarse reb_fine
do
  for use_sep in true false
  do
    for with_crf in true false
    do
       if [ "$use_sep" == "true" -a "$with_crf" == "true" ]; then
         continue
       fi
       output_dir="outputs/run_"$label"_sep_"$use_sep"_crf_"$with_crf"/"
       echo $output_dir
       scripts/train.sh $output_dir $label $use_sep $with_crf
    done
  done
done
