from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline

finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')

nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)

sentences = """
Samsung Electronics recorded an operating profit of KRW 10 trillion in the second quarter of this year, far exceeding market expectations. It achieved a significant improvement in its performance as demand for memory semiconductors increased and prices rose due to the expansion of the artificial intelligence (AI) market.

Samsung Electronics made a public announcement on Tuesday that its sales and operating profit for the second quarter of this year were provisionally estimated at 74 trillion won and 10.4 trillion won. The figures were up 23.3 percent and 1453.2 percent, respectively, from a year earlier. The operating profit was an earnings surprise, which exceeded the market forecast of more than 2 trillion won (approximately 8.31 trillion won). The operating profit exceeded the 10 trillion won mark for the first time in seven quarters since the third quarter of 2022.

"Demand for memory semiconductors will exceed supply in the second half of the year due to strong growth in the AI industry," said Lee Soo-rim, a researcher at DS Investment & Securities. "If we succeed in delivering HBM (High Bandwidth Memory) to major customers such as Nvidia, the trend of profit growth will become more pronounced."

Samsung Electronics shares closed at 87,100 won (81.31 U.S. dollars), up 2.96 percent from the previous day due to improved earnings. It is the highest price in three years and five months since its 52-week high and January 25, 2021 (89,400 won or 89.23 dollars). The KOSPI also rose 37.29 points (1.32 percent) from the previous day to 2,862.23, setting a new yearly high for two consecutive days.
"""
results = nlp(sentences)
print(results)  #LABEL_0: neutral; LABEL_1: positive; LABEL_2: negative
