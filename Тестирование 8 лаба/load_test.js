import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// Кастомные метрики
const errorRate = new Rate('errors');
const responseTimeTrend = new Trend('response_time');
const requestsCounter = new Counter('total_requests');

// Опции теста
export const options = {
  stages: [
    // Первый сценарий: 10 виртуальных пользователей в течение 30 секунд
    { duration: '30s', target: 10 },
    
    // Второй сценарий: 50 виртуальных пользователей в течение 10 секунд  
    { duration: '10s', target: 50 },
    
    // Фаза снижения нагрузки
    { duration: '5s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% запросов должны быть быстрее 500ms
    errors: ['rate<0.1'], // Частота ошибок должна быть менее 10%
  },
};

// Базовый URL API
const BASE_URL = 'http://localhost:8000';

export default function () {
  // Список эндпоинтов для тестирования
  const endpoints = [
    '/',
    '/status',
    '/users',
    '/heavy'
  ];
  
  // Выбираем случайный эндпоинт
  const endpoint = endpoints[Math.floor(Math.random() * endpoints.length)];
  const url = `${BASE_URL}${endpoint}`;
  
  // Параметры запроса
  const params = {
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'k6-load-test',
    },
    tags: {
      endpoint: endpoint,
    },
  };
  
  // Отправляем GET-запрос
  const response = http.get(url, params);
  
  // Считаем кастомные метрики
  requestsCounter.add(1);
  responseTimeTrend.add(response.timings.duration);
  errorRate.add(response.status >= 400);
  
  // Проверяем ответ
  const checkResult = check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 1000ms': (r) => r.timings.duration < 1000,
    'has valid JSON': (r) => {
      try {
        JSON.parse(r.body);
        return true;
      } catch (e) {
        return false;
      }
    },
  });
  
  // Добавляем случайную задержку между запросами (0.5-2 секунды)
  sleep(Math.random() * 1.5 + 0.5);
}

// Функция setup выполняется один раз перед тестом
export function setup() {
  console.log('Starting load test...');
  console.log('Target URL:', BASE_URL);
  
  // Создаем несколько тестовых пользователей
  const responses = [];
  for (let i = 1; i <= 5; i++) {
    const url = `${BASE_URL}/users`;
    const payload = JSON.stringify({
      name: `Test User ${i}`,
      email: `user${i}@test.com`
    });
    
    const params = {
      headers: {
        'Content-Type': 'application/json',
      },
    };
    
    const response = http.post(url, payload, params);
    responses.push(response);
  }
  
  return { setup_complete: true };
}

// Функция teardown выполняется после завершения теста
export function teardown(data) {
  console.log('Load test completed');
  console.log('Setup data:', data);
}

//k6 run load_test.js 