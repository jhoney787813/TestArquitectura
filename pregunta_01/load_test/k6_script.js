import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 10 }, // Ramp-up a 10 usuarios concurrentes
    { duration: '30s', target: 20 }, // Sostener 20 usuarios para saturar el semáforo/pool de 5
    { duration: '10s', target: 0 },  # Ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<9000'], // Validar latencia P95 alrededor de 8s (8000ms)
  },
};

export default function () {
  const orderId = Math.floor(Math.random() * 100000);
  const url = `http://localhost:8000/api/v1/orders/ORD-${orderId}`;
  
  const res = http.get(url);
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response has data': (r) => r.body.includes('data'),
  });
  
  sleep(0.5);
}
