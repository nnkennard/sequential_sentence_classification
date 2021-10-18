import argparse
import collections
import glob
import json
import os
import sys
import tqdm

parser = argparse.ArgumentParser(description='prepare CSVs for ws training')
parser.add_argument(
    '-i',
    '--input_dir',
    default="../peer-review-discourse-dataset/data_prep/final_dataset/",
    type=str,
    help='path to data file containing score jsons')

REVIEW_LABELS = "coarse fine asp pol".split()
REBUTTAL_LABELS = "coarse fine".split()


def build_examples(abstract_id, sentences, label_set):
  fake_confs = [1.0] * len(sentences)
  return {
      "abstract_id": abstract_id,
      "sentences": [sentence["text"] for sentence in sentences],
      "labels": [sentence[label_set] for sentence in sentences],
      "confs": fake_confs
  }

def get_label(alignment):
  align_type, indices = alignment
  if align_type == 'context_sentences':
    if len(indices) == 1:
      return "single_context"
    else:
      return "multiple_context"
  elif 'global' in align_type:
    return "global_context"
  else:
    return "other_context"

def main():

  args = parser.parse_args()

  data_maps = collections.defaultdict(lambda: collections.defaultdict(list))

  overall_counter = 0

  output_dir = "discourse_data/"
  os.makedirs(output_dir + "reb_align/")

  for subset in "train dev test".split():
    example_list = []
    for filename in tqdm.tqdm(glob.glob(args.input_dir + '/' + subset + "/*")):
      with open(filename, 'r') as f:
        file_obj = json.load(f)
        labels = [get_label(sent["alignment"]) for sent in file_obj["rebuttal_sentences"]]
        texts = [sent["text"] for sent in file_obj["rebuttal_sentences"]]
        fake_confs = [1.0] * len(labels)
        example_list.append({
          "abstract_id":overall_counter,
          "sentences": texts,
          "labels": labels,
          "confs":fake_confs
        })
      overall_counter += 1

    with open(output_dir + "reb_align/" + subset + ".jsonl", 'w') as f:
      f.write("\n".join(json.dumps(i) for i in example_list))


if __name__ == "__main__":
  main()
