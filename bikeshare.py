import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    
    city = ''
    while city not in CITY_DATA.keys():
        print('Please choose the city you would like to view data from. Chicago, New York City, or Washington?')
        city = input().lower()
    
        if city not in CITY_DATA.keys():
            print('Provided city is incorrect and not a valid selection...\n')
        
    MONTH_OPTIONS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = ''
    while month not in MONTH_OPTIONS:
        print('Please choose the month you would like to view data from. January, February, March, April, May, or June?')
        print('Or if you would like to view the data from all months please type: all')
        month = input().lower()
        
        if month not in MONTH_OPTIONS:
            print('Provided month is incorrect and not a valid selection...\n')

    DAY_OPTIONS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    day = ''
    while day not in DAY_OPTIONS:
        print('Please choose the day you would like to view data from. Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?')
        print('Or if you would like to view the data from all days please type: all')
        day = input().lower()
        
        if day not in DAY_OPTIONS:
            print('Provided day is incorrect and not a valid selection...\n')

    print('-'*60)
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
    
    print('...loading data...')
    print('-'*60)
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

                  
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['month'].mode()[0]
    print(f"Most common month (1 = January,...,6 = June): {most_common_month}")

    most_common_day = df['day_of_week'].mode()[0]
    print(f"\nMost common day: {most_common_day}")

    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print(f"\nMost common start hour: {most_common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {most_common_start_station}")

    most_common_end_station = df['End Station'].mode()[0]
    print(f"\nThe most commonly used end station is: {most_common_end_station}")

    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep = ' to ')
    combo = df['Start To End'].mode()[0]

    print(f"\nThe most frequent combination of trips are from {combo}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print(f"The total trip duration is {hour} hour(s), {minute} minute(s) and {second} second(s)")


    mean_duration = round(df['Trip Duration'].mean())
    mins, sec = divmod(mean_duration, 60)

    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"\nThe average trip duration is {hrs} hour(s), {mins} minute(s) and {sec} second(s)")
    else:
        print(f"\nThe average trip duration is {mins} minute(s) and {sec} second(s)")
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_type = df['User Type'].value_counts()
    print(f"The types of users by number are :\n{user_type}")

    try:
        gender = df['Gender'].value_counts()
        print(f"\nThe types of users by gender are:\n{gender}")
    except:
        print("\nThere is no gender data for this city")

    try:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth is: {earliest}\n\nThe most recent year of birth is: {most_recent}\n\nThe most common year of birth is: {most_common_year}")
    except:
        print("There is no birth year data for this city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def display_raw_data(df):
    """Displays 5 rows of raw data from the csv file for the selected city."""
    
    RESPONSE_OPTIONS = ['yes', 'no']
    raw_data = ''
    
    while raw_data not in RESPONSE_OPTIONS:
        print('Do you want to see raw data for this city? Please type yes or no')
        raw_data = input().lower()
        
        if raw_data == 'yes':
            print(df.head())
        elif raw_data not in RESPONSE_OPTIONS:
            print('Provided response is incorrect and not a valid selection...\n')
            
    iterator = 0
    while raw_data == 'yes':
        print('Would you like to see more raw data for this city? Please type yes or no')
        iterator += 5
        raw_data = input().lower()
        
        if raw_data == "yes":
             print(df[iterator:iterator+5])
        elif raw_data not in RESPONSE_OPTIONS:
            print('Provided response is incorrect and not a valid selection...\n')
        else:
             break
                
    print('-'*60)
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
