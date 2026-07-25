# -*- coding: utf-8 -*-
"""_pet_raw.json + _pet_detail.json 를 병합하고 지역(시도/시군구)을 정규화해 pets.json 생성"""
import json
import os

SCRIPT_DIR = os.path.dirname(__file__)
RAW_LIST = os.path.join(SCRIPT_DIR, "_pet_raw.json")
DETAIL = os.path.join(SCRIPT_DIR, "_pet_detail.json")
OUT = os.path.join(SCRIPT_DIR, "..", "docs", "pets.json")

REGION_CANON = {
    "전북특별자치도": "전라북도", "전북": "전라북도",
    "강원특별자치도": "강원도", "강원": "강원도",
    "제주특별자치도": "제주도", "제주": "제주도",
    "서울": "서울특별시", "부산": "부산광역시", "대구": "대구광역시",
    "인천": "인천광역시", "광주": "광주광역시", "대전": "대전광역시",
    "울산": "울산광역시", "세종": "세종특별자치시",
    "경기": "경기도", "충북": "충청북도", "충남": "충청남도",
    "경북": "경상북도", "경남": "경상남도", "전남": "전라남도",
}
GWANGJU_GU = {"동구", "서구", "남구", "북구", "광산구"}
KNOWN_REGION_PREFIXES = sorted(
    [
        "서울특별시", "서울", "부산광역시", "부산", "대구광역시", "대구",
        "인천광역시", "인천", "광주광역시", "광주",
        "대전광역시", "대전", "울산광역시", "울산", "세종특별자치시", "세종",
        "경기도", "경기", "강원도", "강원특별자치도", "강원",
        "충청북도", "충북", "충청남도", "충남",
        "전라북도", "전북특별자치도", "전북",
        "전라남도", "전남", "전남광주통합특별시",
        "경상북도", "경북", "경상남도", "경남",
        "제주도", "제주특별자치도", "제주",
    ],
    key=len, reverse=True,
)

CATEGORY_ORDER = ["관광지", "음식점", "숙박", "레포츠", "문화시설", "축제공연행사"]


def extract_region_city(addr):
    for prefix in KNOWN_REGION_PREFIXES:
        if addr.startswith(prefix):
            rest = addr[len(prefix):].strip()
            city = rest.split()[0] if rest else "기타"
            if prefix == "전남광주통합특별시":
                region = "광주광역시" if city in GWANGJU_GU else "전라남도"
            else:
                region = REGION_CANON.get(prefix, prefix)
            return region, city
    toks = addr.split()
    if not toks:
        return None, None
    return toks[0], (toks[1] if len(toks) > 1 else "기타")


def main():
    with open(RAW_LIST, "r", encoding="utf-8") as f:
        items = json.load(f)
    with open(DETAIL, "r", encoding="utf-8") as f:
        details = json.load(f)

    records = []
    skipped = 0
    region_counter = {}
    for it in items:
        addr = (it.get("addr1") or "").strip()
        if not addr:
            skipped += 1
            continue
        region, city = extract_region_city(addr)
        if not region:
            skipped += 1
            continue
        region_counter[region] = region_counter.get(region, 0) + 1

        det = details.get(it["contentid"], {})
        rec = {
            "id": it["contentid"],
            "title": it.get("title", ""),
            "category": it.get("_category", ""),
            "region": region,
            "city": city,
            "addr": addr,
            "addr2": it.get("addr2", ""),
            "tel": it.get("tel", ""),
            "lat": it.get("mapy", ""),
            "lng": it.get("mapx", ""),
            "image": it.get("firstimage", ""),
            "acmpyType": det.get("acmpyTypeCd", ""),
            "acmpySize": det.get("acmpyPsblCpam", ""),
            "acmpyNeed": det.get("acmpyNeedMtr", ""),
            "acmpyEtc": det.get("etcAcmpyInfo", ""),
        }
        records.append(rec)

    print(f"total={len(items)} kept={len(records)} skipped(no addr/region)={skipped}")
    print("\nregion distribution:")
    for r, c in sorted(region_counter.items(), key=lambda x: -x[1]):
        print(f"  {r}: {c}")
    print(f"\n{len(region_counter)} regions")

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False)
    print(f"\nSaved {len(records)} records -> {OUT}")


if __name__ == "__main__":
    main()
