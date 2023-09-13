import argparse


def main():
    # 実行引数で指定されたファイルを読み込む
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="specify file path")
    args = parser.parse_args()
    with open(args.file) as f:
        print(f.read())


if __name__ == "__main__":
    main()
