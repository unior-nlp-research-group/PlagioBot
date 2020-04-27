import key
from utility import escape_markdown

import json
import logging

from dataclasses import dataclass, field
from typing import List, Dict, Any

from firestore_model import Model


@dataclass
class Example(Model):
    name: str
    author: str
    year: int


    @staticmethod
    def create_example(name, author, year):
        answer = Example.make(
            name = name,
            author = author,
            year = year,
            save = True
        )
        return answer


if __name__ == "__main__":
    Example.create_example('name','author',1672)
    