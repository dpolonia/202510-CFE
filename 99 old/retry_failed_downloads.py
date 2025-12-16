#!/usr/bin/env python3
"""
Retry failed downloads until all are successful
"""

import json
import time
from pathlib import Path
from sns_data_downloader_multiformat import SNSMultiFormatDownloader

def get_failed_count():
    """Count failed downloads"""
    log_file = Path("sns_data_multiformat/download_log.json")
    if not log_file.exists():
        return 0

    with open(log_file, 'r') as f:
        log = json.load(f)

    return sum(1 for v in log.values() if v.get('status') == 'failed')

def reset_failed():
    """Reset failed entries so they'll be retried"""
    log_file = Path("sns_data_multiformat/download_log.json")
    if not log_file.exists():
        return 0

    with open(log_file, 'r') as f:
        log = json.load(f)

    failed_count = 0
    failed_items = []
    for key in list(log.keys()):
        if log[key].get('status') == 'failed':
            failed_items.append(key)
            del log[key]
            failed_count += 1

    with open(log_file, 'w') as f:
        json.dump(log, f, indent=2)

    return failed_count, failed_items

def main():
    print("\n" + "="*70)
    print("RETRY FAILED DOWNLOADS - CONTINUOUS MODE")
    print("="*70 + "\n")

    max_attempts = 10
    attempt = 0

    while attempt < max_attempts:
        attempt += 1

        # Check current status
        failed_count = get_failed_count()

        if failed_count == 0:
            print(f"\n{'='*70}")
            print("SUCCESS! All files downloaded successfully!")
            print(f"{'='*70}\n")
            break

        print(f"\nAttempt {attempt}/{max_attempts}")
        print(f"Failed downloads to retry: {failed_count}\n")

        # Reset failed entries
        reset_count, failed_items = reset_failed()
        print(f"Reset {reset_count} failed downloads:")
        for item in failed_items:
            print(f"  - {item}")

        print(f"\nRetrying downloads...\n")

        # Run downloader
        downloader = SNSMultiFormatDownloader(output_dir="sns_data_multiformat")
        downloader.download_all(priorities=[1, 2, 3])

        # Wait a bit before next attempt
        if failed_count > 0 and attempt < max_attempts:
            wait_time = 10
            print(f"\nWaiting {wait_time} seconds before next attempt...")
            time.sleep(wait_time)

    # Final status
    final_failed = get_failed_count()

    with open('sns_data_multiformat/download_log.json', 'r') as f:
        log = json.load(f)

    completed = sum(1 for v in log.values() if v.get('status') == 'completed')

    print(f"\n{'='*70}")
    print("FINAL STATUS")
    print(f"{'='*70}")
    print(f"Completed: {completed}")
    print(f"Failed: {final_failed}")
    print(f"Total: {completed + final_failed}")
    print(f"Success Rate: {completed/(completed+final_failed)*100:.1f}%")
    print(f"{'='*70}\n")

    if final_failed > 0:
        print("Still have some failures. They may be due to:")
        print("  - Network connectivity issues")
        print("  - Server-side problems")
        print("  - Run this script again later to retry")

if __name__ == "__main__":
    main()
