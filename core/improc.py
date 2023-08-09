import io
import logging
from PIL import Image
import cv2
import numpy
from matplotlib import pyplot


RESCALE_SIZE = (640, 360)
HIST_CHANNELS = (0, 1)
HIST_BINS = (180, 256)
HIST_RANGE = (0, 180, 0, 256)
ROUND_PRECISION = 3
THRESHOLD = 99.5


class ImageProcessing:
    source = None
    target = None

    def load_source_from_file(self, fname: str) -> None:
        """Load source image from file.

        :param fname: filename
        :type fname: str
        """
        self.source = cv2.imread(fname)

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

    def compare_images(self) -> bool:
        """Compare source and target images using Hue-Saturation histograms.

        :return: True if result more or equal predefined THRESHOLD, else False
        """
        source_r = cv2.resize(self.source, RESCALE_SIZE,
                              interpolation=cv2.INTER_LINEAR)
        target_r = cv2.resize(numpy.array(self.target), RESCALE_SIZE,
                              interpolation=cv2.INTER_LINEAR)

        source_hsv = cv2.cvtColor(source_r, cv2.COLOR_BGR2HSV)
        target_hsv = cv2.cvtColor(target_r, cv2.COLOR_RGB2HSV)

        source_hist = cv2.calcHist(
            [source_hsv], HIST_CHANNELS, None, HIST_BINS, HIST_RANGE,
            accumulate=False
        )
        cv2.normalize(source_hist, source_hist, alpha=0, beta=1,
                      norm_type=cv2.NORM_MINMAX)
        target_hist = cv2.calcHist(
            [target_hsv], HIST_CHANNELS, None, HIST_BINS, HIST_RANGE,
            accumulate=False
        )
        cv2.normalize(target_hist, target_hist, alpha=0, beta=1,
                      norm_type=cv2.NORM_MINMAX)

        result = round(
            cv2.compareHist(source_hist, target_hist, cv2.HISTCMP_CORREL)*100,
            ROUND_PRECISION
        )
        logging.debug(f'Compare result = {result}')
        if result >= THRESHOLD:
            return True
        else:
            return False


def draw_hist_rgb(image, normalize=False, bins=(256,), ranges=(0, 256)):
    """Draw BGR histogram of (JPEG) image.

    :param image: source image
    :type image: str (filename) or numpy array (already loaded image)

    :param normalize: use normalization
    :type normalize: bool

    :param bins: number of bins
    :param ranges: tuple with ranges

    https://docs.opencv.org/4.8.0/d1/db7/tutorial_py_histogram_begins.html
    """
    if type(image) == str:
        img = cv2.imread(image)
    else:
        img = image

    for i, color in enumerate(('b', 'g', 'r')):
        hist = cv2.calcHist((img,), (i,), None, bins, ranges, accumulate=False)
        if normalize:
            cv2.normalize(hist, hist, alpha=0, beta=1,
                          norm_type=cv2.NORM_MINMAX)

        pyplot.plot(hist, color=color)
        pyplot.grid(True)
        pyplot.title('Blue-Green-Red Histogram')
        pyplot.xlabel('Bins')
        pyplot.ylabel('Pixels')
        pyplot.xlim((0, 256))
    pyplot.show()


def draw_hist_hsv(image, normalize=False,
                  bins=(180, 256), ranges=(0, 180, 0, 256)):
    """Draw Hue-Saturation histogram of (JPEG) image.

    :param image: source image
    :type image: str (filename) or numpy array (already loaded and converted to
                 HSV-colorspace image)

    :param normalize: use normalization
    :type normalize: bool

    :param bins: number of bins
    :param ranges: tuple with ranges

    https://docs.opencv.org/4.8.0/d1/db7/tutorial_py_histogram_begins.html
    """
    if type(image) == str:
        i = cv2.imread(image)
        img = cv2.cvtColor(i, cv2.COLOR_BGR2HSV)
    else:
        img = image

    hist = cv2.calcHist((img,), (0, 1), None, bins, ranges, accumulate=False)
    if normalize:
        cv2.normalize(hist, hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

    plt = pyplot.imshow(hist, interpolation='nearest')
    pyplot.title('Hue-Saturation Histogram')
    pyplot.xlabel('Saturation')
    pyplot.ylabel('Hue')
    pyplot.colorbar(plt, extend='max')
    pyplot.show()
