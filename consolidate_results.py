import glob
import json
import pandas as pd

def get_details_from_dir(dirname):

  _, label, _, sep, _, crf, _, epochs, _, max_sent = dirname.split('-')
  return {"label":label,"sep":sep, "crf":crf, "epochs":int(epochs),
  "max_sent":max_sent}

def main():

  dicts = []
  for dirname in glob.glob("final_final_outputs/*"):
    #final_outputs/run-rev_fine-sep-false-crf-false-epochs-2-max_sent-10
    print(dirname.split('-'))

    mydict = get_details_from_dir(dirname)
   
    try:
      with open(dirname + '/metrics.json', 'r') as f:
        j = json.load(f)
        mydict["val_avgf"] = j["best_validation_avgF"]
        mydict["test_avgf"] = j["test_avgF"]

      dicts.append(mydict)
    except FileNotFoundError:
      pass

  print(pd.DataFrame.from_dict(dicts).to_csv())


if __name__ == "__main__":
  main()

