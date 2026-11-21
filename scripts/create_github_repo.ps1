param(
    [string]$RepoName = "taller2-consumo-energetico-uptc",
    [bool]$Private = $false
)

$inputLines = @"
protocol=https
host=github.com
username=sebastiansierra13

"@

$output = $inputLines | git credential fill
$token = ""
foreach ($line in $output) {
    if ($line -match "^password=(.+)$") {
        $token = $matches[1].Trim()
        break
    }
}

if (-not $token) {
    Write-Error "No se pudo recuperar el token de GitHub desde Git Credential Manager."
    exit 1
}

$body = @{
    name = $RepoName
    description = "Taller II: Preparacion de datos para modelos de prediccion y optimizacion del consumo energetico (UPTC Especializacion en IA)"
    private = $Private
} | ConvertTo-Json

$headers = @{
    "Authorization" = "Bearer $token"
    "User-Agent" = "PowerShell-GitHub-Client"
    "Accept" = "application/vnd.github.v3+json"
}

Write-Host "Creando repositorio '$RepoName' en GitHub..."
try {
    $response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $body -ContentType "application/json"
    Write-Host "Repositorio creado exitosamente en: $($response.html_url)"
    $repoUrl = $response.clone_url
} catch {
    Write-Host "Aviso al crear repositorio: $($_.Exception.Message)"
    # Si ya existe, construimos la URL
    $repoUrl = "https://github.com/sebastiansierra13/$RepoName.git"
}

Write-Host "Configurando remoto en git..."
git remote remove origin 2>$null
git remote add origin "https://github.com/sebastiansierra13/$RepoName.git"
git remote -v

Write-Host "Subiendo ramas a GitHub..."
git push -u origin main
