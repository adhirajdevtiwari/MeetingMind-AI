"""Tests for utils/audio_processor.py.

These tests cover the two audio helpers that work fully offline:

  convert_to_wav  - re-encodes a file to mono 16 kHz WAV
  chunk_audio     - splits a WAV into fixed-length pieces

They generate their own short audio files in a temporary folder, so they
need no network access, no YouTube download, and no Whisper model.
Requirements: pydub (pip install pydub) and ffmpeg installed.

Run from the repo root:

    python tests/test_audio_processor.py
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydub import AudioSegment
from pydub.generators import Sine

from utils.audio_processor import convert_to_wav, chunk_audio


def make_wav(path, seconds, channels=2, frame_rate=44100):
    """Write a short sine-wave WAV file and return its path."""
    tone = Sine(440).to_audio_segment(duration=int(seconds * 1000))
    tone = tone.set_channels(channels).set_frame_rate(frame_rate)
    tone.export(path, format="wav")
    return path


class ConvertToWavTests(unittest.TestCase):
    def test_output_is_mono_16khz_wav(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = make_wav(os.path.join(tmp, "in.wav"), seconds=1,
                              channels=2, frame_rate=44100)
            out_path = convert_to_wav(source)

            self.assertTrue(os.path.exists(out_path))
            self.assertTrue(out_path.endswith("_converted.wav"))

            out = AudioSegment.from_wav(out_path)
            self.assertEqual(out.channels, 1, "converted audio should be mono")
            self.assertEqual(out.frame_rate, 16000,
                             "converted audio should be 16 kHz")
            self.assertAlmostEqual(len(out), 1000, delta=100,
                                   msg="converted audio keeps its duration")


class ChunkAudioTests(unittest.TestCase):
    def test_splits_into_expected_chunks(self):
        # 25 seconds with 12-second chunks -> 12s + 12s + 1s = 3 chunks
        with tempfile.TemporaryDirectory() as tmp:
            wav = make_wav(os.path.join(tmp, "long.wav"), seconds=25)
            chunks = chunk_audio(wav, chunk_minutes=0.2)

            self.assertEqual(len(chunks), 3)
            for path in chunks:
                self.assertTrue(os.path.exists(path))

            lengths = [len(AudioSegment.from_wav(p)) for p in chunks]
            self.assertAlmostEqual(lengths[0], 12000, delta=100)
            self.assertAlmostEqual(lengths[1], 12000, delta=100)
            self.assertAlmostEqual(lengths[2], 1000, delta=100)

    def test_short_audio_gives_one_chunk(self):
        # 5 seconds with 10-minute chunks -> a single chunk, same length
        with tempfile.TemporaryDirectory() as tmp:
            wav = make_wav(os.path.join(tmp, "short.wav"), seconds=5)
            chunks = chunk_audio(wav, chunk_minutes=10)

            self.assertEqual(len(chunks), 1)
            self.assertAlmostEqual(len(AudioSegment.from_wav(chunks[0])),
                                   5000, delta=100)


if __name__ == "__main__":
    unittest.main(verbosity=2)
