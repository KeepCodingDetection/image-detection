
from textblob import TextBlob
from googletrans import Translator
import pandas as pd
import re
import string
data = pd.read_excel('input-translation/supermarket_scrapping_30032022.xlsx')
translator = Translator()

# data['Traduccion'] = data['Categoria'].apply(lambda x: translator.translate(x, dest='en').text)
data['Category'] = data['Categoria'].map(lambda x: translator.translate(x, src="es", dest="en").text)

punc_lower = lambda x: re.sub('[%s]' % re.escape(string.punctuation), ' ', x.lower().strip())
data['Category'] = data.Category.map(punc_lower)

data.to_excel('output/supermarket_scrapping_en_30032022.xlsx', index=False)