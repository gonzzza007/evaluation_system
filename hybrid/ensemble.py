from sklearn.ensemble import VotingRegressor
from rule_based.calculator import RuleBasedValuator
from regression.models.predict import RegressionValuator

class HybridModel:
    def __init__(self, rule_weight=0.5):
        self.rule_model = RuleBasedValuator()
        self.reg_model = RegressionValuator()
        self.weights = [rule_weight, 1-rule_weight]
        
    def predict(self, property_data: dict) -> float:
        rule_pred = self.rule_model.predict(property_data)
        reg_pred = self.reg_model.predict(property_data)
        return (rule_pred * self.weights[0]) + (reg_pred * self.weights[1])