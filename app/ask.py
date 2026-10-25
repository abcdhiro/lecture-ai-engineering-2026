"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(chat, question: str) -> str:
    response = chat.send_message(question)

    # 入力トークン数と出力トークン数を表示（第1回 演習）
    usage = response.usage_metadata
    print(
        f"[tokens] 入力: {usage.prompt_token_count} / "
        f"出力: {usage.candidates_token_count}"
    )

    return response.text



def main() -> None:
    client = genai.Client(api_key=get_api_key())
    chat = client.chats.create(model=MODEL)

    print(f"[model] {MODEL}")
    print("会話を始めます。終了するには exit と入力するか、空のままEnterを押してください。\n")

    while True:
        question = input("あなた> ").strip()
        if question == "" or question.lower() == "exit":
            print("会話を終了します。")
            break

        try:
            print(f"\nAI> {ask(chat, question)}\n")
        except errors.APIError as e:
            print(api_error_message(e.code, e.message))
            continue


if __name__ == "__main__":
    main()