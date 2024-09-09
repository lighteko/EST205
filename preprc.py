import re
import pandas as pd
import gspread as gs
import progressbar
import string
import nltk
nltk.download()
from collections import Counter
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
from emos import Emos
from spellchecker import SpellChecker

class PreProcessor:
    def __init__(self, mode: int):
        print("Step 1: Initializing Preprocessor ...")
        self.serv_acc = gs.service_account(filename='./credentials.json')
        self.sheet = self.serv_acc.open("EST 205 Data Sheet")
        self.file_name = input("Enter the worksheet name: ")
        self.worksheet = self.sheet.worksheet(self.file_name)
        self.model: pd.DataFrame = pd.DataFrame(self.worksheet.get_all_records())
        self.STOPWORDS = stopwords.words('english')
        self.PUNCTUATIONS = string.punctuation
        counter = Counter()
        bar = progressbar.ProgressBar(maxval=len(self.model)).start()
        for (_, row) in self.model.iterrows():
            bar.update(_)
            for word in row['content'].split():
                counter[word] += 1
        self.FREQWORDS = set([w for (w, _) in counter.most_common(10)])
        bar.finish()
        self.RAREWORDS = set([w for (w, _) in counter.most_common()[:-10-1:-1]])
        self.STEMMER = PorterStemmer().stem
        self.LEMMATIZER = WordNetLemmatizer().lemmatize
        self.WORDNET_MAP = {"N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV, "J": wordnet.ADJ}
        self.EMOTICONS = Emos.EMOTICONS
        self.UNICODE_EMO = Emos.UNICODE_EMO
        self.SPELL = SpellChecker().correction
    
    def run(self):
        print("Step 2: Preprocessing Data ...")
        self.lowering()
        self.remove_punctuation()
        self.remove_stop_words()
        self.remove_frequent_words()
        self.remove_rare_words()
        self.stemming()
        self.lemmatizing()
        self.convert_emojis()
        self.convert_emoticons()
        self.remove_urls()
        self.remove_html_tags()
        self.correct_spellings()
        self.save()

    def lowering(self):
        print(">>> Lowering all characters ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            b.update(_)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": row['content'].lower(),
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
            self.model.update
        b.finish()
        self.model = pd.DataFrame(temp_model)
        print(self.model[:2])

    def remove_punctuation(self):
        print(">>> Removing punctuations ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            b.update(_)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": row['content'].translate(str.maketrans('', '', self.PUNCTUATIONS)),
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        self.model = pd.DataFrame(temp_model)
        b.finish()

    def remove_stop_words(self):
        print(">>> Removing stop words ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            b.update(_)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": ' '.join([word for word in row['content'].split() if word not in self.STOPWORDS]),
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        b.finish()

    def remove_frequent_words(self):
        print(">>> Removing frequent words ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            b.update(_)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": ' '.join([word for word in row['content'].split() if word not in self.FREQWORDS]),
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        b.finish()
    
    def remove_rare_words(self):
        print(">>> Removing rare words ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            b.update(_)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": ' '.join([word for word in row['content'].split() if word not in self.RAREWORDS]),
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        b.finish()

    def stemming(self):
        print(">>> Stemming words ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            b.update(_)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": ' '.join([self.STEMMER(word) for word in row['content'].split()]),
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        b.finish()
        self.model = pd.DataFrame(temp_model)

    def lemmatizing(self):
        print(">>> Lemmatizing words ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            b.update(_)
            pos_tagged = nltk.pos_tag(row['content'].split())
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": ' '.join([self.LEMMATIZER(word, self.WORDNET_MAP.get(pos[0], wordnet.NOUN)) for word, pos in pos_tagged]),
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        b.finish()
        self.model = pd.DataFrame(temp_model)

    def convert_emojis(self):
            
        print(">>> Converting emojis ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            content = row['content']
            for emo in self.UNICODE_EMO:
                content = re.sub(r'('+emo+')', "_".join(self.UNICODE_EMO[emo].replace(",","").replace(":","").split()), content)
            b.update(_)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": content,
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        b.finish()
        self.model = pd.DataFrame(temp_model)

    def convert_emoticons(self):
        print(">>> Converting emoticons ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            content = row['content']
            for emot in self.EMOTICONS:
                content = re.sub(u'(' + emot + ')', "_".join(self.EMOTICONS[emot].replace(",","").split()), content)
            b.update(_)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": content,
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        b.finish()
        self.model = pd.DataFrame(temp_model)

    def remove_urls(self):
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        print(">>> Removing URLs ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            b.update(_)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": url_pattern.sub(r'', row['content']),
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        b.finish()
        self.model = pd.DataFrame(temp_model)

    def remove_html_tags(self):
        html_pattern = re.compile('<.*?>')
        print(">>> Removing HTML tags ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            b.update(_)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": html_pattern.sub(r'', row['content']),
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        b.finish()
        self.model = pd.DataFrame(temp_model)

    def correct_spellings(self):
        print(">>> Correcting spellings ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        
        for (_, row) in self.model.iterrows():
            b.update(_)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": ' '.join([self.SPELL(word) for word in row['content'].split()]),
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        b.finish()
        self.model = pd.DataFrame(temp_model)

    def save(self):
        print("Step 3: Saving Preprocessed Data ...")
        self.sheet.add_worksheet(title=f"Preprocessed_{self.file_name}")
        worksheet = self.sheet.worksheet(f"Preprocessed_{self.file_name}")
        worksheet.update([self.model.columns.values.tolist()] + self.model.values.tolist())
        print(">>> Data saved successfully.")
        print(">>> Exiting Preprocessor ...")
        print(">>> Done.")