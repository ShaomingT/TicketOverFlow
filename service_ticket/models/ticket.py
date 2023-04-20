class Ticket:
    def __init__(self, id, concert, user, print_status):
        self.id = id
        self.concert =concert
        self.user = user
        self.print_status = print_status

    def to_dict(self):
        result = {
            "id": self.id,
            "concert": self.concert,
            "user": self.user,
            "print_status": self.print_status
        }
        return result
