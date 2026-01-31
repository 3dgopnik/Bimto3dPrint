@echo off
chcp 65001 > nul
setlocal enableextensions enabledelayedexpansion
cd /d "%~dp0"

set "APP_NAME=Bimto3dPrint"
set "PYTHON_EXE=python"
set "ADDIN_SOURCE=%~dp0RevitPlugin\Bimto3dPrint.addin"
set "DLL_SOURCE="
set "LOG_DIR=%ProgramData%\Bimto3dPrint\Logs"

call :print_header "Установка %APP_NAME%"

where %PYTHON_EXE% > nul 2>&1
if errorlevel 1 (
  call :fail "Python не найден. Установите Python 3.8+ и повторите запуск."
)

"%PYTHON_EXE%" -m pip --version > nul 2>&1
if errorlevel 1 (
  call :fail "pip не найден. Установите pip или переустановите Python."
)

if not exist "%ADDIN_SOURCE%" (
  call :fail "Файл addin не найден: %ADDIN_SOURCE%"
)

if exist "%~dp0RevitPlugin\bin\Release\net48\Bimto3dPrint.dll" set "DLL_SOURCE=%~dp0RevitPlugin\bin\Release\net48\Bimto3dPrint.dll"
if not defined DLL_SOURCE if exist "%~dp0RevitPlugin\bin\Release\Bimto3dPrint.dll" set "DLL_SOURCE=%~dp0RevitPlugin\bin\Release\Bimto3dPrint.dll"
if not defined DLL_SOURCE if exist "%~dp0RevitPlugin\Bimto3dPrint.dll" set "DLL_SOURCE=%~dp0RevitPlugin\Bimto3dPrint.dll"

if not defined DLL_SOURCE (
  call :fail "Bimto3dPrint.dll не найден. Запустите build.bat или используйте релизный пакет."
)

call :print_step "Установка Python-модуля"
"%PYTHON_EXE%" -m pip install "%~dp0PythonProcessor"
if errorlevel 1 (
  call :fail "Не удалось установить Python-модуль. Проверьте доступ к зависимостям."
)

call :print_step "Создание папки логов"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
if errorlevel 1 (
  call :fail "Не удалось создать папку логов: %LOG_DIR%"
)

set "FOUND_REvit=0"
for %%V in (2022 2023 2024 2025) do (
  set "ADDIN_DIR=%ProgramData%\Autodesk\Revit\Addins\%%V"
  if exist "!ADDIN_DIR!\" (
    call :print_step "Копирование в Revit %%V"
    copy /Y "%ADDIN_SOURCE%" "!ADDIN_DIR!\" > nul
    if errorlevel 1 (
      call :fail "Не удалось скопировать addin в !ADDIN_DIR!"
    )
    copy /Y "%DLL_SOURCE%" "!ADDIN_DIR!\" > nul
    if errorlevel 1 (
      call :fail "Не удалось скопировать DLL в !ADDIN_DIR!"
    )
    set "FOUND_REvit=1"
  ) else (
    call :print_step "Revit %%V не найден"
  )
)

if "%FOUND_REvit%"=="0" (
  call :fail "Не найдены папки Revit 2022-2025. Убедитесь, что Revit установлен."
)

call :print_success "Установка завершена"
call :print_info "Дальше:"
call :print_info "1) Запустите Revit."
call :print_info "2) Убедитесь, что кнопка 'Export for 3D Print' доступна."
call :print_info "3) Логи будут в %LOG_DIR%."
exit /b 0

:print_header
set "MSG=%~1"
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║ %MSG%
echo ╚════════════════════════════════════════════════════════════╝
echo.
exit /b 0

:print_step
echo [*] %~1
exit /b 0

:print_success
echo.
echo ✓ %~1
echo.
exit /b 0

:print_info
echo    - %~1
exit /b 0

:fail
echo.
echo ✗ ОШИБКА: %~1
echo.
echo Подсказка: запустите скрипт от имени администратора и проверьте путь.
exit /b 1
