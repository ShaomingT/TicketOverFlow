class Concert:
    def __init__(self, id, name, venue, date, capacity, status):
        self.id = id
        self.name = name
        self.venue = venue
        self.date = date
        self.capacity = capacity
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "venue": self.venue,
            "date": self.date,
            "capacity": self.capacity,
            "status": self.status,
        }
