from concurrent.futures import ThreadPoolExecutor

from agents.code_analysis import CodeAnalysisAgent
from agents.security_agent import SecurityAgent


class MultiAgentOrchestrator:

    def __init__(self):

        self.code_agent = CodeAnalysisAgent()

        self.security_agent = SecurityAgent()

    ###########################################################

    def run(self, code):

        with ThreadPoolExecutor(max_workers=2) as executor:

            future_analysis = executor.submit(
                self.code_agent.analyze,
                code
            )

            future_security = executor.submit(
                self.security_agent.scan,
                code
            )

            analysis_findings = future_analysis.result()

            security_findings = future_security.result()

        findings = analysis_findings + security_findings

        findings.sort(key=lambda x: x.line)

        return findings

    ###########################################################

    def generate_summary(self, findings):

        summary = {

            "Critical": 0,

            "High": 0,

            "Medium": 0,

            "Low": 0

        }

        for finding in findings:

            summary[finding.severity] += 1

        return summary

    ###########################################################

    def generate_report(self, code):

        findings = self.run(code)

        summary = self.generate_summary(findings)

        return {

            "summary": summary,

            "total_findings": len(findings),

            "findings": [

                {

                    "rule": f.rule,

                    "severity": f.severity,

                    "line": f.line,

                    "message": f.message,

                    "recommendation": f.recommendation

                }

                for f in findings

            ]

        }