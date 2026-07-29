#!/usr/bin/env python3
"""Check the STM32 serial stream without starting ROS 2."""

import argparse
import os
import sys
import time
from collections import Counter

try:
    import serial
except ImportError:
    print("pyserial is not installed: sudo apt install python3-serial", file=sys.stderr)
    raise SystemExit(2)


def classify(line):
    if "ODOM" in line:
        return "ODOM"
    if "WHEEL" in line:
        return "WHEEL"
    if "IMU" in line:
        return "IMU"
    if "TOF" in line:
        return "TOF"
    if line.startswith("STATE,"):
        return "STATE"
    return "UNKNOWN"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Read and display the raw STM32 serial stream.",
    )
    parser.add_argument("--port", default="/dev/stm32_link")
    parser.add_argument("--baud", type=int, default=230400)
    parser.add_argument(
        "--duration",
        type=float,
        default=0.0,
        help="Seconds to run; 0 means until Ctrl+C.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=0.2,
        help="Serial read timeout in seconds.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if not os.path.exists(args.port):
        print(f"ERROR: serial device does not exist: {args.port}", file=sys.stderr)
        print("Check: ls -l /dev/stm32_link /dev/ttyACM* /dev/ttyUSB*", file=sys.stderr)
        return 2

    try:
        stm = serial.Serial(
            port=args.port,
            baudrate=args.baud,
            timeout=args.timeout,
        )
    except serial.SerialException as error:
        print(f"ERROR: cannot open {args.port}: {error}", file=sys.stderr)
        print("Stop bringup_node if it is already using the port.", file=sys.stderr)
        return 3

    counts = Counter()
    started = time.monotonic()
    report_started = started
    report_lines = 0
    received_bytes = 0

    print(f"OPEN: {args.port} @ {args.baud} baud")
    print("Waiting for STM32 lines; press Ctrl+C to stop.")

    try:
        stm.reset_input_buffer()
        while args.duration <= 0 or time.monotonic() - started < args.duration:
            raw = stm.readline()
            if not raw:
                continue

            received_bytes += len(raw)
            line = raw.decode("utf-8", errors="replace").strip()
            kind = classify(line)
            counts[kind] += 1
            report_lines += 1

            elapsed = time.monotonic() - started
            print(f"[{elapsed:8.3f}s] {kind:7s} | {line}")

            now = time.monotonic()
            if now - report_started >= 1.0:
                rate = report_lines / (now - report_started)
                summary = " ".join(f"{key}={value}" for key, value in sorted(counts.items()))
                print(f"--- rate={rate:.1f} lines/s total_bytes={received_bytes} {summary}")
                report_started = now
                report_lines = 0
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except serial.SerialException as error:
        print(f"\nERROR: serial connection lost: {error}", file=sys.stderr)
        return 4
    finally:
        stm.close()

    elapsed = time.monotonic() - started
    summary = " ".join(f"{key}={value}" for key, value in sorted(counts.items()))
    print(f"RESULT: elapsed={elapsed:.1f}s bytes={received_bytes} {summary or 'no data'}")
    return 0 if received_bytes else 1


if __name__ == "__main__":
    raise SystemExit(main())
