from yandex_chain import YandexLLM

# Initialize YandexLLM for text generation
LLM = YandexLLM(folder_id="b1ggu7tv4cjs31ug9orn", api_key="AQVN08JTqnJT8fR5GB6X7ELJDelHBQcGSGY3NRi8")


def generate(prompt):
    return LLM(prompt)
