from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.model.Screen import Screen
    from src.levels.Level import Level
class Game: 
    def __init__(self):
        self.services = dict()
        self.entities = dict()
        self.layout = dict()
        self.parameters = dict()
        self.level: Level = None
        self.mainScreen: Screen = None