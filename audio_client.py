import grpc
import AudioSender_pb2 as service
import AudioSender_pb2_grpc as rpc
import wave
import base64
import os

FILES_TO_SEND = '/home/haris/code/data/files_to_send'
MAX_MESSAGE_LENGTH = 104857600


def encode_audio(FILES_TO_SEND):
    audio_list = []
    for filename in os.listdir(FILES_TO_SEND):
        with wave.open(FILES_TO_SEND + '/' + filename, 'rb') as to_encode:
            length = to_encode.getnframes()
            frames = to_encode.readframes(length)
            encoded_frames = base64.b64encode(frames)

        Audio = service.Audio(audio=encoded_frames,
                              ID=filename)
        audio_list.append(Audio)
    return audio_list


def run():

    # with grpc.insecure_channel('127.0.0.1:5005', options=(('grpc.enable_http_proxy', 0),)) as channel:
    channel = grpc.insecure_channel('localhost:5005', options=[('grpc.enable_http_proxy', 0),
                                                               ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH), ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH), ],)
    stub = rpc.AudioSenderStub(channel)
    audio_iterator = encode_audio(FILES_TO_SEND)
    say = stub.SendAudio(audio_iterator)
    print(say)


if __name__ == '__main__':
    run()
