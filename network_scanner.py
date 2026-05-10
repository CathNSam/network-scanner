import socket

target = input("Enter target IP: ")

try:
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))
except ValueError:
    print("Please enter valid numbers.")
    exit()

print(f"\nScanning {target} from port {start_port} to {end_port}...\n")

for port in range(start_port, end_port + 1):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #                            IPV4              TCP

  sock.settimeout(0.5)

  result = sock.connect_ex((target, port))

  try:
    service = socket.getservbyport(port)
  except:
    service = "Unknown"

  print(f"[OPEN] Port {port} - {service}")

  sock.close()

print("\nScan completed.")