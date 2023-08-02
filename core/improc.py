import io
from PIL import Image


class ImageProcessing:
    source = None

    def load_from_bytes(self, raw: bytes) -> None:
        """Load image from bytes.

        :param raw: array of bytes
        :type raw: bytes
        """
        stream = io.BytesIO(raw)
        self.source = Image.open(stream)

    def is_source_image(self) -> bool:
        """Check integrity of source image.

        :return: True if no problems found.
        """
        self.source.verify()
        return True
