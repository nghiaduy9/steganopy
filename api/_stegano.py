from io import BytesIO
from PIL import Image
import struct

import numpy as np


MAX_LSB = 2  # use up to 2 LSBs per channel per pixel


class SteganopyException(Exception):
    pass


def hide(img_buffer: bytes, payload_buffer: bytes) -> bytes:
    """Embed a payload into an image, and return the output image."""

    img = Image.open(BytesIO(img_buffer))
    width, height = img.size

    if not _validate_payload_size(width, height, len(payload_buffer)):
        raise SteganopyException("Cannot process. The payload is too large.")

    # the output image will be encoded as PNG in the end
    img = img.convert("RGBA")
    img_arr = np.array(img)
    payload_bits = _decompose(payload_buffer)

    i = 0  # index of the payload bits
    for nth, y, x in np.ndindex(MAX_LSB, height, width):
        if i >= len(payload_bits):
            break
        r, g, b, a = img_arr[y, x]
        r = _set_bit(r, payload_bits[i], nth)
        g = _set_bit(g, payload_bits[i + 1], nth)
        b = _set_bit(b, payload_bits[i + 2], nth)
        img_arr[y, x] = r, g, b, a
        i += 3
    output_img = Image.fromarray(img_arr)
    output_buffer = BytesIO()
    output_img.save(output_buffer, format="PNG")
    return output_buffer.getvalue()


def reveal(img_buffer: bytes) -> bytes:
    img = Image.open(BytesIO(img_buffer))
    width, height = img.size
    img = img.convert("RGBA")
    img_arr = np.asarray(img)
    payload_bits = np.empty(MAX_LSB * 3 * width * height, np.uint8)

    i = 0  # index of the payload bits
    for nth, y, x in np.ndindex(MAX_LSB, height, width):
        r, g, b, _ = img_arr[y, x]
        payload_bits[i] = _get_bit(r, nth)
        payload_bits[i + 1] = _get_bit(g, nth)
        payload_bits[i + 2] = _get_bit(b, nth)
        i += 3
    return _assemble(payload_bits)


def analyse(img_buffer: bytes):
    pass


def _validate_payload_size(img_w: int, img_h: int, payload_size: int) -> bool:
    """Return True if the payload is small enough, relative to the cover image."""

    # hide data in 3 channels
    max_size = MAX_LSB / 8 * (3 * (img_w * img_h))  # bytes
    return payload_size <= max_size - 4  # need 4 bytes to store the payload size


def _decompose(data: bytes) -> list:
    """Decompose data to a list of bits, with the first 4 bytes is the length of the data."""

    size = len(data)  # bytes
    byte_arr = np.empty(4 + size, np.uint8)
    byte_arr[:4] = tuple(struct.pack("i", size))
    byte_arr[4:] = tuple(data)

    bit_arr = np.unpackbits(byte_arr)
    r = len(bit_arr) % 3
    if not r:
        return bit_arr
    return np.concatenate((bit_arr, np.zeros(3 - r, np.uint8)))


def _assemble(data: list) -> bytes:
    byte_arr = np.packbits(data)
    size = struct.unpack("i", byte_arr[:4])[0]
    return byte_arr[4 : size + 4].tobytes()


def _set_bit(color: int, bit: int, nth: int = 0):
    """Set the n-th bit of a color and return the masked one."""

    mask = 1 << nth
    color &= ~mask
    if bit:
        color |= mask
    return color


def _get_bit(color: int, nth: int = 0) -> int:
    """Get the n-th bit of a color."""

    mask = 1 << nth
    return (color & mask) >> nth
