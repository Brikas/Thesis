from typing import List, Dict
import pandas as pd


class KanoSurvey:

    POSSIBLE_ANSWERS = ["I LIKE IT", "I EXPECT IT", "I AM NEUTRAL", "I CAN TOLERATE IT", "I DISLIKE IT"]
    questions: List[str];
    test_answers: Dict[str, List[str]];
    _surv: pd.DataFrame;

    def __init__(self, csv_file, default_instruction_text: str = None):
        self.test_answers = {}
        self._build(csv_file)
        
        if default_instruction_text is None:
            self.default_instruction_text = f"Your answer should only contain the chosen option. Reply to the statement below with one of the five options: {', '.join(self.POSSIBLE_ANSWERS)}."
        else:
            self.default_instruction_text = default_instruction_text

    def getDefaultPromptBlocks(self) -> List[str]:
        sps = []
        for q in self.surv["question"]:
            sp = f"{self.default_instruction_text}\n\n{q}"
            sps.append(sp)
        return sps
        
    def _build(self, csv_file) -> List[str]:
        surv = pd.read_csv(csv_file)
        surv = surv[surv["type"] != 0]
        self.questions = surv["question"]
        try:
            self.test_answers["airidas"] = list(surv["airidas"])
        except:
            print("No airidas answers column found in the csv file")
        try:
            self.test_answers["elias"] = list(surv["Elias"])
        except:
            print("No elias answers column found in the csv file")

        self._surv = surv
        


def buildPersonalityTestPrompts(csv_file) -> List[str]:
    surv = pd.read_csv(csv_file)

    CONSTANT_TEXT = "Your answer should only contain the chosen option. Reply to the statement below with one of the five options: DISAGREE, SOMEWHAT DISAGREE, NEUTRAL, SOMEHWHAT AGREE, AGREE."

    sps = []
    for q in surv["question"]:
        sp = f"{CONSTANT_TEXT}\n\n{q}"
        sps.append(sp)

    return sps

def buildDictatorGamePrompts(csv_file) -> List[str]:
    surv = pd.read_csv(csv_file)

    CONSTANT_TEXT = "You are given two options, LEFT or RIGHT. Select one of the options. Your answer should contain only the label of the option."

    sps = []
    for q in surv["question"]:
        sp = f"{CONSTANT_TEXT}\n\n{q}"
        sps.append(sp)

    return sps

def buildFairnessPrompts(csv_file) -> List[str]:
    surv = pd.read_csv(csv_file)
    surv = surv[surv["framing"] == "Change"]

    CONSTANT_TEXT = "Your answer should only contain the chosen option. Evalaute to the situation below with one of the four options: COMPLETELY FAIR, ACCEPTABLE, UNFAIR, VERY UNFAIR. "

    sps = []
    for q in surv["question"]:
        sp = f"{CONSTANT_TEXT}\n\n{q}"
        sps.append(sp)

    return sps
