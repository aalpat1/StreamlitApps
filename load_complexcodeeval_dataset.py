import json
import os
import numpy as np

def load_jsonl(file):
    with file as f:
        data = json.load(file)
    return data
if __name__ == "__main__":
    local_file_path = "ComplexCodeEval-Python.json"
    if os.path.isfile(local_file_path):
        file = open(local_file_path, 'rb')
    dataset = load_jsonl(file)
    sampled_indices = np.random.choice(len(dataset), 100, replace=False)
    filtered_dataset = []
    for index in sampled_indices:
        filtered_dataset.append(dataset[index])
    import json
    with open(f'ComplexCodeEval-Python-Sampled.json', 'w') as f:
        json.dump(filtered_dataset, f)
        f.write('\n')




    # if os.path.isfile(local_file_path):
    #     file = open(local_file_path, 'rb')
    # dataset = load_jsonl(file)

    # import pdb; pdb.set_trace()
    # for example in dataset:
    #     metadata = {
    #         "project_name": example["git_name"],
    #         "version": example["version"],
    #         "file_path": example["file_path"],
    #         "file_create_time": example["file_create_time"],
    #         "function_update_time": example["function_update_time"]
    #     }
    #     context_before = example["left_context"]
    #     context_after = example["right_context"]
    #     method_signature = example["function_signature"]
    #     prompt = example["prompt"]
    #     reference_apis = example["reference_apis"]
    #     function_sig = example["function_signature"]
    #     comment = example["comment"]
    #     test_functions = example["test_function"]




