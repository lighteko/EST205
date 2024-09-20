import requests
import os

class EmotionsAPI:
    def __init__(self):
        self.API_URL = "https://api-inference.huggingface.co/models/SamLowe/roberta-base-go_emotions"
        self.headers = {"Authorization": f"Bearer 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"}
    
    """
    returns top three probable emotions from the text
    """
    def query(self, text: str)->list:
        payload = {"inputs": text}
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        try:
            data = response.json()[0]
        except:
            return []
        data = list(map(lambda x: (x['label'], x['score']), data))
        return data[:2]
    