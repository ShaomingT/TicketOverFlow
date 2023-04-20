class Ticket:
    def __init__(self, id, user_id, title, description, status="open"):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.status = status
        self.user = None

    def to_dict(self):
        result = {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
        }
        if self.user:
            result["user"] = self.user
        return result
