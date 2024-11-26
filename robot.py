


class Robot:
    def __init__(self, _id, initial_position) -> None:
        self.id = _id
        self.target = None
        self.targeted_by = None
        self.path  = []
        self.history = [initial_position]
        self.cluster = None

    def __repr__(self):
        return f"Robot-{self.id} (position={self.history[-1]}, target={self.target}, targeted_by={self.targeted_by})"
    
    def move(self):
        if len(self.path) > 0:
            self.history.append(self.path.pop(0))
    
    def get_position(self):
        return self.history[-1]
    
    def add_targeted_by(self, robot):
        if self.targeted_by == None:
            self.targeted_by = [robot]
        else:
            self.targeted_by.append(robot)

    def remove_targeted_by(self, robot):
        if self.targeted_by is not None and robot in self.targeted_by:
            self.targeted_by.remove(robot)
            if len(self.targeted_by) <= 0:
                self.targeted_by = None

    def is_goal(self):
        return len(self.path) <= 0
    
    def get_target_distance(self):
        if self.target is None:
            return None
        return len(self.path)

    