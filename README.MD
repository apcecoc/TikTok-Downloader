## 📚 **Как работает модуль**  

### 1. **Команды**  

Модуль предоставляет две основные команды:  

- **`/tiktokvid <ссылка_на_TikTok>`**  
  Загружает видео по указанной ссылке TikTok и отправляет его пользователю.  

- **`/tiktokaudio <ссылка_на_TikTok>`**  
  Извлекает аудио (в формате MP3) из указанного видео TikTok и отправляет его пользователю.  

### 2. **Процесс работы**  

- **Обработка ввода:**  
  Модуль принимает ссылку на TikTok, отправленную пользователем, и проверяет её корректность.   

- **Обработка ответа:**  
  В зависимости от команды пользователя:  
  - Для видео: загружает видеофайл и подготавливает его для отправки.  
  - Для аудио: извлекает MP3-аудио и подготавливает его для отправки.  

- **Отправка результата:**  
  Загруженный файл (видео или аудио) отправляется пользователю в чате.  

### 3. **Обработка ошибок**  

- Проверяется формат ссылки, чтобы убедиться, что это корректная ссылка TikTok.  
- Модуль обрабатывает ошибки сервера и предоставляет пользователю понятные сообщения в случае проблем (например, неверная ссылка или сбой обработки).  

---

## 📦 **Возможности**  

- Загрузка видео с TikTok в высоком качестве.  
- Извлечение MP3-аудио из TikTok-видео.  
- Простые и удобные команды для взаимодействия.  
- Надёжная обработка ошибок.  

---

## 🧑‍💻 **Разработчик**  

Создан @apcecoc.