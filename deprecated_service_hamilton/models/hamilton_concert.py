class HamiltonTiccket:
    def __init__(self, id, name, date, venue, seats):
        self.id = id
        self.name = name
        self.date = date
        self.venue = venue
        self.seats = seats

    def to_dict(self):
        result = {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "venue": self.venue,
            "seats": self.seats
        }
        return result