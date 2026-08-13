from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.model.Screen import Screen
    from src.levels.Level import Level
    from src.services.EnemyService import EnemyService
    from src.services.PlayerService import PlayerService
class Game: 
    FPS:int = 0
    def __init__(self):
        self.player_service: PlayerService = None
        self.enemy_service: EnemyService = None
        self.entities = dict()
        self.layout = dict()
        self.parameters = dict()
        self.level: Level = None
        self.mainScreen: Screen = None
        self.win = False