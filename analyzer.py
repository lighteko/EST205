from collections import Counter
import pandas as pd
import gspread as gs
import progressbar
import numpy as np
from api import EmotionsAPI as emAPI


class Analyzer:
    def __init__(self):
        print("Step 0: Checking Credentials ...")
        self.serv_acc = gs.service_account(filename='./credentials.json')
        self.sheet = self.serv_acc.open("EST 205 Data Sheet")
        self.file_name = input("> Enter the worksheet name: ")
        print("> Initializing Analyzer ...")
        self.worksheet = self.sheet.worksheet(self.file_name)
        self.model: pd.DataFrame = pd.DataFrame(
            self.worksheet.get_all_records())
        self.emotions = emAPI().query
        self.MAX_TASKS = 3
        self.CUR_TASK = 1
        self.MONTHLY_RATING = {}
        self.VERSION_RATING = {}
        self.WORD_FREQ = []
        self.UPVOTEDS = None

    def run(self):
        # self.anlz_emotion()
        # self.anlz_word_frequency()
        self.anlz_monthly_rating()
        self.anlz_rating_by_version()
        self.anlz_top5_upvoted_reviews()
        self.save()

    def anlz_emotion(self) -> None:
        print(f"[{self.CUR_TASK}/{self.MAX_TASKS}] Analyzing Emotions ...")
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
                "emotion": f"{self.emotions(row['content'])}",
                "upvote": row['upvote'],
                "reply": row['reply'],
                "reply_date": row['reply_date']
            }
            temp_model.append(temp)
        self.model = pd.DataFrame(temp_model)
        self.CUR_TASK += 1
        b.finish()

    def anlz_word_frequency(self) -> None:
        print(f"[{self.CUR_TASK}/{self.MAX_TASKS}] Analyzing Word Frequency ...")
        five, four, three, two, one = Counter(), Counter(), Counter(), Counter(), Counter()
        b = progressbar.ProgressBar(maxval=len(self.model)).start()

        for (_, row) in self.model.iterrows():
            preprc_content = str(row['preprocessed-content']).split()
            for word in preprc_content:
                if (row['score'] == 5):
                    five[word] += 1
                elif (row['score'] == 4):
                    four[word] += 1
                elif (row['score'] == 3):
                    three[word] += 1
                elif (row['score'] == 2):
                    two[word] += 1
                else:
                    one[word] += 1
            b.update(_)
        self.WORD_FREQ = [five, four, three, two, one]
        self.CUR_TASK += 1
        b.finish()

    def anlz_monthly_rating(self) -> None:
        print(f"[{self.CUR_TASK}/{self.MAX_TASKS}] Analyzing Monthly Ratings ...")
        b = progressbar.ProgressBar(maxval=len(self.model) + 10).start()
        for (_, row) in self.model.iterrows():
            b.update(_)
            month = row['date'].split()[0][:-3]
            if month not in self.MONTHLY_RATING:
                self.MONTHLY_RATING[month] = []
            self.MONTHLY_RATING[month].append(int(row['score']))
        for month in self.MONTHLY_RATING:
            self.MONTHLY_RATING[month] = np.mean(
                self.MONTHLY_RATING[month]).round(2)
        self.CUR_TASK += 1
        b.update(len(self.model) + 10)
        b.finish()

    def anlz_rating_by_version(self) -> None:
        print(f"[{self.CUR_TASK}/{self.MAX_TASKS}] Analyzing Ratings by Version ...")
        b = progressbar.ProgressBar(maxval=len(self.model) + 10).start()
        for (_, row) in self.model.iterrows():
            b.update(_)
            version = row['version']
            if version == None:
                continue
            if version not in self.VERSION_RATING:
                self.VERSION_RATING[version] = []
            self.VERSION_RATING[version].append(int(row['score']))
        for version in self.VERSION_RATING:
            self.VERSION_RATING[version] = np.mean(
                self.VERSION_RATING[version]).round(2)
        self.CUR_TASK += 1
        b.update(len(self.model) + 10)
        b.finish()

    def anlz_top5_upvoted_reviews(self) -> None:
        print(
            f"[{self.CUR_TASK}/{self.MAX_TASKS}] Analyzing Top 5 Upvoted Reviews ...")
        self.UPVOTEDS = self.model.sort_values(
            by='upvote', ascending=False).head(5)
        self.CUR_TASK += 1

    def anlz_mentioning_competitors(self) -> None:
        pass
    
    def compare_versions(version1, version2) -> int:
        for i in range(3):
            if version1[i] > version2[i]:
                return 1
            elif version1[i] < version2[i]:
                return -1
        return 0

    def sort_by_version(dataframe) -> None:
        for (i, row) in dataframe.iterrows()[1:]:
            version = row['version']
            if version == None:
                continue
            version = version.split(".")
            version = [int(x) for x in version]
            
            

    def save(self) -> None:
        print("Step 3: Saving Preprocessed Data ...")
        self.worksheet.update([self.model.columns.values.tolist()
                               ] + self.model.values.tolist())
        pd.DataFrame(self.MONTHLY_RATING.items(), columns=[
                     "Month", "Rating"]).to_csv(f"./res/analysis/{self.file_name.lower()}_monthly_rating.csv", index=False)
        version_rating = pd.DataFrame(self.VERSION_RATING.items(), columns=[
                     "Version", "Rating"])
        version_rating.sort_index(inplace=True)
        version_rating.to_csv(f"./res/analysis/{self.file_name.lower()}_version_rating.csv", index=False)
        pd.DataFrame(self.UPVOTEDS).to_csv(
            f"./res/analysis/{self.file_name.lower()}_top5_upvoted_reviews.csv", index=False)
        print("Data saved successfully.")
        print(">>> Exiting Preprocessor ...")
        print("DONE")
