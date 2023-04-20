class Ticket:
    def __init__(self, id, concert_id, concert_url, user_id, user_url, print_status):
        self.id = id
        self.concert = {
            "id": concert_id,
            "url": concert_url,
        }
        self.user = {
            "id": user_id,
            "url": user_url
        }
        self.print_status = print_status

    def to_dict(self):
        result = {
            "id": self.id,
            "concert": self.concert,
            "user": self.user,
            "print_status": self.print_status
        }
        return result
