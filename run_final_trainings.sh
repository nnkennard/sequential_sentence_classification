num_epochs=10
num_sentences=19
use_sep=true
with_crf=false

mkdir final_final_outputs

for label in rev_coarse rev_fine rev_asp rev_pol reb_coarse reb_fine reb_align
do
	output_dir="final_final_outputs/run-"$label"-sep-"$use_sep"-crf-"$with_crf"-epochs-"$num_epochs"-max_sent-"$num_sentences"/"
	scripts/train.sh $output_dir $label $use_sep $with_crf $num_epochs $num_sentences
done
