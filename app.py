from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
import os
from symspellpy.symspellpy import SymSpell  # import the module
from symspellpy.symspellpy import SymSpell, Verbosity
import pandas
import pickle
from itertools import chain
from nltk.tokenize import TweetTokenizer
#import pandas
import re
from nltk.stem import WordNetLemmatizer
import nltk
app = Flask(__name__)
lemmatizer = WordNetLemmatizer()
tknzr = TweetTokenizer()
#nltk.download('stopwords')
from nltk.corpus import stopwords
PIK = "pickle.dat"
PIK_1 = "pickle_1.dat"
PIK_2 = "pickle_2.dat"
PIK_3 = "pickle_3.dat"


with open(PIK, "rb") as f:
    dict_1 = pickle.load(f)
# maximum edit distance per dictionary precalculation
max_edit_distance_dictionary = 3
prefix_length = 9
# create object
with open(PIK_2,"rb") as f:
    dict_2 = pickle.load(f)

with open(PIK_1, "rb") as f:
    sym_spell = pickle.load(f)
with open(PIK_3, "rb") as f:
    sym_spell_1 = pickle.load(f)

def main(string_t):
    #string_t = "i have seizures. I am ashthma attack. Yellow phlegm. "
    string_t_1 = string_t.split(".")
    for string_t in string_t_1:
        max_edit_distance_lookup = 3
        max_edit_distance_lookup_1 = 2
        tokenized_words = tknzr.tokenize(string_t.lower())
        stop_words = stopwords.words('english')
        lst = ["keep","make","feel","feels","i'hv","i've","fort","free","information","other","may","having","what","which","out","contact","business","pm","view","state","good","name","some","yours","really","especially"]
        for t in lst:
            stop_words.append(t)
        #print(stop_words)
        word_list = [word for word in tokenized_words if word not in stop_words]
        print(word_list)
        #print(word_list)
        i = 0
        word_list_1 = []
        for word in word_list:
            tog = 0
            #if(word == lemmatizer.lemmatize(word)):
                #word = lemmatizer.lemmatize(word,'v')
            #else:
                #word = lemmatizer.lemmatize(word)
            #if(word in dict_no_need):
                #if(dict_no_need[word] >= 1500):
                    #print("wword found", word)
                    #tog = 1
            if(tog == 0):
                word = word.replace("ing","")
                word_list_1.append(word)
                word_list[i] = word
                i+=1
        word_list = word_list_1
        #print(word_list)
        input_term  = " ".join(word_list)

        #input_term = = ("hearr pein")
        print(input_term)
        suggestions = sym_spell.lookup_compound(input_term,max_edit_distance_lookup)
        suggestions_1  = sym_spell_1.lookup_compound(input_term,max_edit_distance_lookup_1)
        #print(suggestions[0].term)
        #print("sSSSSSSSSS",suggestions[0])

        if(len(suggestions_1) > 0):
            temp_str_1 = suggestions_1[0].term
        #print( temp_str_1)
        temp_str_1 = temp_str_1.split(" ")
        #print(suggestions[0])
        if(len(suggestions)>0):
            temp_str = suggestions[0].term

        temp_str = temp_str.split(" ")
        i = 0
        result = []
        #print(temp_str)
        #print(dict_1["asthma_attack"])
        while(i< len(temp_str)-1):
            text = temp_str[i] + " "+ temp_str[i+1]
            if(text.lower() in dict_1):
                temp_str_1[i] = "X"
                try:
                    temp_str_1[i+1] = "X"
                except:
                    pass
                result.append([dict_1[text.lower()],text])
                #print(dict_1[text.lower()],"predicted from:", text)
            i+=1
        i = 0

        while(i< len(temp_str_1)):
            if(temp_str_1[i].lower() in dict_2):
                result.append([dict_2[temp_str_1[i].lower()],temp_str_1[i]])
                #print(dict_2[temp_str_1[i].lower()],"one word predicted from:",temp_str_1[i])
            i+=1
        return result
            #for suggestion in suggestions:
        #print(suggestion.term)

@app.route('/')
def index():
    return "OK"

@app.route('/get_data',methods = ['POST','GET'])
def get_data():
    if (request.method == 'POST'):
        '''
        result = request.form
        name = result["text"]
        print("got " ,name)
        name = name.replace("!",".")
        name = name.replace("?",".")
        name = name.replace(",", "")
        name = name.replace(";","")
        name = name.split(".")
        result1 = []
        print(name)
        for sentence in name:
            print("sending ", sentence)
            result = main(sentence)
            return result
            print("result is ", result)
            #print("Symptoms are: ")
            for t in result:
                result1.append(t)
        return result1[0]
        '''
        return "hello"
    else:
        return ("please post!")
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
