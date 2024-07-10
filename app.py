# tested in transformers==4.18.0 
from transformers import BertTokenizer, BertForSequenceClassification, pipeline

inputText = """
Rhonda has been volunteering for several years for a variety of charitable community programs. 
"""

finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-esg',num_labels=4)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-esg')
nlp = pipeline("text-classification", model=finbert, tokenizer=tokenizer)
results = nlp(inputText)
print(results) # [{'label': 'Social', 'score': 0.9906041026115417}]
