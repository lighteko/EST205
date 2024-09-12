from spellchecker import SpellChecker
from emos import Emos
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import re
import pandas as pd
import gspread as gs
import progressbar
import nltk
# nltk.download()


class PreProcessor:
    def __init__(self, mode: int):
        print("Step 0: Checking Credentials ...")
        self.serv_acc = gs.service_account(filename='./credentials.json')
        self.sheet = self.serv_acc.open("EST 205 Data Sheet")
        self.file_name = input(">>> Enter the worksheet name: ")
        print(">>> Initializing Preprocessor ...")
        self.worksheet = self.sheet.worksheet(self.file_name)
        self.model: pd.DataFrame = pd.DataFrame(
            self.worksheet.get_all_records())
        self.STOPWORDS = stopwords.words('english')
        self.PUNCTUATIONS = "'`~!@#$%^&*()_-+={[]}\\|;:\",.<>/?"
        counter = Counter()
        bar = progressbar.ProgressBar(maxval=len(self.model)+10).start()
        for (_, row) in self.model.iterrows():
            bar.update(_)
            for word in row['content'].split():
                counter[word] += 1
        self.FREQWORDS = set([w for (w, _) in counter.most_common(10)])
        self.RAREWORDS = set(
            [w for (w, _) in counter.most_common()[:-10-1:-1]])
        self.LEMMATIZER = WordNetLemmatizer().lemmatize
        self.WORDNET_MAP = {"N": wordnet.NOUN,
                            "V": wordnet.VERB, "R": wordnet.ADV, "J": wordnet.ADJ}
        self.EMOTICONS = Emos.EMOTICONS
        self.UNICODE_EMO = Emos.UNICODE_EMO
        self.CORRECTOR = SpellChecker().correction
        self.UNKNOWN = SpellChecker().unknown
        self.counter = 1
        bar.update(len(self.model)+10)
        bar.finish()

    def run(self):
        print("Step 2: Preprocessing Data ...")
        self.lowering()
        self.remove_punctuation()
        self.remove_stop_words()
        self.remove_frequent_words()
        self.remove_rare_words()
        self.lemmatizing()
        self.convert_emojis()
        self.convert_emoticons()
        self.remove_urls()
        self.remove_html_tags()
        self.correct_spellings()
        self.save()

    def lowering(self):
        print(f"[{self.counter} / 11] Lowering all characters ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            b.update(_)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": row['content'],
                "preprocessed-content": row['content'].lower(),
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
            self.model.update
        self.model = pd.DataFrame(temp_model)
        self.counter += 1
        b.finish()

    def remove_punctuation(self):
        print(f"[{self.counter} / 11] Removing punctuations ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            b.update(_)
            content_list = [c for c in row["preprocessed-content"]]
            for i, c in enumerate(content_list):
                if c in self.PUNCTUATIONS:
                    content_list[i] = ""
            content = "".join(content_list)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": row["content"],
                "preprocessed-content": content,
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        self.model = pd.DataFrame(temp_model)
        self.counter += 1
        b.finish()

    def remove_stop_words(self):
        print(f"[{self.counter} / 11] Removing stop words ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            b.update(_)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": row["content"],
                "preprocessed-content": ' '.join([word for word in row['preprocessed-content'].split() if word not in self.STOPWORDS]),
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        self.model = pd.DataFrame(temp_model)
        self.counter += 1
        b.finish()

    def remove_frequent_words(self):
        print(f"[{self.counter} / 11] Removing frequent words ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            b.update(_)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": row["content"],
                "preprocessed-content": ' '.join([word for word in row['preprocessed-content'].split() if word not in self.FREQWORDS]),
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        self.model = pd.DataFrame(temp_model)
        self.counter += 1
        b.finish()

    def remove_rare_words(self):
        print(f"[{self.counter} / 11] Removing rare words ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            b.update(_)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": row['content'],
                "preprocessed-content": ' '.join([word for word in row['preprocessed-content'].split() if word not in self.RAREWORDS]),
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        self.model = pd.DataFrame(temp_model)
        self.counter += 1
        b.finish()

    def lemmatizing(self):
        print(f"[{self.counter} / 11] Lemmatizing words ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            b.update(_)
            pos_tagged = nltk.pos_tag(row['preprocessed-content'].split())
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": row['content'],
                "preprocessed-content": ' '.join([self.LEMMATIZER(word, self.WORDNET_MAP.get(pos[0], wordnet.NOUN)) for (word, pos) in pos_tagged]),
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        self.model = pd.DataFrame(temp_model)
        self.counter += 1
        b.finish()

    def convert_emojis(self):

        print(f"[{self.counter} / 11] Converting emojis ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            content = row['preprocessed-content']
            for emo in self.UNICODE_EMO:
                content = re.sub(
                    r'('+emo+')', "_".join(self.UNICODE_EMO[emo].replace(",", "").replace(":", "").split()), content)
            b.update(_)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": row['content'],
                "preprocessed-content": content,
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        self.model = pd.DataFrame(temp_model)
        self.counter += 1
        b.finish()

    def convert_emoticons(self):
        print(f"[{self.counter} / 11] Converting emoticons ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            content = row['preprocessed-content']
            for emot in self.EMOTICONS:
                content = re.sub(
                    u'(' + emot + ')', "_".join(self.EMOTICONS[emot].replace(",", "").split()), content)
            b.update(_)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": row['content'],
                "preprocessed-content": content,
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        self.model = pd.DataFrame(temp_model)
        self.counter += 1
        b.finish()

    def remove_urls(self):
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        print(f"[{self.counter} / 11] Removing URLs ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            b.update(_)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": row["content"],
                "preprocessed-content": url_pattern.sub(r'', row['content']),
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        self.model = pd.DataFrame(temp_model)
        self.counter += 1
        b.finish()

    def remove_html_tags(self):
        html_pattern = re.compile('<.*?>')
        print(f"[{self.counter} / 11] Removing HTML tags ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            b.update(_)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": row['content'],
                "preprocessed-content": html_pattern.sub(r'', row['preprocessed-content']),
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        self.model = pd.DataFrame(temp_model)
        self.counter += 1
        b.finish()

    def correct_spellings(self):
        print(f"[{self.counter} / 11] Correcting spellings ...")
        b = progressbar.ProgressBar(maxval=len(self.model)).start()
        temp_model = []
        for (_, row) in self.model.iterrows():
            b.update(_)
            content = row['preprocessed-content']
            corrected_text = []
            misspelled_words = self.UNKNOWN(content.split())
            for word in content.split():
                if word in misspelled_words:
                    corrected_text.append(self.CORRECTOR(word))
                    if corrected_text[-1] == None:
                        corrected_text[-1] = word
                else:
                    corrected_text.append(word)
            temp = {
                "id": row['id'],
                "date": row['date'],
                "version": row['version'],
                "score": row['score'],
                "content": row['content'],
                "preprocessed-content": ' '.join(corrected_text),
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        self.model = pd.DataFrame(temp_model)
        b.finish()

    def save(self):
        print("Step 3: Saving Preprocessed Data ...")
        self.worksheet.update([self.model.columns.values.tolist()
                               ] + self.model.values.tolist())
        print("Data saved successfully.")
        print(">>> Exiting Preprocessor ...")
        print("DONE")
