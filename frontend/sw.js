const CACHE_NAME = "mtg-ai-search-v1";
const urlsToCache = [
  "/",
  "/index.html",
  "/manifest.json",
  // 可以添加其他需要缓存的资源
];

// 安装Service Worker
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("Opened cache");
      return cache.addAll(urlsToCache);
    })
  );
});

// 激活Service Worker
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log("Deleting old cache:", cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// 拦截网络请求
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      // 如果缓存中有响应，返回缓存的响应
      if (response) {
        return response;
      }

      // 否则从网络获取
      return fetch(event.request).then((response) => {
        // 检查是否收到有效响应
        if (!response || response.status !== 200 || response.type !== "basic") {
          return response;
        }

        // 克隆响应
        const responseToCache = response.clone();

        caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, responseToCache);
        });

        return response;
      });
    })
  );
});

// 处理推送通知（可选功能）
self.addEventListener("push", (event) => {
  const options = {
    body: event.data ? event.data.text() : "MTG AI 搜索工具有新消息",
    icon: "/icons/icon-192x192.png",
    badge: "/icons/icon-72x72.png",
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1,
    },
    actions: [
      {
        action: "explore",
        title: "查看详情",
        icon: "/icons/icon-192x192.png",
      },
      {
        action: "close",
        title: "关闭",
        icon: "/icons/icon-192x192.png",
      },
    ],
  };

  event.waitUntil(
    self.registration.showNotification("MTG AI 搜索工具", options)
  );
});

// 处理通知点击
self.addEventListener("notificationclick", (event) => {
  event.notification.close();

  if (event.action === "explore") {
    event.waitUntil(clients.openWindow("/"));
  }
});

