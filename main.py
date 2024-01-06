# This program will convert my schedule into a calendar file, so I don't have to manually enter my shifts and standby's
import pandas as pd
from ics import Calendar, Event
from datetime import datetime, timedelta

NAME = "Djoeke"

# Read CSV file
df = pd.read_csv('./schedules/schedule.csv', engine='python', skipfooter=9, index_col=0)

transposed_df = df.transpose()
# transposed_df.drop(df.columns[0], axis=1, inplace=True)
transposed_df.reset_index(drop=True, inplace=True)

# Drop the first column
transposed_df.drop(transposed_df.columns[0], axis=1, inplace=True)
# Drop the first row
transposed_df.drop(transposed_df.index[0], inplace=True)

# Use melt to reshape the DataFrame
melted_df = pd.melt(transposed_df, id_vars=None, var_name='Category', value_name='Value')

# Extract relevant information
dates = melted_df.loc[melted_df['Category'] == 'Week', 'Value'].reset_index(drop=True)
shift = melted_df.loc[melted_df['Category'] == 'Shift', 'Value'].reset_index(drop=True)
standby = melted_df.loc[melted_df['Category'] == 'Standby', 'Value'].reset_index(drop=True)

# Create a new DataFrame with the reshaped data
new_df = pd.DataFrame({
    'Date': dates,
    'Shift': shift,
    'Standby': standby
})


filtered_df = new_df[new_df.apply(lambda row: NAME in row.values, axis=1)]


cal = Calendar()

shift_df = filtered_df[filtered_df['Shift'] == NAME]
standby_df = filtered_df[filtered_df['Standby'] == NAME]

for index, row in shift_df.iterrows():
    # Create a work shift event
    date_str = row['Date']
    # Convert date string to datetime object
    event_date = datetime.strptime(date_str, '%d/%m/%y')

    # Set the start and end times based on your requirements
    start_time = event_date.replace(hour=20, minute=0)
    end_time = event_date.replace(hour=23, minute=0)

    # Create an event
    event = Event()
    event.name = 'Work Shift'  # Adjust the event name as needed
    event.begin = start_time
    event.end = end_time

    # Add the event to the calendar
    cal.events.add(event)

for index, row in standby_df.iterrows():
    # Create a standby event
    date_str = row['Date']
    # Convert date string to datetime object
    event_date = datetime.strptime(date_str, '%d/%m/%y')

    # Set the start and end times based on your requirements
    start_time = event_date.replace(hour=20, minute=0)
    end_time = event_date.replace(hour=23, minute=0)

    # Create an event
    event = Event()
    event.name = 'Standby'  # Adjust the event name as needed
    event.begin = start_time
    event.end = end_time

    # Add the event to the calendar
    cal.events.add(event)

# Export the calendar
with open('./calendars/schedule.ics', 'w') as f:
    f.writelines(cal)
