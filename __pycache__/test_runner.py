from datetime import datetime
from services.execution_engine import ExecutionEngine
class TestRunner:
    """
    Automated Test Case Runner
    Executes user code against multiple test cases
    and generates pass/fail results.
    """

    def __init__(self, language: str, code: str, test_cases: str):
        self.language = language.lower().strip()
        self.code = code
        self.test_cases = test_cases.strip().split("\n") if test_cases else []
        self.results = []

    # ---------------------------------------------------
    # Public Method
    # ---------------------------------------------------
    def run_tests(self) -> dict:
        if not self.test_cases:
            return {
                "status": "error",
                "message": "No test cases provided."
            }

        engine = ExecutionEngine(self.language, self.code)

        for case in self.test_cases:
            case = case.strip()
            if not case:
                continue

            execution_result = engine.execute()

            output = execution_result.get("output", "")
            error = execution_result.get("error", "")

            passed = (output == case)

            self.results.append({
                "expected": case,
                "actual": output,
                "passed": passed,
                "error": error
            })

        passed_count = sum(1 for r in self.results if r["passed"])
        total = len(self.results)

        return {
            "status": "completed",
            "executed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total": total,
                "passed": passed_count,
                "failed": total - passed_count
            },
            "details": self.results
        }