import json
import requests


accountId = input('New Relic account ID: ')
apiKey = input('New Relic API key: ')

headers = {
    "Content-Type": "application/json",
    "API-Key": "%s" % apiKey
}
data_nrql = {"query": "{actor {account(id: %s) { \
            nrql(query: \"SELECT count(*) \
            from Transaction \
            facet appName, entityGuid \
            limit 5 since 7 days ago\") \
            { results } } } }" % accountId,
        "variables": ""}

session = requests.Session()
session_nrql = session.post("https://api.newrelic.com/graphql", 
    headers=headers, 
    data=json.dumps(data_nrql))

if session_nrql.status_code == 200:
    session_nrql_result = json.loads(session_nrql.text)
    try:
        results = \
            session_nrql_result["data"]["actor"]["account"]["nrql"]["results"]
        
        if results:
            dashboard_template = ""
            with open("dashboard_template", "r") as json_file:
                dashboard_template = json_file.read()

            for num, result in enumerate(results):
                name = result["facet"][0]
                guid = result["facet"][1]
                dashboard = dashboard_template.replace("${name}", name)
                dashboard = dashboard.replace("${accountId}", accountId)
                dashboard = dashboard.replace("${entity.guid}", guid)

                data_dashboard = {
                    "query": "mutation { dashboardCreate(accountId: %s,\
                        dashboard: %s) { errors { description type } } }" \
                        % (accountId, dashboard),
                    "variables": ""}
                session_dashboard = session.post("https://api.newrelic.com/graphql",
                    headers=headers, 
                    data=json.dumps(data_dashboard))
                
                if session_dashboard.status_code == 200:
                    session_dashboard_result = json.loads(session_dashboard.text)
                    if "data" in session_dashboard_result  and \
                        "dashboardCreate" in session_dashboard_result["data"] and \
                        "errors" in session_dashboard_result["data"]["dashboardCreate"]:
                        
                        if session_dashboard_result["data"]["dashboardCreate"]["errors"] is None:
                            print("Dashboard %s created! (%i/%i)" % (name, num+1, len(results)))
                        else:
                            print("[Error] Result: %s" % session_dashboard_result["data"]["dashboardCreate"]["errors"])
                    else:
                        print("[Error] Something wrong: %s" % session_dashboard_result)
                else:
                    print("[Error] status code %i: %s" % (session_dashboard.status_code, session_dashboard.text))                
        else:
            print("There are no transactions!")
    except Exception as err:
        print(err)
else:
    print("[Error] status code %i: %s" % (session_nrql.status_code, session_nrql.text))
