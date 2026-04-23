import yaml

def analyze_category_yaml(yaml_path="triples_by_category.yaml"):
    print('Loading Data ...')
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    print(f"\n📊 Total Categories: {len(data)}\n")

    for entry in data:
        category = entry.get("category", "unknown")
        subjects = entry.get("entries", [])
        print(f"🔹 Category: {category} - {len(subjects)} subject node(s)")

if __name__ == "__main__":
    analyze_category_yaml("triples_by_category.yaml")
