import pandas as pd
import nltk
import nltk.data
import re
from nltk import word_tokenize
import enchant
import spacy
from sklearn import preprocessing

nltk.download('punkt')
nltk.download('stopwords')
nlp = spacy.load('en_core_web_sm')
en_detector = enchant.Dict("en")

#Tokenize sentences
def split_text_into_sentences(text):
  tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
  sentences = tokenizer.tokenize(text)

  return sentences

def clean_text(text, remove_stopwords=False):
    '''Remove unwanted characters, stopwords, and format the text to create fewer nulls word embeddings'''
    
    # Convert words to lower case
    text = text.lower()
    
    # Format words and remove unwanted characters
    text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\<a href', ' ', text)
    text = re.sub(r'&amp;', '', text) 
    text = re.sub(r'[_"\-;%()|+&=*%.,!?:#$@\[\]/]', ' ', text)
    text = re.sub(r'<br />', ' ', text)
    text = re.sub(r'\'', ' ', text)
    
    # Optionally, remove stop words
    if remove_stopwords:
        text = word_tokenize(text)
        stops = set(stopwords.words("english"))
        text = [w for w in text if not w in stops]
        text = " ".join(text)

    return text

def txt_analysis(text):
  total_words = len(word_tokenize(text))
  if total_words == 0:
    return 0, 0, 0

  #remove entity words (e.g name of person) -> Reason: Might get interpretated as Foreign Words
  sent = nlp(text)
  entity_words = sent.ents
  # entity_words = [token.text for token in sent if token.text not in sent.ents] 
  text_words = text.split()
  resultwords  = [word for word in text_words if word.lower() not in [w.text.lower() for w in entity_words]]
  text = ' '.join(resultwords)

  text = word_tokenize(text)
  
  #Foreign Words Count
  foreign_words_count = 0
  for word in text:
    if not en_detector.check(word):
      foreign_words_count += 1

  return total_words, foreign_words_count, foreign_words_count/total_words

def digit_count(df):
  result = []

  for index, row in df.iterrows():
    digits_count = 0
    text = row['cleaned_sentences']

    text = word_tokenize(text)

    for word in text:
      if word.isnumeric():
        digits_count += 1
    
    result.append(digits_count)

  return result

def common_word_check(df):
  ####[our, work] ???
  common_words = ["and", "or", "paper", "based", "data", "design", "model", "problem", "algorithm", "using", "approach", "used", "system", "we", "show", "proposed", "figure", "however", "following", "new", "method", "present", "study", "propose"] #common words found in abstracts
  discourse_markers = ["moreover", "furthermore", "in addition", "in conclusion", "in summary", "finally", "for example", "nevertheless"]

  common_words += discourse_markers

  for word in common_words:
    key = word + "_present"
    df[key] = 0

  for index, row in df.iterrows():
    sentence = row['sentence']

    for word in common_words:
      if word in sentence.lower():
        key = word + "_present"
        df.loc[index, key] = 1

def summariser(source_text, models, n_sents=10):
    #Split text into sentences
    sentences = split_text_into_sentences(source_text)
    print('Sentence Dataframe Completed!')

    df = pd.DataFrame(sentences, columns=['sentence'])

    print('Cleaning Text...')
    df['cleaned_sentences'] = df['sentence'].apply(clean_text)
    print('Text Cleaning successful...')

    summaries = []
    no_sentences = n_sents

    count_features = ['total_words', 'foreign_words', 'digits_count', 'symbols_count']

    for cf in count_features:
        df[cf] = 0

    nan_value = float("NaN")
    df.replace("", nan_value, inplace=True)
    df.dropna(subset = ["cleaned_sentences"], inplace=True)

    sentences = df['sentence'].to_numpy().tolist()

    print('Performing Text Analysis...')
    txt_results = df['cleaned_sentences'].apply(txt_analysis)
    print('Text Analysis successful...')

    df['total_words'] = [row[0] for row in txt_results]
    df['foreign_words'] = [row[1] for row in txt_results]
    df['digits_count'] = digit_count(df)
    df['symbols_count'] = df['sentence'].str.findall(r'[^a-zA-Z0-9 _"\-;()&.,!?\[\]\n]').str.len()
    
    print('Looking for Common Word Check...')
    common_word_check(df)
    print('Common Word Check Complete!')
    
    df.drop('sentence', axis=1, inplace=True)
    df.drop('cleaned_sentences', axis=1, inplace=True)

    val_X = df

    sc = preprocessing.StandardScaler()
    val_X = sc.fit_transform(val_X)

    current_summaries = []
    
    for model in models:
        print('Performing Prediction...')
        prediction = model.predict(val_X)

        if type(model).__name__ in ['KNeighborsClassifier', 'DecisionTreeClassifier', 'RandomForestClassifier']:
            probabilities = model.predict_proba(val_X)
        else:
            probabilities = model.predict_log_proba(val_X)

    summary_sentences = []
    
    print('Generating Summary...')
    for i, sentence in enumerate(sentences):
        if prediction[i] == 1:
            summary_sentences.append({
                'index': i,
                'summary_probability': probabilities[i][1] 
            })
    
        final_summary = sorted(summary_sentences, key=lambda d: d['summary_probability'], reverse=True)[:no_sentences]

        if (len(final_summary) == 0):
            current_summaries.append('')
            continue

        chosen_sentences = [x for idx, x in enumerate(sentences) if idx in [fs['index'] for fs in final_summary]] #sorted sentences as in source_text

    current_summaries.append(' '.join(chosen_sentences))

    summaries.append(current_summaries)
    print('Summary Generated!')

    return summaries