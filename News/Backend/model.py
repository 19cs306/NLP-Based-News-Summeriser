import pandas as pd
import numpy as np
import re,os
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Input, LSTM, Dense, Bidirectional, Concatenate, Attention
from tensorflow.keras.models import Model
from keras.layers import Embedding
import matplotlib.pyplot as plt
import contractions
from keras import load_model
import time

start_time = time.time()

model = load_model("Backend/Static/model.h5")

max_text_len = 300
max_summary_len = 60

def text_preprocessing(file):
    text_tokenizer = Tokenizer()
    text_tokenizer.fit_on_texts(file)
    summary_tokenizer = Tokenizer()
    summary_tokenizer.fit_on_texts(file)
    return text_tokenizer , summary_tokenizer

def clean_text(text):
    text = text.lower()
    text = contractions.fix(text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text


def summrise(file):

    text_tokenizer,summary_tokenizer = text_preprocessing(file)

    def generate_summary(text):
        text = clean_text(text)
        x = text_tokenizer.texts_to_sequences([text])
        x = pad_sequences(x, maxlen=max_text_len, padding='post')
    
        summary_seq = np.zeros((1, max_text_len))
        summary_seq[0, 0] = summary_tokenizer.word_index['start']
    
        for i in range(1, max_summary_len):
            output_tokens = model.predict([x, summary_seq]).argmax(axis=2)
            summary_seq[0, i] = output_tokens[0, i-1]
            index_word = summary_tokenizer.index_word.get(summary_seq[0, i])
            if index_word and index_word == 'end':
                break
            
        summary = ' '.join([summary_tokenizer.index_word[w] for w in summary_seq[0] if w not in [0, summary_tokenizer.word_index['start'], summary_tokenizer.word_index['end']]])
        return summary



    df= pd.read_csv(file,encoding='utf-8')

    df['summary'] = df['ctext'].apply(generate_summary)
    
    base, ext = os.path.splitext(file)
    new_file = base+ "_fin" +ext 
    os.remove(file)
    df.to_csv(new_file, index=False)
