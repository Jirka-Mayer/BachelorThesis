from app.vocabulary import parse_annotation_into_token_groups


# annotations[writer][part][staff]
MUSCIMA_RAW_ANNOTATIONS = {
    # writer 01
    1: {
        2: [
            "clef.G-2 q1 . q3 . q5 . qr | q6 e=6 . =s6 q6 q6 | h8 * qr | br wr | hr qr q-2 | e=5 . =e3 trill q3 e=5 . =e2 . trill q2 | q1 qr qr q-2 | e=5 . =e3 . trill q3 e=5 . =e2 . trill q2 | q1 e=5 * =s5 q5 q5 | w5 |",
            "clef.G-2 q6 e=6 * =s6 q6 q6 | w6 | q7 e=7 * =s7 q7 q7 | w7 | q8 e=8 * =s8 q8 q8 | w8 | b7 w7 | #4 w4 | w5 ( | ) w5 | #4 w4 | w5 |",
            "clef.G-2 #4 q4 er e2 b7 q7 e=7 * =s7 | q6 er e2 b7 q7 e=7 * =s7 | q6 . b7 q7 . q6 . q7 | q6 er * s-5 q-5 q-5 | h-5 ( ) e=-5 =s=-4 #-3 =s-3 s=-2 =s=-1 N0 =s=0 #1 =s1 | h2 ( ) e=2 =s=3 #4 =s4 s=5 =s=6 N7 =s=7 #8 =s8 | q9 qr hr |",
            "clef.G-2 lr lr wr | qr q5 ( #4 q4 N4 q4 | q3 b3 q3 q2 q1 | ) q0 qr #5 h5 ( | ) q6 qr #4 h4 ( | ) N5 q5 qr hr | qr #4 s=4 ( ) =e5 * qr s=4 ( ) =e5 * | qr #4 s=4 ( ) =e5 * hr | qr #4 s=4 ( ) =e5 * qr #4 s=4 ( ) =e5 * |",
            "clef.G-2 qr #4 s=4 ( ) =e5 * hr | lr lr br wr | w-2 | w-1 | w0 | w1 | q2 qr ? q9 * e9 | e8 . er e7 . er e6 . er e8 . er | q7 qr ? q7 * e7 |",
            "clef.G-2 e6 . er e5 er #4 e4 . er e6 . er | q5 qr ? q9 * e9 |"
        ],
        3: [
            "clef.G-2 time.3 time.4 q-6 q1 q2 | q3 q2 q1 | q2 e=3 =e=2 =e=1 =e0 | q1 e=2 ( ) =e=1 =e=0 ( ) =e1 | q0 q3 * e4 | q2 e=1 ( ) =e0 q3 | q1 qr qr | qr q0 q1 |",
            "clef.C0 time.3 time.4 q0 qr qr | qr #4 q4 q5 | q6 q5 #4 q4 | q5 e=6 =e=5 #4 =e=4 #3 =e3 | #4 q4 e=5 ( ) =e=4 #3 =e=3 ( ) =e5 | #4 q4 q6 * e7 | q5 #4 e=4 ( ) #3 =e3 q6 | q2 q2 #4 q4 |",
            "clef.C0 time.3 time.4 q-3 qr qr | wr | wr | qr q0 q1 | q2 q1 q0 | q1 e=2 =e=1 =e=0 =e-1 | q0 e=1 ( ) =e=0 =e=-1 ( ) =e0 | q-1 q2 q2 |",
            "clef.C-4 time.3 time.4 qr q3 q4 | q5 ( ) q4 q3 | q4 ( e=5 =e=4 =e=3 =e2 | q3 e=4 ) =e3 e=2 ( ) =e3 | q2 q5 * e6 | q4 e=3 ( ) =e2 q5 | q3 qr qr | qr q2 q3 |",
            "clef.C0 time.3 time.4 wr | qr #4 q4 q5 | q6 ( ) q5 #4 q4 | q5 ( e=6 =e=5 #4 =e=4 #3 =e3 | #4 q4 e=5 ) =e4 #3 e=3 ( ) =e4 | #4 q4 q6 * e7 | q5 #4 e=4 ( ) #3 =e3 q6 | q2 q2 #4 q4 |",
            "clef.C2 time.3 time.4 wr | wr | wr | qr q0 q1 | q4 ( ) q3 q2 | q3 ( e=4 =e=3 =e=2 =e1 | q2 e=3 ) =e2 e=1 ( ) =e2 | q1 q4 q4 |",
            "clef.F2 time.3 time.4 wr | wr | wr | wr | qr #3 q3 q4 | q5 ( ) q4 #3 q3 | q4 ( e=5 =e=4 #3 =e=3 #2 =e2 | #3 q3 e=4 ) =e3 #2 e=2 ( ) =e1 |"
        ],
        9: [
            "clef.F2 #2 time.3 time.4 e=-4 ( =e0 ) q5 e=4 ( =s=5 ) =s6 | e=5 ( ) =e=4 =e=3 ( ) =e=2 =e=3 ( ) =e0 | e=1 ( ) =e=3 =e6= ( ) =e=4 =e=2 ( ) =e7 | trill h7 h0 h-6 ? | e=-3 ( =e2 ) q6 e=5 ( =s=6 ) =s7 | e=6 ( ) =e=5 =e=4 ( ) =e=3 =e=2 ( ) =e1 | e=2 ( =s=3 ) =s4 e=3 =e=2 =e=1 =e2 | q0 q-3 q-7 :| |: e=0 ( =e2 ) q4 e=3 ( =s=4 ) =s5 |",
            "clef.F2 #2 e=4 ( ) =e=3 =e=2 ( ) =e=1 =e=0 ( ) =e2 | e=-2 =e=0 ( #3 =e=3 ) =e=4 =e=5 =e7 | e=-3 =e=7 ( =e=6 ) =e5 q6 | #0 e=0 ( =e=2 ) =e=4 =e=6 =e=5 =e4 | e=5 ( =e=1 ) =e=-4 =e=4 =e=6 =e=5 | e=4 ( =e=3 ) =e=2 =e=1 =e=-2 #0 =e0 | q-6 * e=1 N0 =e=0 =e-1 | e=-2 ( =e0 ) q3 e=0 ( =s=1 ) N2 =s2 |",
            "clef.F2 #2 N2 e=2 ( ) =e=0 =e=1 ( ) =e=-1 =e=-8 =e-2 | #-1 e=-1 ( =e1 ) q4 e=1 ( =s=2 ) =s3 | e=3 ( ) =e=1 =e=2 ( ) =e=0 =e=-7 =e-3 | e=0 ( =e=2 ) =e=4 =e=6 =e=5 =e6 | e=1 ( =e=3 ) =e=5 =e=7 =e=6 =e8 | e=7 =e=2 =e=3 =e=-2 =e=-7 =e2 | ? fermata :| N2 b-2"
        ]
    }
}

# validate annotations
for writer, parts in MUSCIMA_RAW_ANNOTATIONS.items():
    for part, staves in parts.items():
        for i, staff in enumerate(staves):
            if staff in [None, "TODO"]:
                continue
            _, warnings = parse_annotation_into_token_groups(staff)
            if len(warnings) != 0:
                print(
                    "Invalid muscima annotation at: Writer: %s Part: %s Staff: %s"
                    % (writer, part, i)
                )
                print(staff)
                print("\t" + "\n\t".join(warnings))
