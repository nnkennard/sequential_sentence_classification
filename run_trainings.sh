for num_epochs in 2 10 20
do
  for num_sentences in 10 30
  do
	for label in rev_coarse rev_fine rev_asp rev_pol reb_coarse reb_fine
	do
	  for use_sep in true false
	  do
	    for with_crf in true false
	    do
	       if [ "$use_sep" == "true" -a "$with_crf" == "true" ]; then
		 continue
	       fi
	       output_dir="final_outputs/run-"$label"-sep-"$use_sep"-crf-"$with_crf"-epochs-"$num_epochs"-max_sent-"$num_sentences"/"
	       scripts/train.sh $output_dir $label $use_sep $with_crf $num_epochs $num_sentences
	    done
	  done
	done
  done
done
