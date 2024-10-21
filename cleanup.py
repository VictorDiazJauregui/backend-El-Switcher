import os


def cleanup_test_files():
    files_to_delete = ["test.db", ".coverage"]

    for file in files_to_delete:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Error deleting {file}: {e}")
        else:
            print(f"File not found: {file}")


def main():
    print("\nCleaning up test files...")

    cleanup_test_files()


if __name__ == "__main__":
    main()
