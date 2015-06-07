import analytics
import csv
import datetime
from collections import namedtuple
import random

import fake_user
import user_pool

Day = namedtuple("Day", ["events", "max_temp", "passes", "ticket_price"])
# Divide the number of passes by this value (simulate is O(d*n**2) in the 
# number of days and size of the user pool, so this is handy
compression_factor = 10

def parse_days(data_csv):
    """Read in all the data that we need from a .csv file with a fixed column 
    format."""
    global_reader = csv.reader(open(data_csv,"rb"))
    days = {}
    for line in global_reader:
        # Discard the header lines, this is terrible code
        if line[0] not in "Datescalarmeanstd":
            days[datetime.datetime.strptime(line[0], '%m/%d/%Y').date()] = \
            Day(line[8], 
                int(line[9]), 
                int(line[28].replace(",",""))/compression_factor,
                float(line[31]))
    return days

def simulate(days, all_users):
    """Simulate our resort operating for each day of days, calling Segment once
    every time a user spends a day there."""
    users = []
    # An ugly artifact of earlier iterations of the data generation process
    # refactor if there's time
    for the_date, current_day in sorted(days.items(), key=lambda x: x[0]):
        temp_users = []
        for user in users:
            if not user.leaving():
                temp_users.append(user)
            else:
                all_users.put_user(user)
        users = temp_users
            
        # Bring in new users or have users cancel their stay, depending on
        # the number of passes used today
        l = len(users)
        passes = current_day.passes    
        if l > passes:
            random.shuffle(users)
            for user in users[passes:]:
                user.leave_early()
                all_users.put_user(user)
            for user in users[:passes]:
                user.stay_a_day(the_date, current_day)
            users = users[:passes]
        if l <= passes:
            while l < passes:
                next_client = all_users.get_user()
                next_client.book_stay()
                users.append(next_client)
                l += 1
            for user in users:
                user.stay_a_day(the_date, current_day)
                          
        
if __name__ == "__main__":
    analytics.write_key = "73lfhw3EjbBPKUKF6YrNjUQwSDNgMGAs"
    operating_days = parse_days("Number_of_Passes_sold_and_Total_Revenue.csv")
    # The number 10000 is MAGIC, and bad things will happen if we fiddle with
    # it with our current dataset size
    u = [fake_user.User() for i in range(10000/compression_factor)]
    potential_users = user_pool.UserPool(u)

    simulate(operating_days, potential_users)
    
            