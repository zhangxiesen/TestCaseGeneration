import os
import pandas as pd
from openai import OpenAI

# LLM Client
client = OpenAI(
    api_key="",
    base_url="https://llm-59susyrjcmp9l6z8.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

def call_llm(prompt_text: str) -> str:
    resp = client.chat.completions.create(
        model="qwen3.8-flash",
        messages=[{"role": "user", "content": prompt_text}],
        extra_body={"enable_thinking": True},
        stream=False
    )
    return resp.choices[0].message.content

def extract_java_code(raw_text: str) -> str:
    if "```java" in raw_text and "```" in raw_text:
        start = raw_text.find("```java") + len("```java")
        end = raw_text.find("```", start)
        return raw_text[start:end].strip()
    return raw_text.strip()

def safe_filename(name: str) -> str:
    """清洗文件名，移除Windows非法字符"""
    illegal_chars = r'\/:*?"<>|'
    for c in illegal_chars:
        name = name.replace(c, "_")
    return name.strip()

if __name__ == "__main__":
    CSV_PATH = r"E:\TestingRefactoring\RefWork\FeatureSelection\extract_variable_prompt_output.csv"
    OUTPUT_DIR = "java_output"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(CSV_PATH, header=None, skiprows=1)
    name_series = df.iloc[:, 3]
    prompt_series = df.iloc[:, -1]

    for idx, (file_name_raw, prompt) in enumerate(zip(name_series, prompt_series)):
        if pd.isna(prompt) or str(prompt).strip() == "":
            continue
        base_name = safe_filename(str(file_name_raw))
        out_file = os.path.join(OUTPUT_DIR, f"{base_name}.java")

        print(f"Processing row {idx}, filename: {base_name}.java")
        full_response = call_llm(str(prompt))
        java_code = extract_java_code(full_response)

        with open(out_file, "w", encoding="utf-8") as f:
            f.write(java_code)
        print(f"Saved: {out_file}")
