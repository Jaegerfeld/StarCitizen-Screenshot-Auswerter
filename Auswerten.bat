@echo off
rem SC Screenshot-Auswerter: Ordner oder Bilder auf diese Datei ziehen, oder ohne Argument starten
rem (dann wird der Standard-Screenshot-Ordner von Star Citizen abgefragt).
setlocal
cd /d "%~dp0"
if "%~1"=="" (
  set /p SRC=Ordner mit Konsolen-Screenshots:
  python auswerter.py "%SRC%"
) else (
  python auswerter.py %*
)
if errorlevel 1 (echo. & echo Fehler - siehe Meldung oben. & pause & exit /b 1)
for %%A in (%1) do set FIRST=%%~A
if "%FIRST%"=="" set FIRST=%SRC%
if exist "%FIRST%\Auswertung\auswertung.html" start "" "%FIRST%\Auswertung\auswertung.html"
if exist "%FIRST%\..\Auswertung\auswertung.html" start "" "%FIRST%\..\Auswertung\auswertung.html"
pause
