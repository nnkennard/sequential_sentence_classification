from typing import List
from overrides import overrides

from allennlp.common.util import JsonDict, sanitize
from allennlp.data import Instance
from allennlp.predictors.predictor import Predictor


@Predictor.register('SeqClassificationPredictor')
class SeqClassificationPredictor(Predictor):
    """
    Predictor for the abstruct model
    """
    def predict_json(self, json_dict: JsonDict) -> JsonDict:
        self._dataset_reader.predict = True
        pred_labels = []
        sentences = json_dict['sentences']
        for sentences_loop, _, _, _ in self._dataset_reader.enforce_max_sent_per_example(sentences):
            instance = self._dataset_reader.text_to_instance(sentences=sentences_loop)
            output = self._model.forward_on_instance(instance)
            idx = output['action_probs'].argmax(axis=1).tolist()
            labels = [self._model.vocab.get_token_from_index(i, namespace='labels') for i in idx]
            pred_labels.extend(labels)
        try:
            assert len(pred_labels) == len(sentences)
            json_dict['pred_labels_truncated'] = False
        # If a sequence is too long and gets truncated then some of sentences dont
        # get labels which is super weird I couldn't find where this happened.
        # Seemed to be a small number of cases.
        except AssertionError:
            #print('Added other because of truncation: {:}'.format(json_dict['paper_id']))
            assert len(pred_labels) < len(sentences)
            dif_len = len(sentences)-len(pred_labels)
            pred_labels.extend(['other_label']*dif_len)
            json_dict['pred_labels_truncated'] = True
        json_dict['pred_labels'] = pred_labels
        return json_dict
    
