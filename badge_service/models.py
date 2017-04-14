from enum import Enum, auto


class CrewBadgeInfo:
    def __init__(self, info_json):
        self.id = info_json['id']
        self.name = info_json['name']
        self.nick = info_json['nick']
        self.position = info_json['position']
        self.crew = info_json['crew']


class BadgeType(Enum):
    Crew = auto()
    Blank = auto()
    Invitation = auto()
