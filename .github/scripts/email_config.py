# Email Configuration for Shared Library Alerts

# Primary notification email (repository maintainer)
PRIMARY_EMAIL = "madanipyla@gmail.com"

# Team distribution lists
TEAM_EMAILS = [
    "team-lead@company.com",
    "senior-dev@company.com",
    "devops@company.com"
]

# Teams that should be notified by library
LIBRARY_TEAMS = {
    "CL_Util": ["core-team@company.com"],
    "Clpss_Common": ["clpss-team@company.com"],
    "Clpss_Occupancy": ["clpss-team@company.com"],
    "FireRating": ["fire-team@company.com"],
    "CSM": ["csm-team@company.com"],
    "Clpss_RateCLPolicy": ["policy-team@company.com"],
    "Clpss_ComposePrint": ["print-team@company.com"]
}

# Escalation emails (for critical libraries)
ESCALATION_EMAILS = [
    "manager@company.com",
    "architect@company.com"
]

# Critical libraries that require escalation
CRITICAL_LIBRARIES = [
    "CL_Util",
    "Clpss_Common"
]
