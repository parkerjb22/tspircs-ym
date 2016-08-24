from jira import JIRA


class TicketCreator():
    policies = {
        'Convert Existing Rules/Parameters to CustomRules/Criteria/Parameters',
        'Create upgrade script that converts live rules to custom rules',
        'Convert Daily Processing to Use Custom Rules',
        'Convert Client to use Custom Rules',
        'Convert Custom Rule Creation Dialog to use Parameters',
        'Update Category for each criteria',
        'Risk Modifier Script',
        'Add parameter types and descriptions',
        'Handle Migrations (run upgrade scripts after rules have been migrated)',
        'fix custom rules for credit union installs',
        'Worklist Filter By rule',
    }

    def createTicket(self, jira, desc):
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

    def createTickets(self, username, password):
        jira = JIRA(server='http://mmoyhtools:8080/', basic_auth=(username, password))
        for policy in self.policies:
            issue = self.createTicket(jira, policy)
            print(issue)


ct = TicketCreator().createTickets('', '')
