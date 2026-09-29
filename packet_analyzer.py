from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw
from datetime import datetime

packet_count = 0


def analyze_packet(packet):
    global packet_count

    if IP not in packet:
        return

    packet_count += 1

    source_ip = packet[IP].src
    destination_ip = packet[IP].dst

    # Identify protocol and ports
    if TCP in packet:
        protocol = "TCP"
        source_port = packet[TCP].sport
        destination_port = packet[TCP].dport

    elif UDP in packet:
        protocol = "UDP"
        source_port = packet[UDP].sport
        destination_port = packet[UDP].dport

    elif ICMP in packet:
        protocol = "ICMP"
        source_port = "-"
        destination_port = "-"

    else:
        protocol = str(packet[IP].proto)
        source_port = "-"
        destination_port = "-"

    # Get limited packet payload information
    if Raw in packet:
        payload = bytes(packet[Raw].load)
        payload_preview = payload[:32].hex()

        if len(payload) > 32:
            payload_preview += "..."
    else:
        payload_preview = "No application payload"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n" + "=" * 65)
    print(f"PACKET #{packet_count}")
    print("=" * 65)

    print(f"Timestamp        : {timestamp}")
    print(f"Source IP        : {source_ip}")
    print(f"Destination IP   : {destination_ip}")
    print(f"Protocol         : {protocol}")
    print(f"Source Port      : {source_port}")
    print(f"Destination Port : {destination_port}")
    print(f"Packet Length    : {len(packet)} bytes")
    print(f"Packet Data      : {payload_preview}")


print("=" * 65)
print("             NETWORK PACKET ANALYZER")
print("=" * 65)
print("Starting packet capture...")
print("Press Ctrl+C to stop.")

sniff(prn=analyze_packet, store=False)