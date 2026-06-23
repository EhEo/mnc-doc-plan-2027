#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 줄단위 텍스트 추출기
지정한 PDF에서 페이지별·줄별로 영어 텍스트를 추출해 텍스트 파일로 저장.
"""

import argparse
import sys
from pathlib import Path

import fitz


def extract_lines(page: fitz.Page, min_len: int = 1) -> list[dict]:
    results = []
    blocks = page.get_text("dict")["blocks"]
    for block in blocks:
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            parts = []
            for span in line.get("spans", []):
                txt = span.get("text", "")
                if txt:
                    parts.append(txt)
            line_text = "".join(parts).strip()
            if len(line_text) >= min_len:
                results.append({
                    "text": line_text,
                    "bbox": line.get("bbox"),
                })
    return results


def main():
    ap = argparse.ArgumentParser(description="PDF 줄단위 텍스트 추출")
    ap.add_argument("--pdf", required=True, help="입력 PDF 경로")
    ap.add_argument("--output", required=True, help="출력 텍스트 파일 경로")
    ap.add_argument("--pages", default="all", help="페이지 범위 (예: 4-45, all)")
    ap.add_argument("--min-len", type=int, default=1, help="최소 텍스트 길이 (기본: 1)")
    args = ap.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        sys.exit(f"PDF 파일이 없습니다: {pdf_path}")

    doc = fitz.open(pdf_path)
    total = len(doc)

    if args.pages.lower() == "all":
        page_nums = list(range(total))
    else:
        page_nums = set()
        for chunk in args.pages.split(","):
            chunk = chunk.strip()
            if "-" in chunk:
                a, b = chunk.split("-")
                for p in range(int(a), int(b) + 1):
                    if 1 <= p <= total:
                        page_nums.add(p - 1)
            else:
                p = int(chunk)
                if 1 <= p <= total:
                    page_nums.add(p - 1)
        page_nums = sorted(page_nums)

    print(f"PDF: {pdf_path.name} (총 {total}p, 추출 대상 {len(page_nums)}p)")

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    total_lines = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for pno in page_nums:
            page = doc[pno]
            lines = extract_lines(page, min_len=args.min_len)
            f.write(f"{'=' * 80}\n")
            f.write(f"PAGE {pno + 1}\n")
            f.write(f"{'=' * 80}\n")
            for i, item in enumerate(lines, 1):
                f.write(f"{i:>4} | {item['text']}\n")
            f.write("\n")
            total_lines += len(lines)
            print(f"  p.{pno + 1}: {len(lines)} lines")

    doc.close()
    print(f"\n완료: {out_path} (총 {total_lines}줄)")


if __name__ == "__main__":
    main()
