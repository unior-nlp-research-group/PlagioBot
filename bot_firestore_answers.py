import key
from utility import escape_markdown

import json
import logging

from dataclasses import dataclass, field
from typing import List, Dict, Any

from firestore_model import Model


@dataclass
class Answers(Model):
    language: str
    game_type: str
    incomplete_part: str
    answer: str
    author: str
    observed: int
    selected: int



    @staticmethod
    def create_user(application, serial_id, name, username, bot=False):
        answer = Answer.make(
            save = True
        )
        return answer


if __name__ == "__main__":
    pass
    