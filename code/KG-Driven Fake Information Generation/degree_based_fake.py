import yaml
from collections import defaultdict
import json
from tqdm import tqdm 

def load_triplets(yaml_path="triples_by_category.yaml"):
    print('[+] LOADING TRIPLETS ...')
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    print('[+] TRIPLETS LOADED ...')
    
    excluded_categories = {
        "type", "freebase", "common", "other", "broadcast", "base",
        "symbols", "user", "cvg", "topic_server", "dataworld",
        "transportation", "protected_sites", "internet"
    }

    triples_with_description = []
    for category_entry in tqdm(data, desc='Building original triplets'):
        category = category_entry.get("category", "")
        if category in excluded_categories:
            continue
        for entry in category_entry["entries"]:
            subject = entry["subject"]
            description = entry.get("description", None)
            for triple in entry["triples"]:
                s, p, o = triple
                triples_with_description.append({
                    "subject": s,
                    "predicate": p,
                    "object": o,
                    "description": description
                })
    return triples_with_description

def build_structures(triples):
    sp_to_o = defaultdict(dict)
    predicate_object_to_subjects = defaultdict(lambda: defaultdict(set))

    for triple in tqdm(triples, desc='Building Structures'):
        s = triple["subject"]
        p = triple["predicate"]
        o = triple["object"]
        sp_to_o[s][p] = o
        predicate_object_to_subjects[p][o].add(s)

    return sp_to_o, predicate_object_to_subjects


def jaccard_sets(set1, set2):
    if not set1 or not set2:
        return 0.0
    return len(set1 & set2) / len(set1 | set2)

def generate_fake_triplets_from_yaml(triples, sp_to_o, predicate_object_to_subjects):
    fake_triplets = []

    for triple in tqdm(triples, desc='Generating Fake Triplets...'):
        s = triple["subject"]
        p = triple["predicate"]
        true_o = triple["object"]
        description = triple.get("description", None)

        candidates = [o for o in predicate_object_to_subjects[p] if o != true_o]
        if len(candidates) < 3:
            continue

        true_degree = len(predicate_object_to_subjects[p][true_o])

        scores = []
        for o_alt in candidates:
            alt_degree = len(predicate_object_to_subjects[p][o_alt])
            similarity = -abs(true_degree - alt_degree)  # più vicino → più plausibile
            scores.append((o_alt, similarity))

        scores.sort(key=lambda x: x[1], reverse=True)

        high = scores[0][0]
        medium = scores[len(scores) // 2][0]
        low = scores[-1][0]

        fake_triplets.append({
            "subject": s,
            "description": description,
            "predicate": p,
            "true_object": true_o,
            "fakes": {
                "high": high,
                "medium": medium,
                "low": low
            }
        })

    return fake_triplets




def main():
    triples = load_triplets("triples_by_category.yaml")
    sp_to_o, predicate_object_to_subjects = build_structures(triples)
    fake_triplets = generate_fake_triplets_from_yaml(triples, sp_to_o, predicate_object_to_subjects)

    with open("fake_triplets_degree.json", "w", encoding="utf-8") as f:
        json.dump(fake_triplets, f, indent=2, ensure_ascii=False)

    print(f"✅ Generati {len(fake_triplets)} set di fake triplets basati su proprietà strutturali.")

if __name__ == "__main__":
    main()
