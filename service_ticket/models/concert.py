from . import db


class Concert(db.Model):
    __tablename__ = "concerts"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    venue = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    svg = db.Column(db.String, nullable=True)
    svg_seat_num = db.Column(db.Integer, nullable=True)

    # Add the relationship to the Concert model
    # concert = db.relationship("Concert", backref="tickets")

    def to_dict(self, exclude_fields=[]):
        concert_dict = {
            "id": self.id,
            "name": self.name,
            "venue": self.venue,
            "date": self.date,
            "capacity": self.capacity,
            "status": self.status,
            "svg": self.svg if self.svg else None,
            "svg_seat_num": self.svg_seat_num if self.svg_seat_num else None,
        }

        for field in exclude_fields:
            if field in concert_dict:
                del concert_dict[field]

        return concert_dict
