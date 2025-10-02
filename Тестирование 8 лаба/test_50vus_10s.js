import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '5s', target: 50 },  // Быстрый рост до 50 пользователей
    { duration: '10s', target: 50 }, // Удержание 50 пользователей
    { duration: '3s', target: 0 },   // Быстрое снижение
  ],
  thresholds: {
    http_req_duration: ['p(95)<800'],
    http_req_failed: ['rate<0.15'],
  },
};

export default function () {
  const endpoints = ['/', '/status', '/users', '/heavy'];
  const endpoint = endpoints[Math.floor(Math.random() * endpoints.length)];
  const url = `http://localhost:8000${endpoint}`;
  
  const response = http.get(url);
  
  check(response, {
    'status is 200': (r) => r.status === 200,
  });
  
  sleep(0.5); // Более короткая задержка между запросами
}