import time

import opencc as opencc
import torch
from librosa import load
CONVERTER_T2S = opencc.OpenCC("t2s.json")
CONVERTER_S2T = opencc.OpenCC("s2t.json")
def do_st_corrections(text: str) -> str:
    simplified = CONVERTER_T2S.convert(text)
    return CONVERTER_S2T.convert(simplified)
def transcribe(file,lang='chinese'):
    torch.cuda.empty_cache()
    start_time = time.time()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    processor = torch.load('ASR/whisper/processor.pt')
    model = torch.load('ASR/whisper/model.pt').to(device)
    model.config.forced_decoder_ids = None
    forced_decoder_ids = processor.get_decoder_prompt_ids(language=lang,task="transcribe")
    audio, sr = load(file, sr=16_000, mono=True)
    size=25*sr
    audio_tensor = torch.tensor(audio)
    audio_tensor=torch.split(audio_tensor,size)

    transcriptions=""
    for i in audio_tensor:
        input_features = processor(i, sampling_rate=sr, return_tensors="pt").input_features.to(device)
        with torch.no_grad():
            predicted_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids,max_length=448)
        # decode token ids to text
        transcription = processor.batch_decode(predicted_ids,skip_special_tokens=True)
        transcriptions+=do_st_corrections(transcription[0])
    end_time = time.time()
    elapsed_time = end_time - start_time
    torch.cuda.empty_cache()
    print(f"經過時間：{elapsed_time:.2f}秒")
    return transcriptions
