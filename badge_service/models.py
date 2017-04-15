from enum import Enum, auto


class CrewBadgeInfo:
    def __init__(self, json=None, wannabe_json=None):
        if (json and wannabe_json) or (not json and not wannabe_json):
            raise Exception('Must have exactly one argument')
        if json:
            self.id = json['id']
            self.name = json['name']
            self.nick = json['nick']
            self.position = json['position']
            self.crew = json['crew']
        else:
            self.id = wannabe_json['id']
            self.name = wannabe_json['realname']
            self.nick = wannabe_json['nickname']
            self.position = wannabe_json['crews']['crew'][0]['usertitle']
            self.crew = wannabe_json['crews']['crew'][0]['name']


class BadgeType(Enum):
    Crew = auto()
    Blank = auto()
    Invitation = auto()
