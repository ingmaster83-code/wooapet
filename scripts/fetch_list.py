# -*- coding: utf-8 -*-
"""KorPetTourService2 petTourSyncList2 전체 목록 수집 (관광지/문화시설/축제/레포츠/숙박/음식점)"""
import json
import os
import time
import urllib.request
import urllib.parse

API_KEY = "9490b1d34e92aa9e25b32a4cff1438fc7b9c71e5d332413916a391e867f61e86"
BASE = "http://apis.data.go.kr/B551011/KorPetTourService2/petTourSyncList2"
CONTENT_TYPES = {
    "12": "관광지",
    "14": "문화시설",
    "15": "축제공연행사",
    "28": "레포츠",
    "32": "숙박",
    "39": "음식점",
}
OUT = os.path.join(os.path.dirname(__file__), "_pet_raw.json")


def fetch_page(content_type_id, page_no, num_of_rows=1000):
    params = {
        "serviceKey": API_KEY,
        "numOfRows": num_of_rows,
        "pageNo": page_no,
        "MobileOS": "ETC",
        "MobileApp": "wooahouse",
        "_type": "json",
        "contentTypeId": content_type_id,
    }
    url = BASE + "?" + urllib.parse.urlencode(params)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            body = data["response"]["body"]
            total = body["totalCount"]
            items = body.get("items", "")
            if items == "":
                return [], total
            item_list = items["item"]
            if isinstance(item_list, dict):
                item_list = [item_list]
            return item_list, total
        except Exception as e:
            print(f"  retry {content_type_id} p{page_no}: {e}")
            time.sleep(1.5)
    raise RuntimeError(f"failed {content_type_id} p{page_no}")


def main():
    all_items = []
    for ct_id, ct_name in CONTENT_TYPES.items():
        page = 1
        collected = 0
        while True:
            items, total = fetch_page(ct_id, page)
            for it in items:
                it["_category"] = ct_name
            all_items.extend(items)
            collected += len(items)
            print(f"{ct_name}({ct_id}) page {page}: {len(items)} (total {collected}/{total})")
            if collected >= total or not items:
                break
            page += 1
            time.sleep(0.2)

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False)
    print(f"\nSaved {len(all_items)} records -> {OUT}")


if __name__ == "__main__":
    main()
