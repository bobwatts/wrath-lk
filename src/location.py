class Location:
    def __init__(self, name, region, neighbors):
        self.name = name
        self.region = region
        self.neighbors = neighbors
        self.quest = None
        self.contents = []

    def get_location_info(self):
        return f"{self.name} in {self.region} has neighbors: {', '.join(self.neighbors)} and a quest: {self.quest}"

    def __str__(self):
        return f"Location: {self.name}\nRegion: {self.region}\nNeighbors: {', '.join(self.neighbors)}\nQuest: {self.quest}\nContents: {self.contents}"
