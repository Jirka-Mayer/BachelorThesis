from typing import Dict, List
from app.Label import Label


class EncodedLabel:
    def __init__(self):
        # all encoded channels
        self._channels: Dict[any, List[int]] = {}
        Label._create_empty_channels(self)

    def get_channel(self, name) -> List[int]:
        """Returns the value of an encoded channel"""
        return self._channels[name]

    def set_channel(self, name, value: List[int]):
        """Sets the value of an encoded channel"""
        self._channels[name] = value
