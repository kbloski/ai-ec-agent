import tiktoken

def count_tokens(text: str, model: str = "gpt-5") -> int:
    """
    Liczy liczbę tokenów w tekście dla danego modelu OpenAI.
    """
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)


# przykład
wiadomosc = "Cześć, ile tokenów zajmuje ta wiadomość?"

print(count_tokens(wiadomosc))