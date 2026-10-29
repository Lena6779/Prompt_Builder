# Code that creates a system prompt and formats chunks of text for an LLM to use as context.

# --- Step 1: Simulated retrieved chunks ---
# These stand in for what ChromaDB would return from collection.query()

# Test 1: 2 chunks, both related to the question
chunks_test1 = [
    {
        "source": "module5_auth.md",
        "text": "JWT authentication in FastAPI works by creating a /auth/token "
        "endpoint that validates credentials and returns a signed token. "
        "Protected endpoints verify the token on each request.",
    },
    {
        "source": "module5_validation.md",
        "text": "FastAPI uses Pydantic models for automatic request validation. "
        "Invalid requests return 422 errors.",
    },
]

# Test 2: 3 chunks, only the first answers the question (the other 2 are unrelated)
chunks_test2 = [
    {
        "source": "module6_streamlit.md",
        "text": "Streamlit session state persists data across re-runs using "
        "st.session_state. Without it, all variables reset on every "
        "widget interaction.",
    },
    {
        "source": "module7_chromadb.md",
        "text": "ChromaDB is a vector database that stores document embeddings "
        "for fast similarity search.",
    },
    {
        "source": "module6_css.md",
        "text": "CSS Flexbox arranges child elements in a row or column. "
        "Use display: flex on the container.",
    },
]

# --- Step 2: System Prompt: Rules the LLM must follow ---
system_prompt = (
    "You are a helpful AI assistant for students learning AI engineering. "
    "Answer the user's question based ONLY on the context provided below. "
    "If the context doesn't contain enough information to answer, say so. "
    "Do not use outside knowledge."
)


# --- Step 3: Format the chunks with source labels ---
def format_chunks(chunks):
    """Turn a list of chunk dicts into a labeled string for the LLM to use as context."""
    labeled_chunks = []
    for chunk in chunks:
        labeled_chunks.append(f"[Source: {chunk['source']}]\n{chunk['text']}")
    # Join the labeled chunks with blank lines between chunks
    # so the LLM can clearly see the separation between sources.
    return "\n\n".join(labeled_chunks)


# --- Step 4: Assemble the full prompt ---
def build_rag_prompt(user_question, chunks):
    """Build a prompt for the LLM that includes the system prompt, user question, and context chunks."""
    context = format_chunks(chunks)

    full_prompt = f"""SYSTEM PROMPT: {system_prompt}

CONTEXT: 
{context}

USER QUESTION: {user_question}

INSTRUCTIONS: Answer using ONLY the context provided above. Cite the source of the info you use in your answer, in the format [Source: filename]. If the context does not contain enough info to answer the question, say so. Please do not use outside knowledge to answer the question.

ANSWER:"""
    return full_prompt


# --- Step 5: Estimate the token count ---
def estimate_tokens(text):
    """Rough token estimate: about 4 characters per token."""
    return len(text) // 4


# --- Step 6: Run a test and print the results ---
def run_test(test_name, user_question, chunks):
    """Build the prompt for one test and print it with its token estimate."""
    prompt = build_rag_prompt(user_question, chunks)

    print("=" * 60)
    print(test_name)
    print("=" * 60)
    print(prompt)
    print(f"\nPrompt length: {len(prompt)} characters")
    print(f"Estimated tokens: {estimate_tokens(prompt)} (characters / 4)\n")


run_test(
    "TEST 1",
    "How do I protect my API endpoints so only logged-in users can access them?",
    chunks_test1,
)

run_test(
    "TEST 2",
    "Why do my Streamlit variables reset every time I click a button?",
    chunks_test2,
)
