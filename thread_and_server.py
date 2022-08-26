import random
import time
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer


class DropsHTTPRequestHandler(SimpleHTTPRequestHandler):
    record_provider: any

    def do_GET(self):
        if self.path == '/':
            try:
                self.send_response(200)
            except:
                self.send_response(404)
        self.end_headers()
        self.wfile.write(
            bytes(f'Result {DropsHTTPRequestHandler.record_provider.record}', 'utf-8')
        )


class Drops:

    def __init__(self):
        super().__init__()
        self.record = -1
        self.is_stopped = False

    def run(self):
        while not self.is_stopped:
            time.sleep(1)
            self.record = random.gauss(1, 5)
            print(f'Thread is calculating {self.record}')

    def serve_app(self, host: str, port: int):
        DropsHTTPRequestHandler.record_provider = self
        httpd = HTTPServer((host, port), DropsHTTPRequestHandler)
        thread = threading.Thread(target=self.run)
        try:
            thread.start()
            httpd.serve_forever()
        except KeyboardInterrupt as kbd:
            print(kbd)

    def stop(self):
        self.is_stopped = True


# def serve_app(app: Drops, host: str, port: int):
#     DropsHTTPRequestHandler.record_provider = app
#     httpd = HTTPServer((host, port), DropsHTTPRequestHandler)
#     thread = threading.Thread(target=app.run)
#     try:
#         thread.start()
#         httpd.serve_forever()
#     except KeyboardInterrupt as kbd:
#         print(kbd)


if __name__ == '__main__':
    app = Drops()
    app.serve_app(host='localhost', port=8081)
    app.stop()
