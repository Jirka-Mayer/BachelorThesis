from mashcima.primus_adapter import load_primus_as_mashcima_annotations

for d in load_primus_as_mashcima_annotations(10):
    print(d["path"])
    print(d["mashcima"])
