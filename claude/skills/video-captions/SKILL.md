---
name: video-captions
description: Use when the user asks to extract captions, subtitles, or transcribe audio/speech from a video file. Triggers on "extract captions", "transcribe video", "get subtitles", "transcrever vídeo", "legendas do vídeo", or when a video file path is provided alongside a transcription request.
disable-model-invocation: true
---

# video-captions

Extract captions or subtitles from video files using `video-captions` (Whisper-based CLI).

## Quick Reference

| Option | Default | Description |
|--------|---------|-------------|
| `--language LANG` | `en` | Source language code (`en`, `pt`, `es`, `fr`, …) |
| `--model MODEL` | `base` | Model size: `tiny`, `base`, `small`, `medium`, `large` |
| `--format FORMAT` | `text` | Output: `text`, `srt`, `vtt`, `json` |
| `--output FILE` | stdout | Save to file instead of printing |

## Usage

```bash
# Plain text to stdout
video-captions video.mp4

# Portuguese audio, small model
video-captions --language pt --model small video.mp4

# SRT file output
video-captions --format srt --output captions.srt video.mp4

# WebVTT with better accuracy
video-captions --model medium --format vtt talk.mkv
```

## Model Trade-offs

- `tiny` / `base` — fast, good for short clips or clear speech
- `small` / `medium` — better accuracy, slower (recommended for accented speech)
- `large` — highest accuracy, requires more RAM (~10 GB)

## When to Use a Larger Model

The `base` model is sufficient for most clear English audio. Use `small` or `medium` when:
- Audio has background noise or music
- Speaker has a strong accent
- Language is not English

## Dependency

Requires `openai-whisper` for Python 3.12:
```bash
pip install openai-whisper --break-system-packages
```
