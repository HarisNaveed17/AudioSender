import grpc
import AudioSender_pb2 as service
import AudioSender_pb2_grpc as rpc
import base64
import os
from scipy.io.wavfile import read

FILES_TO_SEND = '/home/haris/code/data/files_to_send'
MAX_MESSAGE_LENGTH = 104857600


def encode_audio(FILES_TO_SEND):
    audio_list = []
    for filename in os.listdir(FILES_TO_SEND):
        file_path = f'{FILES_TO_SEND}/{filename}'
        sr, data = read(file_path)
        encoded_data = base64.b64encode(data)
        Audio = service.Audio(audio=encoded_data,
                              ID=filename, samplerate=sr)
        audio_list.append(Audio)
    return audio_list


def generate_stream(audio_files):
    for file in audio_files:
        yield file


def run():

    # with grpc.insecure_channel('127.0.0.1:5005', options=(('grpc.enable_http_proxy', 0),)) as channel:
    channel = grpc.insecure_channel('localhost:5005', options=[('grpc.enable_http_proxy', 0),
                                                               ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH), ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH), ],)
    stub = rpc.AudioSenderStub(channel)
    encoded_audios = encode_audio(FILES_TO_SEND)
    audio_iterator = generate_stream(encoded_audios)

    say = stub.SendAudio(audio_iterator)
    print(say)


if __name__ == '__main__':
    run()
