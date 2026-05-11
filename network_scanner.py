import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

# =========================
# Argument Parser
# =========================

parser = argparse.ArgumentParser(description="Simple Network Scanner")

parser.add_argument(
    "target",
    help="Target IP address"
)

parser.add_argument(
    "--ports",
    default="1-100",
    help="Port range example: 1-100"
)

parser.add_argument(
    "--banner",
    action="store_true",
    help="Enable banner grabbing"
)

args = parser.parse_args()

target = args.target

# =========================
# Parse Port Range
# =========================

try:
    start_port, end_port = map(int, args.ports.split("-"))

except ValueError:
    print("Invalid port range format. Use example: 1-100")
    exit()

print(f"\nScanning {target} from port {start_port} to {end_port}...\n")


# =========================
# Scan Function
# =========================

def scan_port(port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.settimeout(0.5)

    result = sock.connect_ex((target, port))

    if result == 0:

        try:
            service = socket.getservbyport(port)

        except:
            service = "Unknown"

        banner = ""

        # =========================
        # Banner Grabbing
        # =========================

        if args.banner:

            try:

                # HTTP Request
                if port == 80 or port == 8080:

                    sock.send(
                        b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n"
                    )

                banner = sock.recv(1024).decode(
                    errors="ignore"
                ).strip()

            except:
                pass

        sock.close()

        return {
            "port": port,
            "service": service,
            "banner": banner
        }

    sock.close()

    return None


# =========================
# Multithreading
# =========================

with ThreadPoolExecutor(max_workers=100) as executor:

    ports = range(start_port, end_port + 1)

    results = executor.map(scan_port, ports)


# =========================
# Organize Results
# =========================

sorted_results = sorted(
    [r for r in results if r],
    key=lambda x: x["port"]
)


# =========================
# Output
# =========================

for result in sorted_results:

    print(
        f"[OPEN] Port {result['port']} - {result['service']}"
    )

    if result["banner"]:

        print(
            f"   Banner: {result['banner'][:100]}"
        )

print("\nScan completed.")