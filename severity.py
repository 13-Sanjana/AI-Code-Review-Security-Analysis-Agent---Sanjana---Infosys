SEVERITY = {

    # Code Analysis Agent
    "Long Method": "Medium",
    "Large Class": "High",
    "Too Many Parameters": "Low",
    "Deep Nesting": "Medium",
    "High Cyclomatic Complexity": "High",
    "Duplicate Code": "Medium",
    "Unused Variable": "Low",

    # Security Agent
    "SQL Injection": "Critical",
    "Hardcoded Secret": "High",
    "Dangerous Function": "Critical",
    "Command Injection": "Critical",
    "Weak Cryptography": "Medium",
    "Insecure File Operation": "Medium",
    "Weak Password": "High",
    "Java SQL Injection": "Critical",
    "Java Command Injection": "Critical"
}

def get_severity(rule):
    return SEVERITY.get(rule, "Low")