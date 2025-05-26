from datetime import datetime

class Donation:
    def __init__(self, donor_email, amount, method):
        self.donor_email = donor_email
        self.amount = amount
        self.method = method
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "Donor Email": self.donor_email,
            "Amount": self.amount,
            "Method": self.method,
            "Date": self.date
        }
