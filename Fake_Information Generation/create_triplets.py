import yaml
import networkx as nx
import os
from tqdm import tqdm 
from collections import defaultdict, Counter

def generate_yaml_grouped_by_category(G, output_file="triples_by_category.yaml"):
    # Step 1: Raggruppa tutte le triplette per subject
    subject_to_triples = defaultdict(list)

    for u, v, data in G.edges(data=True):
        predicate = data.get("relation", "")
        subject_to_triples[u].append((u, predicate, v))

    # Step 2: Per ogni subject, trova categoria predominante
    category_data = defaultdict(list)

    for subject, triples in subject_to_triples.items():
        category_counts = Counter()

        for _, predicate, _ in triples:
            cat = extract_category(predicate)
            category_counts[cat] += 1

        if not category_counts:
            continue

        # Prendi la categoria più frequente per questo subject
        dominant_category = category_counts.most_common(1)[0][0]

        # Filtra le triplette che appartengono solo a quella categoria
        filtered_triples = [
            (s, p, o) for (s, p, o) in triples if extract_category(p) == dominant_category
        ]

        if filtered_triples:
            # Cerca description per il subject
            description = None
            for _, predicate, obj in triples:
                if predicate == "ns/common.topic.description":
                    description = obj
                    break

            entry = {
                "subject": subject,
                "triples": [list(triple) for triple in filtered_triples]
            }
            if description:
                entry["description"] = description

            category_data[dominant_category].append(entry)


    # Step 3: Salva in YAML
    structured_output = []

    for category, subjects in category_data.items():
        structured_output.append({
            "category": category,
            "entries": subjects
        })

    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(structured_output, f, allow_unicode=True)

    print(f"✅ File YAML generato: {output_file}")


def extract_category(relation: str) -> str:
    if relation.startswith("ns/"):
        parts = relation.split(".")
        if "/" in parts[0]:
            return parts[0].split("/")[1]  # es: ns/music.something -> music
    return "other"


def create_networkx_graph(graphs):
    G = nx.DiGraph()
    for i, graph in enumerate(graphs):
        print(f'Graph {graph["title"]} - {i + 1} out of {len(graphs)}')
        center = graph['center']
        title = graph['title']
        G.add_node(center, title=title)
        
        for edge in tqdm(graph['edges'], desc='Building Graph ...'):
            subject, predicate, obj = edge
            G.add_node(subject)
            G.add_node(obj)
            G.add_edge(subject, obj, relation=predicate)
    
    return G

def _parse_wikigraph_file(file_path):
    graphs = []
    with open(file_path, 'r', encoding='utf-8') as f:
        graph = None
        for line in f:
            line = line.strip()
            if line.startswith('<graph'):
                if graph:
                    graphs.append(graph)
                parts = line.split(' ')
                graph_center = parts[1].split('=')[1].strip('"')
                graph_title = parts[2].split('=')[1].strip('"')
                graph = {'center': graph_center, 'title': graph_title, 'edges': []}
            elif '\t' in line:
                fields = line.split('\t')
                if len(fields) == 4:
                    subject, predicate, obj, _ = fields
                    graph['edges'].append((subject, predicate, obj))
        if graph:
            graphs.append(graph)
    return graphs

def parse_all_wikigraph_files(directory_path):
    all_graphs = []
    for filename in ['train', 'test', 'valid']:
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            print(f"Parsing {filename}...")
            file_graphs = _parse_wikigraph_file(file_path)
            all_graphs.extend(file_graphs)
    return all_graphs

def load_taxonomy_from_yaml(filepath):
    with open(filepath, 'r') as yaml_file:
        taxonomy = yaml.load(yaml_file, Loader=yaml.FullLoader)
    return taxonomy

def save_graph(G, path='./wikigraph.graphml'):
    nx.write_graphml(G, path)
    print(f"Grafo salvato in {path}")

def load_graph_if_exists(path='./wikigraph.graphml'):
    if os.path.exists(path):
        print(f"📂 Caricamento grafo da file: {path}")
        return nx.read_graphml(path)
    return None

def normalize_graph_with_names(G):
    # Step 1: Mappa ID → nome se esiste
    id_to_name = {}
    for u, v, data in G.edges(data=True):
        if data.get("relation") == "ns/type.object.name":
            id_to_name[u] = v

    # Step 2: Nuovo grafo normalizzato
    G_norm = nx.DiGraph()

    for u, v, data in G.edges(data=True):
        relation = data.get("relation")

        # Salta gli edge type.object.name, li usiamo già come mappatura
        if relation == "ns/type.object.name":
            continue

        # Sostituisci subject e object con il loro nome, se disponibile
        subject_name = id_to_name.get(u, u)
        object_name = id_to_name.get(v, v)

        G_norm.add_node(subject_name)
        G_norm.add_node(object_name)
        G_norm.add_edge(subject_name, object_name, relation=relation)

    return G_norm

def main(PRINT=False):
    taxonomy = load_taxonomy_from_yaml('../taxonomy.yaml')
    graph_path = './wikigraph.graphml'

    G = load_graph_if_exists(graph_path)
    if G is None:
        print("⚙️  Grafo non trovato, lo ricreo da zero...")
        directory_path = '../Wikigraph_files/'
        graphs = parse_all_wikigraph_files(directory_path)
        G = create_networkx_graph(graphs)
        save_graph(G, graph_path)
    else:
        print("✅ Grafo caricato correttamente.")

    # 🔄 Normalizza il grafo
    G_normalized = normalize_graph_with_names(G)

    if PRINT:
        # 🔁 Analisi: stampa soggetti con più di una tripla
        subject_to_triples = {}
        for u, v, data in G_normalized.edges(data=True):
            predicate = data.get('relation', '')
            if u not in subject_to_triples:
                subject_to_triples[u] = []
            subject_to_triples[u].append((predicate, v))
        
        print("\n🔍 Subjects con più di una tripla (dopo normalizzazione):")
        for subject, triples in subject_to_triples.items():
            if len(triples) > 1:
                print(f"\nSubject: {subject}")
                for predicate, obj in triples:
                    print(f"  ({subject}, {predicate}, {obj})")

    return G_normalized


if __name__ == "__main__":
    G = main()
    generate_yaml_grouped_by_category(G)
