import csv
import os
from rules.rule_detector import RuleBasedDetector
from model.ml_detector import MLPromptInjectionDetector


class PromptInjectionSystem:
    def __init__(self, data_path):
        self.rule_detector = RuleBasedDetector()
        self.ml_detector = MLPromptInjectionDetector()
        self.ml_detector.train(data_path)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_path = os.path.join(base_dir, "logs", "prompt_logs.csv")

    def _risk_level(self, confidence):
        if confidence >= 0.7:
            return "HIGH"
        if confidence >= 0.4:
            return "MEDIUM"
        return "LOW"

    def _log(self, result, prompt):
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        with open(self.log_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                prompt,
                result["is_malicious"],
                result["method"],
                result["attack_type"],
                result["risk_level"],
                result["confidence"]
            ])

    def analyze_prompt(self, prompt):
       
        rule_flag, matched_rule, attack_type, severity = self.rule_detector.check(prompt)

        if rule_flag:
            result = {
                "is_malicious": True,
                "method": "rule_based",
                "attack_type": attack_type,
                "risk_level": "HIGH",
                "reason": f"Matched explicit rule pattern: '{matched_rule}'",
                "confidence": 1.0
            }
            self._log(result, prompt)
            return result

        ml_prediction, ml_confidence = self.ml_detector.predict(prompt)

        if ml_prediction:
            reason = "Statistically similar to known prompt injection attempts"
            attack_type = "ml_detected_general"
        else:
            reason = "No known prompt injection patterns detected"
            attack_type = "none"

        result = {
            "is_malicious": bool(ml_prediction),
            "method": "ml_based",
            "attack_type": attack_type,
            "risk_level": self._risk_level(ml_confidence),
            "reason": reason,
            "confidence": round(ml_confidence, 2)
        }

        self._log(result, prompt)
        return result
