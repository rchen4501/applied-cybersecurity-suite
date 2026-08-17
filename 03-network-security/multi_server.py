#!/usr/bin/env python3

import argparse
import functools
import http.server
import pathlib
import socketserver
import threading


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def serve_directory(directory: pathlib.Path, port: int) -> ReusableTCPServer:
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler,
        directory=str(directory),
    )
    httpd = ReusableTCPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Serve the XSS lab on two local origins."
    )
    parser.add_argument("--target-port", type=int, default=8000)
    parser.add_argument("--attacker-port", type=int, default=8001)
    args = parser.parse_args()

    lab_dir = pathlib.Path(__file__).resolve().parent
    servers = [
        serve_directory(lab_dir, args.target_port),
        serve_directory(lab_dir, args.attacker_port),
    ]

    print("XSS lab servers are running.")
    print(f"Target page:   http://127.0.0.1:{args.target_port}/target.html")
    print(f"Attacker page: http://127.0.0.1:{args.attacker_port}/attacker.html")
    print("Press Ctrl+C to stop both servers.")

    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        print("\nStopping servers...")
        for server in servers:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    main()
