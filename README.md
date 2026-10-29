# Prompt Builder

A Python script that demonstrates the **prompt assembly** step of a RAG (Retrieval-Augmented Generation) pipeline. It takes a user question and a list of retrieved document chunks (simulated), builds a complete prompt for an LLM, and estimates its token count.

## What the Script Does

- Uses a system prompt that tells the model to answer **only** from the provided context
- Formats retrieved chunks with source labels, e.g. `[Source: module5_auth.md]`
- Includes the user's question and instructions to cite sources
- Prints the full prompt and a token estimate (characters ÷ 4)
- Runs 2 tests with different questions and different sets of retrieved chunks

## How to Run

No libraries need to be installed.

```bash
python prompt_builder.py
```

## Results

| Test | Chunks | Characters | Est. Tokens |
|------|--------|------------|-------------|
| Test 1 | 2 (both relevant) | 983 | 245 |
| Test 2 | 3 (1 relevant, 2 unrelated) | 1043 | 260 |

Test 2 added a third chunk but only 15 tokens, because token cost depends on text length, not on how many chunks there are. About a quarter of Test 2's prompt was spent on chunks unrelated to the question. This shows why filtering retrieval results (with similarity thresholds or metadata filters) matters: unrelated chunks add cost without improving the answer.

## Technologies

- Python 3 (f-strings, functions, lists and dictionaries)