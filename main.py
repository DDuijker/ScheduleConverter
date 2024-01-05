# This program will convert my schedule into a calendar file, so I don't have to manually enter my shifts and standby's

# import pandas
import pandas as pd
# Read CSV file
df = pd.read_csv('./schedules/01-2024.csv' )
df.columns = ["Key", "Weeknummer", "Maandag", "Dinsdag","Woensdag", "Donderdag", "Vrijdag"]

dates_row = df[df["Key"] == "Week"]
shift_row = df[df["Key"] == "Shift"]

# print(dates_row)
print(shift_row)


