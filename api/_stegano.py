from io import BytesIO
from PIL import Image
import struct

import numpy as np


class SteganopyException(Exception):
    pass


def conceal(img_buffer: bytes, payload_buffer: bytes) -> bytes:
    """Embed data into an image, and return the output image."""

    img = Image.open(BytesIO(img_buffer))
    width, height = img.size

    if not _validate_payload_size(width, height, len(payload_buffer)):
        raise SteganopyException("Cannot process. The payload is too large.")

    img_arr = np.array(img.convert("RGBA"))

    payload_bits = _decompose(payload_buffer)
    bits_len = len(payload_bits)
    i = 0  # index of the payload bits
    for color in np.nditer(img_arr, op_flags=["readwrite"]):
        color[...] = _set_bit(color, payload_bits[i])
        i += 1
        if i >= bits_len:
            break
    output_img = Image.fromarray(img_arr)
    output_buffer = BytesIO()
    output_img.save(output_buffer, format="PNG")
    return output_buffer.getvalue()


def reveal(img_buffer: bytes) -> bytes:
    """Extract secret data from an image."""

    img = Image.open(BytesIO(img_buffer))
    img_arr = np.asarray(img.convert("RGBA")).ravel()

    payload_size_bits = np.empty(32, np.uint8)
    i = 0
    for color in np.nditer(img_arr[:32]):
        payload_size_bits[i] = _get_bit(color)
        i += 1
    payload_size = _assemble_int(payload_size_bits)  # bytes

    bits_len = payload_size * 8  # bits
    payload_bits = np.empty(bits_len, np.uint8)
    i = 0
    for color in np.nditer(img_arr[32:]):
        payload_bits[i] = _get_bit(color)
        i += 1
        if i >= bits_len:
            break
    return _assemble(payload_bits)


def _validate_payload_size(img_w: int, img_h: int, payload_size: int) -> bool:
    """Return True if the payload is small enough, relative to the cover image."""

    # conceal data in 4-channel pixels, 1 bit per channel
    max_size = img_w * img_h // 2  # bytes, (4 * img_w * img_h // 8) actually
    return payload_size <= max_size - 4  # need 4 bytes to store the payload size


def _decompose(data: bytes) -> list:
    """Decompose data to a list of bits, with the first 4 bytes is the length of the data."""

    size = len(data)  # bytes
    byte_arr = np.empty(4 + size, np.uint8)
    byte_arr[:4] = tuple(struct.pack("i", size))
    byte_arr[4:] = tuple(data)
    return np.unpackbits(byte_arr)


def _assemble_int(bit_arr: np.ndarray) -> int:
    """Assemble a list of 32 bits to a 4-byte integer."""

    assert len(bit_arr) == 32

    byte_arr = np.packbits(bit_arr)
    return struct.unpack("i", byte_arr)[0]


def _assemble(bit_arr: np.ndarray) -> bytes:
    """Assemble a list of bits to binary data."""

    byte_arr = np.packbits(bit_arr)
    return byte_arr.tobytes()


def _set_bit(color: np.ndarray, bit: int, nth: int = 0):
    """Set the n-th bit of a color and return the masked one."""

    mask = 1 << nth
    color = np.bitwise_and(color, ~mask)
    if bit:
        color = np.bitwise_or(color, mask)
    return color


def _get_bit(color: np.ndarray, nth: int = 0) -> int:
    """Get the n-th bit of a color."""

    mask = 1 << nth
    return (color & mask) >> nth
