import pandas as pd


class GenerateCSV:
    def __init__(self, unfiltered_csv):
        self.output_df = None
        self.unfiltered_csv = unfiltered_csv

    def generateOutputCsv(self):
        unfiltered_df = pd.read_csv(self.unfiltered_csv)
        # FilterForOnlyAnomalousRows
        self.output_df = ""
        # generateOutputCsv
        return

    def getOutputDf(self):
        return self.output_df
