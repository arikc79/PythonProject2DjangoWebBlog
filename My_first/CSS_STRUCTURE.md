# 📁 Структура CSS файлів проекту Кінотеатр

CSS файли розбиті на модулі відповідно до функціональності та шаблонів.

## 🎨 CSS Файли

### 1. **base.css** - Базові стилі
**Використовується в:** `base.html` (завантажується на всіх сторінках)

**Містить:**
- CSS змінні (`:root`)
- Загальні стилі body, main-content
- Стилі навігації (navbar)
- Стилі футера
- Загальні стилі кнопок (.btn-primary, .btn-secondary, .btn-danger)
- Анімації (@keyframes fadeIn)
- Порожній стан (.empty-state)
- Плейсхолдер для постерів (.placeholder-poster)

---

### 2. **movie-list.css** - Список фільмів
**Використовується в:** `movie_list.html`

**Містить:**
- Стилі карток фільмів (.movie-card)
- Стилі постерів (.movie-poster)
- Заголовки фільмів (.movie-title)
- Жанри (.movie-genre)
- Рік і тривалість (.movie-year, .movie-duration)
- Hover ефекти для карток
- Responsive стилі

---

### 3. **movie-detail.css** - Деталі фільму
**Використовується в:** `movie_detail.html`

**Містить:**
- Заголовок деталей (.movie-detail-header)
- Великий постер (.movie-detail-poster)
- Рейтинг (.rating-badge)
- Заголовки секцій (.section-title)
- Картки відгуків (.review-card)
- Автор відгуку (.review-author)
- Оцінка відгуку (.review-rating)
- Текст відгуку (.review-text)
- Дата відгуку (.review-date)
- Responsive стилі

---

### 4. **session.css** - Сеанси
**Використовується в:** 
- `session_list.html`
- `movie_detail.html` (секція сеансів)

**Містить:**
- Картки сеансів (.session-card)
- Дата сеансу (.session-date)
- Номер зали (.session-hall)
- Hover ефекти

---

### 5. **forms.css** - Форми
**Використовується в:** 
- `movie_form.html`
- `movie_confirm_delete.html`
- `session_form.html`
- `session_confirm_delete.html`
- `review_confirm_delete.html`

**Містить:**
- Обгортка форми (.form-card)
- Заголовок форми (.form-title)

---

## 📋 Карта підключення CSS до шаблонів

| Шаблон | Підключені CSS файли |
|--------|---------------------|
| `base.html` | `base.css` (автоматично на всіх сторінках) |
| `movie_list.html` | `base.css` + `movie-list.css` |
| `movie_detail.html` | `base.css` + `movie-detail.css` + `session.css` + `forms.css` |
| `movie_form.html` | `base.css` + `forms.css` |
| `movie_confirm_delete.html` | `base.css` + `forms.css` |
| `session_list.html` | `base.css` + `session.css` |
| `session_form.html` | `base.css` + `forms.css` |
| `session_confirm_delete.html` | `base.css` + `forms.css` |
| `review_confirm_delete.html` | `base.css` + `forms.css` |

---

## 🔧 Як це працює

### 1. Базовий шаблон завантажує base.css

```html
<!-- base.html -->
<link rel="stylesheet" href="{% static 'cinema/css/base.css' %}">
{% block extra_css %}{% endblock %}
```

### 2. Дочірні шаблони додають специфічні CSS

```html
<!-- movie_list.html -->
{% block extra_css %}
    <link rel="stylesheet" href="{% static 'cinema/css/movie-list.css' %}">
{% endblock %}
```

---

## ✅ Переваги такої структури

1. **Модульність** - кожен CSS файл відповідає за певний функціонал
2. **Продуктивність** - завантажуються тільки потрібні стилі
3. **Підтримуваність** - легко знайти та змінити стилі
4. **Повторне використання** - `forms.css` та `session.css` використовуються в кількох місцях
5. **Чистота коду** - немає дублювання стилів
6. **Зручність розробки** - швидко знайти потрібні стилі

---

## 📝 Резервна копія

Старий об'єднаний файл збережено як `style.css.old` для порівняння або відновлення.

---

## 🎯 Рекомендації

- Якщо додаєте нову сторінку, створіть відповідний CSS файл
- Загальні стилі додавайте в `base.css`
- Специфічні стилі - в окремі файли
- Використовуйте CSS змінні з `:root` для кольорів

**Структура готова до використання!** ✨

