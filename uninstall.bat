@echo off
chcp 65001 > nul
setlocal enableextensions enabledelayedexpansion
cd /d "%~dp0"

set "PYTHON_EXE=python"
set "LOG_DIR=%ProgramData%\Bimto3dPrint\Logs"

call :print_header "Удаление Bimto3dPrint"

where %PYTHON_EXE% > nul 2>&1
if errorlevel 1 (
  call :fail "Python не найден. Установите Python 3.8+ и повторите."
)

"%PYTHON_EXE%" -m pip uninstall -y bimto3dprint
if errorlevel 1 (
  call :print_step "Python-модуль не найден или уже удалён"
)

for %%V in (2022 2023 2024 2025) do (
  set "ADDIN_DIR=%ProgramData%\Autodesk\Revit\Addins\%%V"
  if exist "!ADDIN_DIR!\" (
    call :print_step "Удаление из Revit %%V"
    del /f /q "!ADDIN_DIR!\Bimto3dPrint.addin" > nul 2>&1
    del /f /q "!ADDIN_DIR!\Bimto3dPrint.dll" > nul 2>&1
  )
)

if exist "%LOG_DIR%" (
  call :print_step "Очистка папки логов"
  rmdir /s /q "%LOG_DIR%"
)

call :print_success "Удаление завершено"
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

:fail
echo.
echo ✗ ОШИБКА: %~1
echo.
exit /b 1
