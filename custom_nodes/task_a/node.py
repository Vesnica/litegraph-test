class TaskAClass:
    def __init__(self):
        pass
    
    def execute(self):
        return f"{self.__class__} did something!"

class TaskAInnerClass:
    def __init__(self):
        pass
    
    def execute(self):
        return f"{self.__class__} did something!"