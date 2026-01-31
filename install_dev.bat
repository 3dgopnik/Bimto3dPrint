@echo off
chcp 65001 > nul
setlocal enableextensions enabledelayedexpansion
cd /d "%~dp0"

set "REVIT_VERSION=%~1"
set "ADDIN_SOURCE=%~dp0RevitPlugin\bin\Release\net48\Bimto3dPrint.addin"
set "DLL_SOURCE=%~dp0RevitPlugin\bin\Release\net48\Bimto3dPrint.dll"

call :print_header "Dev установка Bimto3dPrint"

if "%REVIT_VERSION%"=="" (
  call :fail "Укажите версию Revit. Пример: install_dev.bat 2024"
)

if not exist "%ADDIN_SOURCE%" (
  call :fail "Addin не найден. Сначала выполните build.bat."
)

if not exist "%DLL_SOURCE%" (
  call :fail "DLL не найдена. Сначала выполните build.bat."
)

set "ADDIN_DIR=%ProgramData%\Autodesk\Revit\Addins\%REVIT_VERSION%"
if not exist "%ADDIN_DIR%\" (
  call :fail "Папка Revit %REVIT_VERSION% не найдена: %ADDIN_DIR%"
)

call :print_step "Копирование в %ADDIN_DIR%"
copy /Y "%ADDIN_SOURCE%" "%ADDIN_DIR%\" > nul
if errorlevel 1 (
  call :fail "Не удалось скопировать addin в %ADDIN_DIR%"
)
copy /Y "%DLL_SOURCE%" "%ADDIN_DIR%\" > nul
if errorlevel 1 (
  call :fail "Не удалось скопировать DLL в %ADDIN_DIR%"
)

call :print_success "Установка завершена"
call :print_info "Запустите Revit %REVIT_VERSION% и проверьте кнопку Export for 3D Print."
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
exit /b 1
