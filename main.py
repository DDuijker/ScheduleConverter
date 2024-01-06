# This program will convert my schedule into a calendar file, so I don't have to manually enter my shifts and standby's
import pandas as pd

# Read CSV file
df = pd.read_csv('./schedules/01-2024.csv', engine='python', skipfooter=9, index_col=0)

transposed_df = df.transpose()
# transposed_df.drop(df.columns[0], axis=1, inplace=True)
transposed_df.reset_index(drop=True, inplace=True)

# Drop the first column
transposed_df.drop(transposed_df.columns[0], axis=1, inplace=True)
# Drop the first row
transposed_df.drop(transposed_df.index[0], inplace=True)

## Use melt to reshape the DataFrame
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
print(new_df)

