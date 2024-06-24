import requests
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import signal
import sys
import os


openapi_endpoint = "http://localhost:11434/v1"
auth_token = "ollama"
model = "llama3:70b"

# Define the directory where the content is located
files_directory = "."

# Load files from the file system
files = {}
for filename in os.listdir(files_directory):
    if '.txt' in filename: # we only care about .txt files
        with open(os.path.join(files_directory, filename), 'r') as file:
            files[filename] = file.read()
system_prompt = """
You will act as a http server for www.personalblog.com. You will get requests and will respond, but only with the body, the rest I will take care of. The representation you use is determined by the request. The content you send back is determined by the path. The style of the pages should be dark and mysterious. You will choose content based on the files available under the Files section.

### Files

"""

for filename, content in files.items():
    system_prompt += f'File: {filename}\n{content}'


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if '/favicon.ico' in self.path:
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(get_body_content(self.command, self.path, self.headers), "utf-8"))

def run(server_class=HTTPServer, handler_class=MyServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Server stopped by user.')
        httpd.server_close()


def get_body_content(method, path, headers):
    if method == 'GET':
        response = fetch_from_llm(method, path, ','.join(headers.get_all('accept', ())))

        # Sometimes the LLM adds a bit of extra, let's try and extract what we want
        try:
            response_text = response.split('<html>')[1].split('</html>')[0]
        except IndexError:
            response_text = response

        # Return the response text wrapped in HTML
        return f"{response_text}"
    pass



def fetch_from_llm(method, path, accept):
    prompt = f"{method} {path} HTTP/1.1\r\nAccept: {accept}\r\n\r\n"
    print(prompt)
    messages = [
         {"role": "system", "content": system_prompt},
         {"role": "user", "content": prompt}
    ]
    response = requests.post(f"{openapi_endpoint}/chat/completions",
                         headers={
                              "Content-Type": "application/json",
                              "Accept": "application/json",
                              "Authorization": f"Bearer {auth_token}"
                         },
                         data=json.dumps({
                            "model": f"{model}",
                            "messages": messages,
                            "max_tokens": 1000,
                        }))

    # Check if the request was successful
    if response.status_code == 200:
        data = json.loads(response.content)
        print(data)
        return data['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    run()
