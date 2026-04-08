"""
audio_generator.py — Converts podcast script to MP3 using OpenAI TTS.

OpenAI TTS has a 4096 character limit per request, so long scripts
are split into chunks and concatenated.
"""

import os
import math
from openai import OpenAI
from pathlib import Path
from config import TTS_VOICE


MAX_CHARS = 4000  # Stay safely under the 4096 limit


def split_into_chunks(text: str) -> list[str]:
    """Split text at sentence boundaries to stay under TTS character limit."""
    if len(text) <= MAX_CHARS:
        return [text]

    chunks = []
    # Split on sentence endings
    sentences = []
    current = ""
    for char in text:
        current += char
        if char in ".!?" and len(current) > 1:
            sentences.append(current.strip())
            current = ""
    if current.strip():
        sentences.append(current.strip())

    # Group sentences into chunks
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 > MAX_CHARS:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += " " + sentence

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def generate_audio(script: str, output_filename: str) -> Path:
    """Generate MP3 from script text. Returns path to output file."""
    client = OpenAI()  # reads OPENAI_API_KEY from environment

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / output_filename

    chunks = split_into_chunks(script)
    print(f"  📢 Generating audio in {len(chunks)} chunk(s) with voice '{TTS_VOICE}'...")

    audio_parts = []

    for i, chunk in enumerate(chunks, 1):
        print(f"     Chunk {i}/{len(chunks)} ({len(chunk)} chars)...")
        response = client.audio.speech.create(
            model="tts-1",
            voice=TTS_VOICE,
            input=chunk,
            response_format="mp3",
        )
        audio_parts.append(response.content)

    # Concatenate all audio chunks (MP3 frames can be safely concatenated)
    with open(output_path, "wb") as f:
        for part in audio_parts:
            f.write(part)

    size_kb = output_path.stat().st_size // 1024
    print(f"  ✅ Audio saved: {output_path} ({size_kb} KB)")
    return output_path
