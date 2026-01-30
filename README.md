# Bimto3dPrint

[Баннер/логотип — placeholder]

## RU

### 🎯 Что это?

Bimto3dPrint — автоматический инструмент для извлечения внешней оболочки здания из Revit/IFC и подготовки модели к 3D-печати на принтерах Bambu Lab и других FDM/FFF устройствах.

**Одна кнопка в Revit → готовая модель для 3ds Max и 3D-принтера.**

### ✨ Возможности

- ✅ Автоматическая фильтрация элементов (только оболочка здания)
- ✅ Исключение мебели, инженерных систем и внутренних перегородок
- ✅ Закрытие оконных/дверных проёмов для герметичного меша
- ✅ Оптимизация геометрии для 3D-печати
- ✅ Экспорт в форматы: FBX (3ds Max), OBJ, STL
- ✅ Валидация модели для печати
- ✅ Масштабирование под размер принтера

### 🖼️ Скриншоты

Плейсхолдер для будущих скриншотов:

- До: сложная Revit-модель с мебелью и инженерией
- После: чистая оболочка здания, готовая к печати

### 🎬 Демо

Плейсхолдер для видео или GIF с процессом экспорта.

---

### 📥 Установка

#### Требования

**Система:**

- Windows 10/11
- Autodesk Revit 2022–2025
- Python 3.8+
- 4 GB RAM минимум
- 10 GB свободного места

**Опционально:**

- 3ds Max для доработки модели
- Bambu Studio для подготовки к печати

#### Шаг 1: Установка Python-модуля

Откройте CMD или PowerShell:

```bash
# Склонировать репозиторий
git clone https://github.com/3dgopnik/Bimto3dPrint.git
cd Bimto3dPrint

# Перейти в папку Python
cd PythonProcessor

# Установить зависимости
pip install -r requirements.txt

# Установить как пакет
pip install -e .

# Проверить установку
bimto3dprint --help
```

#### Шаг 2: Установка плагина Revit

**Автоматическая установка (рекомендуется):**

1. Скачать последний релиз: <https://github.com/3dgopnik/Bimto3dPrint/releases>
2. Запустить `Install_Bimto3dPrint.bat`
3. Перезапустить Revit

**Ручная установка:**

1. Собрать проект `RevitPlugin` в Visual Studio (см. документацию разработчика).
2. Скопировать файлы:
   - `Bimto3dPrint.dll` → `%APPDATA%\Autodesk\Revit\Addins\2024\`
   - `Bimto3dPrint.addin` → `%APPDATA%\Autodesk\Revit\Addins\2024\`
3. Перезапустить Revit

#### Шаг 3: Проверка установки

1. Открыть Revit.
2. На вкладке Add-Ins должна появиться кнопка **Bimto3dPrint**.
3. Если кнопки нет — см. раздел Troubleshooting.

---

### 🚀 Быстрый старт

#### Использование в Revit (GUI)

**Сценарий 1: Простое использование**

1. Откройте модель в Revit.
2. Нажмите кнопку **Bimto3dPrint**.
3. В диалоге выберите:
   - **Пресет:** `shell_only`
   - **Формат вывода:** FBX или STL
   - **Путь сохранения:** папка для результата
4. Нажмите **Export**.
5. Дождитесь завершения (индикатор прогресса).
6. Откройте результат в 3ds Max или Bambu Studio.

**Сценарий 2: Настройка параметров**

1. Выберите пресет `custom`.
2. Настройте категории:
   - ✅ Стены (внешние)
   - ✅ Крыша
   - ✅ Перекрытия (верх/низ)
   - ❌ Мебель
   - ❌ Двери/окна (или включите «Закрыть проёмы»)
3. Настройте упрощение:
   - Уровень детализации: Low/Medium/High
   - Минимальная толщина стенок: 2–3 мм
4. Укажите масштаб (если модель большая).
5. Нажмите **Export**.

#### Использование через CLI

```bash
# Базовое использование
bimto3dprint process model.ifc --output building_shell.stl

# С выбором пресета
bimto3dprint process model.ifc --preset shell_only --output result.fbx --format fbx

# С настройками
bimto3dprint process model.ifc \
  --preset shell_with_structure \
  --output output.obj \
  --format obj \
  --scale 0.1 \
  --simplify high

# Проверка модели на пригодность к печати
bimto3dprint validate building_shell.stl

# Список доступных пресетов
bimto3dprint list-presets
```

---

### 📖 Пресеты конфигурации

Пресеты находятся в `Config/Presets/`:

| Пресет | Описание | Использование |
| --- | --- | --- |
| **shell_only** | Только внешняя оболочка, проёмы закрыты | Максимально простая модель для печати |
| **shell_with_structure** | Оболочка + несущие колонны/балки | Сохранение конструктива |
| **full_exterior** | Внешние элементы (балконы, лестницы, козырьки) | Детальная модель |
| **simple_box** | Максимальное упрощение | Концептуальная модель |

**Создание своего пресета:**

1. Скопируйте любой JSON из `Config/Presets/`.
2. Измените настройки категорий.
3. Сохраните с новым именем.
4. Используйте: `--preset my_custom_preset`.

---

### 🔧 Troubleshooting

**Проблема: Revit не видит плагин**

1. Проверьте путь `%APPDATA%\Autodesk\Revit\Addins\2024\`.
2. Убедитесь, что там есть `Bimto3dPrint.dll` и `Bimto3dPrint.addin`.
3. Проверьте поддерживаемую версию Revit (2022–2025).
4. Посмотрите логи Revit в `C:\Users\[USER]\AppData\Local\Autodesk\Revit\[VERSION]\Journals\`.

**Проблема: Python not found**

1. Проверьте `python --version`.
2. Добавьте Python в PATH.
3. При необходимости укажите полный путь в настройках плагина.

**Проблема: пустой результат**

1. Проверьте пресеты в `Config/Presets/`.
2. Попробуйте `full_exterior`.
3. Посмотрите логи: `%APPDATA%/Bimto3dPrint/logs/`.

**Проблема: модель не герметична (not watertight)**

1. Включите «Закрыть проёмы».
2. Запустите `bimto3dprint validate model.stl`.
3. Упростите геометрию (High).
4. Почините меш в Meshmixer или Blender.

**Проблема: модель слишком большая**

1. Укажите масштаб (например, 0.01 для 1:100).
2. В CLI: `--scale 0.01`.
3. Для Bambu Lab H2S максимум 450×450×450 мм.

---

### 📚 Документация

- [User guide (RU)](docs/ru/user_guide.md)
- [User guide (EN)](docs/en/user_guide.md)
- [CLI (RU)](docs/ru/cli.md)
- [CLI (EN)](docs/en/cli.md)
- [Configuration (RU)](docs/ru/config.md)
- [Configuration (EN)](docs/en/config.md)
- [Troubleshooting (RU)](docs/ru/troubleshooting.md)
- [Troubleshooting (EN)](docs/en/troubleshooting.md)

---

### 🗺️ Roadmap

См. [ROADMAP.md](ROADMAP.md).

---

### 🤝 Contributing

См. [CONTRIBUTING.md](CONTRIBUTING.md).

---

### 📄 Лицензия

TBD.

---

### 👏 Благодарности

- [IFC_BuildingEnvExtractor](https://github.com/tudelft3d/IFC_BuildingEnvExtractor)
- Revit API Community
- Разработчики ifcopenshell и trimesh

---

### 📞 Контакты / Поддержка

- Issues: <https://github.com/3dgopnik/Bimto3dPrint/issues>
- Discussions: <https://github.com/3dgopnik/Bimto3dPrint/discussions>

---

### Badges (placeholder)

- ![GitHub release](...)
- ![License](...)
- ![Python version](...)
- ![Revit version](...)

## EN

### 🎯 What is it?

Bimto3dPrint is an automated tool that extracts the building exterior shell from Revit/IFC and prepares it for 3D printing on Bambu Lab and other FDM/FFF printers.

**One click in Revit → a ready-to-print model for 3ds Max and your 3D printer.**

### ✨ Features

- ✅ Automatic element filtering (building shell only)
- ✅ Excludes furniture, MEP, and internal partitions
- ✅ Seals window/door openings for watertight meshes
- ✅ Geometry optimization for 3D printing
- ✅ Export formats: FBX (3ds Max), OBJ, STL
- ✅ Model validation for printability
- ✅ Scaling to printer volume

### 🖼️ Screenshots

Placeholder for future screenshots:

- Before: complex Revit model with furniture/MEP
- After: clean building shell ready to print

### 🎬 Demo

Placeholder for a video or GIF demo.

---

### 📥 Installation

#### Requirements

**System:**

- Windows 10/11
- Autodesk Revit 2022–2025
- Python 3.8+
- 4 GB RAM minimum
- 10 GB free disk space

**Optional:**

- 3ds Max for post-editing
- Bambu Studio for print prep

#### Step 1: Install the Python module

Open CMD or PowerShell:

```bash
# Clone the repo
git clone https://github.com/3dgopnik/Bimto3dPrint.git
cd Bimto3dPrint

# Go to the Python folder
cd PythonProcessor

# Install dependencies
pip install -r requirements.txt

# Install editable package
pip install -e .

# Verify installation
bimto3dprint --help
```

#### Step 2: Install the Revit plugin

**Automatic install (recommended):**

1. Download the latest release: <https://github.com/3dgopnik/Bimto3dPrint/releases>
2. Run `Install_Bimto3dPrint.bat`
3. Restart Revit

**Manual install:**

1. Build the `RevitPlugin` project in Visual Studio (see developer docs).
2. Copy the files:
   - `Bimto3dPrint.dll` → `%APPDATA%\Autodesk\Revit\Addins\2024\`
   - `Bimto3dPrint.addin` → `%APPDATA%\Autodesk\Revit\Addins\2024\`
3. Restart Revit

#### Step 3: Verify installation

1. Open Revit.
2. You should see the **Bimto3dPrint** button under Add-Ins.
3. If the button is missing, check Troubleshooting.

---

### 🚀 Quick start

#### Using Revit (GUI)

**Scenario 1: Simple workflow**

1. Open your model in Revit.
2. Click **Bimto3dPrint**.
3. Choose:
   - **Preset:** `shell_only`
   - **Output format:** FBX or STL
   - **Output path:** destination folder
4. Click **Export**.
5. Wait for completion (progress bar).
6. Open the result in 3ds Max or Bambu Studio.

**Scenario 2: Custom settings**

1. Choose the `custom` preset.
2. Configure categories:
   - ✅ Walls (exterior only)
   - ✅ Roof
   - ✅ Floors (top/bottom)
   - ❌ Furniture
   - ❌ Doors/Windows (or enable “Seal openings”)
3. Simplification options:
   - Detail level: Low/Medium/High
   - Minimum wall thickness: 2–3 mm
4. Set scaling (if the model is large).
5. Click **Export**.

#### Using CLI

```bash
# Basic usage
bimto3dprint process model.ifc --output building_shell.stl

# Using a preset
bimto3dprint process model.ifc --preset shell_only --output result.fbx --format fbx

# With custom options
bimto3dprint process model.ifc \
  --preset shell_with_structure \
  --output output.obj \
  --format obj \
  --scale 0.1 \
  --simplify high

# Validate printability
bimto3dprint validate building_shell.stl

# List available presets
bimto3dprint list-presets
```

---

### 📖 Configuration presets

Presets live in `Config/Presets/`:

| Preset | Description | Use case |
| --- | --- | --- |
| **shell_only** | Exterior shell only, openings sealed | Simplest print-ready model |
| **shell_with_structure** | Shell + structural columns/beams | Keeps structural context |
| **full_exterior** | All exterior elements (balconies, stairs, canopies) | Detailed model |
| **simple_box** | Maximum simplification | Conceptual models |

**Create your own preset:**

1. Copy any JSON from `Config/Presets/`.
2. Adjust category filters.
3. Save with a new name.
4. Use it via `--preset my_custom_preset`.

---

### 🔧 Troubleshooting

**Problem: Revit does not see the plugin**

1. Check `%APPDATA%\Autodesk\Revit\Addins\2024\`.
2. Confirm `Bimto3dPrint.dll` and `Bimto3dPrint.addin` are present.
3. Verify supported Revit versions (2022–2025).
4. Review Revit logs in `C:\Users\[USER]\AppData\Local\Autodesk\Revit\[VERSION]\Journals\`.

**Problem: Python not found**

1. Run `python --version`.
2. Ensure Python is on PATH.
3. Set a full Python path in the plugin settings if needed.

**Problem: Empty export result**

1. Review presets in `Config/Presets/`.
2. Try the `full_exterior` preset.
3. Check logs at `%APPDATA%/Bimto3dPrint/logs/`.

**Problem: Model is not watertight**

1. Enable “Seal openings”.
2. Run `bimto3dprint validate model.stl`.
3. Simplify geometry (High).
4. Repair the mesh in Meshmixer or Blender.

**Problem: Model is too large for the printer**

1. Use scaling (for example, 0.01 for 1:100).
2. CLI: `--scale 0.01`.
3. Bambu Lab H2S max volume: 450×450×450 mm.

---

### 📚 Documentation

- [User guide (RU)](docs/ru/user_guide.md)
- [User guide (EN)](docs/en/user_guide.md)
- [CLI (RU)](docs/ru/cli.md)
- [CLI (EN)](docs/en/cli.md)
- [Configuration (RU)](docs/ru/config.md)
- [Configuration (EN)](docs/en/config.md)
- [Troubleshooting (RU)](docs/ru/troubleshooting.md)
- [Troubleshooting (EN)](docs/en/troubleshooting.md)

---

### 🗺️ Roadmap

See [ROADMAP.md](ROADMAP.md).

---

### 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

### 📄 License

TBD.

---

### 👏 Acknowledgements

- [IFC_BuildingEnvExtractor](https://github.com/tudelft3d/IFC_BuildingEnvExtractor)
- Revit API Community
- ifcopenshell & trimesh maintainers

---

### 📞 Support

- Issues: <https://github.com/3dgopnik/Bimto3dPrint/issues>
- Discussions: <https://github.com/3dgopnik/Bimto3dPrint/discussions>

---

### Badges (placeholder)

- ![GitHub release](...)
- ![License](...)
- ![Python version](...)
- ![Revit version](...)
