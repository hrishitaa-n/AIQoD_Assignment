

from langchain_ollama import OllamaLLM

from config import OLLAMA_MODEL
from database import (
    get_db,
    load_csv,
    run_query
)
from llm import (
    build_llama_index,
    ask_llm
)
from output_utils import (
    show,
    save,
    log_query,
    validate_columns
)


# Security,so that user does not enter too many words 
def validate_input(question):
    if len(question) > 500:
        raise ValueError("Input too long.")

    banned = [
        "ignore previous",
        "system prompt",
        "forget instructions"
    ]

    if any(b in question.lower() for b in banned):
        raise ValueError("Invalid input detected.")

    return question


# Test Cases
TEST_CASES = [
    (
        "Find all products with a rating below 4.5 that have more than 200 reviews "
        "and are offered by the brand 'Nike' or 'Sony'.",
        "test_case1.csv"
    ),

    (
        "Which products in the Electronics category have a rating of 4.5 or higher "
        "and are in stock?",
        "test_case2.csv"
    ),

    (
        "List products launched after January 1, 2022, in the Home & Kitchen or Sports "
        "categories with a discount of 10% or more, sorted by price in descending order.",
        "test_case3.csv"
    ),
]


def run_test_cases(col, llm):
    open("Queries_generated.txt", "w").close()

    for question, filename in TEST_CASES:

        print(f"\n{'=' * 60}")
        print(f"Q: {question}")

        query = ask_llm(llm, question)

        results = run_query(col, query)

        show(results)

        save(results, filename)

        log_query(question, query)

    print(
        "\nDone. "
        "CSVs  ./output/   "
        "Queries  Queries_generated.txt"
    )


# Interactive Mode 
def interactive(col, llm, df, query_engine):

    print("\nType your question or 'quit' to exit.")
    print(f"Available columns: {list(df.columns)}\n")

    while True:

        raw_q = input("Question: ").strip()

        if raw_q.lower() in ("quit", "exit", "q"):
            break

        if not raw_q:
            continue

        try:
            q = validate_input(raw_q)

        except ValueError as e:
            print(f" {e}")
            continue

        validate_columns(q, df)

        print("\n[LlamaIndex context]")
        print(str(query_engine.query(q)))

        query = ask_llm(llm, q)

        results = run_query(col, query)

        choice = input(
            "\nDisplay (d) or Save (s)? [d]: "
        ).strip().lower()

        if choice == "s":

            filename = (
                input("Filename: ").strip()
                or "results.csv"
            )

            save(results, filename)

        else:
            show(results)

        log_query(q, query)



if __name__ == "__main__":

    db = get_db()

    col, df = load_csv(db)

    llm = OllamaLLM(
        model=OLLAMA_MODEL
    )

    print("\n1 - Run test cases")
    print("2 - Interactive mode")

    mode = input("Choose [1]: ").strip()

    if mode == "2":

        query_engine = build_llama_index(df)

        interactive(
            col,
            llm,
            df,
            query_engine
        )

    else:
        run_test_cases(
            col,
            llm
        )