param([int]$runs = 10)

$executable = "x64/Debug/Tema3.exe"
$csvFile = "rezultate_mediu.csv"

$testConfigs = @(
    @{Varianta = "secventiala"; Procese = 1},
    @{Varianta = "mpi_send"; Procese = 5},
    @{Varianta = "mpi_scatter"; Procese = 4},
    @{Varianta = "mpi_async"; Procese = 5}
)

"Varianta,Procese,Tip,TimpMediu" | Out-File $csvFile -Encoding UTF8

Write-Host "=== TESTARE MPI CU CALCUL MEDIE ===" -ForegroundColor Cyan
Write-Host "Rulez $runs rulari per test..." -ForegroundColor White
Write-Host ""

foreach ($config in $testConfigs) {
    $varianta = $config.Varianta
    $procese = $config.Procese
    
    Write-Host "=== $varianta cu $procese procese ===" -ForegroundColor Green
    
    $content = @"
#include <iostream>
#include <string>
using namespace std;

int variantaSecventiala();
int variantaMPISend();
int variantaMPIScatter();
int variantaMPIAsincron();

string varianta = "$varianta";

int main(int argc, char* argv[]) {
    if (varianta == "secventiala") variantaSecventiala();
    else if (varianta == "mpi_send") variantaMPISend();
    else if (varianta == "mpi_scatter") variantaMPIScatter();
    else if (varianta == "mpi_async") variantaMPIAsincron();
    return 0;
}
"@
    $content | Out-File "Tema3.cpp" -Encoding UTF8
    Start-Sleep -Milliseconds 100

    $sumaTimp = 0
    for ($i = 1; $i -le $runs; $i++) {
        Write-Host "  Run $i..." -NoNewline
        
        if ($procese -eq 1) {
            $time = Measure-Command { .\$executable 2>$null }
        } else {
            $time = Measure-Command { & "mpiexec" -n $procese .\$executable 2>$null }
        }
        
        $timp = [math]::Round($time.TotalSeconds, 6)
        $sumaTimp += $timp
        Write-Host " $timp secunde" -ForegroundColor White
    }
    
    $media = [math]::Round(($sumaTimp / $runs), 6)
    Write-Host "  ** MEDIE: $media secunde **" -ForegroundColor Green
    
    Add-Content $csvFile "$varianta,$procese,16_16,$media"
    
    Write-Host ""
}

Write-Host "=== TESTARE COMPLETATA ===" -ForegroundColor Cyan
Write-Host "Rezultate medii salvate in: $csvFile" -ForegroundColor Yellow

Write-Host "`nRezultatele medii:" -ForegroundColor White
Get-Content $csvFile | ForEach-Object { Write-Host "  $_" }