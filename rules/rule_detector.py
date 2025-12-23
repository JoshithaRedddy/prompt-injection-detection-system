class RuleBasedDetector:
    def __init__(self):
        self.patterns = {
            "instruction_override": [
                "ignore previous instructions",
                "ignore all previous instructions",
                "forget your previous instructions",
                "disregard earlier instructions",
                "override system instructions",
                "reset your instructions",
                "forget all rules above",
                "do not follow the above rules"
            ],

            "role_manipulation": [
                "act as",
                "pretend you are",
                "you are no longer an ai",
                "you are not an ai",
                "simulate an unrestricted model",
                "assume the role of"
            ],

            "policy_bypass": [
                "bypass safety",
                "bypass content filters",
                "disable safety",
                "disable moderation",
                "without any restrictions",
                "no ethical limitations",
                "uncensored response"
            ],

            "system_prompt_leakage": [
                "show system prompt",
                "reveal system instructions",
                "print developer message",
                "what are your hidden instructions"
            ]
        }

        self.safe_roles = [
            "teacher",
            "student",
            "interviewer",
            "mentor",
            "tutor",
            "coach",
            "storyteller",
            "friend"
        ]

        self.dangerous_roles = [
            "unrestricted",
            "jailbroken",
            "no rules",
            "hacker",
            "evil",
            "without restrictions"
        ]

    def check(self, prompt):
        text = prompt.lower()

        if "act as" in text:
            if any(role in text for role in self.safe_roles):
                return False, None, None
            if any(role in text for role in self.dangerous_roles):
                return True, "act as (dangerous role)", "role_manipulation"

        for attack_type, patterns in self.patterns.items():
            for pattern in patterns:
                if pattern in text:
                    return True, pattern, attack_type

        return False, None, None
