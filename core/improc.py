import io
from PIL import Image


class ImageProcessing:
    target = None

    def load_target_from_bytes(self, raw: bytes) -> None:
        """Load target image from bytes.

        :param raw: array of bytes
        :type raw: bytes
        """
        stream = io.BytesIO(raw)
        self.target = Image.open(stream)

    def is_target_image(self) -> bool:
        """Check integrity of target image.

        :return: True if no problems found.
        """
        self.target.verify()
        return True
