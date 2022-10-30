import os
import dataclasses
import logging


@dataclasses.dataclass
class Config:
    log_level: str = os.getenv("LOG_LEVEL", "DEBUG")

    def validate(self):
        logging._checkLevel(self.log_level)


config = Config()
