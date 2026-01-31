@echo off
chcp 65001 > nul
setlocal enableextensions enabledelayedexpansion
cd /d "%~dp0"

call :print_header "Очистка артефактов сборки"

call :remove_dir "%~dp0PythonProcessor\build"
call :remove_dir "%~dp0PythonProcessor\dist"
call :remove_dir "%~dp0PythonProcessor\*.egg-info"

call :remove_dir "%~dp0RevitPlugin\bin"
call :remove_dir "%~dp0RevitPlugin\obj"

for /d /r "%~dp0" %%D in (__pycache__) do call :remove_dir "%%D"
for /r "%~dp0" %%F in (*.pyc *.pyo) do call :remove_file "%%F"
for /r "%~dp0" %%F in (*.user *.suo) do call :remove_file "%%F"

call :print_success "Очистка завершена"
exit /b 0

:remove_dir
if exist "%~1" (
  rmdir /s /q "%~1"
  if errorlevel 1 (
    call :fail "Не удалось удалить папку %~1"
  )
  call :print_step "Удалено: %~1"
)
exit /b 0

:remove_file
if exist "%~1" (
  del /f /q "%~1"
  if errorlevel 1 (
    call :fail "Не удалось удалить файл %~1"
  )
  call :print_step "Удалено: %~1"
)
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
