from typing import List, Dict
import pandas as pd


class KanoSurvey:

    POSSIBLE_ANSWERS = ["I LIKE IT", "I EXPECT IT", "I AM NEUTRAL", "I CAN TOLERATE IT", "I DISLIKE IT"]
    questions: List[str]
    test_answers: Dict[str, List[str]]
    df: pd.DataFrame


    def __init__(self, csv_file):
        # Parse Survey questions
        df = pd.read_csv(csv_file)
        df = df[df["type"] != 0]
        self.questions = df["question"]

        # Parse Test answers
        self.test_answers = {}
        try:
            self.test_answers["airidas"] = list(df["airidas"])
        except:
            print("No airidas answers column found in the csv file")
        try:
            self.test_answers["elias"] = list(df["Elias"])
        except:
            print("No elias answers column found in the csv file")

        self.df = df 
        

        
class PersonalitySurvey:
    
    POSSIBLE_ANSWERS = ["DISAGREE", "SOMEWHAT DISAGREE", "NEUTRAL", "SOMEWHAT AGREE", "AGREE"]
    questions: List[str]
    test_answers: Dict[str, List[str]]
    df: pd.DataFrame

    def __init__(self, csv_file):
        # Parse Survey questions
        surv = pd.read_csv(csv_file)
        self.questions = surv["question"]

        # Parse Test answers
        self.test_answers = {}
        try:
            self.test_answers["airidas"] = list(surv["airidas"])
        except:
            print("No airidas answers column found in the csv file")
        try:
            self.test_answers["elias"] = list(surv["Elias"])
        except:
            print("No elias answers column found in the csv file")

        self.df = surv 

class DictatorGameSurvey:
    
    POSSIBLE_ANSWERS = ["LEFT", "RIGHT"]
    questions: List[str]
    test_answers: Dict[str, List[str]]
    df: pd.DataFrame

    def __init__(self, csv_file):
        # Parse Survey questions
        surv = pd.read_csv(csv_file)
        self.questions = surv["question"]

        # Parse Test answers
        self.test_answers = {}
        try:
            self.test_answers["airidas"] = list(surv["airidas"])
        except:
            print("No airidas answers column found in the csv file")
        try:
            self.test_answers["elias"] = list(surv["Elias"])
        except:
            print("No elias answers column found in the csv file")

        self.df = surv 


def buildFairnessPrompts(csv_file) -> List[str]:
    surv = pd.read_csv(csv_file)
    surv = surv[surv["framing"] == "Change"]

    CONSTANT_TEXT = "Your answer should only contain the chosen option. Evalaute to the situation below with one of the four options: COMPLETELY FAIR, ACCEPTABLE, UNFAIR, VERY UNFAIR. "

    sps = []
    for q in surv["question"]:
        sp = f"{CONSTANT_TEXT}\n\n{q}"
        sps.append(sp)

    return sps
