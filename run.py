from preswald.main import start_server
import os

script_path = os.environ.get('SCRIPT_PATH', 'hello.py')
port = int(os.environ.get('PORT', 8503))

start_server(script=script_path, port=port)