// 오프라인 캐시: 처음 한 번 열면 앱 전체를 저장해 두고, 이후엔 인터넷 없이 실행
// 파일을 갱신하면 아래 VERSION 값을 바꿔 주세요 (예: v2, v3 …)
const VERSION = 'jpw-v1';
const FILES = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png', './icon-maskable-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
// 캐시 우선, 네트워크가 되면 조용히 새 버전으로 갱신
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request, { ignoreSearch: true }).then(cached => {
      const fresh = fetch(e.request).then(res => {
        if (res && res.ok && new URL(e.request.url).origin === location.origin) caches.open(VERSION).then(c => c.put(e.request, res.clone()));
        return res;
      }).catch(() => cached);
      return cached || fresh;
    })
  );
});
