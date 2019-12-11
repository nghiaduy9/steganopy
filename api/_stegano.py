from io import BytesIO
from PIL import Image
import struct

import numpy as np


def conceal(img: Image, payload_buffer: bytes) -> bytes:
    """Embed data into an image, and return the output image."""

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


def reveal(img: Image) -> bytes:
    """Extract secret data from an image."""

    img_arr = np.asarray(img.convert("RGBA")).ravel()

    payload_size = _get_payload_size(img_arr)
    bits_len = payload_size * 8  # bits
    payload_bits = np.empty(bits_len, np.uint8)
    i = 0
    for color in np.nditer(img_arr[32:]):
        payload_bits[i] = _get_bit(color)
        i += 1
        if i >= bits_len:
            break
    return _assemble(payload_bits)


def detect(img: Image) -> bool:
    """Return False if this image cannot contain any secret data. Return True if it MAY contain."""

    img_arr = np.asarray(img.convert("RGBA")).ravel()
    payload_size = _get_payload_size(img_arr)
    return payload_size <= get_max_payload_size(img)


def validate_payload_size(img: Image, payload_buffer: bytes) -> bool:
    """Return True if the payload size is small enough, relative to the cover image."""

    max_payload_size = get_max_payload_size(img)
    payload_size = len(payload_buffer)
    return payload_size <= max_payload_size


def get_max_payload_size(img: Image) -> int:
    """Get the maximum payload size this image can conceal."""

    width, height = img.size
    # conceal data in 4-channel pixels, 1 bit per channel
    # and need another 4 bytes to store the payload size
    return (width * height // 2) - 4  # bytes, (4 * img_w * img_h // 8) - 4 actually


def _decompose(data: bytes) -> list:
    """Decompose data to a list of bits, with the first 4 bytes is the length of the data."""

    size = len(data)  # bytes
    byte_arr = np.empty(4 + size, np.uint8)
    byte_arr[:4] = tuple(struct.pack("i", size))
    byte_arr[4:] = tuple(data)
    return np.unpackbits(byte_arr)


def _get_payload_size(img_arr: np.ndarray) -> int:
    """Get the payload size this image may contain."""

    payload_size_bits = np.empty(32, np.uint8)
    i = 0
    for color in np.nditer(img_arr[:32]):
        payload_size_bits[i] = _get_bit(color)
        i += 1
    return _assemble_int(payload_size_bits)  # bytes


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
