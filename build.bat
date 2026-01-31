@echo off
chcp 65001 > nul
setlocal enableextensions enabledelayedexpansion
cd /d "%~dp0"

set "APP_NAME=Bimto3dPrint"
set "PYTHON_EXE=python"
set "MSBUILD_EXE="
set "PROJECT_FILE=%~dp0RevitPlugin\Bimto3dPrint.csproj"

call :print_header "Сборка %APP_NAME% (для разработчиков)"

where %PYTHON_EXE% > nul 2>&1
if errorlevel 1 (
  call :fail "Python не найден. Установите Python 3.8+ и повторите."
)

"%PYTHON_EXE%" -m pip --version > nul 2>&1
if errorlevel 1 (
  call :fail "pip не найден. Установите pip или переустановите Python."
)

set "VSWHERE=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"
if exist "%VSWHERE%" (
  for /f "usebackq delims=" %%I in (`"%VSWHERE%" -latest -products * -requires Microsoft.Component.MSBuild -find MSBuild\**\Bin\MSBuild.exe`) do (
    set "MSBUILD_EXE=%%I"
  )
)

if not defined MSBUILD_EXE (
  call :fail "MSBuild не найден. Установите Visual Studio 2019/2022 с компонентом MSBuild."
)

if not exist "%PROJECT_FILE%" (
  call :fail "Проект не найден: %PROJECT_FILE%"
)

call :print_step "Установка Python-модуля (editable)"
"%PYTHON_EXE%" -m pip install -e "%~dp0PythonProcessor"
if errorlevel 1 (
  call :fail "Не удалось установить Python-модуль."
)

call :print_step "Восстановление NuGet пакетов"
"%MSBUILD_EXE%" "%PROJECT_FILE%" /t:Restore /p:Configuration=Release /p:Platform=x64
if errorlevel 1 (
  call :fail "Не удалось восстановить NuGet пакеты."
)

call :print_step "Сборка Revit плагина"
"%MSBUILD_EXE%" "%PROJECT_FILE%" /t:Build /p:Configuration=Release /p:Platform=x64
if errorlevel 1 (
  call :fail "Сборка плагина завершилась с ошибкой."
)

call :print_success "Сборка завершена"
call :print_info "DLL: %~dp0RevitPlugin\bin\Release\net48\Bimto3dPrint.dll"
call :print_info "ADDIN: %~dp0RevitPlugin\bin\Release\net48\Bimto3dPrint.addin"
call :print_info "Дальше: запустите install_dev.bat <версия Revit>."
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
