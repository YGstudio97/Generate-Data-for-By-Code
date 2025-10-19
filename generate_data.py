# generate_data.py
# Generates data up to a user-specified file size (in TB/GB/MB/KB/Bytes)
# By YGstudio97 — Open Source (OS)

import random
import os
import time
import sys

# Configuration
OUTPUT_FILE = "data.txt"
PROGRESS_EVERY = 10_000_000  # Show progress every 10M lines

base_pairs = [
    ("hello", "Hi there! How can I help you?"),
    ("who made you", "I was created by YGstudio97."),
    ("about", "I'm a local offline AI powered by YGstudio97."),
    ("help", "You can ask me anything about my creator or myself."),
    ("what is ai", "AI means Artificial Intelligence — machines that can learn."),
    ("what is python", "Python is a high-level programming language great for AI work."),
    ("goodbye", "See you again! — from YGstudio97"),
]

WORDS = [
    "data", "science", "python", "machine", "learning", "AI", "chatbot",
    "knowledge", "model", "system", "logic", "math", "smart", "neural",
    "compute", "training", "memory", "dataset", "function", "code", "analysis",
    "algorithm", "network", "intelligence", "robot", "automation", "pattern",
    "prediction", "statistics", "framework", "library", "developer", "engineer"
]

# Estimate average line length (in bytes) based on sample
# Format: "question noise | answer noise\n"
# We'll measure a few samples to get a realistic avg
def estimate_avg_line_size(samples=1000):
    total = 0
    for _ in range(samples):
        q, a = random.choice(base_pairs)
        noise = " ".join(random.choices(WORDS, k=random.randint(6, 12))).capitalize() + "."
        line = f"{q} {noise} | {a} {noise}\n"
        total += len(line.encode('utf-8'))
    return total / samples

def random_sentence():
    length = random.randint(6, 12)
    return " ".join(random.choices(WORDS, k=length)).capitalize() + "."

def get_target_bytes():
    print("\n" + "="*50)
    print("Data Generator | by YGstudio97 — Open Source (OS)")
    print("="*50)

    while True:
        try:
            size_input = input("Enter File Data Size: ").strip()
            if not size_input:
                print("❌ Input cannot be empty. Please enter a number.")
                continue
            size_value = float(size_input)
            if size_value <= 0:
                print("❌ Size must be greater than 0.")
                continue
            break
        except ValueError:
            print("❌ Invalid number. Please enter a numeric value (e.g., 5.5).")

    units = {"TB": 1024**4, "GB": 1024**3, "MB": 1024**2, "KB": 1024, "BYTES": 1}
    print("\nSelect Size Format:")
    print("[1] TB (Terabytes)")
    print("[2] GB (Gigabytes)")
    print("[3] MB (Megabytes)")
    print("[4] KB (Kilobytes)")
    print("[5] Bytes")

    while True:
        choice = input("Choose option (1-5): ").strip()
        unit_map = {'1': 'TB', '2': 'GB', '3': 'MB', '4': 'KB', '5': 'BYTES'}
        if choice in unit_map:
            unit = unit_map[choice]
            target_bytes = int(size_value * units[unit])
            break
        else:
            print("❌ Invalid choice. Please select 1–5.")

    # Confirmation loop
    while True:
        confirm = input(f"\nYou sure to create a ~{size_value} {unit} file? (Type 'Yes', 'No', or 'back'): ").strip().lower()
        if confirm == 'yes':
            return target_bytes
        elif confirm == 'no':
            print("❌ Operation cancelled by user.")
            sys.exit(0)
        elif confirm == 'back':
            return None  # Go back to start
        else:
            print("❌ Please type 'Yes', 'No', or 'back'.")

def generate_until_size(target_bytes):
    avg_line_size = estimate_avg_line_size()
    estimated_lines = max(1, int(target_bytes / avg_line_size))
    print(f"\n📊 Estimated lines needed: {estimated_lines:,} (avg line: {avg_line_size:.1f} bytes)")

    print(f"🚀 Starting generation up to ~{target_bytes / (1024**3):.2f} GB in '{OUTPUT_FILE}'")
    print("⚠️  WARNING: This may take a long time and use significant disk space!")
    print("Press Ctrl+C to stop safely at any time.\n")

    start_time = time.time()
    line_count = 0

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8", buffering=1024*1024) as f:
            while True:
                q, a = random.choice(base_pairs)
                noise = random_sentence()
                line = f"{q} {noise} | {a} {noise}\n"
                f.write(line)
                line_count += 1

                # Check file size every 1M lines to avoid constant I/O overhead
                if line_count % 1_000_000 == 0:
                    current_size = os.path.getsize(OUTPUT_FILE)
                    if current_size >= target_bytes:
                        break

                # Progress report
                if line_count % PROGRESS_EVERY == 0:
                    elapsed = time.time() - start_time
                    lines_per_sec = line_count / elapsed if elapsed > 0 else 0
                    print(
                        f"[{line_count:,} lines] | "
                        f"Speed: {lines_per_sec:,.0f} lines/sec | "
                        f"Elapsed: {elapsed/60:.1f} min"
                    )

        # Final stats
        final_size = os.path.getsize(OUTPUT_FILE)
        final_size_gb = final_size / (1024**3)
        total_time = time.time() - start_time
        print(f"\n✅ Done! {line_count:,} lines written.")
        print(f"📁 Final file size: {final_size_gb:.2f} GB ({final_size:,} bytes)")
        print(f"⏱️  Total time: {total_time/60:.1f} minutes")

    except KeyboardInterrupt:
        print(f"\n🛑 Stopped by user at {line_count:,} lines.")
        if os.path.exists(OUTPUT_FILE):
            size = os.path.getsize(OUTPUT_FILE) / (1024**3)
            print(f"📄 Partial file saved as '{OUTPUT_FILE}' (~{size:.2f} GB)")

def main():
    while True:
        target = get_target_bytes()
        if target is None:
            continue  # Go back to input
        else:
            generate_until_size(target)
            break

if __name__ == "__main__":
    main()
