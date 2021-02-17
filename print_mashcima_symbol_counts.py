from mashcima import Mashcima
mc = Mashcima(use_cache=True, skip_writers=[13, 17, 20, 34, 41, 49])

print()

print("WHOLE_NOTES:", len(mc.WHOLE_NOTES))
print("HALF_NOTES:", len(mc.HALF_NOTES))
print("QUARTER_NOTES:", len(mc.QUARTER_NOTES))
print("EIGHTH_NOTES:", len(mc.EIGHTH_NOTES))
print("SIXTEENTH_NOTES:", len(mc.SIXTEENTH_NOTES))
print("LONGA_RESTS:", len(mc.LONGA_RESTS))
print("BREVE_RESTS:", len(mc.BREVE_RESTS))
print("WHOLE_RESTS:", len(mc.WHOLE_RESTS))
print("HALF_RESTS:", len(mc.HALF_RESTS))
print("QUARTER_RESTS:", len(mc.QUARTER_RESTS))
print("EIGHTH_RESTS:", len(mc.EIGHTH_RESTS))
print("SIXTEENTH_RESTS:", len(mc.SIXTEENTH_RESTS))
print("FLATS:", len(mc.FLATS))
print("SHARPS:", len(mc.SHARPS))
print("NATURALS:", len(mc.NATURALS))
print("DOTS:", len(mc.DOTS))
print("LEDGER_LINES:", len(mc.LEDGER_LINES))
print("BAR_LINES:", len(mc.BAR_LINES))
print("TALL_BAR_LINES:", len(mc.TALL_BAR_LINES))
print("G_CLEFS:", len(mc.G_CLEFS))
print("F_CLEFS:", len(mc.F_CLEFS))
print("C_CLEFS:", len(mc.C_CLEFS))

for key in mc.TIME_MARKS:
    print("TIME_MARKS[" + str(key) + "]:", len(mc.TIME_MARKS[key]))

print()
