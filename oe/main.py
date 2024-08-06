import pandas as pd

class OE:
    def __init__(self, dimResponser, dimAnswer, dimQuestion, Fact):
        self.dimResponser = dimResponser
        self.dimAnswer = dimAnswer
        self.dimQuestion = dimQuestion
        self.Fact = Fact
        self.dataframes = pd.DataFrame({
            'responseID': [],
            'questionCode': [],
            'root': [],
            'processed': []
        })
    
    def process_OE(self, question_code, function, answer_value=True):
        info_df = self.Fact.query('questionCode == @question_code').copy()
        if answer_value:
            info_df['processed'] = info_df['answerValuesText'].apply(function)
        else:
            info_df['processed'] = info_df['answerText'].apply(function)
        info_df = info_df.explode('processed')
        info_df.rename(columns={'answerValuesText': 'root', 'answerText': 'root'}, inplace=True)
        print(self.dataframes.columns)
        print(info_df.columns)
        self.dataframes = pd.concat([self.dataframes, info_df])