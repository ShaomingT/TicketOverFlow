class HamiltonTicket:
    def __init__(self, id, name, email, concert, print_status):
        self.id = id
        self.name = name
        self.email = email
        self.concert = concert
    def to_dict(self):
        result = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "concert": self.concert,
        }
        return result