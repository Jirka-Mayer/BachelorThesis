from muscima.io import CropObject


def get_outlink_to(obj: CropObject, clsname: str) -> CropObject:
    from mashcima import CROP_OBJECT_DICT
    for l in obj.outlinks:
        if CROP_OBJECT_DICT[l].clsname == clsname:
            return CROP_OBJECT_DICT[l]
    raise Exception("Object has no outlink of requested clsname")


def has_outlink_to(obj: CropObject, clsname: str) -> bool:
    from mashcima import CROP_OBJECT_DICT
    for l in obj.outlinks:
        if CROP_OBJECT_DICT[l].clsname == clsname:
            return True
    return False


def show_images(images, row_length=5):
    """For debugging - shows many images in a single plot"""
    import matplotlib.pyplot as plt

    n_total = len(images)
    n_rows = n_total // row_length + 1
    n_cols = min(n_total, row_length)
    fig = plt.figure()
    for i, img in enumerate(images):
        plt.subplot(n_rows, n_cols, i+1)
        plt.imshow(img, cmap='gray', interpolation='nearest')
    # Let's remove the axis labels, they clutter the image.
    for ax in fig.axes:
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_yticks([])
        ax.set_xticks([])
    plt.show()
