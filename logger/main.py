

def find_issues(jira, username):
    jql='project = FDT AND status = "blah" AND assignee in (%s) AND Sprint in openSprints()' % username
    issues = jira.search_issues(jql)
    for issue in issues:
        jissue = jira.issue(issue)
        createTicket(jissue)

def createTicket(jira, jissue):
        desc = 'Create ' + desc + ' data point'
        issue_dict = {
            'project': 'FDT',
            'summary': desc,
            'description': desc,
            'issuetype': {'name': 'New Feature'},
            'customfield_10900': 'Daily Fraud Scenarios',
            "timetracking": {"originalEstimate": "6"},
        }
        return jira.create_issue(fields=issue_dict)
