import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def print_pause(string):
    print(string)
    time.sleep(1)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('-'*40)
    print('\nHello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington)
    while True:
        city = input('Please choose which city you want to explore [Chicago, New York City, Washington]: ').lower()

        # check if user entered a valid input. if not, propmpt again
        if city in ['chicago', 'new york city', 'washington']:
            break
        else: 
            print('\nPlease enter a proper input')

    # get the user input for month (all, january, february, ... , june)
    while True:
        month = input('Please choose which month you want [Jan, Feb, Mar, Apr, May, June] or "all": ').lower()

        # check if user entered a valid input. if not, propmpt again
        if month in ['jan', 'feb', 'mar', 'apr', 'may', 'june', 'all']:
            break
        else:
            print('\nPlease enter a proper input')

    # get user input for day of week (all, monday tuesday, ... , sunday)
    while True:
        day = input('Please choose which day you want [Mon, Tu, Wed, Th, Fri, Sat, Sun] or "all": ').lower()

        # check if user entered a valid input. if not, propmpt again
        if day in ['mon', 'tu', 'wed', 'th', 'fri', 'sat', 'sun', 'all']:
            break
        else:
            print('\nPlease enter a proper input')

    print('-'*40)

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data files into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # converting Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        month = ['jan', 'feb', 'mar', 'apr', 'may', 'june'].index(month) + 1

        # filter by month to create the new DataFrame
        df = df[df['month'] == month]

    # filter by day if applicable
    if day != 'all':
        day = ['mon', 'tu', 'wed', 'th', 'fri', 'sat', 'sun'].index(day)

        # filter by day if week to create the new DataFrame
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n\n')
    start_time = time.time()

    # most common month
    popular_month = df['month'].mode()[0]

    months = ['January', 'February', 'March', 'April', 'May', 'June'] # listing the months to print them
    print(f'The most popular month is: {months[popular_month - 1]}')

    # most common day of week
    popular_day = df['day_of_week'].mode()[0]

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'] # listing the days to print them
    print(f'The most popular day is: {days[popular_day]}')

    # most common start hour
    df['hour'] = df['Start Time'].dt.hour # exttact hour from Start Time
    popular_hour = df['hour'].mode()[0]

    # setting time to be in am/pm format
    if popular_hour == 12:
        print(f'The most popular hour is: {popular_hour}pm')
    elif popular_hour == 24 or popular_hour == 0:
        print('The most popular hour is: 12am')
    elif popular_hour > 12:
        print(f'The most popular hour is: {popular_hour - 12}pm')
    else:
        print(f'The most popular hour is: {popular_hour}am')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n\n')
    start_time = time.time()

    # most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print(f'The most popular start station is: {popular_start_station}')

    # most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print(f'The most popular end station is: {popular_end_station}')

    # most frequent combination of start station and end station trip
    stations = df['Start Station'].value_counts().keys() # list Start Stations to iterate over them later

    start_stations_counts = df['Start Station'].value_counts() # value counts of Start Stations
    end_stations_counts = df['End Station'].value_counts() # value counts of End Stations

    popular_station = '' # this is the most frequent station
    count = 0 # number of frequencies of most frequent station

    # iterating over stations and summing frequencies in Start Station + in End Station
    for n in stations:
        add = 0 # temp 

        # make sure the station is in both start_stations_counts and end_stations_counts else go to next iteration
        if n in start_stations_counts and n in end_stations_counts: 
            add = start_stations_counts[n] + end_stations_counts[n]
        else:
            continue

        if add > count:
            count = add
            popular_station = n
    
    print(f'The most popular station is: {popular_station}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n\n')
    start_time = time.time()

    # total travel time (in seconds)
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is:')
    print(f'{total_travel_time} seconds')
    print(f'{round(total_travel_time / 60, 2)} minuts')
    print(f'{round(total_travel_time / (60*60), 2)} hours')
    print(f'{round(total_travel_time / (60*60*24), 2)} days')

    # mean travel time (in seconds)
    mean_travel_time = df['Trip Duration'].mean()
    print('\nMean travel time is:')
    print(f'{round(mean_travel_time, 2)} seconds')
    print(f'{round(mean_travel_time / 60, 2)} minuts')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n\n')
    start_time = time.time()

    # counts of user types
    counts_user_types = df['User Type'].value_counts()

    print('Number of users for each user type,')
    for key, value in counts_user_types.items():
        print(f'{key} type: {value} users')

    # counts of gender
    # check if Gender column exists or not
    if 'Gender' in df:
        counts_gender = df['Gender'].value_counts()

        print('\nNumber of males and females,')
        for key, value in counts_gender.items():
            print(f'number of {key.lower()}s is: {value}')
    else:
        print('\nThis city does not have gender stats')
    
    # earliest, most recent, most common year of birth
        # check if Birth Year column exists or not
    if 'Birth Year' in df:
        earliest_birth_year = int(df['Birth Year'].value_counts().keys().min())
        most_recent_birth_year = int(df['Birth Year'].value_counts().keys().max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])

        print(f'\nThe earliest year of birth is: {earliest_birth_year}')
        print(f'The most recent year of birth is: {most_recent_birth_year}')
        print(f'The most common year of birth is: {most_common_birth_year}')
    else:
        print('\nThis city does not have birth year stats')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    view_data = input('\nWould you like to see individual trip data? [Yes/Y, No/N]: ').lower()

    count = 0
    start = 0

    while count < df.shape[0]:
        if view_data == 'yes' or view_data == 'y':
            print('-'*40)
            start = count
            count += 5

            for n in range(start ,count):
                print(df.iloc[n])
                print('\n')
            
            view_data = input('Would you like to continue? [Yes/Y, No/N]: ').lower()
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
        display_data(df)

        restart = input('\nWould you like to restart? [Yes/Y, No/N]: ').lower()
        if restart == 'yes' or restart == 'y':
            continue
        else:
            break


if __name__ == "__main__":
	main()
