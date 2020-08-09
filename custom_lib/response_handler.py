import json

class Response():
    """ response handler """
    def __init__(self, data, status="ok"):
        self.status = status
        self.data = data

    def __str__(self):
        return self.json()

    def json(self):
        """
        returns json data
        """
        return json.dumps({
            "status": self.status,
            "data": self.data            
        }, indent=4)
