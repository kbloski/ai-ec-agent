class ExperimentCreateDto:
    def __init__(self, count: int):
        self.count = count

    def to_content_dict(self):
        return {"count": self.count}
