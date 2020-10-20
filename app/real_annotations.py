from app.vocabulary import parse_annotation_into_token_groups

# annotations[image][staff]
REAL_RAW_ANNOTATIONS = {
    "001-cavatine-01.png": [
        "clef.G-2 b0 b3 b-1 b2 time.C q-4 | h-4 ( q-3 q2 | ) h1 * q1 ( | q0 q3 q0 q1 | ) h2 * q2 |",
        "clef.G-2 b0 b3 b-1 b2 q2 ( s=3 =e=2 =e=1 =e2 q4 ) q3 | q2 ( q1 q3 ) q6 | q6 ( ) h0 q1 | h1 ( q0 ) q-4 |",
        "clef.G-2 b0 b3 b-1 b2 h-4 ( q-3 q2 | ) h1 * q1 ( | q0 q3 q0 q1 | ) h2 * q2 |",
        "clef.G-2 b0 b3 b-1 b2 N2 q2 ( s=3 =s=2 #1 =s=1 =s2 q6 ) q5 | h5 * ( ) q3 | N2 q2 ( s=3 =s=2 #1 =s=1 =s2 q6 * ) e5 | h5 q4 ( ) q3 |",
        
        "clef.G-2 b0 b3 b-1 b2 N2 q2 ( q3 q5 q8 | q8 q7 q5 ) q6 | q5 ( s=0 =s=1 =s=0 N-1 =s=-1 =s=0 ) =s5 q5 * e4 | h3 * q3 |",
        
        "clef.G-2 b0 b3 b-1 b2 q3 ( e=2 =e1 q4 * ) e1 | h1 ( ) q2 q4 ( | ) e=4 b5 =e=5 =e=4 =e3 q6 * ) N3 e3 | N3 h3 ( ) q4 q5 ( ) |",
        "clef.G-2 b0 b3 b-1 b2 ) e=5 =e=6 =e=4 ) =e3 qr q5 ( | ) e=5 =e=6 =e=5 ) =e4 h6 ( | ) e=6 =e=5 =e=4 =e3 e=2 =e=1 =e=0 ) =e-3 | h-1 ( ) q-2 q0 ( ) |",
        "clef.G-2 b0 b3 b-1 b2 ) q0 e=-1 * ) =s-2 q1 * ( ) e-2 | h-2 ( ) q-1 q1 ( | ) e=1 =e=2 =e=1 =e0 q3 * ) N0 e0 | N0 h0 ( ) q1 N2 q2 (",
        "clef.G-2 b0 b3 b-1 b2 ) e=2 =e=3 N2 =e=2 ) =e1 qr q2 ( | ) e=2 =e=3 N2 =e=2 =e1 ) h10 ( | ) e=10 N9 =e=9 ( =e=8 =e7 e=6 =e=5 =e=4 =e3 | N2 e=2 =e=1 =e=-1 =e-6 ) e-2 q-2 ( ) e-3 |",
        "clef.G-2 b0 b3 b-1 b2 h-4 * qr | hr qr q-4 | h-4 ( b-3 q-3 ) q2 | h1 * ( ) b1 q1 |",
        "clef.G-2 b0 b3 b-1 b2 q0 ( q3 q0 N1 q1 | ) h2 * q2 | q2 ( s=3 =s=2 =s=1 =s2 q4 ) q3 | q2 ( q1 q3 ) q6 |",
        "clef.G-2 b0 b3 b-1 b2 q6 ( h0 ) q1 | h1 ( ) q0 q3 | h3 ( q4 q9 | ) h8 * q8 ( ) |"
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
