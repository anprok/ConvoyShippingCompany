class Person:

    def __init__(self, name, email):
        self.name = name
        self.email = email

    @classmethod
    def from_string(cls, data):
        name, surname = data.split('-')
        return cls(name, surname)