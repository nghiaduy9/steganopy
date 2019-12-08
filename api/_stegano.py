from io import BytesIO
from PIL import Image
import struct


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
    payload_bits = _decompose(payload_buffer)

    i = 0  # index of the payload bits
    nth = 0
    while i < len(payload_bits):
        for y in range(height):
            for x in range(width):
                if i >= len(payload_bits):
                    output_buffer = BytesIO()
                    img.save(output_buffer, format="PNG")
                    return output_buffer.getvalue()

                r, g, b, a = img.getpixel((x, y))
                r = _set_bits(r, payload_bits[i], nth)
                g = _set_bits(g, payload_bits[i + 1], nth)
                b = _set_bits(b, payload_bits[i + 2], nth)
                img.putpixel((x, y), (r, g, b, a))
                i += 3
        nth += 1


def analyse(img_buffer: bytes):
    pass


def reveal(img_buffer: bytes):
    pass


def _validate_payload_size(img_w: int, img_h: int, payload_size: int) -> bool:
    """Return True if the payload is small enough, relative to the cover image."""

    # each pixel is 3 bytes long
    # use up to 3 LSBs
    max_size = 3 / 8 * (3 * (img_w * img_h))  # bytes
    return payload_size <= max_size - 4  # need 4 bytes to store the payload size


def _decompose(data: bytes) -> list:
    """Decompose data to a list of bits, with the first 4 bytes is the length of the data."""

    size = len(data)  # bytes

    byte_arr = []
    for b in struct.pack("i", size):
        byte_arr.append(b)
    for b in data:
        byte_arr.append(b)

    bit_arr = []
    for b in byte_arr:
        for i in range(7, -1, -1):
            bit_arr.append((b >> i) & 1)

    while len(bit_arr) % 3:
        bit_arr.append(0)

    return bit_arr


def _set_bits(color: int, bit: int, n: int = 0):
    """Set the n-th bit of a color and return the masked one."""

    mask = 1 << n
    color &= ~mask
    if bit:
        color |= mask
    return color
