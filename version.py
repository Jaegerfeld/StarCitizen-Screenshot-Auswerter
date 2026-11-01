# =============================================================================
# Autor:          Robert Seebauer
# Repository:     https://github.com/Jaegerfeld/StarCitizen-Screenshot-Auswerter
# KI-Unterstützung: Erstellt mit Unterstützung von Claude (Anthropic)
# Erstellt:       28.10.2026
# Geändert:       01.11.2026
# Lizenz:         BSD-3-Clause (siehe LICENSE)
#
# Fachliche Funktion:
#   Einzige Quelle der Versionsnummer des Screenshot-Auswerters. Der Build
#   (auswerter_bauen.py) setzt sie in die Seite, die Kopfzeile und den
#   „Was ist neu?“-Dialog ein; der Export trägt sie im Feld "generator".
# =============================================================================
"""Single source of the Screenshot-Auswerter version number."""

#: Current release of the reader (semantic versioning); shown on the page and in exports.
VERSION = "0.7.1"
