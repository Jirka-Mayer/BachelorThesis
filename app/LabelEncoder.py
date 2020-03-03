from typing import List
from app.Symbol import Symbol
from app.Channel import Channel
from app.Label import Label
from app.EncodedLabel import EncodedLabel
import tensorflow as tf


class LabelEncoder:
    """
    Encodes/decodes labels to/from integer list representation
    NOTE: blank is encoded as "num_classes - 1" in my version
    of tensorflow 1.12.0, however the new version uses 0
    """

    if tf.__version__ != "1.12.0":
        raise Exception("Make sure you know, how your blank is encoded!")

    @staticmethod
    def encode_label(label: Label) -> EncodedLabel:
        """Turns a label into an encoded label"""
        out = EncodedLabel()

        # encode note channels
        for name in Channel.VOICE_CHANNEL_NAMES:
            out.set_channel(
                name,
                LabelEncoder._encode_note_channel(
                    label.get_channel(name)
                )
            )

        return out

    @staticmethod
    def decode_label(encoded_label: EncodedLabel) -> Label:
        """Turns an encoded label into a label"""
        out = Label()

        # decode note channels
        for name in Channel.VOICE_CHANNEL_NAMES:
            out.set_channel(
                name,
                LabelEncoder._decode_note_channel(
                    encoded_label.get_channel(name)
                )
            )

        return out

    @staticmethod
    def _encode_note_channel(channel: List[Symbol]) -> List[int]:
        return [
            LabelEncoder._encode_note_symbol(symbol)
            for symbol in channel
        ]

    @staticmethod
    def _decode_note_channel(encoded_channel: List[int]) -> List[Symbol]:
        return [
            LabelEncoder._decode_note_symbol(integer)
            for integer in encoded_channel
        ]

    @staticmethod
    def _encode_note_symbol(symbol: Symbol) -> int:
        for i in range(Channel.VOICE_CHANNEL_SYMBOL_COUNT):
            if Channel.VOICE_CHANNEL_SYMBOLS[i].name == symbol.name:
                return i
        raise Exception("Symbol %s couldn't be encoded" % (symbol,))

    @staticmethod
    def _decode_note_symbol(integer: int) -> Symbol:
        return Channel.VOICE_CHANNEL_SYMBOLS[integer]
