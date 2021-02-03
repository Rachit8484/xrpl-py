"""Codec for serializing and deserializing vectors of Hash256."""
from __future__ import annotations

from typing import List, Optional

from typing_extensions import Final

from xrpl.binary_codec import XRPLBinaryCodecException
from xrpl.binary_codec.binary_wrappers.binary_parser import BinaryParser
from xrpl.binary_codec.types.hash256 import Hash256
from xrpl.binary_codec.types.serialized_type import SerializedType

_HASH_LENGTH_BYTES: Final = 32


class Vector256(SerializedType):
    """A vector of Hash256 objects."""

    def __init__(self: Vector256, buffer: bytes) -> None:
        """Construct a Vector256."""
        super().__init__(buffer)

    @classmethod
    def from_value(cls: Vector256, value: List[str]) -> Vector256:
        """Construct a Vector256 from a list of strings.

        Args:
            value: A list of hashes encoded as hex strings.

        Returns:
            A Vector256 object representing these hashes.
        """
        byte_list = []
        for string in value:
            byte_list.append(Hash256.from_value(string).to_bytes())
        return cls(b"".join(byte_list))

    @classmethod
    def from_parser(
        cls: Vector256, parser: BinaryParser, length_hint: Optional[int] = None
    ) -> SerializedType:
        """Construct a Vector256 from a BinaryParser.

        Args:
            parser: The parser to construct a Vector256 from.
            length_hint: The number of bytes to consume from the parser.

        Returns:
            A Vector256 object.
        """
        byte_list = []
        num_bytes = length_hint if length_hint is not None else len(parser)
        num_hashes = num_bytes // _HASH_LENGTH_BYTES
        for i in range(num_hashes):
            byte_list.append(Hash256.from_parser(parser).to_bytes())
        return cls(b"".join(byte_list))

    def to_json(self: Vector256) -> List[str]:
        """Return a list of hashes encoded as hex strings.

        Returns:
            The JSON representation of this Vector256.

        Raises:
            XRPLBinaryCodecException: If the number of bytes in the buffer
                                        is not a multiple of the hash length.
        """
        if len(self.buffer) % _HASH_LENGTH_BYTES != 0:
            raise XRPLBinaryCodecException("Invalid bytes for Vector256.")
        hash_list = []
        for i in range(0, len(self.buffer), _HASH_LENGTH_BYTES):
            hash_list.append(self.buffer[i : i + _HASH_LENGTH_BYTES].hex().upper())
        return hash_list