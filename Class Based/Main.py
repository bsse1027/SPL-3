from RuleGenerator import RuleGenerator
from UserInterface import UserInterface


def main():
    user_interface = UserInterface()

    df = user_interface.inputFile()
    rule_implement = RuleGenerator(df)
    rule_implement.ruleRareCountries()
    ruled_df = rule_implement.getDf()
    print(ruled_df['isAnomaly'])



if __name__ == "__main__":
    main()
