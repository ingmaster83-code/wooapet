#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wooapet 페이지 생성기 — 반려동물 동반여행 KorPetTourService2 기반 지역별 페이지"""
import json
import os
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(BASE, "docs")
DATA_PATH = os.path.join(DOCS, "pets.json")

REGION_SHORT = {
    "서울특별시": "서울", "부산광역시": "부산", "대구광역시": "대구",
    "인천광역시": "인천", "광주광역시": "광주", "대전광역시": "대전",
    "울산광역시": "울산", "세종특별자치시": "세종", "경기도": "경기",
    "강원특별자치도": "강원", "강원도": "강원", "충청북도": "충북",
    "충청남도": "충남", "전북특별자치도": "전북", "전라북도": "전북",
    "전라남도": "전남", "경상북도": "경북", "경상남도": "경남",
    "제주특별자치도": "제주", "제주도": "제주",
}

CATEGORIES = ["관광지", "음식점", "숙박", "레포츠", "문화시설", "축제공연행사"]
CATEGORY_ICON = {
    "관광지": "🏞️", "음식점": "🍽️", "숙박": "🏨",
    "레포츠": "⚽", "문화시설": "🎨", "축제공연행사": "🎉",
}

with open(DATA_PATH, encoding="utf-8") as f:
    raw = json.load(f)

by_region = defaultdict(lambda: defaultdict(list))
for it in raw:
    by_region[it["region"]][it["city"]].append(it)

TOTAL = len(raw)
REGIONS = sorted(by_region.keys())

HEAD_STYLE = """<link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800&display=swap" rel="stylesheet">"""


def esc(s):
    return (s or "").replace("&", "&amp;").replace('"', "&quot;")


def category_tabs(records):
    counts = defaultdict(int)
    for r in records:
        counts[r["category"]] += 1
    btns = [f'<button class="tab-btn active" data-tab="전체">전체 <span class="tab-cnt">{len(records)}</span></button>']
    for cat in CATEGORIES:
        if counts[cat]:
            btns.append(f'<button class="tab-btn" data-tab="{esc(cat)}">{CATEGORY_ICON[cat]} {esc(cat)} <span class="tab-cnt">{counts[cat]}</span></button>')
    return "".join(btns)


def region_page(region, cities, depth):
    up = "../" * depth
    short = REGION_SHORT.get(region, region)
    all_records = [r for recs in cities.values() for r in recs]
    count = len(all_records)
    city_names = sorted(cities.keys())

    subnav = "".join(
        f'<a href="{esc(region)}/{esc(c)}.html" class="btn-sub-nav">{esc(c)} <span class="sub-cnt">{len(cities[c])}</span></a>'
        for c in city_names
    )

    records_json = json.dumps(all_records, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(short)} 반려동물 동반여행지 {count}곳 — 식당·숙박·관광지 | 우아펫</title>
  <meta name="description" content="{esc(region)} 반려동물 동반 가능 장소 {count}곳. 강아지 동반 식당, 애견펜션, 반려동물 동반 관광지를 지역별로 확인하세요.">
  <meta name="keywords" content="{esc(short)} 반려동물 동반,{esc(short)} 강아지 동반 식당,{esc(short)} 애견펜션,{esc(short)} 반려동물 여행">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://wooapet.wooahouse.com/지역/{esc(region)}.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc(short)} 반려동물 동반여행지 {count}곳 | 우아펫">
  <meta property="og:description" content="{esc(region)} 반려동물 동반 가능 식당·숙박·관광지 {count}곳 안내">
  <meta property="og:url" content="https://wooapet.wooahouse.com/지역/{esc(region)}.html">
  <meta name="twitter:card" content="summary">
  {HEAD_STYLE}
  <link rel="stylesheet" href="{up}css/style.css">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"CollectionPage",
   "name":"{esc(short)} 반려동물 동반여행지 목록","url":"https://wooapet.wooahouse.com/지역/{esc(region)}.html",
   "description":"{esc(region)} 반려동물 동반 가능 장소 {count}곳"}}
  </script>
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <a href="{up}" class="site-logo"><span class="logo-icon">🐾</span><span class="logo-text">우아펫</span></a>
    <nav class="header-nav">
      <a href="{up}">동반여행지 찾기</a>
      <a href="{up}지역/" class="active-nav">지역별</a>
      <a href="https://wooahouse.com" target="_blank" rel="noopener">WooaHouse →</a>
    </nav>
    <button class="mobile-menu-btn" aria-label="메뉴">☰</button>
  </div>
<script src="{up}js/wooa-sites-bar.js"></script>
<script src="{up}js/ad-dev-placeholder.js"></script>
</header>

<section class="region-hero">
  <nav class="breadcrumb-hero">
    <a href="{up}">홈</a> <span>›</span> <span>지역별</span> <span>›</span> <span>{esc(region)}</span>
  </nav>
  <h1>🐾 {esc(region)} 반려동물 동반여행지</h1>
  <p class="sub">{count}곳의 반려동물 동반 가능 식당·숙박·관광지를 확인하세요</p>
  <p class="keywords">{esc(short)} 강아지 동반 식당 · {esc(short)} 애견펜션 · {esc(short)} 반려동물 동반 여행지</p>
  <div class="region-search-bar">
    <input type="text" id="regionSearchInput" placeholder="장소명 또는 주소 검색">
    <button id="regionSearchBtn">검색</button>
  </div>
</section>

<div class="sub-nav-bar">
  <div class="sub-nav-inner">
    <span class="sub-nav-label">{esc(short)} 시/군/구 선택</span>
    <div class="sub-nav-btns">
      {subnav}
    </div>
  </div>
</div>

<div class="tab-bar">
  <div class="tab-inner">
    {category_tabs(all_records)}
  </div>
</div>

<div class="tab-bottom-ad">
  <ins class="adsbygoogle" style="display:inline-block;width:728px;max-width:100%;height:90px"
       data-ad-client="ca-pub-6464921081676309" data-ad-slot="7080296704"></ins>
</div>

<div class="region-layout">
  <div class="region-list-col">
    <div class="result-header">
      <div class="result-count">총 <strong id="listCount">{count}</strong>곳</div>
      <a href="{up}" class="result-back">← 전국 검색</a>
    </div>
    <div id="parkingList"></div>
    <div id="loadMore" style="text-align:center;margin:20px 0;display:none;">
      <button id="loadMoreBtn" style="padding:10px 28px;background:var(--primary);color:#fff;border-radius:8px;font-size:.9rem;font-weight:600;">더 보기</button>
    </div>
  </div>
  <div class="region-aside">
    <div class="mid-ad" style="min-height:600px;">
      <div class="ad-label">📢 광고</div>
      <ins class="adsbygoogle" style="display:inline-block;width:300px;height:600px"
           data-ad-client="ca-pub-6464921081676309" data-ad-slot="6255378195"></ins>
    </div>
  </div>
</div>

<section class="seo-section">
  <h2>{esc(region)} 반려동물 동반여행 안내</h2>
  <p>{esc(region)}의 반려동물 동반 가능 장소는 총 {count}곳입니다.
  강아지와 함께 갈 수 있는 식당, 애견펜션, 관광지 정보를 위 목록에서 확인하시고,
  각 장소의 동반 조건(목줄 착용, 구역 제한 등)을 미리 확인한 뒤 방문하세요.</p>
</section>

<div class="crosslink-box">
  <a href="https://wooatown.wooahouse.com/지역/{esc(short)}.html" target="_blank" rel="noopener" class="crosslink-link">
    🏠 {esc(short)} 다른 생활정보 보기 (우아동네) →
  </a>
</div>

<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-grid">
      <div class="footer-col"><p class="footer-logo">🐾 우아펫</p><p>전국 반려동물 동반여행지 정보<br>설치 불필요 · 로그인 불필요</p><a href="https://wooahouse.com" target="_blank" style="color:var(--primary);margin-top:8px;display:inline-block;">wooahouse.com →</a></div>
      <div class="footer-col"><p class="footer-heading">정보</p><a href="{up}privacy.html">개인정보처리방침</a><a href="{up}">메인으로</a></div>
    </div>
    <div class="footer-bottom"><p>&copy; 2026 WooaHouse. All rights reserved.</p><p>데이터 출처: 한국관광공사 반려동물 동반여행 서비스</p></div>
  </div>
</footer>

<script src="{up}js/config.js"></script>
<script>
  const PET_RECORDS = {records_json};
  const REGION_NAME = '{esc(region)}';
  const REGION_SHORT = '{esc(short)}';
</script>
<script src="{up}js/region.js"></script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6464921081676309" crossorigin="anonymous"></script>
<script>document.querySelectorAll('ins.adsbygoogle').forEach(function(){{(adsbygoogle=window.adsbygoogle||[]).push({{}});}});</script>
</body>
</html>"""
    return html


def city_page(region, city, records):
    short = REGION_SHORT.get(region, region)
    count = len(records)
    records_json = json.dumps(records, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(city)} 반려동물 동반여행지 {count}곳 — 식당·숙박·관광지 | 우아펫</title>
  <meta name="description" content="{esc(region)} {esc(city)} 반려동물 동반 가능 장소 {count}곳. 강아지 동반 식당, 애견펜션, 동반 관광지를 확인하세요.">
  <meta name="keywords" content="{esc(city)} 반려동물 동반,{esc(city)} 강아지 동반 식당,{esc(region)} {esc(city)} 애견펜션,{esc(short)} {esc(city)} 반려동물 여행">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://wooapet.wooahouse.com/지역/{esc(region)}/{esc(city)}.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc(city)} 반려동물 동반여행지 {count}곳 | 우아펫">
  <meta property="og:description" content="{esc(region)} {esc(city)} 반려동물 동반 가능 식당·숙박·관광지 {count}곳">
  <meta property="og:url" content="https://wooapet.wooahouse.com/지역/{esc(region)}/{esc(city)}.html">
  <meta name="twitter:card" content="summary">
  {HEAD_STYLE}
  <link rel="stylesheet" href="../../css/style.css">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"CollectionPage",
   "name":"{esc(city)} 반려동물 동반여행지 목록","url":"https://wooapet.wooahouse.com/지역/{esc(region)}/{esc(city)}.html",
   "description":"{esc(region)} {esc(city)} 반려동물 동반 가능 장소 {count}곳"}}
  </script>
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <a href="../../" class="site-logo"><span class="logo-icon">🐾</span><span class="logo-text">우아펫</span></a>
    <nav class="header-nav">
      <a href="../../">동반여행지 찾기</a>
      <a href="../" class="active-nav">지역별</a>
      <a href="https://wooahouse.com" target="_blank" rel="noopener">WooaHouse →</a>
    </nav>
    <button class="mobile-menu-btn" aria-label="메뉴">☰</button>
  </div>
<script src="../../js/wooa-sites-bar.js"></script>
<script src="../../js/ad-dev-placeholder.js"></script>
</header>

<section class="region-hero">
  <nav class="breadcrumb-hero">
    <a href="../../">홈</a> <span>›</span>
    <a href="../{esc(region)}.html">{esc(region)}</a> <span>›</span>
    <span>{esc(city)}</span>
  </nav>
  <h1>🐾 {esc(city)} 반려동물 동반여행지</h1>
  <p class="sub">{count}곳의 반려동물 동반 가능 식당·숙박·관광지를 확인하세요</p>
  <p class="keywords">{esc(city)} 강아지 동반 식당 · {esc(city)} 애견펜션 · {esc(region)} {esc(city)} 반려동물 여행</p>
  <div class="region-search-bar">
    <input type="text" id="regionSearchInput" placeholder="장소명 또는 주소 검색">
    <button id="regionSearchBtn">검색</button>
  </div>
</section>

<div class="tab-bar">
  <div class="tab-inner">
    {category_tabs(records)}
  </div>
</div>

<div class="tab-bottom-ad">
  <ins class="adsbygoogle" style="display:inline-block;width:728px;max-width:100%;height:90px"
       data-ad-client="ca-pub-6464921081676309" data-ad-slot="7080296704"></ins>
</div>

<div class="region-layout">
  <div class="region-list-col">
    <div class="result-header">
      <div class="result-count">총 <strong id="listCount">{count}</strong>곳</div>
      <a href="../{esc(region)}.html" class="result-back">← {esc(region)}</a>
    </div>
    <div id="parkingList"></div>
    <div id="loadMore" style="text-align:center;margin:20px 0;display:none;">
      <button id="loadMoreBtn" style="padding:10px 28px;background:var(--primary);color:#fff;border-radius:8px;font-size:.9rem;font-weight:600;">더 보기</button>
    </div>
  </div>
  <div class="region-aside">
    <div class="mid-ad" style="min-height:600px;">
      <div class="ad-label">📢 광고</div>
      <ins class="adsbygoogle" style="display:inline-block;width:300px;height:600px"
           data-ad-client="ca-pub-6464921081676309" data-ad-slot="6255378195"></ins>
    </div>
  </div>
</div>

<section class="seo-section">
  <h2>{esc(city)} 반려동물 동반여행 안내</h2>
  <p>{esc(region)} {esc(city)}의 반려동물 동반 가능 장소는 총 {count}곳입니다.
  강아지와 함께 갈 수 있는 식당, 애견펜션, 관광지 정보를 위 목록에서 확인하시고,
  각 장소의 동반 조건을 미리 확인한 뒤 방문하세요.
  {esc(region)} 전체 목록은 <a href="../{esc(region)}.html">{esc(region)} 동반여행지 페이지</a>에서 확인하세요.</p>
</section>

<div class="crosslink-box">
  <a href="https://wooatown.wooahouse.com/지역/{esc(short)}.html" target="_blank" rel="noopener" class="crosslink-link">
    🏠 {esc(short)} 다른 생활정보 보기 (우아동네) →
  </a>
</div>

<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-grid">
      <div class="footer-col"><p class="footer-logo">🐾 우아펫</p><p>전국 반려동물 동반여행지 정보<br>설치 불필요 · 로그인 불필요</p><a href="https://wooahouse.com" target="_blank" style="color:var(--primary);margin-top:8px;display:inline-block;">wooahouse.com →</a></div>
      <div class="footer-col"><p class="footer-heading">상위 지역</p><a href="../{esc(region)}.html">{esc(region)} 전체</a></div>
      <div class="footer-col"><p class="footer-heading">정보</p><a href="../../privacy.html">개인정보처리방침</a><a href="../../">메인으로</a></div>
    </div>
    <div class="footer-bottom"><p>&copy; 2026 WooaHouse. All rights reserved.</p><p>데이터 출처: 한국관광공사 반려동물 동반여행 서비스</p></div>
  </div>
</footer>

<script src="../../js/config.js"></script>
<script>
  const PET_RECORDS = {records_json};
  const REGION_NAME = '{esc(city)}';
  const REGION_SHORT = '{esc(city)}';
</script>
<script src="../../js/region.js"></script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6464921081676309" crossorigin="anonymous"></script>
<script>document.querySelectorAll('ins.adsbygoogle').forEach(function(){{(adsbygoogle=window.adsbygoogle||[]).push({{}});}});</script>
</body>
</html>"""
    return html


def index_page():
    cards = []
    for region in REGIONS:
        short = REGION_SHORT.get(region, region)
        count = sum(len(v) for v in by_region[region].values())
        cards.append(
            f'<a href="지역/{esc(region)}.html" class="region-card">'
            f'<span class="region-card-name">{esc(short)}</span>'
            f'<span class="region-card-count">{count}곳</span></a>'
        )
    cards_html = "".join(cards)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>전국 반려동물 동반여행지 찾기 — 강아지 동반 식당·숙박·관광지 | 우아펫</title>
  <meta name="description" content="전국 {TOTAL:,}곳 반려동물 동반 가능 식당, 애견펜션, 관광지를 한눈에 확인하세요. 지역별·카테고리별로 강아지와 함께 갈 수 있는 곳을 검색할 수 있습니다.">
  <meta name="keywords" content="반려동물 동반여행,강아지 동반 식당,애견펜션,반려동물 동반 카페,애견동반 여행지,강아지와 함께">
  <meta name="robots" content="index, follow">
  <meta name="naver-site-verification" content="394d3ed195ebdca78c2f87c53949713d1baaed4c" />
  <link rel="canonical" href="https://wooapet.wooahouse.com/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="전국 반려동물 동반여행지 찾기 | 우아펫">
  <meta property="og:description" content="전국 {TOTAL:,}곳 반려동물 동반 가능 식당·숙박·관광지를 한눈에">
  <meta property="og:url" content="https://wooapet.wooahouse.com/">
  <meta property="og:image" content="https://wooapet.wooahouse.com/og-image.png">
  <meta name="twitter:card" content="summary">
  {HEAD_STYLE}
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <a href="./" class="site-logo"><span class="logo-icon">🐾</span><span class="logo-text">우아펫</span></a>
    <nav class="header-nav">
      <a href="./" class="active-nav">동반여행지 찾기</a>
      <a href="지역/">지역별</a>
      <a href="https://wooahouse.com" target="_blank" rel="noopener">WooaHouse →</a>
    </nav>
    <button class="mobile-menu-btn" aria-label="메뉴">☰</button>
  </div>
<script src="js/wooa-sites-bar.js"></script>
<script src="js/ad-dev-placeholder.js"></script>
</header>

<section class="hero">
  <h1>🐾 전국 반려동물 동반여행지 찾기</h1>
  <p class="sub">전국 {TOTAL:,}곳 반려동물 동반 가능 식당·숙박·관광지를 한눈에 확인하세요</p>
  <div class="region-search-bar" style="max-width:520px;margin:24px auto 0;">
    <input type="text" id="homeSearchInput" placeholder="지역명, 장소명으로 검색">
    <button id="homeSearchBtn">검색</button>
  </div>
</section>

<div class="main-layout">
  <div class="main-col">
    <div class="tab-bottom-ad">
      <ins class="adsbygoogle" style="display:inline-block;width:728px;max-width:100%;height:90px"
           data-ad-client="ca-pub-6464921081676309" data-ad-slot="7080296704"></ins>
    </div>

    <section class="section">
      <h2 class="section-title" style="text-align:center;margin-bottom:24px;">📍 지역별로 찾기</h2>
      <div class="region-grid">
        {cards_html}
      </div>
    </section>

    <section class="seo-intro">
      <h2 style="font-size:1.2rem;font-weight:700;margin-bottom:16px;">우아펫 — 전국 반려동물 동반여행지 정보</h2>
      <p style="color:var(--text-muted);font-size:.9rem;line-height:1.9">
        <strong>우아펫</strong>은 한국관광공사 반려동물 동반여행 데이터를 기반으로,
        강아지·고양이와 함께 갈 수 있는 식당, 카페, 애견펜션, 관광지, 레포츠 시설을 한곳에서 검색할 수 있는 무료 서비스입니다.
        각 장소별 동반 가능 여부, 목줄 착용 등 준비물, 구역 제한 등 구체적인 동반 조건까지 확인할 수 있습니다.
        <br><br>
        서울·경기·인천 등 수도권부터 강원·충청·전라·경상·제주까지 전국 17개 시도의 반려동물 동반여행지를 지역별로 모아 확인하세요.
      </p>
    </section>
  </div>

  <aside class="sidebar">
    <div class="sidebar-box">
      <h3>💡 우아펫이란?</h3>
      <ul>
        <li>🐾 반려동물 동반 가능 장소 정보</li>
        <li>🍽️ 강아지 동반 식당·카페</li>
        <li>🏨 애견펜션 등 동반 숙박</li>
        <li>📋 목줄·구역제한 등 동반 조건 안내</li>
        <li>📍 전국 약 {TOTAL:,}곳</li>
      </ul>
    </div>
    <div class="sidebar-ad">
      <ins class="adsbygoogle" style="display:inline-block;width:300px;height:600px"
           data-ad-client="ca-pub-6464921081676309" data-ad-slot="6255378195"></ins>
    </div>
  </aside>
</div>

<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-grid">
      <div class="footer-col"><p class="footer-logo">🐾 우아펫</p><p>전국 반려동물 동반여행지 정보<br>설치 불필요 · 로그인 불필요</p><a href="https://wooahouse.com" target="_blank" style="color:var(--primary);margin-top:8px;display:inline-block;">wooahouse.com →</a></div>
      <div class="footer-col"><p class="footer-heading">관련 사이트</p><a href="https://wooabike.wooahouse.com" target="_blank">🚲 우아자전거</a><a href="https://wooatrail.wooahouse.com" target="_blank">🥾 우아트레일 (둘레길)</a></div>
      <div class="footer-col"><p class="footer-heading">정보</p><a href="privacy.html">개인정보처리방침</a></div>
    </div>
    <div class="footer-bottom"><p>&copy; 2026 WooaHouse. All rights reserved.</p><p>데이터 출처: 한국관광공사 반려동물 동반여행 서비스</p></div>
  </div>
</footer>

<script src="js/config.js"></script>
<script>
  document.getElementById('homeSearchBtn').addEventListener('click', doSearch);
  document.getElementById('homeSearchInput').addEventListener('keydown', e => {{ if (e.key === 'Enter') doSearch(); }});
  function doSearch() {{
    const q = document.getElementById('homeSearchInput').value.trim();
    if (q) location.href = '지역/?q=' + encodeURIComponent(q);
  }}
</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6464921081676309" crossorigin="anonymous"></script>
<script>document.querySelectorAll('ins.adsbygoogle').forEach(function(){{(adsbygoogle=window.adsbygoogle||[]).push({{}});}});</script>
</body>
</html>"""


def region_index_page():
    cards = []
    for region in REGIONS:
        short = REGION_SHORT.get(region, region)
        count = sum(len(v) for v in by_region[region].values())
        cards.append(
            f'<a href="{esc(region)}.html" class="region-card">'
            f'<span class="region-card-name">{esc(short)}</span>'
            f'<span class="region-card-count">{count}곳</span></a>'
        )
    cards_html = "".join(cards)
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>지역별 반려동물 동반여행지 — 전국 17개 시도 | 우아펫</title>
  <meta name="description" content="전국 17개 시도별 반려동물 동반여행지 목록. 지역을 선택해서 강아지 동반 식당, 숙박, 관광지를 확인하세요.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://wooapet.wooahouse.com/지역/">
  {HEAD_STYLE}
  <link rel="stylesheet" href="../css/style.css">
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <a href="../" class="site-logo"><span class="logo-icon">🐾</span><span class="logo-text">우아펫</span></a>
    <nav class="header-nav">
      <a href="../">동반여행지 찾기</a>
      <a href="./" class="active-nav">지역별</a>
      <a href="https://wooahouse.com" target="_blank" rel="noopener">WooaHouse →</a>
    </nav>
    <button class="mobile-menu-btn" aria-label="메뉴">☰</button>
  </div>
<script src="../js/wooa-sites-bar.js"></script>
<script src="../js/ad-dev-placeholder.js"></script>
</header>
<section class="hero">
  <h1>📍 지역별 반려동물 동반여행지</h1>
  <p class="sub">전국 17개 시도 중 지역을 선택하세요</p>
</section>
<section class="section" style="max-width:1100px;margin:0 auto;padding:40px 20px;">
  <div class="region-grid">
    {cards_html}
  </div>
</section>
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-bottom"><p>&copy; 2026 WooaHouse. All rights reserved.</p></div>
  </div>
</footer>
</body>
</html>"""


def main():
    os.makedirs(os.path.join(DOCS, "지역"), exist_ok=True)

    with open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_page())

    with open(os.path.join(DOCS, "지역", "index.html"), "w", encoding="utf-8") as f:
        f.write(region_index_page())

    for region, cities in by_region.items():
        region_dir = os.path.join(DOCS, "지역", region)
        os.makedirs(region_dir, exist_ok=True)
        with open(os.path.join(DOCS, "지역", f"{region}.html"), "w", encoding="utf-8") as f:
            f.write(region_page(region, cities, depth=1))
        for city, records in cities.items():
            with open(os.path.join(region_dir, f"{city}.html"), "w", encoding="utf-8") as f:
                f.write(city_page(region, city, records))

    write_sitemap()

    total_pages = 2 + len(REGIONS) + sum(len(v) for v in by_region.values())
    print(f"생성 완료: 시도 {len(REGIONS)}개, 시군구 {sum(len(v) for v in by_region.values())}개, 총 {total_pages}개 페이지")


def write_sitemap():
    urls = ["https://wooapet.wooahouse.com/"]
    for region, cities in by_region.items():
        urls.append(f"https://wooapet.wooahouse.com/지역/{region}.html")
        for city in cities:
            urls.append(f"https://wooapet.wooahouse.com/지역/{region}/{city}.html")
    entries = "\n".join(
        f"  <url><loc>{u}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>"
        for u in urls
    )
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}\n</urlset>\n'
    with open(os.path.join(DOCS, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)


if __name__ == "__main__":
    main()
