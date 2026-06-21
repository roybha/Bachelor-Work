// api.js - відповідає за взаємодію з бекендом (логіка HTTP-запитів)

// Функція, що виконує запит до бекенду для детекції об'єктів на зображенні
// file — файл зображення (File із input)
// modelName — назва моделі, яку потрібно використати
// confidence — поріг впевненості для фільтрації детекцій
export async function detectImage(file, modelName, confidence) {

  // Формуємо об'єкт multipart/form-data, що очікується FastAPI backend-ом
  const formData = new FormData();
  formData.append("file", file);
  formData.append("model_name", modelName);
  formData.append("confidence", confidence);

  // відправлямо POST запит із стовреним об'єктом
  const response = await fetch("/detect/annotated_data", {
    method: "POST",
    body: formData
  });

  // Якщо отримали помилку — передаємо її вгору для обробки в main.js
  if (!response.ok) {
    const errData = await response.json();
    throw new Error(errData.detail || "Помилка детекції");
  }

  // Результат - JSON із набором даних (bbox, класи, час, кількість)
  return await response.json();
}