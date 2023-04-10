import json
import requests
import wave

class VcGenerator:
    def __init__(self):
        self.spaeker = 1
    def set_speaker(self, value):
        self.speaker = value
    def get_speaker(self):
        return self.speaker
    def generate_wav(self, text, filepath='./output.wav'):
        print(f"{self.speaker}:{text}")
        host = 'localhost'
        port = 50021
        params = (
            ('text', text),
            ('speaker', self.speaker),
        )
        response1 = requests.post(
            f'http://{host}:{port}/audio_query',
            params=params,
        )
        headers = {'Content-Type': 'application/json',}
        vc_data = response1.json()
        vc_data['speedScale'] = 1.0
        vc_data['pitchScale'] = 0
        response2 = requests.post(
            f'http://{host}:{port}/synthesis',
            headers=headers,
            params=params,
            data=json.dumps(vc_data)
        )

        wf = wave.open(filepath, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(response2.content)
        wf.close()
