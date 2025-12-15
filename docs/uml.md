# 2.6. Модели в нотации UML

## 2.6.1. Диаграмма вариантов использования (Use Case) — поведенческая

```mermaid
flowchart TB
    subgraph system ["Система BookSwap"]
        UC1(("Регистрация"))
        UC2(("Авторизация"))
        UC3(("Редактирование профиля"))
        UC4(("Добавление книги"))
        UC5(("Редактирование книги"))
        UC6(("Удаление книги"))
        UC7(("Поиск книг"))
        UC8(("Просмотр карточки книги"))
        UC9(("Отправка запроса на обмен"))
        UC10(("Ответ на запрос"))
        UC11(("Чат с пользователем"))
        UC12(("Подтверждение обмена"))
        UC13(("Оценка пользователя"))
        UC14(("Управление wishlist"))
        UC15(("Модерация контента"))
        UC16(("Блокировка пользователя"))
        UC17(("Управление системой"))
        UC18(("Просмотр статистики"))
    end

    Guest["Гость"]
    User["Пользователь"]
    Moderator["Модератор"]
    Admin["Администратор"]

    Guest --> UC1
    Guest --> UC7
    Guest --> UC8

    User --> UC2
    User --> UC3
    User --> UC4
    User --> UC5
    User --> UC6
    User --> UC7
    User --> UC8
    User --> UC9
    User --> UC10
    User --> UC11
    User --> UC12
    User --> UC13
    User --> UC14

    Moderator --> UC15
    Moderator --> UC16

    Admin --> UC17
    Admin --> UC18

    UC4 -.->|"extend"| UC4a(("Автозаполнение по ISBN"))
    UC7 -.->|"extend"| UC7a(("Геолокационный поиск"))
    UC12 -.->|"include"| UC13
```

### Комментарии к диаграмме Use Case

**Акторы:**

| Актор | Описание |
|-------|----------|
| Гость | Неавторизованный пользователь. Может просматривать каталог и регистрироваться |
| Пользователь | Авторизованный участник. Полный доступ к функциям обмена |
| Модератор | Сотрудник платформы. Разбирает жалобы и блокирует нарушителей |
| Администратор | Технический специалист. Управляет настройками и просматривает статистику |

**Основные варианты использования:**

- *Регистрация / Авторизация* — создание аккаунта и вход в систему
- *Добавление книги* — внесение книги в личную библиотеку с возможностью автозаполнения по ISBN (extend)
- *Поиск книг* — текстовый и фильтрованный поиск с расширением геолокации (extend)
- *Отправка запроса на обмен* — инициация обмена книгами
- *Подтверждение обмена* — фиксация завершённой сделки, обязательно включает оценку (include)
- *Управление wishlist* — ведение списка желаемых книг

---

## 2.6.2. Диаграмма классов (Class Diagram) — структурная

```mermaid
classDiagram
    class User {
        +int id
        +string email
        +string password_hash
        +string name
        +string avatar_url
        +float latitude
        +float longitude
        +float rating
        +int exchanges_count
        +datetime created_at
        +bool is_verified
        +bool is_blocked
        +register()
        +login()
        +updateProfile()
        +updateLocation()
    }

    class Book {
        +int id
        +int owner_id
        +string title
        +string author
        +string isbn
        +string genre
        +string condition
        +string description
        +string[] photo_urls
        +bool is_available
        +datetime created_at
        +create()
        +update()
        +delete()
        +markUnavailable()
    }

    class Wishlist {
        +int id
        +int user_id
        +string title
        +string author
        +string isbn
        +datetime created_at
        +add()
        +remove()
    }

    class Exchange {
        +int id
        +int initiator_id
        +int owner_id
        +int book_id
        +int offered_book_id
        +string status
        +datetime created_at
        +datetime completed_at
        +create()
        +accept()
        +reject()
        +complete()
        +cancel()
    }

    class Message {
        +int id
        +int exchange_id
        +int sender_id
        +string text
        +datetime created_at
        +bool is_read
        +send()
        +markAsRead()
    }

    class Review {
        +int id
        +int exchange_id
        +int author_id
        +int target_id
        +int rating
        +string comment
        +datetime created_at
        +create()
    }

    class Notification {
        +int id
        +int user_id
        +string type
        +string title
        +string body
        +bool is_read
        +datetime created_at
        +send()
        +markAsRead()
    }

    class Report {
        +int id
        +int reporter_id
        +int target_user_id
        +string reason
        +string status
        +int moderator_id
        +string decision
        +datetime created_at
        +datetime resolved_at
        +create()
        +resolve()
    }

    User "1" --> "*" Book : owns
    User "1" --> "*" Wishlist : has
    User "1" --> "*" Exchange : initiates
    User "1" --> "*" Exchange : receives
    User "1" --> "*" Message : sends
    User "1" --> "*" Review : writes
    User "1" --> "*" Review : receives
    User "1" --> "*" Notification : receives
    User "1" --> "*" Report : submits
    User "1" --> "*" Report : moderates

    Book "1" --> "*" Exchange : subject_of
    Exchange "1" --> "*" Message : contains
    Exchange "1" --> "0..2" Review : has
```

### Комментарии к диаграмме классов

**Основные сущности:**

| Класс | Описание |
|-------|----------|
| User | Пользователь системы. Хранит учётные данные, геолокацию, рейтинг |
| Book | Книга в каталоге. Принадлежит пользователю, имеет статус доступности |
| Wishlist | Желаемая книга. Связь с пользователем без привязки к конкретному экземпляру |
| Exchange | Обмен. Связывает инициатора, владельца и книгу. Имеет статус жизненного цикла |
| Message | Сообщение в чате обмена. Привязано к конкретному Exchange |
| Review | Отзыв после обмена. Каждый участник может оставить один отзыв |
| Notification | Уведомление пользователя о событиях в системе |
| Report | Жалоба на пользователя. Обрабатывается модератором |

**Ключевые связи:**

- User → Book: один пользователь владеет многими книгами (1:*)
- User → Exchange: пользователь может быть инициатором или владельцем (1:*)
- Exchange → Message: один обмен содержит много сообщений (1:*)
- Exchange → Review: один обмен может иметь до двух отзывов — от каждой стороны (1:0..2)

**Статусы Exchange:**
- `pending` — ожидает ответа владельца
- `accepted` — принят, идёт согласование
- `rejected` — отклонён владельцем
- `completed` — обмен завершён
- `cancelled` — отменён одной из сторон

---

## 2.6.3. Диаграмма последовательности (Sequence Diagram) — поведенческая

### Сценарий: Успешный обмен книгами

```mermaid
sequenceDiagram
    autonumber
    participant I as Инициатор
    participant S as Система
    participant DB as База данных
    participant O as Владелец

    I->>S: Поиск книги
    S->>DB: SELECT books WHERE available
    DB-->>S: Список книг
    S-->>I: Результаты поиска

    I->>S: Запрос на обмен (book_id)
    S->>DB: INSERT exchange (status=pending)
    S->>O: Push-уведомление
    S-->>I: Запрос создан

    O->>S: Просмотр запроса
    S->>DB: SELECT exchange, user
    DB-->>S: Данные запроса и профиль
    S-->>O: Карточка запроса

    O->>S: Принять запрос
    S->>DB: UPDATE exchange (status=accepted)
    S->>I: Push-уведомление
    S-->>O: Запрос принят

    I->>S: Сообщение в чат
    S->>DB: INSERT message
    S->>O: Push-уведомление
    S-->>I: Отправлено

    O->>S: Сообщение в чат
    S->>DB: INSERT message
    S->>I: Push-уведомление
    S-->>O: Отправлено

    Note over I,O: Встреча и физический обмен книгами

    I->>S: Подтвердить получение
    S->>DB: UPDATE exchange (initiator_confirmed=true)
    S-->>I: Ожидание подтверждения владельца

    O->>S: Подтвердить передачу
    S->>DB: UPDATE exchange (status=completed)
    S->>DB: UPDATE book (is_available=false)
    S->>I: Запрос на отзыв
    S->>O: Запрос на отзыв
    S-->>O: Обмен завершён

    I->>S: Оставить отзыв (5 звёзд)
    S->>DB: INSERT review
    S->>DB: UPDATE user SET rating
    S-->>I: Отзыв сохранён

    O->>S: Оставить отзыв (5 звёзд)
    S->>DB: INSERT review
    S->>DB: UPDATE user SET rating
    S-->>O: Отзыв сохранён
```

### Комментарии к диаграмме последовательности

**Участники:**
- Инициатор — пользователь, желающий получить книгу
- Система — серверная часть BookSwap
- База данных — PostgreSQL
- Владелец — пользователь, владеющий книгой

**Этапы сценария:**

1. **Поиск (шаги 1–4):** Инициатор ищет книгу, система возвращает доступные варианты.

2. **Создание запроса (шаги 5–8):** Инициатор отправляет запрос, система сохраняет его со статусом `pending` и уведомляет владельца.

3. **Рассмотрение запроса (шаги 9–12):** Владелец просматривает профиль инициатора и принимает решение.

4. **Принятие (шаги 13–16):** Статус меняется на `accepted`, инициатор получает уведомление.

5. **Согласование в чате (шаги 17–24):** Стороны обмениваются сообщениями для договорённости о месте и времени встречи.

6. **Подтверждение обмена (шаги 25–32):** После физической встречи обе стороны подтверждают факт обмена. Книга помечается как недоступная.

7. **Отзывы (шаги 33–40):** Каждый участник оставляет оценку, рейтинги обновляются.