from engine import action, auto_generator, hint_generator, item_decoder, puzzle_decoder
from engine import room

import json
import time
import psutil
import spacy
from transformers import pipeline

def get_input(config_file):
    with open(config_file, "r") as f:
        data = json.load(f)
    dataset = []
    for i in range(len(data)):
        item = data[i]['item']
        intents = data[i]['labels']
        dataset.append([item, intents])
    return dataset

def measure_latency(func, dataset, labels):
    start = time.time()
    outputs = [[func(intent, labels) for intent in data[1]] for data in dataset]
    end = time.time()
    return outputs, (end - start) / len(dataset)

# Test starts
def main():
    # [For Developers to modify]
    item_config_file = "evaluation/eval_item.json"
    # puzzle_config_file = "my_room/puzzle_config.json"
    items = item_decoder.system_init(item_config_file)
    # puzzles = puzzle_decoder.system_init(puzzle_config_file, items)


    action_spacy = action.Action(items, "classic")
    action_bart = action.Action(items, "transformer")
    action_llm = action.Action(items, "llm")
    action_hybrid = action.Action(items, "hybrid")
    dataset = get_input("evaluation/dataset.json")

    labels = action_hybrid.update_all_labels()
    print("Labels: ", end = "")
    print(labels)

    process = psutil.Process()
    bart_preds, bart_latency = measure_latency(action_bart.interpret, dataset, labels)
    print(f"Initialization")

    # --- #

    process = psutil.Process()
    print(f"Memory usage: {process.memory_info().rss / 1024 ** 2:.2f} MB")
    print(f"CPU usage: {psutil.cpu_percent(interval=1)}%")

    spacy_preds, spacy_latency = measure_latency(action_spacy.interpret, dataset, labels)
    print(f"spaCy Output: {spacy_preds}, Latency: {spacy_latency:.4f}s")

    process = psutil.Process()
    print(f"Memory usage: {process.memory_info().rss / 1024 ** 2:.2f} MB")
    print(f"CPU usage: {psutil.cpu_percent(interval=1)}%")

    bart_preds, bart_latency = measure_latency(action_bart.interpret, dataset, labels)
    print(f"BART Output: {bart_preds}, Latency: {bart_latency:.4f}s")

    process = psutil.Process()
    print(f"Memory usage: {process.memory_info().rss / 1024 ** 2:.2f} MB")
    print(f"CPU usage: {psutil.cpu_percent(interval=1)}%")

    llm_preds, llm_latency = measure_latency(action_llm.interpret, dataset, labels)
    print(f"LLM Output: {llm_preds}, Latency: {llm_latency:.4f}s")

    process = psutil.Process()
    print(f"Memory usage: {process.memory_info().rss / 1024 ** 2:.2f} MB")
    print(f"CPU usage: {psutil.cpu_percent(interval=1)}%")

    hybrid_preds, hybrid_latency = measure_latency(action_hybrid.interpret, dataset, labels)
    print(f"Hybrid Output: {hybrid_preds}, Latency: {hybrid_latency:.4f}s")

    process = psutil.Process()
    print(f"Memory usage: {process.memory_info().rss / 1024 ** 2:.2f} MB")
    print(f"CPU usage: {psutil.cpu_percent(interval=1)}%")




# --------------------------------- #

