# This program will convert my schedule into a calendar file, so I don't have to manually enter my shifts and standby's
from scheduler import read_schedule_csv, create_calendar_events, export_calendar


def main():
    NAME = "Djoeke"
    FOOTER_LINES = 9
    WORK_START_HOUR = 20
    STANDBY_START_HOUR = 19
    STANDBY_START_MINUTES = 0

    schedule_df = read_schedule_csv('./schedules/schedule.csv', FOOTER_LINES)
    generated_calendar = create_calendar_events(NAME, schedule_df, WORK_START_HOUR, STANDBY_START_HOUR,
                                                STANDBY_START_MINUTES)
    export_calendar(generated_calendar, f'./calendars/schedule_{NAME}.ics')


if __name__ == "__main__":
    main()
