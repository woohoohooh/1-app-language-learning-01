// Имя кэша
const CACHE_NAME = 'english-learner-v1';

// Ресурсы для кэширования при установке
const CACHE_ASSETS = [
  './',
  './index.html',
  './review.html',
  './review-combined.html',
  './manifest.json',
  './icon-192x192.png',
  'https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap'
];

// Установка Service Worker
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Installing...');

  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[Service Worker] Caching app shell...');
        return cache.addAll(CACHE_ASSETS);
      })
      .then(() => {
        console.log('[Service Worker] Installation complete');
        return self.skipWaiting();
      })
  );
});

// Активация Service Worker
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Activating...');

  // Удаляем старые кэши
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('[Service Worker] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('[Service Worker] Activation complete');
      return self.clients.claim();
    })
  );
});

// Стратегия кэширования: Network First, затем Cache
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Игнорируем запросы к chrome-extension
  if (url.protocol === 'chrome-extension:') {
    return;
  }

  // Для HTML страниц - Network First
  if (event.request.headers.get('Accept')?.includes('text/html')) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
          return response;
        })
        .catch(() => {
          return caches.match(event.request)
            .then((cachedResponse) => {
              if (cachedResponse) {
                return cachedResponse;
              }
              // Fallback для offline
              if (event.request.mode === 'navigate') {
                return caches.match('./index.html');
              }
            });
        })
    );
    return;
  }

  // Для JSON файлов и аудио - Cache First
  if (url.pathname.endsWith('.json') ||
      url.pathname.includes('/audio/') ||
      url.pathname.endsWith('.wav') ||
      url.pathname.endsWith('.mp3')) {
    event.respondWith(
      caches.match(event.request)
        .then((cachedResponse) => {
          if (cachedResponse) {
            return cachedResponse;
          }

          return fetch(event.request)
            .then((response) => {
              // Не кэшируем слишком большие файлы
              if (response.status === 200 && response.headers.get('content-length') < 10485760) { // 10MB
                const responseClone = response.clone();
                caches.open(CACHE_NAME).then((cache) => {
                  cache.put(event.request, responseClone);
                });
              }
              return response;
            })
            .catch(() => {
              // Если файл не найден в кэше и нет сети
              if (url.pathname.endsWith('.json')) {
                return new Response(
                  JSON.stringify({
                    error: 'Offline mode',
                    message: 'Content not available offline'
                  }),
                  {
                    headers: { 'Content-Type': 'application/json' }
                  }
                );
              }
            });
        })
    );
    return;
  }

  // Для остальных запросов (CSS, JS, шрифты) - Cache First
  event.respondWith(
    caches.match(event.request)
      .then((cachedResponse) => {
        if (cachedResponse) {
          return cachedResponse;
        }

        return fetch(event.request)
          .then((response) => {
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseClone);
            });
            return response;
          })
          .catch(() => {
            // Fallback для CSS
            if (url.pathname.endsWith('.css')) {
              return new Response(
                `body::before {
                  content: "Offline Mode";
                  display: block;
                  padding: 20px;
                  background: #ff9800;
                  color: white;
                  text-align: center;
                  font-weight: bold;
                }`,
                { headers: { 'Content-Type': 'text/css' } }
              );
            }
          });
      })
  );
});

// Фоновая синхронизация (если браузер поддерживает)
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-progress') {
    console.log('[Service Worker] Background sync started');
    // Здесь можно синхронизировать прогресс с сервером
  }
});

// Получение сообщений от клиента
self.addEventListener('message', (event) => {
  if (event.data === 'skipWaiting') {
    self.skipWaiting();
  }

  if (event.data && event.data.type === 'CACHE_AUDIO') {
    // Кэширование аудио файлов по требованию
    const audioFiles = event.data.files;
    caches.open(CACHE_NAME).then((cache) => {
      audioFiles.forEach(audioUrl => {
        fetch(audioUrl)
          .then(response => {
            if (response.ok) {
              cache.put(audioUrl, response);
            }
          })
          .catch(console.error);
      });
    });
  }
});