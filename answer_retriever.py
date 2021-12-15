import torch
from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering


class AnswerRetriever:

    def getAnswer(self, question, questionContext):
        distilBertTokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased', return_token_type_ids=True, return_dict=False)
        distilBertForQuestionAnswering = DistilBertForQuestionAnswering.from_pretrained(
            'distilbert-base-uncased-distilled-squad', return_dict=False)

        encodings = distilBertTokenizer.encode_plus(question, questionContext)

        inputIds, attentionMask = encodings["input_ids"], encodings["attention_mask"]

        scoresStart, scoresEnd = distilBertForQuestionAnswering(torch.tensor([inputIds]),
                                                                attention_mask=torch.tensor([attentionMask]))

        tokens = inputIds[torch.argmax(scoresStart): torch.argmax(scoresEnd) + 1]
        answerTokens = distilBertTokenizer.convert_ids_to_tokens(tokens, skip_special_tokens=True)
        return distilBertTokenizer.convert_tokens_to_string(answerTokens)

#import torch
# from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
#
#
# class AnswerRetriever:
#
#     def getAnswer(self, question, questionContext):
#         distilBertTokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased', return_token_type_ids=True)
#         distilBertForQuestionAnswering = DistilBertForQuestionAnswering.from_pretrained(
#             'distilbert-base-uncased-distilled-squad')
#
#         encodings = distilBertTokenizer.encode_plus(question, questionContext)
#
#         inputIds, attentionMask = encodings["input_ids"], encodings["attention_mask"]
#
#         scoresStart, scoresEnd = distilBertForQuestionAnswering(torch.tensor([inputIds]),
#                                                                 attention_mask=torch.tensor([attentionMask]))
#
#         tokens = inputIds[torch.argmax(scoresStart): torch.argmax(scoresEnd) + 1]
#         answerTokens = distilBertTokenizer.convert_ids_to_tokens(tokens, skip_special_tokens=True)
#         return distilBertTokenizer.convert_tokens_to_string(answerTokens)