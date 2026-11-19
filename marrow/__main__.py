from marrow.runner import awake, sleep

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "sleep":
        print(sleep())
    else:
        print(awake(" ".join(sys.argv[1:]) or "cycle"))
