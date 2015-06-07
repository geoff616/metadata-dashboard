import random

class UserPool():
    """"A container for users so that they can be re-used."""
    def __init__(self, users):
        self.satisfaction = sum([user.satisfaction for user in users])
        self.users = {user.id: user for user in users}
            
    def get_user(self):
        """Remove and return a user chosen randomly with probability proportional
        to their satisfaction."""
        user_index = random.random() * self.satisfaction
        for user in self.users.itervalues():
            if user_index <= 0:
                self.satisfaction =- user.satisfaction
                del self.users[user.id]
                return user
            else:
                user_index -= user.satisfaction
                
    def put_user(self, user):
        """Return a user to the pool and keep self.satisfaction equal to the 
        sum of our users satisfaction."""
        self.satisfaction += user.satisfaction
        self.users[user.id] = user
