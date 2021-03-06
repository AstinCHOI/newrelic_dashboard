# New Relic Dashboard for Basic Users

The new user model of New Relic has two kind of users, FULL and BASIC user. The big difference between FULL and BASIC user is that BASIC users don't have the curated menu such as APM. This script creates a few dashboards which have SOME same plots as FULL user's APM view for Basic Users.

For example, APM menu for Full users:  
<p align="center">
<img src="https://raw.githubusercontent.com/AstinCHOI/_newrelic_resources/main/newrelic_dashboard_fulluser.png" alt="Full User" width="900"/>
</p>

Basic users don't have APM menu, so this script creates the APM dashboard which is able to import from New Relic One.
<p align="center">
<img src="https://raw.githubusercontent.com/AstinCHOI/_newrelic_resources/main/newrelic_dashboard_basicuser.png" alt="Basic User" width="900"/>
</p>


## Run
It's python 3 script and needs [requests](https://pypi.org/project/requests/) module.
```bash
$ pip install requests
$ git clone https://github.com/AstinCHOI/newrelic_dashboard
$ cd newrelic_dashboard
$ python newrelic_dashboard.py
New Relic account ID: xxxxxx
New Relic API key: yyyyyy....
```
- You can find your account ID and API key: [one.newrelic.com](one.newrelic.com) > Top right ⌽ button > API keys  
- The key type must be USER.
- This script finds top 5 transactions' services for the last week then creates ~5 dashboards.


## Reference
#### New Relic GraphQL
https://api.newrelic.com/graphiql

#### New Relic Data Retention
https://docs.newrelic.com/docs/telemetry-data-platform/ingest-manage-data/manage-data/manage-data-retention/#adjust-retention