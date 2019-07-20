# chapter03
Let's write to GoogleSpreadSheet.

# Setup
## Create Service Account
### By Website
```zsh
# create service account
https://cloud.google.com/iam/docs/creating-managing-service-accounts
# set gcp path
$ copy key.json ../.gcp/key.json
# enable sheet api
https://cloud.google.com/apis/docs/enable-disable-apis
```

### By command line
```zsh
# login google suite
$ gcloud auth login
# create GCP project
$ gcloud projects create [PROJECT_ID]
# create service account
$ gcloud iam service-accounts create [SA-NAME] --display-name [SA-DISPLAY-NAME]
# generate service account key
$ gcloud iam service-accounts keys create ../.gcp/key.json --iam-account [SA-NAME]@[PROJECT-ID].iam.gserviceaccount.com
# enable sheets api
$ gcloud services enable sheets.googleapis.com
```

## Add Sheet Permission
Create a GoogleSpreadSheet and from "Share" add the edit permission of the service account created above.

# Run
## Write Google Spread Sheet
```zsh
$ python spread_sheet.py --help
usage: spread_sheet.py [-h] [-k KEY_PATH] [-s SPREAD_SHEET_ID] [-l LABEL]
                       [-t INPUT_TEXT]

Google Spread Sheet Script

optional arguments:
  -h, --help            show this help message and exit
  -k KEY_PATH, --key-path KEY_PATH
                        set service account key path (default
                        ../.gcp/key.json)
  -s SPREAD_SHEET_ID, --spread-sheet-id SPREAD_SHEET_ID
                        set spread sheet id
  -l LABEL, --label LABEL
                        set spread sheet cell label (default A1)
  -t INPUT_TEXT, --input-text INPUT_TEXT
                        set script interval seconds (default 100)


# Pass SPREAD_SHEET_ID in command line argument
$ python spread_sheet.py -s SPREAD_SHEET_ID -t 1234
# or update DEFAULT_SHEET_ID
$ python spread_sheet.py -t 1234
```