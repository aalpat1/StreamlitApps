import os
import numpy as np
import openai
import asyncio
import numpy as np

client = openai.OpenAI()

class Example(object):
    """A single training/test example."""
    def __init__(self,
                 idx,
                 source_question,
                 source_code,
                 target,
                 ):
        self.idx = idx
        self.source_question = source_question
        self.source_code = source_code
        self.target = target

def read_examples(filename, stage):
    """Read examples from filename."""
    # filename: e.g. $data_dir/$lang/train/
    # stage: e.g. train
    examples=[]
    idx = 0
    codefile = os.path.join(filename, stage + ".code")
    quesfile = os.path.join(filename, stage + ".question")
    ansfile = os.path.join(filename, stage + ".answer")
    with open(codefile,encoding="utf-8") as code_f:
        with open(ansfile, encoding="utf-8") as ans_f:
            with open(quesfile, encoding="utf-8") as ques_f:
                for codeline, quesline, ansline in zip(code_f,ques_f,ans_f):
                    code = codeline.strip()
                    question = quesline.strip()
                    ans = ansline.strip()
                    examples.append(
                        Example(
                                idx = idx,
                                # source= question + " " + code,
                                source_question = question,
                                source_code = code,
                                target = ans,
                                )
                    )
                    idx += 1
    return examples

def render_pretty(examples):
    responses = asyncio.run(format_code(examples))
    return [response.choices[0].message.content for response in responses]


async def format_code(examples):
    tasks = []
    for ex in examples:
        tasks.append(openai_chat(ex.source_code))
    responses = await asyncio.gather(*tasks)
    return responses


async def openai_chat(query, model="gpt-4"):
    def format_message(query):
        return [{"role": "system", "content": "You are a helpful Python code formatter assistant formatting badly formatted code into valid Python code."},
                {"role": "user", "content": f"Please format the following badly formatted code into valid Python code. Do not make any changes to the code other adding formatting. Return ONLY the formatted code. Code to format: {query}"}]
    messages = format_message(query)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response

if __name__ == "__main__":
    file_name = "/Users/aalhadpatankar/Downloads/test"
    examples = read_examples(file_name, "test")
    # Randomly sample 100 examples from the dataset
    sampled_indices = np.random.choice(len(examples), 100, replace=False)
    filtered_examples = []
    for i, example in enumerate(examples):
        if i in sampled_indices:
            filtered_examples.append(example)

    formatted_code = render_pretty(filtered_examples)
    def example_to_dict(idx: int, ex: Example):
        return {
            "question": ex.source_question,
            "code": ex.source_code,
            "golden_answer": ex.target,
            "idx": ex.idx,
            "formatted_code": formatted_code[idx],
        }
    filtered_examples = [example_to_dict(idx, ex) for idx, ex in enumerate(filtered_examples)]
    import json
    with open(f'codeqa_samples.jsonl', 'w') as f:
        json.dump(filtered_examples, f)
        f.write('\n')