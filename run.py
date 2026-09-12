"""
Tradenza International - Application Launcher
"""
import sys
import os
import socket

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

if __name__ == '__main__':
    from app import app, database
    database.init_db()

    # Find available port starting at 5000
    port = 5000
    while is_port_in_use(port) and port < 5010:
        port += 1

    print("=" * 60)
    print("Tradenza International Private Limited - Web Platform")
    print(f"Server URL: http://127.0.0.1:{port}")
    print(f"Admin URL:  http://127.0.0.1:{port}/admin")
    print("=" * 60)
    app.run(host='0.0.0.0', port=port, debug=False)
