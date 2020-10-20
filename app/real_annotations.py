from app.vocabulary import parse_annotation_into_token_groups

# annotations[image][staff]
REAL_RAW_ANNOTATIONS = {
    "001-cavatine-01.png": [
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "clef.G-2 b0 b3 b-1 b2 h-4 * qr | hr qr q-4 | h-4 ( b-3 q-3 ) q2 | h1 * ( ) b1 q1 |",
        "TODO",
        "TODO"
    ],
    "002-cavatine-02.png": [
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO"
    ],
    "003-cavatine-03.png": [
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO",
        "TODO"
    ]
}

# validate annotations
for file, staves in REAL_RAW_ANNOTATIONS.items():
    for i, staff in enumerate(staves):
        if staff in [None, "TODO"]:
            continue
        _, warnings = parse_annotation_into_token_groups(staff)
        if len(warnings) != 0:
            print(
                "Invalid real image annotation at: File: %s Staff: %s"
                % (file, i)
            )
            print(staff)
            print("\t" + "\n\t".join(warnings))
