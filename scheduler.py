import pandas as pd
from ics import Calendar, Event
from datetime import datetime


def read_schedule_csv(file_path, footer_lines):
    df = pd.read_csv(file_path, engine='python', skipfooter=footer_lines, index_col=0)
    transposed_df = df.transpose()
    transposed_df.reset_index(drop=True, inplace=True)
    transposed_df.drop(transposed_df.columns[0], axis=1, inplace=True)
    transposed_df.drop(transposed_df.index[0], inplace=True)
    melted_df = pd.melt(transposed_df, id_vars=None, var_name='Category', value_name='Value')

    dates = melted_df.loc[melted_df['Category'] == 'Week', 'Value'].reset_index(drop=True)
    shift = melted_df.loc[melted_df['Category'] == 'Shift', 'Value'].reset_index(drop=True)
    standby = melted_df.loc[melted_df['Category'] == 'Standby', 'Value'].reset_index(drop=True)

    new_df = pd.DataFrame({
        'Date': dates,
        'Shift': shift,
        'Standby': standby
    })

    return new_df


def create_calendar_events(name, df, work_start_hour, work_start_minutes, work_end_hour, work_end_minutes,
                           standby_start_hour, standby_start_minutes, standby_end_hour, standby_end_minutes):
    cal = Calendar()
    filtered_df = df[df.apply(lambda row: name in row.values, axis=1)]

    shift_df = filtered_df[filtered_df['Shift'] == name]
    standby_df = filtered_df[filtered_df['Standby'] == name]

    for index, row in shift_df.iterrows():
        create_event(cal, row['Date'], 'Work Shift', work_start_hour, work_start_minutes, work_end_hour,
                     work_end_minutes)

    for index, row in standby_df.iterrows():
        create_event(cal, row['Date'], 'Standby', standby_start_hour, standby_start_minutes, standby_end_hour,
                     standby_end_minutes)

    return cal


def create_event(calendar, date_str, event_name, start_hour, start_minutes, end_hour, end_minutes):
    event_date = datetime.strptime(date_str, '%d/%m/%y')
    start_time = event_date.replace(hour=start_hour, minute=start_minutes)
    end_time = event_date.replace(hour=end_hour, minute=end_minutes)

    event = Event()
    event.name = event_name
    event.begin = start_time
    event.end = end_time

    calendar.events.add(event)


def export_calendar(calendar, file_path):
    with open(file_path, 'w') as f:
        f.writelines(calendar)
