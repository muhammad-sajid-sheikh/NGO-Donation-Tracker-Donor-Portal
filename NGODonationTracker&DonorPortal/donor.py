class Donor:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def to_dict(self):
        return {
            "Name": self.name,
            "Email": self.email
        }
