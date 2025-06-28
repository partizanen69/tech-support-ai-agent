# Загальні функції, інтеграції та налаштування

> Охоплює всі питання, що не підпадають під «Auth», «Billing» чи «Troubleshooting».

---

## 1. Відновлення видаленого проєкту (Q4)

### Час життя у корзині

- **Starter**: 15 днів
- **Pro**: 30 днів
- **Enterprise**: 90 днів

### Повернення проєкту

1. **Проєкти → Корзина**.
2. Знайдіть потрібний елемент, натисніть **Restore**.
3. Виберіть локацію (Original / New folder).

> ⚠️ Якщо корзина порожня — лише команда підтримки може витягнути
> снапшот із резервної копії (RTO 1 год).

---

## 2. Налаштування email-сповіщень (Q6)

- **Коментарі** — миттєві.
- **Щоденний дайджест** — 10:00 за часовим поясом профілю.
- **Критичні збої** — Web-push + Email + Slack (якщо інтегровано).

```jsonc
// Webhook payload
{
  "event": "incident.opened",
  "severity": "critical",
  "title": "CPU > 95% for 5m"
}
```

---

### 3. Збільшення дискової квоти (Q7)

План Базова квота Максимальне розширення
Starter 10 ГБ 50 ГБ (+$5/міс)
Pro 100 ГБ 500 ГБ (+$20/міс)
Enterprise 1 ТБ 5 ТБ (договір)

---

### 4. Генерація API-ключа (Q8)

1. Settings → API Keys → Generate.
2. Задайте теги (prod/staging) та обмеження за IP (< CIDR> або \*).
3. У відповідь повернеться:

`sk-live-51d6… — збережіть у Password Manager (не показується вдруге).`

---

### 5. Видалення акаунта та скасування видалення (Q9 & Q44)

• Заплановане видалення ставить акаунт у pending-delete.
• Протягом 14 днів можна натиснути Undo delete у банері, або надіслати DELETE_CANCEL через API:

POST /v1/account/undelete
Authorization: Bearer <token>

---

### 6. Push-сповіщення на iOS (Q24)

- Переконайтесь у Token Status: Active в Settings → Devices.
- Якщо після оновлення iOS сповіщення не приходять — видаліть і встановіть застосунок, дайте дозвіл «Allow Critical Alerts».

---

### 7. Масове додавання користувачів (Q42)

Формат CSV

```
email,role
alice@acme.com,Editor
bob@acme.com,Reader
```

Підтримує до 10 000 рядків. Помилкові рядки потрапляють у файл
import*errors*<date>.csv.

---

### 8. Синхронізація Google Calendar (Q43)

- Період оновлення — кожні 5 хв (pull-model).
- При першій авторизації видайте доступ до https://www.googleapis.com/auth/calendar.events.
- Тест-дзвінок:

```
H "Authorization: Bearer <token>" \
 https://www.googleapis.com/calendar/v3/calendars/primary/events
```

---

### 9. Ліміти API (Q23 & Q50)

План Запитів/хв Burst IP-фільтр
Free 60 10 –
Starter 600 100 5 IP
Pro 3 000 300 20 IP
Enterprise 15 000 1 000 CIDR-список

Налаштування → API → Rate Limit. Для кожного ключа можна задати власний
поріг + білу IP-підмережу.

---

### 10. SLA (Q45) — витяг головних метрик

uptime: 99.9%
response_time_p95: 300ms
support:
critical: 2h
normal: 24h
backup:
rto: 1h
rpo: 15m

---

### 11. Плагіни сторонніх розробників (Q46)

    • SDK → @service/plugin-sdk (npm, v2.1).
    • Після завантаження архів проходить static analyzer + ручний code review.
    • Контракти: init(ctx), render(), onEvent(e).

---

### 12. Автозбереження темної теми (Q48)

- Налаштування зберігаються в localStorage.theme.
- Якщо cookies/LS очищаються після рестарту — увімкніть Sync settings, тоді тема зберігатиметься у хмарі.

---

### 13. Хто редагував файл останнім (Q49)

```
ai-cli files info <file-id> --json | jq '.last_modified_by'
```

CLI поверне:

```
{
"id": "u_123",
"email": "kate@acme.com",
"timestamp": "2025-06-28T09:18:01Z"
}
```

---

### 14. Обмеження доступу до API за IP (Q50)

```
POST /v1/apikeys/<id>/restrict
Authorization: Bearer <token>
Content-Type: application/json
```

```
{
"allowed_ips": ["203.0.113.0/24", "198.51.100.42"]
}
```

---

### 15. Додаткові розділи

- webhooks.md — приклади JSON-подій.
- integrations/jira.md — карта полів, сценарії автоматичного створення Issue.
