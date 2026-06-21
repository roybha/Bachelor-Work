// main.js - відповідає за основну логіку сторінки (обробка подій, взаємодія між UI та API)
// імпорт функцій з допоміжних файлів
import { detectImage } from "./api.js";
import { showResults } from "./ui.js";

// Отримуємо всі необхідні DOM-елементи
const input = document.getElementById("imageInput");
const detectBtn = document.getElementById("detectBtn");
const previewImg = document.getElementById("preview");
const modelSelect = document.getElementById("modelSelect");

const confSlider = document.getElementById("confSlider");
const confValue = document.getElementById("confValue");

// Слайдер значення confidence, що синхронізує своє значення з текстом поруч
if (confSlider && confValue) {
    confSlider.addEventListener("input", () => {
        // Відображаємо поточне значення(0.25, 0.50, 0.75)
        confValue.textContent = confSlider.value;
    });
} else {
     // Якщо HTML зміниться і елементів не буде — повідомлення про проблему
    console.error("Елементи слайдера не знайдено в HTML!");
}

// Функція для отримання списку моделей з сервера
// Якщо моделей нема/сталася помилка —  показуємо відповідне повідомлення
async function loadModels() {
    try {
        // Завантажує список доступних моделей із бекенду через GET-запит на /models
        const res = await fetch("/models");
        const models = await res.json();

         // Очищаємо тег випадаючого списку перед наповненням
        modelSelect.innerHTML = "";

        // Якщо моделей немає — показуємо повідомлення
        if (models.length === 0) {
             const opt = document.createElement("option");
             opt.text = "Моделі відсутні у папці weights";
             modelSelect.add(opt);
             return;
        }

        // Динамічно наповнююмо випадаючий список, якщо вони є
        models.forEach((modelName, index) => {
            const opt = document.createElement("option");
            opt.value = modelName;
            opt.text = modelName;

            // Перша модель за замовчуванням - перша за індексом(0)
            if (index === 0) opt.selected = true; // Вибрати першу за замовчуванням
            modelSelect.add(opt);
        });
    } catch (e) {
        //Якщо сервер недоступний або сталася інша помилка
        console.error("Не вдалося завантажити моделі:", e);
        modelSelect.innerHTML = "<option>Помилка з'єднання</option>";
    }
}

// Завантажуємо список одразу при завантаженні сторінки
loadModels();

//  Обробник кнопки Detect, що формує запит до бекенду і
//  отримує результат, передаючи його в UI
detectBtn.addEventListener("click", async () => {
  // Перевірка, чи обрано файл
  if (!input.files.length) {
    alert("Оберіть файл");
    return;
  }

  // Отримуємо вибрану модель і confidence( якщо слацдер відсутній - 0.5 за замовчуванням)
  const selectedModel = modelSelect.value;
  const confidence = confSlider ? confSlider.value : 0.5;

  // Додаткова перевірка обраної моделі
  if (!selectedModel) {
      alert("Будь ласка, оберіть модель зі списку (або перевірте папку weights)");
      return;
  }

  // Показ прев'ю локального файлу ще до відправки до backend-у
  const file = input.files[0];
  previewImg.src = URL.createObjectURL(file);

  try {
    // Відправляємо файл + параметри на сервер
    const result = await detectImage(file, selectedModel, confidence);

    // Передаємо результат у UI-шар
    showResults(result, previewImg);

  } catch (err) {
    // Центральна обробка помилок
    console.error(err);
    alert("Помилка: " + err.message);
  }
});