param(
    [Parameter(Mandatory=$true)][string]$SourceRom,
    [Parameter(Mandatory=$true)][string]$OutputRom,
    [Parameter(Mandatory=$true)][string]$XdeltaExe
)
$ErrorActionPreference = 'Stop'
$info = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'verification.json') -Raw | ConvertFrom-Json
$sourcePath = (Resolve-Path -LiteralPath $SourceRom).Path
$toolPath = (Resolve-Path -LiteralPath $XdeltaExe).Path
$patchPath = Join-Path $PSScriptRoot $info.xdelta_patch.filename
$outputPath = [System.IO.Path]::GetFullPath($OutputRom)
if (Test-Path -LiteralPath $outputPath) { throw 'Output already exists; choose a new filename.' }
if ([System.IO.Path]::GetExtension($outputPath) -ne '.gba') { throw 'Output must be a .gba file.' }
if (-not (Test-Path -LiteralPath ([System.IO.Path]::GetDirectoryName($outputPath)) -PathType Container)) {
    throw 'Output parent directory must already exist.'
}
if ((Get-Item -LiteralPath $sourcePath).Length -ne $info.source.bytes -or
    (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash -ne $info.source.sha256) {
    throw 'Unsupported source ROM: size or SHA-256 differs.'
}
if ((Get-FileHash -LiteralPath $patchPath -Algorithm SHA256).Hash -ne $info.xdelta_patch.sha256) {
    throw 'Patch SHA-256 differs.'
}
if ((Get-FileHash -LiteralPath $toolPath -Algorithm SHA256).Hash -ne $info.xdelta_tool.sha256) {
    throw 'Use the pinned official Windows xdelta3 3.2.2 x86_64 executable.'
}
$temporaryPath = $outputPath + '.' + [Guid]::NewGuid().ToString('N') + '.tmp'
$savedXdeltaOptions = $env:XDELTA
try {
    $env:XDELTA = $null
    & $toolPath -d -s $sourcePath $patchPath $temporaryPath
    if ($LASTEXITCODE -ne 0) { throw 'xdelta3 failed.' }
    if ((Get-Item -LiteralPath $temporaryPath).Length -ne $info.target.bytes -or
        (Get-FileHash -LiteralPath $temporaryPath -Algorithm SHA256).Hash -ne $info.target.sha256) {
        throw 'Applied output differs from the tested ROM.'
    }
    [System.IO.File]::Move($temporaryPath, $outputPath)
    Write-Output "PASS: $outputPath"
    Write-Output 'Development build only: automatic Hangul keyboard/save is not installed.'
}
finally {
    $env:XDELTA = $savedXdeltaOptions
    if (Test-Path -LiteralPath $temporaryPath) { Remove-Item -LiteralPath $temporaryPath }
}
