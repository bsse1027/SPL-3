import pandas as pd

import DataPreProcessor as DataPreProcessor
from GenerateCSV import GenerateCSV


class UserInterface:
    # csv_generator = GenerateCSV()

    def inputFile(self):
        # data_process = DataPreProcessor()
        # csv_path = './test_v2.csv'
        # df = data_process.getDf(csv_path, nrows=None)
        pre_processed_csv_path = '../pre_processed.csv'
        input_df = pd.read_csv(pre_processed_csv_path)
        return input_df

    def notifyUser(self):
        anomaly_count = 0
        return anomaly_count

    def showResult(self, final_csv):
        self.csv_generator(final_csv)
        final_df = self.csv_generator.generateOutputCsv()
        return
