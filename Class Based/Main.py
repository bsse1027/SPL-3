from DataPreProcessor import DataPreProcess
from RuleGenerator import Rules
import pandas as pd


def main():
    # data_process = DataPreProcess()
    # csv_test_path = './test_v2.csv'
    # test = data_process.load_df(csv_test_path, nrows=None)
    pre_processed_csv_path = '../pre_processed.csv'
    df = pd.read_csv(pre_processed_csv_path)
    print(df.head())
    # rules = Rules(df)
    # rules.rule_one()
    # print(df['isAnomaly'])

if __name__ == "__main__":
    main()
