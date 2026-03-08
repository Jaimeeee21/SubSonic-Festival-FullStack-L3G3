param(
    [string]$RootPath = (Get-Location).Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-DataVariableName {
    param([string]$BaseName)

    # Example: "product-detail" -> "PRODUCT_DETAIL_DATA"
    return ($BaseName -replace '-', '_').ToUpperInvariant() + '_DATA'
}

if (-not (Test-Path -LiteralPath $RootPath)) {
    throw "La ruta '$RootPath' no existe."
}

$jsonFiles = Get-ChildItem -LiteralPath $RootPath -File -Filter '*-data.json' | Sort-Object Name

if (-not $jsonFiles -or $jsonFiles.Count -eq 0) {
    Write-Host 'No se encontraron archivos *-data.json para sincronizar.' -ForegroundColor Yellow
    exit 0
}

$updatedCount = 0

foreach ($jsonFile in $jsonFiles) {
    $baseName = $jsonFile.BaseName -replace '-data$', ''
    $varName = Get-DataVariableName -BaseName $baseName
    $jsPath = Join-Path $RootPath ($baseName + '-data.js')

    $jsonContent = Get-Content -LiteralPath $jsonFile.FullName -Raw -Encoding UTF8
    $jsContent = "window.$varName = $jsonContent`r`n"

    [System.IO.File]::WriteAllText($jsPath, $jsContent, [System.Text.UTF8Encoding]::new($false))
    $updatedCount++

    Write-Host ("Sincronizado: {0} -> {1} ({2})" -f $jsonFile.Name, (Split-Path $jsPath -Leaf), $varName)
}

Write-Host ("Completado. Archivos sincronizados: {0}" -f $updatedCount) -ForegroundColor Green
