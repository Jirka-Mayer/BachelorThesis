import numpy as np
import cv2
import math
from typing import List


def get_staff_images_from_sheet_image(sheet_image: np.ndarray, dilate=False) -> List[np.ndarray]:
    """Breaks a sheet image up into individual staff images"""

    # by how many pixels should a line bounding box grow vertically
    # (in order for boxes to start overlapping within one staff)
    LINE_BOUNDING_BOX_GROW = 20

    # lines above this angle will no longer be considered horizontal
    # and will be ignored
    LINE_ANGLE_THRESHOLD = 0.02

    # how much space to leave on the sides
    HORIZONTAL_PADDING_IN_STAFF_HEIGHTS = 0.5

    # how much space to leave above and below
    VERTICAL_PADDING_IN_STAFF_HEIGHTS = 1

    # print debugging image
    DEBUG = False

    # dilate horizontally
    if dilate:
        dilatation_size_x, dilatation_size_y = 10, 1
        element = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE,
            (2 * dilatation_size_x + 1, 2 * dilatation_size_y + 1),
            (dilatation_size_x, dilatation_size_y)
        )
        dilated_sheet_image = cv2.dilate(sheet_image, element)

    # this image will contain debugging information
    debug_image = None
    if DEBUG:
        debug_image = cv2.cvtColor(
            dilated_sheet_image if dilate else sheet_image,
            cv2.COLOR_GRAY2BGR
        )

    # detected lines
    lines = cv2.HoughLinesP(
        dilated_sheet_image if dilate else sheet_image,
        1,  # spatial resolution
        np.pi / 180,  # angular resolution
        threshold=800,
        minLineLength=1000,
        maxLineGap=100
    )

    # this image will contain blobs where staves are
    blob_img = np.zeros(shape=sheet_image.shape, dtype=sheet_image.dtype)

    # create the blob image
    if lines is not None:
        for i in range(0, len(lines)):
            l = lines[i][0]
            angle = abs(math.atan2(abs(l[1] - l[3]), abs(l[0] - l[2])))

            if DEBUG:
                cv2.line(
                    debug_image,
                    (l[0], l[1]),
                    (l[2], l[3]),
                    (255, 0, 0) if angle <= LINE_ANGLE_THRESHOLD else (0, 0, 255),
                    3,
                    cv2.LINE_AA
                )

            if angle > LINE_ANGLE_THRESHOLD:
                continue

            top = min(l[1], l[3])
            bottom = max(l[1], l[3])
            left = min(l[0], l[2])
            right = max(l[0], l[2])
            top -= LINE_BOUNDING_BOX_GROW
            bottom += LINE_BOUNDING_BOX_GROW

            cv2.rectangle(
                blob_img,
                (left, top),
                (right, bottom),
                color=255,
                thickness=-1  # fill
            )

    # extract staff bounding boxes from blob image
    staff_boxes = []
    ret, labels = cv2.connectedComponents(blob_img)
    for i in range(1, ret):
        mask = (labels == i).astype(np.uint8)
        x, y, w, h = cv2.boundingRect(cv2.findNonZero(mask))

        y += LINE_BOUNDING_BOX_GROW
        h -= LINE_BOUNDING_BOX_GROW * 2

        # filter out too thin boxes
        # (sometimes a long line is detected as a staff)
        if h < LINE_BOUNDING_BOX_GROW * 2:  # magic constant
            continue

        staff_boxes.append((x, y, w, h))

    # sort staff bounding boxes from top to bottom
    staff_boxes.sort(key=lambda b: b[1])

    # print staff boxes into the debug image
    if DEBUG:
        for x, y, w, h in staff_boxes:
            cv2.rectangle(
                debug_image,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                thickness=3
            )

    # show the debugging image
    if DEBUG:
        import matplotlib.pyplot as plt
        plt.imshow(debug_image)
        plt.show()

    # crop-out staff images
    staff_images = []
    for x, y, w, h in staff_boxes:
        staff_height = h
        x -= int(HORIZONTAL_PADDING_IN_STAFF_HEIGHTS * staff_height)
        w += int(HORIZONTAL_PADDING_IN_STAFF_HEIGHTS * staff_height * 2)
        y -= int(VERTICAL_PADDING_IN_STAFF_HEIGHTS * staff_height)
        h += int(VERTICAL_PADDING_IN_STAFF_HEIGHTS * staff_height * 2)

        # clamp
        if x < 0:
            x = 0
            w += x
        if x + w >= sheet_image.shape[1]:
            w = sheet_image.shape[1] - 1 - x
        if y < 0:
            y = 0
            h += y
        if y + h >= sheet_image.shape[0]:
            h = sheet_image.shape[0] - 1 - y

        staff_images.append(sheet_image[y:(y + h), x:(x + w)])

    return staff_images
