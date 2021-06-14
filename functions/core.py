from django.http import HttpResponse
from django import urls

import pandas as pd
import matplotlib.pyplot as plot

def analysis(file):
    # CSV is read into a Pandas dataframe.
    #upload_df = pd.read_csv (r'.\input.csv')
    upload_df = pd.read_csv (file)

    # Find top value of cell A1
    title = (upload_df.columns.values[0])

    # Fill NaN with 0
    upload_df.fillna(0)

    # upload_df is melted from sales by month into category, date, and value columns.
    melted_df = pd.melt(upload_df, id_vars = upload_df.columns.values[0], value_vars = upload_df.columns.values[1:])

    # melted_df is sorted by category then date
    sorted_df = melted_df.sort_values(by = [melted_df.columns.values[1], melted_df.columns.values[0]])

    # sorted_df without the category and date columns
    values_df = sorted_df.select_dtypes('number')

    # values_df is run through a diff offset by the number of rows in the dataframe
    number_of_rows = len(upload_df.index)
    # The result is written into a new 'change' column in the sorted_df.
    sorted_df['change'] = values_df.diff(periods = number_of_rows)


    # Find the first and last non-zero values per category
    first_non_zero_days_df = sorted_df.loc[sorted_df['value'] != 0].groupby(title).first()
    last_non_zero_days_df = sorted_df.loc[sorted_df['value'] != 0].groupby(title).last()

    # Merge first and last date onto sorted_df
    first_merged_df = pd.merge(sorted_df, first_non_zero_days_df, on=[title], how='inner')
    first_merged_df.drop(first_merged_df.iloc[:, -2:], axis=1, inplace = True)
    second_merged_df = pd.merge(first_merged_df, last_non_zero_days_df, on=[title], how='inner')
    second_merged_df.drop(second_merged_df.iloc[:, -2:], axis=1, inplace = True)

    # Rename the resulting columns
    renamed_df = second_merged_df.rename({
        "variable_x":"period",
        "value_x":"value",
        "change_x":"change_from_previous_period",
        "variable_y":"first",
        "variable":"last",
    }, axis='columns') 

    # IF/ELSE statement to classify "first", "last" "increase", "decrease", or "no_change"
    def change_type(row):
        if row['first'] == row['period']:
            val = 'first'
        elif row['last'] == row['period']:
            val = 'last'
        elif row['change_from_previous_period'] > 0:
            val = 'increase'
        elif row['change_from_previous_period'] < 0:
            val = 'decrease'
        else:
            val = 'stable'
        return val

    # Applies change_type function to each row of 
    renamed_df['change_type'] = renamed_df.apply(change_type, axis = 1)

    final_df = renamed_df.groupby(['period', 'change_type']).sum()
    final_df.drop(final_df.iloc[:, -1:], axis=1, inplace = True)

    renamed_df.plot.bar(x="period", y="value", rot=70, title="Sales over Time")

    # plot.show(block=True)

    #print(renamed_df)
    #print(final_df)

    #output_file = renamed_df.to_csv('category.csv')

    #return output_file

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=category.csv'
    csv_file = renamed_df.to_csv(path_or_buf=response)
    return response
    #final_df.to_csv('total.csv')    

