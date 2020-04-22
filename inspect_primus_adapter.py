from mashcima.primus_adapter import load_primus_as_mashcima_annotations
from app.vocabulary import to_generic, get_pitch

# for d in load_primus_as_mashcima_annotations(10):
#     print(d["path"])
#     print(d["mashcima"])

pitch_histogram = {}
generic_histogram = {}
for d in load_primus_as_mashcima_annotations(1000):
    for token in d["mashcima"].split():
        pitch = get_pitch(token)
        generic = to_generic(token)

        if pitch not in pitch_histogram:
            pitch_histogram[pitch] = 1
        else:
            pitch_histogram[pitch] += 1

        if generic not in generic_histogram:
            generic_histogram[generic] = 1
        else:
            generic_histogram[generic] += 1

print("Pitches:")
for key in pitch_histogram:
    print(key, pitch_histogram[key])

print("Generic histogram:")
print(generic_histogram)
