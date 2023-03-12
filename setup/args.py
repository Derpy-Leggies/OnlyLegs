"""
Startup arguments for the OnlyLegs gallery

    -p, --port: Port to run on (default: 5000)
    -a, --address: Address to run on (default:0.0.0.0)
    -w, --workers: Number of workers to run (default: 4)
    
    -d, --debug: Run as Flask app in debug mode (default: False)
    -V, --verbose: Show verbose output (default: False)
    -h, --help: Show a help message
"""

import argparse


parser = argparse.ArgumentParser(description='Run the OnlyLegs gallery')
parser.add_argument('-p', '--port', type=int, default=5000, help='Port to run on')
parser.add_argument('-a', '--address', type=str, default='0.0.0.0', help='Address to run on')
parser.add_argument('-w', '--workers', type=int, default=4, help='Number of workers to run')
parser.add_argument('-d', '--debug', action='store_true', help='Run as Flask app in debug mode')
parser.add_argument('-V', '--verbose', action='store_true', help='Show verbose output')
args = parser.parse_args()


PORT = args.port
ADDRESS = args.address
WORKERS = args.workers

DEBUG = args.debug
VERBOSE = args.verbose