from datetime import datetime
class FeedbackEngine:
    """
    Intelligent Feedback Generator
    Generates performance feedback based on:
    - Review score
    - Test results
    - Execution errors
    """

    def __init__(self, review_result: dict, test_result: dict = None, execution_result: dict = None):
        self.review_result = review_result or {}
        self.test_result = test_result or {}
        self.execution_result = execution_result or {}

    # ---------------------------------------------------
    # Public Method
    # ---------------------------------------------------
    def generate_feedback(self) -> dict:
        performance = self._evaluate_performance()
        improvement = self._suggest_improvements()

        return {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "performance_level": performance,
            "improvement_advice": improvement
        }

    # ---------------------------------------------------
    # Performance Evaluation
    # ---------------------------------------------------
    def _evaluate_performance(self) -> str:
        score = self.review_result.get("score", 0)

        if score >= 85:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 50:
            return "Average"
        else:
            return "Needs Improvement"

    # ---------------------------------------------------
    # Improvement Suggestions
    # ---------------------------------------------------
    def _suggest_improvements(self) -> list:
        advice = []

        # Based on review warnings
        warnings = self.review_result.get("warnings", [])
        if warnings:
            advice.append("Resolve warnings to improve code quality.")

        # Based on test results
        if self.test_result:
            failed = self.test_result.get("summary", {}).get("failed", 0)
            if failed > 0:
                advice.append(f"{failed} test case(s) failed. Review your logic carefully.")

        # Based on execution errors
        if self.execution_result:
            if self.execution_result.get("error"):
                advice.append("Fix runtime errors before submission.")

        if not advice:
            advice.append("Great job! Keep improving your coding practices.")

        return advice