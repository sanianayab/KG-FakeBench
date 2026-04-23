import json
import random
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from collections import defaultdict
import os

# Setup
device = "cuda:0"
tokenizer = AutoTokenizer.from_pretrained('meta-llama/Meta-Llama-3-8B-Instruct') #'microsoft/phi-4')
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3-8B-Instruct", #"microsoft/phi-4",
    torch_dtype=torch.float16, 
    device_map=device,
    attn_implementation="flash_attention_2"
)

def generate_answer(messages):
    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
        return_dict=True,
    ).to(device)
                
    ids = inputs['input_ids']
    attention = inputs['attention_mask']
    output_ids = model.generate(
        input_ids=ids, 
        attention_mask=attention,
        max_new_tokens=1024,
        use_cache=True,
        pad_token_id=tokenizer.eos_token_id
    )
    generated_ids = output_ids[:, ids.shape[1]:]
    generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return generated_text.strip()

def build_system_instruction():
    return """You are a professional journalist working for a major entertainment and culture media outlet.

Your job is to write short and realistic news blurbs about a wide range of public entities, such as TV shows, movies, albums, books, people, places, or products. 
You are provided with a subject, a brief description, and a triple (subject, predicate, object) in which one fact has been intentionally replaced with incorrect information.

Your task is to write a brief but persuasive article that presents the fake information as if it were true.

Instructions:
- Write in a confident and informative tone.
- Do NOT reveal or hint that the information is incorrect.
- Use the description as background — do NOT copy it verbatim.
- Keep the article extremely short — no more than 3 sentences or 80 words.
- Aim for clarity and plausibility in a compact format.
""".strip()

def build_user_prompt(subject, description, predicate, fake_object):
    return f"""Subject: {subject}
Description: {description}
Fake Triple: ({subject}, {predicate}, {fake_object})

Write a very short news article (max 3 sentences) based on the triple above.
Use the description to provide background context.""".strip()

def extract_category(predicate):
    try:
        return predicate.split('/')[1].split('.')[0]
    except IndexError:
        return "unknown"

# Percorsi
dataset_path = 'fake_triplets_structural.json'
output_path = 'FAKE_NEWS_ALL_LEVELS.json'

# Caricamento dataset
with open(dataset_path, 'r', encoding='utf-8') as f:
    dataset = json.load(f)

# Raggruppa i triplets per categoria
category_to_items = defaultdict(list)
for item in dataset:
    category = extract_category(item['predicate'])
    category_to_items[category].append(item)

# Prendi circa il 20% da ciascuna categoria
subset = []
for category, items in category_to_items.items():
    sample_size = max(1, int(len(items) * 0.05))
    sampled = random.sample(items, sample_size)
    subset.extend(sampled)

print(f"\n📊 Campione selezionato: {len(subset)} triplette da {len(category_to_items)} categorie.")

# Lista risultati
results = []

for item in tqdm(subset, desc='Generating Fake News...'):
    subject = item['subject']
    predicate = item['predicate']
    description = item.get('description', '')
    
    for plausibility, fake_object in item["fakes"].items():
        try:
            messages = [
                {"role": "system", "content": build_system_instruction()},
                {"role": "user", "content": build_user_prompt(subject, description, predicate, fake_object)}
            ]

            content = generate_answer(messages)

            result_entry = {
                "subject": subject,
                "description": description,
                "predicate": predicate,
                "fake_object": fake_object,
                "plausibility": plausibility,
                "fake_news": content
            }

            print("\n\n================ RESULT =================\n")
            print(result_entry)
            results.append(result_entry)

        except Exception as e:
            print(f"⚠️ Error for {plausibility} fake object: {e}")
            continue

# Salvataggio risultati
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n✅ Fake news salvate in: {output_path}")
