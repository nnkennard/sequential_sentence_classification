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


def main():

  args = parser.parse_args()

  data_maps = collections.defaultdict(lambda: collections.defaultdict(list))

  overall_counter = 0

  for subset in "train dev test".split():
    for filename in tqdm.tqdm(glob.glob(args.input_dir + '/' + subset + "/*")):
      with open(filename, 'r') as f:
        file_obj = json.load(f)

        for label in REVIEW_LABELS:
          data_maps["rev_" + label][subset].append(
              build_examples(overall_counter, file_obj["review_sentences"],
                             label))
        for label in REBUTTAL_LABELS:
          data_maps["reb_" + label][subset].append(
              build_examples(overall_counter, file_obj["rebuttal_sentences"],
                             label))

      overall_counter += 1

  output_dir = "discourse_data/"
  for label, examples_by_label in data_maps.items():
    os.makedirs(output_dir + label +"/")
    for subset, examples in examples_by_label.items():
      with open(output_dir + label + '/' + subset + ".jsonl", 'w') as f:
        f.write("\n".join(json.dumps(i) for i in examples))


if __name__ == "__main__":
  main()
