from . import db


class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.String, primary_key=True)
    concert_id = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, nullable=False)
    print_status = db.Column(db.String, nullable=False)
    svg = db.Column(db.String, nullable=True)


    def to_dict(self):
        return {
            "id": self.id,
            "concert": self.concert.to_dict(),
            "user": self.user_id,
            "print_status": self.print_status,
            "svg": self.svg if self.svg else None,
        }
