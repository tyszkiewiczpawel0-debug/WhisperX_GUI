$ErrorActionPreference = 'Stop'
# Keep this bootstrap ASCII: Windows PowerShell 5.1 reads BOM-less scripts as ANSI.
try {
    $configPath = Join-Path $PSScriptRoot 'config/local.toml'
    if (-not (Test-Path -LiteralPath $configPath -PathType Leaf)) {
        throw 'Brak config/local.toml. Skopiuj config/local.example.toml i uzupelnij sciezki wedlug README.'
    }
    # Configuration itself is UTF-8, including non-ASCII workstation paths.
    $matches = @(Select-String -LiteralPath $configPath -Encoding UTF8 -Pattern "^\s*python\s*=\s*'([^']+)'\s*$")
    if ($matches.Count -ne 1) {
        throw 'Niepoprawne pole python w config/local.toml. Wymagana jedna sciezka w pojedynczych apostrofach, jak we wzorze.'
    }
    $pythonPath = $matches[0].Matches[0].Groups[1].Value
    if (-not (Test-Path -LiteralPath $pythonPath -PathType Leaf)) {
        throw "Nie znaleziono interpretera Python: $pythonPath. Popraw config/local.toml."
    }
    & $pythonPath -B (Join-Path $PSScriptRoot 'src/gui.py')
    exit $LASTEXITCODE
}
catch {
    Write-Host ('Blad uruchomienia WhisperX GUI: ' + $_.Exception.Message) -ForegroundColor Red
    exit 1
}
