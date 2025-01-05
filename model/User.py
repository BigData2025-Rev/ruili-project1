class User:
    
    def __init__(self, userid, username, password, role):
        self.id = userid
        self.username = username
        self.password = password
        self.role = role
    
    # string format
    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, role={self.role})"
    
    def is_admin(self):
        return self.role == 'admin'
    
    # return the dict format of the object
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "role": self.role
        }
    
    # create a user object from the dict data
    def from_dict(user_data):
        return User(
            userid=user_data.get('id'),
            username=user_data.get('username'),
            password=user_data.get('password'),
            role=user_data.get('role')
        )