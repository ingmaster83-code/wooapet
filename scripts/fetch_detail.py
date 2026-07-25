# -*- coding: utf-8 -*-
"""detailPetTour2 로 각 장소의 반려동물 동반 정책 상세정보 수집 (병렬)"""
import json
import os
import time
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = "9490b1d34e92aa9e25b32a4cff1438fc7b9c71e5d332413916a391e867f61e86"
BASE = "http://apis.data.go.kr/B551011/KorPetTourService2/detailPetTour2"
SCRIPT_DIR = os.path.dirname(__file__)
RAW_LIST = os.path.join(SCRIPT_DIR, "_pet_raw.json")
OUT = os.path.join(SCRIPT_DIR, "_pet_detail.json")

PET_FIELDS = [
    "acmpyTypeCd", "acmpyPsblCpam", "acmpyNeedMtr", "etcAcmpyInfo",
    "relaAcdntRiskMtr", "relaPosesFclty", "relaFrnshPrdlst",
    "relaPurcPrdlst", "relaRntlPrdlst",
]


def fetch_detail(content_id):
    params = {
        "serviceKey": API_KEY,
        "contentId": content_id,
        "MobileOS": "ETC",
        "MobileApp": "wooahouse",
        "_type": "json",
    }
    url = BASE + "?" + urllib.parse.urlencode(params)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            body = data["response"]["body"]
            items = body.get("items", "")
            if items == "":
                return content_id, {}
            item = items["item"]
            if isinstance(item, list):
                item = item[0] if item else {}
            return content_id, {k: item.get(k, "") for k in PET_FIELDS}
        except Exception as e:
            time.sleep(1.0)
    return content_id, {}


def main():
    with open(RAW_LIST, "r", encoding="utf-8") as f:
        items = json.load(f)

    # resume support
    details = {}
    if os.path.exists(OUT):
        with open(OUT, "r", encoding="utf-8") as f:
            details = json.load(f)

    todo = [it["contentid"] for it in items if it["contentid"] not in details]
    print(f"total={len(items)} already_done={len(details)} todo={len(todo)}")

    done_count = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(fetch_detail, cid): cid for cid in todo}
        for fut in as_completed(futures):
            cid, info = fut.result()
            details[cid] = info
            done_count += 1
            if done_count % 100 == 0:
                print(f"  progress {done_count}/{len(todo)}")
                with open(OUT, "w", encoding="utf-8") as f:
                    json.dump(details, f, ensure_ascii=False)

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(details, f, ensure_ascii=False)
    print(f"Saved {len(details)} details -> {OUT}")


if __name__ == "__main__":
    main()
