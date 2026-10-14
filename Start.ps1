$ErrorActionPreference = 'Stop'
$configPath = Join-Path $PSScriptRoot 'config/local.toml'
if (-not (Test-Path -LiteralPath $configPath)) { throw 'Uzupełnij config/local.toml według README.' }
# The template uses a TOML literal string for the interpreter, no shell evaluation.
$match = Select-String -LiteralPath $configPath -Pattern "^python\s*=\s*'([^']+)'\s*$"
if (-not $match) { throw 'Pole python musi być pojedynczo cytowaną ścieżką TOML (jak we wzorze).' }
$pythonPath = $match.Matches[0].Groups[1].Value
& $pythonPath -B (Join-Path $PSScriptRoot 'src/gui.py')
