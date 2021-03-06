#import logging
import analytics
import faker
import random
import time
import uuid

fake = faker.Faker()

age_multipliers = [0.0, 0.0, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]

analytics.write_key = "73lfhw3EjbBPKUKF6YrNjUQwSDNgMGAs"

#logging.basicConfig()
#analytics.debug = False

user_lookup = {}

class User():
    def __init__(self):
        """Generate this user's properties and sign it up to Segment."""
        self.name = fake.name()
        self.id = str(uuid.uuid4())
        
        # The tens digit of the user's age
        self.age_bracket = random.randint(2, 7)
        # Max number of consecutive days that user will stay before leaving
        self.perferred_stay = [1, 2, 5, 7][random.randint(0,3)]

        # A multiplier to enthusiasm losses to bad weather
        self.weather_tolerance = random.random() * self.age_bracket
        self.satisfaction = random.random()
        
        self.reservation_length = self.perferred_stay
        analytics.identify(self.id, {'name': self.name}) 
        
    def stay_a_day(self,the_date, day):
        """Generate a Segment call's worth of data and perform internal upkeep
        for buying a single ticket."""
        self.reservation_length -= 1
        enthusiasm = 1.0
        if "Hail" in day.events:
            enthusiasm -= 0.5*age_multipliers[self.age_bracket]
        elif "Thunderstorm" in day.events:
            enthusiasm -= 0.4*age_multipliers[self.age_bracket]
        else:
            if "Rain" in day.events:
                enthusiasm -= 0.2*age_multipliers[self.age_bracket]            
            if "Fog" in day.events:
                enthusiasm -= 0.1*age_multipliers[self.age_bracket]
            if "Snow" in day.events:
                enthusiasm += 0.5
        if day.max_temp >= 40:
           enthusiasm = enthusiasm/4.0
        elif day.max_temp >= 32:
            enthusiasm = enthusiasm/2.0
        time.sleep(.02)
        analytics.track(self.id, "used-pass", {"date": str(the_date),
                                               "hours-spent": 8.0*enthusiasm,
                                                "price": day.ticket_price, 
                                                "enthusiasm": enthusiasm,
                                                "weather": day.events.split('-'),
                                                "cloud_cover": day.cloud_cover})
        return True
    
    def leaving(self):
        """Return whether this user wants to stay the next day."""
        return self.reservation_length == 0
    
    def leave_early(self):
        """Perform internal upkeep when the user leaves earlier than planned -
        decreased satisfaction makes them less likely to attend in the future.
        """
        self.satisfaction *= 0.7 # This is arbitrary subject to tweaking
        
    def book_stay(self):
        """Set the number of days until leaving equal to the number of days this
        user would prefer to stay"""
        self.reservation_length = self.perferred_stay