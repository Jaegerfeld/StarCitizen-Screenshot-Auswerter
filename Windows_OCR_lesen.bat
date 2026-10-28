@echo off
rem Optional: Screenshots mit der Windows-OCR lesen (genauer als die Browser-OCR, nur Windows).
rem Ordner oder Bilder auf diese Datei ziehen. Ergebnis: ocr_words.json neben den Screenshots -
rem diese Datei dann in SC_Screenshot_Auswerter.html ziehen.
setlocal
cd /d "%~dp0"
if "%~1"=="" (echo Bitte einen Ordner oder Bilder auf diese Datei ziehen. & pause & exit /b 1)
if exist "%~1\" (
  powershell -NoProfile -ExecutionPolicy Bypass -File ocr_engine.ps1 -Folder "%~1" -Out "%~1\ocr_words.json"
) else (
  set IMGS=%1
  :loop
  shift
  if not "%~1"=="" (set IMGS=%IMGS%,%1& goto loop)
  powershell -NoProfile -ExecutionPolicy Bypass -File ocr_engine.ps1 -Images %IMGS% -Out "%~dp1ocr_words.json"
)
if errorlevel 1 (echo. & echo Fehler - siehe Meldung oben. & pause & exit /b 1)
echo.
echo Fertig: ocr_words.json liegt neben den Screenshots. Jetzt SC_Screenshot_Auswerter.html oeffnen und die Datei hineinziehen.
start "" "SC_Screenshot_Auswerter.html"
pause
