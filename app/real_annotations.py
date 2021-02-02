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
        "clef.G-2 b0 b3 b-1 b2 q7 ( q10 q7 q8 | ) h9 * q9 ( | q8 q11 q8 ) N9 e9 | b10 h10 * q10 ( | q11 q10 q8 ) q6 ( |",
        "clef.G-2 b0 b3 b-1 b2 ) q6 h6 q6 ( | ) q6 h6 q6 ( | ) q6 q3 q1 ) q4 | h4 ( q3 ) q2 | h1 ( ) h-1 | h4 * ( ) q3 |",
        "clef.G-2 b0 b3 b-1 b2 h-1 * qr | qr q-4 ( N-3 q-3 q2 | ) h1 * q1 | h2 * b1 q1 | N-1 q-1 N-4 q-4 b-2 q-2 q-4 |",
        "clef.G-2 b0 b3 b-1 b2 h-4 ( ) e=-4 N-3 ? =e=-4 ( N-5 =e=-5 =e-4 | ) q1 h1 ( ) q0 | w-1 ( | ) w-1 ( | ) e-1 er q-1 . ( ) h-1 . ( | ) w-1 ( | ) w-1 ( | ) q-1 qr qr |",
        None,
        "clef.G-2 #4 | e0 . q3 e0 . | #2 s=2 . =s=3 . =s=4 . =s2 . q3 | e0 . q5 e3 . | s=4 . =s=5 . =s=6 . =s4 . q5 | s=6 . #5 =s=5 . =s=6 . =s7 . e=8 =s=7 . =s6 . | N5 s=5 . =s=4 . =s=5 . =s6 . e=7 =s=6 . =s5 . |",
        "clef.G-2 #4 s=4 . #3 =s=3 . =s=4 . =s5 . e=6 =s=5 . =s4 . | s=5 . =s=6 . =s=5 . =s4 . e3 . er | wr | wr | wr | hr qr er e7 |",
        "clef.G-2 #4 s=6 . #5 =s=5 . =s=6 . =s7 . e=8 =s=7 . =s6 . | N5 s=5 . =s=4 . =s=5 . =s6 . e=7 =s=6 . =s5 . | s=4 . #3 =s=3 . =s=4 . =s5 . e=6 =s=5 . =s4 . | s=5 =s=6 =s=5 =s4 e3 er |",
        "clef.G-2 #4 e0 . q3 e0 . | #2 s=2 =s=3 =s=4 =s2 q3 | e0 q5 e3 | s=4 . =s=5 . =s=6 . =s4 . q5 | s=6 . #5 =s=5 . =s=6 . =s7 . e=8 =s=7 . =s6 . |",
        "clef.G-2 #4 N5 s=5 . =s=4 . =s=5 . =s6 . e=7 =s=6 . =s5 . | s=4 . #3 =s=3 . =s=4 . =s5 . e=6 =s=5 . =s4 . | s=5 . =s=6 . =s=5 . =s4 . e3 . sr |",
        "clef.G-2 #4 | s=0 ( ) #-1 =s=-1 =s=0 . #1 =s1 . #2 s=2 ( ) =s=0 =s=1 . =s2 . | s=3 ( ) #2 =s=2 =s=3 . =s4 . s=5 ( ) =s=3 =s=4 . =s5 . | s=6 ( ) #5 =s=5 =s=6 . =s7 . s=8 ( ) =s=6 =s=7 . =s8 . | s=7 ( ) =s=8 =s=7 . =s6 . s=5 ( ) =s=6 =s=7 . =s5 . |",
        "clef.G-2 #4 s=6 ( ) =s=7 =s=6 . =s5 . s=4 ( ) =s=5 =s=6 . =s4 . | s=5 ( ) =s=6 =s=5 . =s4 . s=3 ( ) =s=4 =s=5 . =s3 . | s=4 ( ) =s=5 =s=4 . =s3 . #2 s=2 ( ) =s=3 =s=4 . =s2 . | s=3 ( ) =s=4 =s=5 . =s4 . e3 . er |"
    ],
    "003-cavatine-03.png": [
        "clef.G-2 #4 e0 . q3 e0 . | #2 s=2 =s=3 =s=4 =s2 q3 | e0 . q5 e3 | s=4 =s=5 =s=6 =s4 q5 | s=6 . #5 =s=5 . =s=6 . =s7 . e=8 =s=7 . =s6 . |",
        "clef.G-2 #4 N5 s=5 . =s=4 . =s=5 . =s6 . e=7 =s=6 . =s5 . | s=4 . #3 =s=3 . =s=4 . =s5 . e=6 =s=5 . =s4 . | s=5 . =s=6 . =s=5 . =s4 . e3 . er | #4 #1 #5 #2 hr | hr | hr | qr er e7 . |",
        "clef.G-2 #4 #1 #5 #2 s=6 . #5 =s=5 . =s=6 . =s7 . e=8 =s=7 . =s6 . | s=5 . ? =s=4 . =s=5 . =s6 . e=7 =s=6 . =s5 . | #4 s=4 . #3 =s=3 . =s=4 . =s5 . e=6 =s=5 . =s4 . | s=5 . =s=6 . =s=5 . =s4 . e3 . er |",
        "clef.G-2 e3 . qr q3 | s=3 ( =s=4 =s=3 ) =s2 q1 | s=1 ( =s=2 =s=1 =s0 s=-1 #-2 =s=-2 =s=-1 =s0 | s=1 =s=0 =s=1 =s2 s=3 =s=4 =s=5 ) =s4 | e3 . er q3 | s=3 ( =s=4 =s=3 ) =s2 q1 | s=1 ( =s=2 =s=1 =s0 s=-1 #-2 =s=-2 =s=-1 =s0 | s=1 =s=0 =s=2 =s2 s=3 =s=4 =s=5 ) #6 =s6 |",
        "clef.G-2 ) e6 . sr q6 | s=6 ( b7 =s=7 =s=6 ) =s5 q4 | s=4 ( =s=5 =s=4 =s3 s=2 #1 =s=1 =s=2 =s3 | s=4 =s=3 =s=4 =s5 s=6 b7 =s=7 =s=8 ) =s7 | e6 . er q6 | s=6 ( b7 =s=7 =s=6 =s5 ) q4 | s=4 . =s=5 ( =s=4 =s3 s=2 #1 =s=1 =s=2 ) =s3 |",
        "clef.G-2 s=4 ( =s=3 =s=4 =s5 s=6 =s=7 =s=8 ) #8 =s8 | e9 . er q9 | s=8 ( =s=9 =s=8 b7 =s7 ) q6 | b7 e7 er q7 | s=6 ( b7 =s=7 =s=6 =s5 ) q4 | s=5 . #4 =s=4 . =s=5 . =s6 . b7 e=7 =s=6 . =s5 . | N4 s=4 . =s=3 . =s=4 . =s5 . e=6 =s=5 . =s4 . |",
        "clef.G-2 s=3 #2 =s=2 =s=3 =s4 e=5 =s=4 =s3 | s=4 =s=5 =s=4 =s3 N2 s=2 #1 =s=1 =s=2 =s3 | s=4 . =s=5 . =s=6 . =s5 . s=4 . =s=5 . =s=4 . =s3 . | s=2 . =s=3 . =s=4 . =s5 . e=6 . =e4 . | #5 s=5 . =s=6 . =s=7 . =s6 . s=4 . =s=5 . =s=4 . #3 =s3 . | #3 s=3 . #4 =s=4 . #5 =s=5 . =s6 . N7 e=7 . =e5 . |",
        "clef.G-2 #6 s=6 . =s=7 . #8 =s=8 . =s7 . s=6 . =s=7 . =s=6 . #5 =s5 . | ? s=4 . #5 =s=5 . #6 =s=6 =s7 . #8 e=8 . =e6 . | s=9 . b10 =s=10 . =s=9 . N8 =s8 . b7 s=7 . =s=8 . =s=7 . =s6 . | N5 s=5 . =s=6 . b7 =s=7 . =s8 . e=9 . =e7 . | #4 s=7 . =s=8 . =s=7 . =s6 . s=5 . =s=6 . =s=5 . =s3 . |",
        "clef.G-2 #4 s=4 . =s=5 . =s=4 . =s3 . #2 s=2 . =s=3 . =s=2 . N1 =s1 . | s=0 . =s=1 . =s=0 . =s-1 . s=-2 . =s=-1 . =s=-2 . =s-4 . | s=-3 . =s=-2 . =s=-3 . =s-4 . #-5 s=-5 . =s=-4 . =s=-3 . =s-2 . | e-4 . #-3 e=-3 ( ) =e-2 #-1 s=-1 ( ) =s=0 #2 =s=2 ( ) =s3 | e5 . q3 ( ) e7 . |",
        "clef.G-2 #4 e5 . #-1 s=-1 ( ) =s0 #2 s=2 ( ) =s=3 =s=4 ( ) =s5 | e7 . q5 ( ) e10 . | e8 . er qr | e7 . er qr | #2 h2 ? s=1 =s2 | e3 er qr | e-4 . #-3 s=-3 ( ) =s-2 #-1 s=-1 ( ) =s=0 #2 =s=2 ( ) =s3 | e5 . q3 ( ) e7 . |",
        "clef.G-2 #4 e5 . #-1 s=-1 ( ) =s0 #2 s=2 ( ) =s=3 =s=4 ( ) =s5 | e7 . q5 ( ) e10 . | e8 . er qr | e7 . er qr | #2 w2 ? s=1 =s2 | wr | wr | e0 q3 e0 | #2 s=2 . =s=3 . =s=4 . =s2 . q3 |",
        "clef.G-2 #4 e0 . q5 e3 | s=4 . =s=5 . =s=6 . =s4 . q5 | s=6 . #5 =s=5 . =s=6 . =s7 . e=8 =s=7 . =s6 . | N5 s=5 . #4 =s=4 . =s=5 . =s6 . e=7 =s=6 . =s5 . | s=4 . #3 =s=3 . =s=4 . =s5 . e=6 =s=5 . =s4 . | s=5 . =s=6 . =s=5 . =s4 . e3 . er |"
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
