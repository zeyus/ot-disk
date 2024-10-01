from sqlalchemy.ext.declarative import DeclarativeMeta  # type: ignore
from otree.api import (  # type: ignore
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    models,
    Page,
    ExtraModel,
    widgets,
)
from otree.models import Participant  # type: ignore
from random import shuffle, randint
import json
import datetime
from typing import Generator, Any
from pathlib import Path
import csv

doc = """
Disk study
"""


class AnnotationFreeMeta(DeclarativeMeta):
    """Metaclass to remove the __annotations__ attribute from the class
    this fixes an error where oTree tries to use __annotations__ and thinks it's a dict
    that needs saving.
    """

    def __new__(cls, name, bases, dct):
        dct.pop("__annotations__", None)
        return super().__new__(cls, name, bases, dct)


class C(BaseConstants):
    NAME_IN_URL: str = "disks"
    PLAYERS_PER_GROUP: int | None = None
    NUM_ROUNDS: int = 5
    STIM_PATH: Path = Path(__file__).parent / "static/stim"
    STIM_CSV: Path = Path(__file__).parent / "_private/stim.csv"


def get_stim_list() -> dict[str, dict[str, str]]:
    stim_list = {}
    with open(C.STIM_CSV) as f:
        reader = csv.DictReader(f)
        for row in reader:
            stim_list[row["id"]] = row
    return stim_list
            

class Subsession(BaseSubsession, metaclass=AnnotationFreeMeta):
    pass


def creating_session(subsession: Subsession) -> None:
    # read the CSV file
    stim_list = get_stim_list()
    stim_ids = list(stim_list.keys())
    for player in subsession.get_players():
        # shuffle the list
        shuffle(stim_ids)
        # assign the shuffled list to the player
        player.stim_order = json.dumps(stim_ids)




class Group(BaseGroup, metaclass=AnnotationFreeMeta):
    pass


class Player(BasePlayer, metaclass=AnnotationFreeMeta):
    stim_order: str = models.LongStringField(initial="")



# PAGES
class WelcomePage(Page):
    @staticmethod
    # only display this page on the first round
    def is_displayed(player: Player):
        return player.round_number == 1


class DiskTrialPage(Page):
    pass


class ThankYouPage(Page):
    @staticmethod
    # only display this page on the last round
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [WelcomePage, DiskTrialPage, ThankYouPage]
