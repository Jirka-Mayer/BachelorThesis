import cv2
import os
import editdistance
from app.get_staff_images_from_sheet_image import get_staff_images_from_sheet_image
from app.muscima_annotations import MUSCIMA_RAW_ANNOTATIONS
from app.Network import Network
from app.GeneratedDataset import normalize_image_height
from app.vocabulary import get_measures


CVC_MUSCIMA = os.path.join(
    os.environ['HOME'],
    'Data/CvcMuscima-Distortions/ideal'
)

network = Network.load(name="April15", threads=4)

ser_sum = 0
mer_sum = 0
item_count = 0

for writer, parts in MUSCIMA_RAW_ANNOTATIONS.items():
    for part, staves in parts.items():
        print("Validating on Writer: %s Part: %s ..." % (writer, part))
        image_path = os.path.join(
            CVC_MUSCIMA,
            "w-{:02d}/image/p{:03d}.png".format(writer, part)
        )
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        staff_images = get_staff_images_from_sheet_image(img)
        assert len(staff_images) == len(staves)

        for i, gold_annotation in enumerate(staves):
            prediction = network.predict(
                normalize_image_height(staff_images[i])
            )

            symbol_error_rate = editdistance.eval(
                gold_annotation.split(),
                prediction.split()
            ) / len(gold_annotation.split())
            measure_error_rate = editdistance.eval(
                get_measures(gold_annotation),
                get_measures(prediction)
            ) / len(get_measures(gold_annotation))

            print(
                "\tSER: {:.2f}\tMER: {:.2f}".format(
                    symbol_error_rate,
                    measure_error_rate
                )
            )

            ser_sum += symbol_error_rate
            mer_sum += measure_error_rate
            item_count += 1

print("==========================================")
print("Average symbol error rate: {:.2f}".format(ser_sum / item_count))
print("Average measure error rate: {:.2f}".format(mer_sum / item_count))
