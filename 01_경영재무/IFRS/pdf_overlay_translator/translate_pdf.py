#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Overlay Translator
======================
원본 PDF의 텍스트 박스 위치 그대로 베트남어(또는 다른 언어)로 오버레이 번역.

사용 예:
    python translate_pdf.py --pdf input.pdf --pages 4-45 --output ch1_vi.pdf
    python translate_pdf.py --pdf input.pdf --pages all --provider claude
    python translate_pdf.py --pdf input.pdf --pages 60-101 --provider deepl --target vi

지원 번역 제공사:
    - claude  (Anthropic API)
    - deepl   (DeepL API)
    - google  (Google Cloud Translation API)
    - none    (오프라인 검증 모드 - 원본 텍스트 그대로 유지)

설정:
    config.yaml 파일에 API 키를 넣으세요 (config.yaml.example 참조).

작동 방식:
    1. PyMuPDF로 페이지별 텍스트 스팬과 bounding box 추출
    2. 캐시 확인 → 미번역 항목만 API 호출
    3. 원본 텍스트 위에 흰색 사각형으로 마스킹
    4. 동일 위치에 번역문 삽입 (박스 폭/높이에 맞춰 폰트 자동 축소)
    5. 진행 상황을 cache.json에 즉시 기록 → 중단 후 재실행 가능
"""

from __future__ import annotations
import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

import fitz  # PyMuPDF


# ============================================================
# 설정 로드
# ============================================================
def load_config(config_path: Path) -> dict:
    """config.yaml 파일에서 API 키 등 로드. PyYAML 의존성 없이 간단 파서."""
    if not config_path.exists():
        return {}
    cfg = {}
    for line in config_path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            k, v = line.split(':', 1)
            cfg[k.strip()] = v.strip().strip('"').strip("'")
    return cfg


# ============================================================
# 캐시
# ============================================================
class TranslationCache:
    """원문→번역문 캐시. 같은 텍스트는 한 번만 번역."""

    def __init__(self, cache_path: Path):
        self.path = cache_path
        if cache_path.exists():
            self.data = json.loads(cache_path.read_text(encoding='utf-8'))
        else:
            self.data = {}
        self.dirty = False

    def get(self, key: str) -> Optional[str]:
        return self.data.get(key)

    def set(self, key: str, value: str):
        self.data[key] = value
        self.dirty = True

    def save(self):
        if self.dirty:
            self.path.write_text(
                json.dumps(self.data, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )
            self.dirty = False


# ============================================================
# 번역 백엔드
# ============================================================
def translate_with_claude(texts: list[str], target_lang: str, api_key: str,
                          model: str = 'claude-sonnet-4-6') -> list[str]:
    """Claude API로 배치 번역."""
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)

    lang_name = {
        'vi': 'Vietnamese', 'ko': 'Korean', 'en': 'English',
        'zh': 'Chinese', 'ja': 'Japanese'
    }.get(target_lang, target_lang)

    numbered = "\n".join(f"[{i+1}] {t}" for i, t in enumerate(texts))
    prompt = (
        f"Translate the following numbered English texts into {lang_name}.\n"
        f"These are slide texts from an IFRS accounting course. Keep accounting "
        f"terminology accurate (use standard IFRS/VAS terms in {lang_name}).\n"
        f"Output ONLY the translations in the same numbered format. "
        f"Do not add explanations.\n\n"
        f"{numbered}"
    )

    resp = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    out = resp.content[0].text

    # [1] xxx / [2] yyy ... 파싱
    result = [""] * len(texts)
    for line in out.splitlines():
        m = re.match(r'^\[(\d+)\]\s*(.+)', line.strip())
        if m:
            idx = int(m.group(1)) - 1
            if 0 <= idx < len(texts):
                result[idx] = m.group(2).strip()
    # 빈 항목 fallback - 원문 유지
    for i, t in enumerate(result):
        if not t:
            result[i] = texts[i]
    return result


def translate_with_deepl(texts: list[str], target_lang: str, api_key: str) -> list[str]:
    """DeepL API로 배치 번역."""
    import requests
    target = {'vi': 'VI', 'ko': 'KO', 'en': 'EN-US', 'zh': 'ZH', 'ja': 'JA'}.get(
        target_lang, target_lang.upper())
    url = 'https://api.deepl.com/v2/translate' if not api_key.endswith(':fx') \
        else 'https://api-free.deepl.com/v2/translate'
    headers = {'Authorization': f'DeepL-Auth-Key {api_key}'}
    data = [('target_lang', target), ('source_lang', 'EN')]
    data += [('text', t) for t in texts]
    r = requests.post(url, headers=headers, data=data, timeout=30)
    r.raise_for_status()
    return [item['text'] for item in r.json()['translations']]


def translate_with_google(texts: list[str], target_lang: str, api_key: str) -> list[str]:
    """Google Cloud Translation API v2로 배치 번역."""
    import requests
    url = f'https://translation.googleapis.com/language/translate/v2?key={api_key}'
    payload = {
        'q': texts, 'target': target_lang, 'source': 'en', 'format': 'text'
    }
    r = requests.post(url, json=payload, timeout=30)
    r.raise_for_status()
    return [item['translatedText'] for item in r.json()['data']['translations']]


def translate_offline(texts: list[str], target_lang: str, api_key: str) -> list[str]:
    """검증 모드 - 원문 그대로 반환 (오프라인 동작 확인용)."""
    return [f"[{target_lang}] {t}" for t in texts]


PROVIDERS = {
    'claude': translate_with_claude,
    'deepl': translate_with_deepl,
    'google': translate_with_google,
    'none': translate_offline,
}


# ============================================================
# 텍스트 박스 추출 + 오버레이
# ============================================================
@dataclass
class TextSpan:
    page: int
    bbox: tuple  # (x0, y0, x1, y1)
    text: str
    font_size: float
    color: int  # RGB int


def extract_spans(page: fitz.Page, min_len: int = 2) -> list[TextSpan]:
    """페이지에서 줄 단위 텍스트 스팬 추출."""
    spans = []
    blocks = page.get_text("dict")["blocks"]
    for block in blocks:
        if block.get("type") != 0:  # 0 = text block
            continue
        for line in block.get("lines", []):
            # 한 줄을 하나의 단위로 합치기
            line_text = ""
            line_bbox = None
            max_size = 0
            colors = []
            for span in line.get("spans", []):
                txt = span.get("text", "")
                if not txt:
                    continue
                line_text += txt
                bbox = span.get("bbox", (0, 0, 0, 0))
                if line_bbox is None:
                    line_bbox = list(bbox)
                else:
                    line_bbox[0] = min(line_bbox[0], bbox[0])
                    line_bbox[1] = min(line_bbox[1], bbox[1])
                    line_bbox[2] = max(line_bbox[2], bbox[2])
                    line_bbox[3] = max(line_bbox[3], bbox[3])
                max_size = max(max_size, span.get("size", 10))
                colors.append(span.get("color", 0))

            line_text = line_text.strip()
            if len(line_text) >= min_len and line_bbox:
                spans.append(TextSpan(
                    page=page.number,
                    bbox=tuple(line_bbox),
                    text=line_text,
                    font_size=max_size,
                    color=colors[0] if colors else 0,
                ))
    return spans


def group_spans_for_translation(spans: list[TextSpan], max_chars: int = 200) -> list[list[int]]:
    """근접한 스팬들을 묶어서 API 배치 호출 단위 생성.
    너무 짧은 단편 번역은 컨텍스트가 없어 품질이 떨어지므로 그룹화."""
    groups = []
    cur = []
    cur_len = 0
    for i, s in enumerate(spans):
        cur.append(i)
        cur_len += len(s.text)
        if cur_len >= max_chars:
            groups.append(cur)
            cur = []
            cur_len = 0
    if cur:
        groups.append(cur)
    return groups


def overlay_translation(page: fitz.Page, span: TextSpan, translated: str,
                        font: fitz.Font, white_mask: bool = True):
    """원본 텍스트 위에 마스킹 후 번역문 삽입."""
    x0, y0, x1, y1 = span.bbox
    w = x1 - x0
    h = y1 - y0

    # 1) 원본 텍스트를 흰색 사각형으로 가림
    if white_mask:
        rect = fitz.Rect(x0 - 0.5, y0 - 0.5, x1 + 0.5, y1 + 0.5)
        page.draw_rect(rect, color=None, fill=(1, 1, 1), overlay=True)

    # 2) 폰트 크기 자동 조정 - 번역문이 박스 폭을 넘으면 축소
    font_size = span.font_size
    text_width = font.text_length(translated, font_size)
    min_size = max(6.0, span.font_size * 0.5)

    while text_width > w * 1.05 and font_size > min_size:
        font_size -= 0.5
        text_width = font.text_length(translated, font_size)

    # 3) 색상 변환 (int → RGB tuple)
    c = span.color
    color = ((c >> 16) & 0xff) / 255, ((c >> 8) & 0xff) / 255, (c & 0xff) / 255

    # 4) 번역문 삽입
    insert_point = fitz.Point(x0, y1 - max(0.5, h * 0.15))
    try:
        page.insert_text(
            insert_point, translated,
            fontname=font.name, fontfile=None,
            fontsize=font_size, color=color, overlay=True,
        )
    except Exception:
        # 폰트 미등록 시 fallback - 페이지에 폰트 등록 후 재시도
        page.insert_font(fontname=font.name, fontbuffer=font.buffer)
        page.insert_text(
            insert_point, translated,
            fontname=font.name, fontsize=font_size, color=color, overlay=True,
        )


# ============================================================
# 페이지 범위 파싱
# ============================================================
def parse_pages(spec: str, total: int) -> list[int]:
    """'4-45' / '4,7,9' / '4-45,60-101' / 'all' → [3, 4, ..., 44] (0-indexed)"""
    if spec.lower() == 'all':
        return list(range(total))
    pages = set()
    for chunk in spec.split(','):
        chunk = chunk.strip()
        if '-' in chunk:
            a, b = chunk.split('-')
            for p in range(int(a), int(b) + 1):
                if 1 <= p <= total:
                    pages.add(p - 1)
        else:
            p = int(chunk)
            if 1 <= p <= total:
                pages.add(p - 1)
    return sorted(pages)


# ============================================================
# 폰트 로드
# ============================================================
def load_font(font_path: Optional[str]) -> fitz.Font:
    """베트남어/한국어 지원 폰트 로드. 기본은 Noto Sans."""
    if font_path and Path(font_path).exists():
        return fitz.Font(fontfile=font_path, fontname="VietFont")
    # 시스템 폰트 fallback - Windows
    for candidate in [
        r'C:\Windows\Fonts\malgun.ttf',
        r'C:\Windows\Fonts\NotoSans-Regular.ttf',
        '/Library/Fonts/Arial Unicode.ttf',
        '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf',
    ]:
        if Path(candidate).exists():
            return fitz.Font(fontfile=candidate, fontname="VietFont")
    # 최후 - PyMuPDF 내장 폰트 (Vietnamese 일부 미지원 가능)
    return fitz.Font("helv")


# ============================================================
# 메인 파이프라인
# ============================================================
def main():
    ap = argparse.ArgumentParser(
        description='PDF Overlay Translator — 원본 PDF 양식 유지하면서 본문만 번역',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument('--pdf', required=True, help='입력 PDF 경로')
    ap.add_argument('--pages', default='all', help='페이지 범위 (예: 4-45, 4,7,9, all)')
    ap.add_argument('--output', required=True, help='출력 PDF 경로')
    ap.add_argument('--target', default='vi', help='대상 언어 코드 (기본: vi)')
    ap.add_argument('--provider', default='claude',
                    choices=list(PROVIDERS.keys()), help='번역 제공사')
    ap.add_argument('--config', default='config.yaml', help='설정 파일 경로')
    ap.add_argument('--cache', default='cache.json', help='번역 캐시 파일')
    ap.add_argument('--font', default=None, help='베트남어 지원 폰트 .ttf 경로')
    ap.add_argument('--model', default='claude-sonnet-4-6',
                    help='Claude 모델명 (provider=claude일 때)')
    ap.add_argument('--rate-limit', type=float, default=0.5,
                    help='API 호출 사이 대기시간 (초)')
    ap.add_argument('--dry-run', action='store_true',
                    help='텍스트 추출만 하고 번역·출력 생략')
    args = ap.parse_args()

    # 설정 로드
    cfg = load_config(Path(args.config))
    api_key_map = {
        'claude': cfg.get('claude_api_key') or os.getenv('ANTHROPIC_API_KEY', ''),
        'deepl': cfg.get('deepl_api_key') or os.getenv('DEEPL_API_KEY', ''),
        'google': cfg.get('google_api_key') or os.getenv('GOOGLE_API_KEY', ''),
        'none': '',
    }
    api_key = api_key_map[args.provider]
    if args.provider != 'none' and not api_key and not args.dry_run:
        sys.exit(f"❌ {args.provider} API 키가 설정되지 않았습니다. "
                 f"config.yaml 또는 환경변수를 확인하세요.")

    # PDF 로드
    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        sys.exit(f"❌ PDF 파일이 없습니다: {pdf_path}")
    doc = fitz.open(pdf_path)
    total = len(doc)
    pages_to_process = parse_pages(args.pages, total)
    print(f"📄 입력: {pdf_path.name} (총 {total}p)")
    print(f"📌 처리 대상: {len(pages_to_process)}p ({args.pages})")
    print(f"🌐 번역: EN → {args.target.upper()} via {args.provider}")

    # 캐시·폰트
    cache = TranslationCache(Path(args.cache))
    font = load_font(args.font)
    print(f"🔤 폰트: {font.name}")

    # 처리
    translator = PROVIDERS[args.provider]
    total_spans = 0
    cache_hits = 0
    api_calls = 0

    for pno in pages_to_process:
        page = doc[pno]
        spans = extract_spans(page)
        total_spans += len(spans)
        if args.dry_run:
            print(f"  p.{pno+1}: {len(spans)} spans")
            continue
        if not spans:
            continue

        # 캐시 미스만 추려서 번역
        to_translate_idx = []
        to_translate_text = []
        for i, s in enumerate(spans):
            cached = cache.get(s.text)
            if cached is None:
                to_translate_idx.append(i)
                to_translate_text.append(s.text)
            else:
                cache_hits += 1

        # 배치 호출 (한 페이지 단위)
        if to_translate_text:
            try:
                translated = translator(to_translate_text, args.target, api_key)
                for idx, vi in zip(to_translate_idx, translated):
                    cache.set(spans[idx].text, vi)
                api_calls += 1
                cache.save()
                if args.rate_limit > 0:
                    time.sleep(args.rate_limit)
            except Exception as e:
                print(f"  ⚠ p.{pno+1} 번역 실패: {e} (원문 유지)")
                for idx in to_translate_idx:
                    cache.set(spans[idx].text, spans[idx].text)
                cache.save()

        # 오버레이 적용
        for s in spans:
            translated = cache.get(s.text) or s.text
            overlay_translation(page, s, translated, font)

        print(f"  p.{pno+1}: {len(spans)} spans 처리 (캐시 {len(spans)-len(to_translate_idx)} / API {len(to_translate_idx)})")

    # 저장
    if not args.dry_run:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(out_path, garbage=4, deflate=True)
        print(f"\n✅ 저장: {out_path}")
        print(f"   총 스팬: {total_spans} / 캐시 적중: {cache_hits} / API 호출: {api_calls}")
    else:
        print(f"\n[DRY-RUN] 총 추출 스팬: {total_spans}")

    doc.close()
    cache.save()


if __name__ == '__main__':
    main()
