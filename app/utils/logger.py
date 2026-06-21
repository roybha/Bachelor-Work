import logging
import sys

# Налаштування формату: Час - Рівень - Повідомлення
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("YOLO_APP")