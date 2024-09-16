from collections import Counter
import re
import pandas as pd
import gspread as gs
import progressbar
import numpy as np
import matplotlib.pyplot as plt
from api import EmotionsAPI as emAPI


class Analyzer:
    def __init__(self):
        print("Step 0: Checking Credentials ...")
        self.serv_acc = gs.service_account(filename='./credentials.json')
        self.sheet = self.serv_acc.open("EST 205 Data Sheet")
        self.file_name = input(">>> Enter the worksheet name: ")
        print(">>> Initializing Analyzer ...")
        self.worksheet = self.sheet.worksheet(self.file_name)
        self.model: pd.DataFrame = pd.DataFrame(
            self.worksheet.get_all_records())
        self.emotions = emAPI().query

    def run(self):
        pass

    def anlz_emotion(self):
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
                "preprocessed-content": row['preprocessed-content'],
                "emotion": self.emotions(row['preprocessed-content']),
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        self.model = pd.DataFrame(temp_model)
        b.finish()

    def anlz_word_frequency(self, score: int):
        pass

    def anlz_monthly_rating(self):
        pass

    def save(self):
        print("Step 3: Saving Preprocessed Data ...")
        self.worksheet.update([self.model.columns.values.tolist()
                               ] + self.model.values.tolist())
        print("Data saved successfully.")
        print(">>> Exiting Preprocessor ...")
        print("DONE")
