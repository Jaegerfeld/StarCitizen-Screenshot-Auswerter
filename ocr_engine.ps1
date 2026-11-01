# -*- coding: utf-8 -*-
# =============================================================================
# Autor:          Robert Seebauer
# Repository:     https://github.com/Jaegerfeld/StarCitizen-Screenshot-Auswerter
# KI-Unterstuetzung: Erstellt mit Unterstuetzung von Claude (Anthropic)
# Erstellt:       28.10.2026
# Geaendert:      28.10.2026
# Lizenz:         BSD-3-Clause (siehe LICENSE)
#
# Fachliche Funktion:
#   Optionaler, genauerer Leseweg nur fuer Windows: liest Screenshots der
#   Star-Citizen-Handelskonsole mit der eingebauten Windows-OCR
#   (Windows.Media.Ocr, offline, ohne Zusatzsoftware) statt mit Tesseract.js
#   im Browser. Je Bild entstehen drei Ausschnitte (linkes Panel mit dem
#   Standort, rechtes Panel mit den Waren, rechtes Panel mit hohem Kontrast
#   als zweite Lesung fuer die Preise); dazu wird die Helligkeit hinter den
#   Reitern "Kaufen" und "Lokaler Marktwert" gemessen, um den aktiven Reiter
#   (Kauf oder Verkauf) zu erkennen.
#   Ergebnis ist ocr_words.json mit allen Woertern samt Lage in
#   Original-Bildkoordinaten. Gestartet wird das Skript ueber
#   Windows_OCR_lesen.bat; die JSON-Datei wird dann in die Browser-Seite
#   SC_Screenshot_Auswerter.html gezogen, die sie mit demselben Parser
#   auswertet wie die Browser-OCR. OCR-Sprache: Deutsch bevorzugt, sonst
#   Profilsprache, sonst Englisch.
# =============================================================================
<#
  SC Screenshot-Auswerter – OCR-Engine
  Liest Handelskonsolen-Screenshots mit der eingebauten Windows-OCR (Windows.Media.Ocr, offline).
  Je Bild werden drei Ausschnitte erzeugt (System.Drawing, ohne Zusatzsoftware):
    L  : linkes Panel  (Standort), 3-fach vergroessert, Graustufen
    R  : rechtes Panel (Waren),    3-fach vergroessert, Graustufen
    RB : rechtes Panel,            4-fach vergroessert, hoher Kontrast (zweite Lesung fuer Preise)
  Alle erkannten Woerter werden mit Position in Original-Bildkoordinaten nach JSON geschrieben.

  Aufruf (normalerweise durch Windows_OCR_lesen.bat; die JSON-Datei wird danach in
  SC_Screenshot_Auswerter.html gezogen):
    powershell -ExecutionPolicy Bypass -File ocr_engine.ps1 -Folder "C:\Screenshots" -Out ocr_words.json
    powershell -ExecutionPolicy Bypass -File ocr_engine.ps1 -Images "a.jpg","b.png" -Out ocr_words.json
#>
param(
  [string[]]$Images,
  [string]$Folder,
  [string]$Pattern = "*.*",
  [Parameter(Mandatory = $true)][string]$Out
)
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

# ---- WinRT + await bridge (PowerShell 5.1) ----
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Storage.StorageFile, Windows.Foundation, ContentType = WindowsRuntime]
try { Add-Type -AssemblyName System.Runtime.WindowsRuntime -ErrorAction Stop }
catch { [System.Reflection.Assembly]::LoadWithPartialName("System.Runtime.WindowsRuntime") | Out-Null }
$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and
    $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
# Waits synchronously for a WinRT IAsyncOperation and returns its result typed as $t.
function Await($op, $t) {
  $m = $asTaskGeneric.MakeGenericMethod($t)
  $task = $m.Invoke($null, @($op)); $task.Wait(-1) | Out-Null; $task.Result
}

# ---- OCR engine: German preferred (German game client), else profile language, else English ----
$engine = $null
foreach ($tag in @("de-DE", "de")) {
  if (-not $engine) { try { $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage((New-Object Windows.Globalization.Language $tag)) } catch {} }
}
if (-not $engine) { $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages() }
if (-not $engine) { $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage((New-Object Windows.Globalization.Language "en-US")) }
if (-not $engine) { Write-Error "Keine Windows-OCR-Sprache verfuegbar (Einstellungen > Sprache > Sprachpaket mit OCR installieren)."; exit 2 }
Write-Host ("OCR-Sprache: " + $engine.RecognizerLanguage.DisplayName)

# Runs Windows OCR on one image file and returns its words with bounding boxes (image pixels).
function Ocr-File($path) {
  $sf = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($path)) ([Windows.Storage.StorageFile])
  $stream = Await ($sf.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
  $dec = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
  $bmp = Await ($dec.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
  $res = Await ($engine.RecognizeAsync($bmp)) ([Windows.Media.Ocr.OcrResult])
  $stream.Dispose()
  $words = New-Object System.Collections.ArrayList
  foreach ($line in $res.Lines) {
    foreach ($word in $line.Words) {
      $r = $word.BoundingRect
      [void]$words.Add([ordered]@{ text = $word.Text; x = [double]$r.X; y = [double]$r.Y; w = [double]$r.Width; h = [double]$r.Height })
    }
  }
  return $words
}

# ---- Crop + upscale + colour filter (System.Drawing) ----
# Crops a region, upscales it by $scale, converts to greyscale with contrast $contrast and saves it as PNG.
function Make-Variant($src, $x0, $y0, $w, $h, $scale, $contrast, $dest) {
  $bmp = New-Object System.Drawing.Bitmap ([int]($w * $scale)), ([int]($h * $scale)), ([System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
  # Greyscale (luminance) + contrast stretched around 0.5: v' = (v-0.5)*c+0.5
  $t = (0.5 - (0.5 * $contrast))
  $m = New-Object 'float[][]' 5
  $m[0] = [float[]]@((0.299 * $contrast), (0.299 * $contrast), (0.299 * $contrast), 0, 0)
  $m[1] = [float[]]@((0.587 * $contrast), (0.587 * $contrast), (0.587 * $contrast), 0, 0)
  $m[2] = [float[]]@((0.114 * $contrast), (0.114 * $contrast), (0.114 * $contrast), 0, 0)
  $m[3] = [float[]]@(0, 0, 0, 1, 0)
  $m[4] = [float[]]@($t, $t, $t, 0, 1)
  $cm = New-Object -TypeName System.Drawing.Imaging.ColorMatrix -ArgumentList (, $m)
  $ia = New-Object System.Drawing.Imaging.ImageAttributes
  $ia.SetColorMatrix($cm)
  $destRect = New-Object System.Drawing.Rectangle 0, 0, $bmp.Width, $bmp.Height
  $g.DrawImage($src, $destRect, [int]$x0, [int]$y0, [int]$w, [int]$h, [System.Drawing.GraphicsUnit]::Pixel, $ia)
  $g.Dispose()
  $bmp.Save($dest, [System.Drawing.Imaging.ImageFormat]::Png)
  $bmp.Dispose()
}

# ---- Active tab: mean brightness behind "KAUFEN" / "LOKALER MARKTWERT" (the active tab is lit) ----
# Returns the mean luminance of a rectangle (every second pixel), or $null for an empty area.
function Mean-Brightness($img, $x, $y, $w, $h) {
  $bmp = New-Object System.Drawing.Bitmap $img
  $x0 = [math]::Max(0, [int]$x); $y0 = [math]::Max(0, [int]$y)
  $x1 = [math]::Min($bmp.Width - 1, [int]($x + $w)); $y1 = [math]::Min($bmp.Height - 1, [int]($y + $h))
  $sum = 0.0; $n = 0
  for ($yy = $y0; $yy -le $y1; $yy += 2) { for ($xx = $x0; $xx -le $x1; $xx += 2) {
      $c = $bmp.GetPixel($xx, $yy); $sum += (0.299 * $c.R + 0.587 * $c.G + 0.114 * $c.B); $n++ } }
  $bmp.Dispose()
  if ($n -eq 0) { return $null } else { return [math]::Round($sum / $n, 1) }
}
# Measures the brightness behind the BUY and LOCAL MARKET VALUE tab words found in the R variant.
function Measure-Tabs($img, $variants) {
  $words = ($variants | Where-Object { $_.tag -eq "R" } | Select-Object -First 1).words
  $out = [ordered]@{ kaufen = $null; markt = $null }
  foreach ($wd in $words) {
    $t = $wd.text.ToUpper()
    if ($t -like "KAUF*" -and $out.kaufen -eq $null) { $out.kaufen = Mean-Brightness $img ($wd.x - $wd.w * 0.3) ($wd.y - $wd.h * 0.3) ($wd.w * 1.6) ($wd.h * 1.6) }
    elseif (($t -like "LOKAL*" -or $t -like "MARKT*" -or $t -like "MRKT*") -and $out.markt -eq $null) { $out.markt = Mean-Brightness $img ($wd.x - $wd.w * 0.3) ($wd.y - $wd.h * 0.3) ($wd.w * 1.6) ($wd.h * 1.6) }
  }
  return $out
}

# ---- Input files ----
$files = @()
if ($Images) { $files = $Images | ForEach-Object { Get-Item -LiteralPath $_ } }
elseif ($Folder) { $files = Get-ChildItem -LiteralPath $Folder -File | Where-Object { $_.Name -like $Pattern -and $_.Extension -match '^\.(png|jpe?g|bmp)$' } | Sort-Object Name }
if (-not $files) { Write-Error "Keine Screenshots gefunden."; exit 1 }

$tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("sc_ocr_" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $tmp | Out-Null
$pages = New-Object System.Collections.ArrayList
try {
  foreach ($f in $files) {
    Write-Host ("OCR: " + $f.Name)
    $src = [System.Drawing.Image]::FromFile($f.FullName)
    $W = $src.Width; $H = $src.Height
    $variants = @(
      @{ tag = "L";  x0 = 0;                  y0 = 0; w = [int]($W * 0.45); h = $H; scale = 3; contrast = 1.3 },
      @{ tag = "R";  x0 = [int]($W * 0.55);   y0 = 0; w = $W - [int]($W * 0.55); h = $H; scale = 3; contrast = 1.3 },
      @{ tag = "RB"; x0 = [int]($W * 0.55);   y0 = 0; w = $W - [int]($W * 0.55); h = $H; scale = 4; contrast = 3.0 }
    )
    $vout = New-Object System.Collections.ArrayList
    foreach ($v in $variants) {
      $dest = Join-Path $tmp ($f.BaseName + "_" + $v.tag + ".png")
      Make-Variant $src $v.x0 $v.y0 $v.w $v.h $v.scale $v.contrast $dest
      $words = Ocr-File $dest
      foreach ($wd in $words) {   # back to original image coordinates
        $wd.x = [math]::Round($v.x0 + $wd.x / $v.scale, 1); $wd.y = [math]::Round($v.y0 + $wd.y / $v.scale, 1)
        $wd.w = [math]::Round($wd.w / $v.scale, 1); $wd.h = [math]::Round($wd.h / $v.scale, 1)
      }
      [void]$vout.Add([ordered]@{ tag = $v.tag; words = $words })
      Write-Host ("   " + $v.tag + ": " + $words.Count + " Woerter")
    }
    $tabs = Measure-Tabs $src $vout
    $src.Dispose()
    [void]$pages.Add([ordered]@{ file = $f.Name; path = $f.FullName; imgW = $W; imgH = $H
        mtime = $f.LastWriteTime.ToString("s"); tabs = $tabs; variants = $vout })
  }
}
finally { Remove-Item -LiteralPath $tmp -Recurse -Force -ErrorAction SilentlyContinue }

$payload = [ordered]@{ generated = (Get-Date -Format s); ocrLanguage = $engine.RecognizerLanguage.LanguageTag; pages = $pages }
[System.IO.File]::WriteAllText($Out, ($payload | ConvertTo-Json -Depth 8), (New-Object System.Text.UTF8Encoding $false))
Write-Host ("geschrieben: " + $Out)
