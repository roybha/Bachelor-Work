// ui.js - відповідає за відображення результатів користувачеві

// Функція безпосереднього відображення результатів детекції на сторінці
// data - об'єкт (base64) відповіді від бекенду
// imgElerment - DOM-елемент(<img>), що підставляється у результат
export function showResults(data, imgElement) {
  // Встановлюємо зображення, що повернув backend (з bbox)
  // Backend віддає base64, тож збираємо src
  imgElement.src = "data:image/png;base64," + data.image_base64;

  // Блок статистики, де є час інференсу та кількість знайдених об'єктів
  const statsBlock = document.getElementById("statsBlock");
  const timeVal = document.getElementById("timeVal");
  const countVal = document.getElementById("countVal");

  // Робимо блок видимим, в разі наявності результатів
  if (statsBlock) {
      statsBlock.style.display = "block";
      // Отримуємо час обробкти зі серверу
      timeVal.textContent = data.inference_time;
      countVal.textContent = data.object_count;
  }

  // Таблиця результатів, що очищується від старих даних
  const tbody = document.querySelector("#resultsTable tbody");
  tbody.innerHTML = "";

  // Кнопка скачування вже обробленого зображення
  const downloadLink = document.getElementById("downloadLink");
  if (downloadLink) {
      downloadLink.href = imgElement.src; // Показуємо ту ж картинку
      downloadLink.style.display = "inline-block"; // Показуємо кнопку
  }

  // Заповнення таблиці, для кожного знайденого об'єкта додаємо рядок
  data.objects.forEach(obj => {
    const row = document.createElement("tr");

    // class_name — клас об'єкта
    // confidence — ймовірність (у %)
    row.innerHTML = `
      <td>${obj.class_name}</td>
      <td>${(obj.confidence * 100).toFixed(1)}%</td>
    `;
    tbody.appendChild(row);
  });
}