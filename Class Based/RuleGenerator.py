import time
import json
import numpy as np
import pandas as pd
import ast
from pandas import json_normalize
import matplotlib.pyplot as plt

from OutlierDetector import OutlierDetector


class RuleGenerator:

    def __init__(self, test):
        self.test = test

    def ruleRareCountries(self):
        # First Rule : If total hits of a session from NON Opearting/rare countries is outlier means 1.5 IQR from Q3

        sum = 0
        lowCountries = []
        cnt = self.test['geoNetwork.country'].value_counts(sort=True)

        for i in range(0, cnt.size):
            sum = sum + cnt[i]

        # Identify the Non Operating Countries

        for i in range(0, cnt.size):
            # print(f"Country Name: {cnt.index[i]} Frequency: {(cnt[i]/sum)*100}%" )
            if ((cnt[i] / sum) * 100 < 0.01):
                lowCountries.append(cnt.index[i])

        inputCountries = self.test.at[0, 'geoNetwork.country']

        self.test['totals.hits'] = pd.to_numeric(self.test['totals.hits'])
        data = self.test['totals.hits']
        outlier_detector = OutlierDetector(data)
        upper_whisker = outlier_detector.getUpperWhisker()

        for indx in range(self.test.index.start, self.test.index.stop):
            country = self.test.at[indx, 'geoNetwork.country']
            oneIndex = (self.test.at[indx, 'hits'])
            hitsInfo = ast.literal_eval(oneIndex)
            # print(hitsInfo)
            if country in lowCountries:
                hit = self.test.at[indx, 'totals.hits']
                if int(hit) > upper_whisker:
                    self.test.loc[indx, 'isAnomaly'] = 1
                    # print(f"Index Number : {indx} Anomalous traffic Info: {country} Total Hits : {int(hit)}")
        #             for ind in range(0, len(hitsInfo)):
        #                 print(f"Hit Number: {hitsInfo[ind]['hitNumber']} Visited Page: {hitsInfo[ind]['appInfo']['screenName']} Keyword: {test.at[indx, 'trafficSource.keyword']}")
        # print(f"Country Name: {country} --> Total hits: {hit}")
        #         if country in hitWithCountry.keys():
        #             hitWithCountry[country] += 1
        #         else:
        #             hitWithCountry[country]=1

        # newArr = test['hits'].to_numpy()

    def ruleTotalPageView(self):
        

    def getDf(self):
        return self.test
