import sounddevice as sd
import numpy as np
import wave
import os
from funasr import AutoModel

model = AutoModel(
    model="FunAudioLLM/Fun-ASR-Nano-2512",
    device="cuda",
    disable_update=True,
    trust_remote_code=True
)


def record_once(sample_rate=16000, silence_threshold=500, silence_duration=0.5):
    audio_chunks = []
    silent_samples = 0
    chunk_size = 1024

    with sd.InputStream(samplerate=sample_rate, channels=1, dtype='int16') as stream:
        print("Listening...")

        while True:
            chunk, _ = stream.read(chunk_size)
            if np.max(np.abs(chunk)) > silence_threshold:
                audio_chunks.append(chunk.copy())
                break

        while True:
            chunk, _ = stream.read(chunk_size)
            audio_chunks.append(chunk.copy())
            if np.max(np.abs(chunk)) < silence_threshold:
                silent_samples += chunk_size
                if silent_samples >= silence_duration * sample_rate:
                    break
            else:
                silent_samples = 0

    audio_data = np.concatenate(audio_chunks)

    temp_filename = "temp_recording.wav"
    with wave.open(temp_filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

    try:
        res = model.generate(input=[temp_filename], cache={}, batch_size=1)

        if isinstance(res, list) and len(res) > 0:
            item = res[0]
            if isinstance(item, dict):
                return item.get("text", "").strip()
            elif isinstance(item, list) and len(item) > 0 and isinstance(item[0], dict):
                return item[0].get("text", "").strip()
        return ""

    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


if __name__ == "__main__":
    print(record_once())