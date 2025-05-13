#!/usr/bin/env -S uv run --script

from transformers import BartForConditionalGeneration, BartTokenizer
import typer
from pathlib import Path

app = typer.Typer()

model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)


@app.command()
def read_file(file: Path):
    text = file.read_text(encoding="utf-8")
    inputs = preprocess_text(text)
    summary = generate_summary(inputs)

    print(f"Summary: {summary}")


def preprocess_text(text):
    inputs = tokenizer([text], max_length=1024, return_tensors="pt", truncation=True)
    return inputs


def generate_summary(inputs):
    summary_ids = model.generate(
        inputs["input_ids"],
        num_beams=4,
        min_length=256,
        max_length=1024,
        early_stopping=True,
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


def main():
    app()


if __name__ == "__main__":
    main()
