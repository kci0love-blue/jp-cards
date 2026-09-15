# -*- coding: utf-8 -*-
"""
카드 발음 MP3 생성기 (GitHub Actions에서 실행)
- tts/texts.json 의 각 항목을 ja-JP 신경망 음성(Nanami)으로 읽어 audio/<id>.mp3 로 저장
- 이미 있는 파일은 건너뛰므로 카드가 추가돼도 새 것만 만들어요
"""
import asyncio, json, os, sys, time

VOICE = os.environ.get("TTS_VOICE", "ja-JP-NanamiNeural")   # 여성: NanamiNeural / 남성: KeitaNeural
RATE  = os.environ.get("TTS_RATE", "-8%")                     # 학습용으로 살짝 천천히
OUT   = "audio"
CONCURRENCY = 3

def sentence(t):
    t = t.strip()
    if t and t[-1] not in "。！？!?":
        t += "。"
    return t

async def make_one(sem, item, stats):
    import edge_tts
    path = os.path.join(OUT, item["id"] + ".mp3")
    if os.path.exists(path) and os.path.getsize(path) > 500:
        stats["skip"] += 1
        return
    async with sem:
        for attempt in range(4):
            try:
                com = edge_tts.Communicate(sentence(item["text"]), VOICE, rate=RATE)
                tmp = path + ".part"
                await com.save(tmp)
                if os.path.getsize(tmp) < 500:
                    raise RuntimeError("empty audio")
                os.replace(tmp, path)
                stats["ok"] += 1
                await asyncio.sleep(0.25)
                return
            except Exception as e:  # 일시적 오류는 잠깐 쉬고 재시도
                wait = 3 * (attempt + 1)
                print(f"retry {attempt+1} {item['id']} {item['text']}: {e} (wait {wait}s)", flush=True)
                await asyncio.sleep(wait)
        stats["fail"].append(item)

async def main():
    os.makedirs(OUT, exist_ok=True)
    items = json.load(open("tts/texts.json", encoding="utf-8"))
    stats = {"ok": 0, "skip": 0, "fail": []}
    sem = asyncio.Semaphore(CONCURRENCY)
    t0 = time.time()
    await asyncio.gather(*(make_one(sem, it, stats) for it in items))
    print(f"done: 새로 생성 {stats['ok']} · 이미 있음 {stats['skip']} · 실패 {len(stats['fail'])} · {time.time()-t0:.0f}s")
    if stats["fail"]:
        json.dump(stats["fail"], open(os.path.join(OUT, "_failed.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        for f in stats["fail"][:20]:
            print("  실패:", f["id"], f["text"])
    # 앱이 "어떤 파일이 있는지" 빠르게 알 수 있도록 목록 저장
    ids = sorted(f[:-4] for f in os.listdir(OUT) if f.endswith(".mp3"))
    json.dump(ids, open(os.path.join(OUT, "index.json"), "w"), separators=(",", ":"))
    print("audio files:", len(ids))

if __name__ == "__main__":
    asyncio.run(main())
