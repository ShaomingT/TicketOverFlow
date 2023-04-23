from . import db


class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.String, primary_key=True)
    concert_id = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, nullable=False)
    print_status = db.Column(db.String, nullable=False)
    svg = db.Column(db.String, nullable=True)

    def to_dict(self, include_fields=[]):
        ticket_dict = {
            "id": self.id,
            "concert_id": self.concert_id,
            "user_id": self.user_id,
            "print_status": self.print_status,
            "svg": self.svg if self.svg else None,
        }

        # if include_fields is not empty, only return the fields in include_fields
        if include_fields:
            ticket_dict = {key: value for key, value in ticket_dict.items() if key in include_fields}

        return ticket_dict


