import http.server
import socketserver
import requests
import json

url = "https://api.chucknorris.io/jokes/random"

def getJoke(jokes):
    while True:
        response = requests.get(url)
        joke = response.json()
        if joke['id'] not in jokes:
            jokes.add(joke['id'])
            return {'id': joke['id'], 'url': joke['url']}

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            jokes = set()
            jokesList = []

            for _ in range(25):
                joke = getJoke(jokes)
                jokesList.append(joke)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(jokesList).encode())
        else:
            self.send_response(404)

with socketserver.TCPServer(("", 8080), Handler) as httpd:
    print(":) Serving at port :)", 8080)
    httpd.serve_forever()