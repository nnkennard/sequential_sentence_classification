num_epochs=10
num_sentences=10

mkdir analysis_outputs

for label in CSAbstruct rev_coarse rev_fine #rev_asp rev_pol reb_coarse reb_fine #reb_align
#for label in reb_coarse reb_fine reb_align

do
  for use_sep in true false
  do
    for with_crf in true #false
    do
      if [ "$use_sep" == "true" -a "$with_crf" == "true" ]; then
        continue
      fi

      output_dir="analysis_outputs/run-"$label"-sep-"$use_sep"-crf-"$with_crf"/"
      #scripts/train.sh $output_dir $label $use_sep $with_crf $num_epochs $num_sentences

      model_path=$output_dir"/model.tar.gz"
      input_file=discourse_data/$label/all.jsonl
      output_file=$output_dir"/predictions.json"
      python -m allennlp.run predict $model_path $input_file  --include-package sequential_sentence_classification --predictor SeqClassificationPredictor --output-file $output_file
      git add $output_file

    done
  done
done
