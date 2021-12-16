from concurrent import futures
import grpc
import AudioSender_pb2 as service
import AudioSender_pb2_grpc as rpc
import base64
import wave

MAX_MESSAGE_LENGTH = 104857600


def save_audio(encoded_audio, ID):
    decoded_audio = base64.b64decode(encoded_audio)
    with wave.open(ID, 'wb') as decoded_file:
        decoded_file.writeframes(decoded_audio)
    return 1


class AudioSenderServicer(rpc.AudioSenderServicer):
    def SendAudio(self, request_iterator, context):
        for request in request_iterator:
            pt = save_audio(encoded_audio=request.audio, ID=request.ID)
            if pt == 1:
                continue
            else:
                return service.Response(ack='ERROR')
        return service.Response(ack='All files received!')


def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=12), options=[
        ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH), ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH), ],)
    rpc.add_AudioSenderServicer_to_server(
        AudioSenderServicer(), server)
    print('Starting server. Listening on port 5005.')
    server.add_insecure_port('localhost:5005')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    server()
