# Test EDHREC sorting functionality

$baseUrl = "https://mtg-ai-backend.onrender.com/api/search"

Write-Host "Testing EDHREC sorting functionality..." -ForegroundColor Green

# Test different sorting methods
$testCases = @(
    @{
        name = "By Name Ascending"
        sort = "name"
        order = "asc"
    },
    @{
        name = "By EDHREC Rating Descending"
        sort = "edhrec"
        order = "desc"
    }
)

foreach ($testCase in $testCases) {
    Write-Host "`nTest: $($testCase.name)" -ForegroundColor Yellow
    
    $body = @{
        query = "red creatures"
        language = "en"
        sort = $testCase.sort
        order = $testCase.order
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri $baseUrl -Method POST -Body $body -ContentType "application/json" -TimeoutSec 60
        
        Write-Host "Success - Found $($response.total_cards) cards" -ForegroundColor Green
        Write-Host "Scryfall query: $($response.scryfall_query)" -ForegroundColor Cyan
        
        if ($response.cards.Count -gt 0) {
            Write-Host "First 5 cards:" -ForegroundColor White
            for ($i = 0; $i -lt [Math]::Min(5, $response.cards.Count); $i++) {
                $card = $response.cards[$i]
                Write-Host "  $($i+1). $($card.name)" -ForegroundColor White
            }
        }
    }
    catch {
        Write-Host "Failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`nTest completed!" -ForegroundColor Green
