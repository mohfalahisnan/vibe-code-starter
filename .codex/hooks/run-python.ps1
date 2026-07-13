param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Script,

    [Parameter(Position = 1, ValueFromRemainingArguments = $true)]
    [string[]]$ScriptArgs
)

$payload = [Console]::In.ReadToEnd()

function Invoke-Python {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Executable,
        [string[]]$PrefixArgs = @()
    )

    $arguments = @($PrefixArgs) + @($Script) + @($ScriptArgs)
    if ($payload.Length -gt 0) {
        $payload | & $Executable @arguments
    }
    else {
        & $Executable @arguments
    }
    $script:PythonExitCode = $LASTEXITCODE
}

if ($env:CODEX_PYTHON -and (Test-Path -LiteralPath $env:CODEX_PYTHON)) {
    Invoke-Python -Executable $env:CODEX_PYTHON
    exit $script:PythonExitCode
}

$runtimePattern = Join-Path $HOME ".cache/codex-runtimes/*/dependencies/python/python.exe"
$runtimePython = Get-ChildItem -Path $runtimePattern -File -ErrorAction SilentlyContinue |
    Select-Object -First 1
if ($runtimePython) {
    Invoke-Python -Executable $runtimePython.FullName
    exit $script:PythonExitCode
}

$launcher = Get-Command py.exe -ErrorAction SilentlyContinue
if ($launcher) {
    Invoke-Python -Executable $launcher.Source -PrefixArgs @("-3")
    exit $script:PythonExitCode
}

$python = Get-Command python.exe -ErrorAction SilentlyContinue
if ($python -and $python.Source -notlike "*WindowsApps*") {
    Invoke-Python -Executable $python.Source
    exit $script:PythonExitCode
}

Write-Error "No Python 3 runtime found. Set CODEX_PYTHON or install Python 3."
exit 127
