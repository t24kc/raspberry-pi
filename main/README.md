# main
Let's carry out watering when the solar radiation a certain value.

# Setup
## Create OAuth 2.0 client
### By Website
```zsh
# create oauth client
https://developers.google.com/gmail/api/quickstart/python#step_1_turn_on_the
# set credentials path
$ mv credentials.json .gcp/credentials.json
# enable gmail api
https://cloud.google.com/apis/docs/enable-disable-apis
```

### By command line
```zsh
# login google suite
$ gcloud auth login
# create GCP project
$ gcloud projects create [PROJECT_ID]
# create oauth client
https://console.cloud.google.com/apis/credentials
# set credentials path
$ mv credentials.json .gcp/credentials.json
# enable gmail api
$ gcloud services enable gmail.googleapis.com
```

## Update Credential Consent
https://console.cloud.google.com/apis/credentials/consent

# Run
## Write All Sensors to Google Spread Sheet and Trun on water
```zsh
# update config file
$ config.yaml

# run script
$ python3 handler.py
```