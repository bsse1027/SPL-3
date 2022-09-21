import numpy as np


class OutlierDetector:
    def __init__(self, data):
        self.upper_q = 0
        self.lower_q = 0
        self.iqr = 0
        self.lower_whisker = 0
        self.upper_whisker = 0
        self.data = data
        self.adjusted_z = 0
        self.z_score = 0

    def boxAndWhisker(self):
        np.median(self.data)
        self.upper_q = np.percentile(self.data, 75)
        self.lower_q = np.percentile(self.data, 25)
        self.iqr = self.upper_q - self.lower_q
        self.upper_whisker = self.data[self.data <= self.upper_q + 1.5 * self.iqr].max()
        self.lower_whisker = self.data[self.data >= self.lower_q - 1.5 * self.iqr].min()

    def getUpperWhisker(self):
        return self.upper_whisker

    def adjustedZScore(self):
        return

    def ZScore(self):
        return
