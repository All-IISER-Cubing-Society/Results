# For using GSpread, first refer to Authentication Docs:
# https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account
# Make sure to share spreadsheet with the service account email

import os

import gspread
import pandas as pd

results_dir = "results/"

# Create results directory if it does not exist
if not os.path.exists(results_dir):
    os.mkdir(results_dir)

# Get all worksheets
gc = gspread.service_account()
sh = gc.open("AICS-Results")
worksheets = sh.worksheets()

for ws in worksheets:
    df = pd.DataFrame(ws.get_all_records())
    csv_path = os.path.join(results_dir, ws.title + ".csv")
    df.to_csv(csv_path, index=False)
