from cia import receiver, sender


EXAMPLES = [
    {
        "name": "Example 1",
        "key": "ElliotSimpsons",
        "message": "HelloWorld",
        "expected_output": "10::HelloWorldQAWVBWXLOBDTRW",
    },
    {
        "name": "Example 2",
        "key": "LockAndKey",
        "message": "abort",
        "expected_output": "5::abortSYMLKCRW",
    },
]


def run_examples():
    failures = 0

    for example in EXAMPLES:
        actual_output = sender(example["message"], example["key"])
        output_matches = actual_output == example["expected_output"]
        receiver_accepts = receiver(actual_output, example["key"])

        print(example["name"])
        print(f"Running Key: {example['key']}")
        print(f"Message: {example['message']}")
        print(f"Expected Output: {example['expected_output']}")
        print(f"Actual Output:   {actual_output}")
        print(f"Output Match:    {'PASS' if output_matches else 'FAIL'}")
        print(f"Receiver Check:  {'PASS' if receiver_accepts else 'FAIL'}")
        print()

        if not output_matches or not receiver_accepts:
            failures += 1

    if failures:
        print(f"{failures} example test(s) failed.")
        raise SystemExit(1)

    print("All example tests passed.")


if __name__ == "__main__":
    run_examples()
