import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '5s', target: 10 },  // Плавный рост до 10 пользователей
    { duration: '30s', target: 10 }, // Удержание 10 пользователей
    { duration: '5s', target: 0 },   // Плавное снижение
  ],
};

export default function () {
  const response = http.get('http://localhost:8000/status');
  
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  sleep(1);
}