import re
from collections import defaultdict

from PIL import Image, ImageOps
import pytesseract
from pytesseract import Output


REPLACEMENTS = str.maketrans({
    ",": ".",
    "“": "-",
    "”": "-",
    "‘": "-",
    "’": "-",
    "–": "-",
    "—": "-",
    "−": "-",
})


def normalize_token(text):
    text = text.strip().translate(REPLACEMENTS)
    text = re.sub(r"[^0-9.\-]", "", text)

    # Clean up repeated minus signs
    if text.count("-") > 1:
        text = "-" + text.replace("-", "")

    # Clean up repeated decimal points
    if text.count(".") > 1:
        parts = text.split(".")
        text = parts[0] + "." + "".join(parts[1:])

    return text


def is_number(text):
    return bool(re.fullmatch(r"-?\d+(?:\.\d+)?", text))


def extract_two_lists(image_path, conf_min=10):
    img = Image.open(image_path)
    gray = ImageOps.grayscale(img)

    data = pytesseract.image_to_data(
        gray,
        output_type=Output.DICT,
        config="--oem 3 --psm 6"
    )

    lines = defaultdict(list)
    n = len(data["text"])

    for i in range(n):
        raw = data["text"][i]
        conf_raw = data["conf"][i]
        conf = float(conf_raw) if conf_raw != "-1" else -1.0

        if conf < conf_min:
            continue

        token = normalize_token(raw)
        if not is_number(token):
            continue

        key = (
            data["block_num"][i],
            data["par_num"][i],
            data["line_num"][i],
        )

        lines[key].append({
            "left": data["left"][i],
            "top": data["top"][i],
            "text": token,
        })

    ordered_lines = sorted(
        lines.values(),
        key=lambda row: min(item["top"] for item in row)
    )

    left_col = []
    right_col = []

    for row in ordered_lines:
        row_sorted = sorted(row, key=lambda item: item["left"])

        if len(row_sorted) >= 2:
            left_col.append(float(row_sorted[0]["text"]))
            right_col.append(float(row_sorted[1]["text"]))

    return left_col, right_col


if __name__ == "__main__":
    left, right = extract_two_lists("sample6.png")
    print("Left column:", left)
    print("Right column:", right)