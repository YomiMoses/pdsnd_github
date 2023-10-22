#import packages
import time
import pandas as pd
import numpy as np


# Load the dataset by global variable
CITY_DATA = {'ch': 'chicago.csv',
             'ny': 'new_york_city.csv',
             'w': 'washington.csv'}


def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # 1- check for input validation for city
    # ask the user to input city (chicago (ch), new york city (ny), washington(w)
    while True:
        city = input(
            "Please, pick a city to analyze: (ch) for Chicago, (ny) for New York City, or (w) for Washington: \n").lower()
        if city in CITY_DATA.keys():
            break
        else:
            print("Oops!! Invalid Input...")

    # 2- ask the user to input month (jan, feb, ..., jun, all)
    # check for input validation for month
    months = ["jan", "feb", "mar", "apr", "may", "jun", "all"]
    while True:
        month = input(
            "Please, pick a month (jan, feb, mar, apr, may, jun) to filter or type (all) for no filtering: \n").lower()
        if month in months:
            break
        else:
            print("Oops!! Invalid Input...")

    # 3- ask the user to input the day of the week (sat, sun, mon, ..., fri, all)
    # check for input validation
    days = ["sat", "sun", "mon", "tus", "wen", "thu", "fri", "all"]
    while True:
        day = input(
            "Please, pick a day of the week (sat, sun, mon, tus, wen, thu, fri) to filter or (all) for no filtering: \n").lower()
        if day in days:
            break
        else:
            print("Oops!! Invalid Input...")

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # data file as a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # converting (Start Time) column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'].str.startswith(month.title())]

    # filter by day of the week if applicable
    if day != 'all':
        # filter by day of the week to create the new dataframe
        df = df[df['day_of_week'].str.startswith(day.title())]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most frequent month
    df['month'] = df['Start Time'].dt.month_name()
    most_common_month = df['month'].mode()[0]
    print("Most common month is ", most_common_month)

    # display the most common day of the week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    most_common_day = df['day_of_week'].mode()[0]
    print('The most common day is ', most_common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common hour is ', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trips."""

    print('\nCalculating The Most Popular Stations and Trips...\n')
    start_time = time.time()

    # display the most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print('The most commonly used start station is', most_common_start)

    # display the most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print('The most commonly used end station is', most_common_end)

    # display the most frequent combination of start station and end station trip
    common_trip = 'from ' + df['Start Station'] + " to " + df['End Station'].mode()[0]
    print('Most frequent combination of start station and end station trip', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print('Total travel time is', total_trip_duration)
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time is', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_frame()
    print('Here are user types:\n', user_types)

    # Display counts of gender and birth year statistics
    try:
        print("Gender distribution:\n", df['Gender'].value_counts())
        print('Birth Year statistics:')
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])

        print('Earliest year of birth:', earliest_birth_year)
        print('Most recent year of birth:', most_recent_birth_year)
        print('Most common year of birth:', most_common_birth_year)

    except KeyError:
        print('No gender and birth year data available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


# Asking if the user wants to see more raw data
def ask_more_data(df):
    start_loc = 0
    while True:
        more_data = input("Would you like to view 5 rows of raw data? Enter yes or no: ").lower()
        if more_data == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            if start_loc >= len(df):
                print("\nNo more data to display.")
                break
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Display raw data upon user request
        ask_more_data(df)

        restart = input('\nWould you like to restart? Enter yes or no: ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()


