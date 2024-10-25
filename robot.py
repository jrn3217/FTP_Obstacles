


class Robot:
    def __init__(self, _id, initial_position) -> None:
        self.id = _id
        self.target = None
        self.targeted_by = None
        self.path  = []
        self.history = [initial_position]

    def __repr__(self):
        return f"Robot-{self.id} (position={self.history[-1]}, target={self.target}, targeted_by={self.targeted_by})"
    
    def move(self):
        self.history.append(self.path.pop(0))
    
    def get_position(self):
        return self.history[-1]
    
    def add_targeted_by(self, robot):
        if self.targeted_by == None:
            self.targeted_by = [robot]
        else:
            self.targeted_by.append(robot)

    def is_goal(self):
        return len(self.path) <= 0

    