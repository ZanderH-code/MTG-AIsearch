# Test basic sorting functionality

$baseUrl = "https://mtg-ai-backend.onrender.com/api/search"

Write-Host "Testing basic sorting functionality..." -ForegroundColor Green

# Test with name sorting first
$body = @{
    query = "lightning bolt"
    language = "en"
    sort = "name"
    order = "asc"
} | ConvertTo-Json

try {
    Write-Host "`nTesting name sorting..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri $baseUrl -Method POST -Body $body -ContentType "application/json" -TimeoutSec 30
    
    Write-Host "Success! Found $($response.total_cards) cards" -ForegroundColor Green
    
    if ($response.cards.Count -gt 0) {
        Write-Host "First 3 cards:" -ForegroundColor White
        for ($i = 0; $i -lt [Math]::Min(3, $response.cards.Count); $i++) {
            Write-Host "  $($i+1). $($response.cards[$i].name)" -ForegroundColor White
        }
    }
}
catch {
    Write-Host "Name sorting failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test with CMC sorting
$body = @{
    query = "red creatures"
    language = "en"
    sort = "cmc"
    order = "desc"
} | ConvertTo-Json

try {
    Write-Host "`nTesting CMC sorting..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri $baseUrl -Method POST -Body $body -ContentType "application/json" -TimeoutSec 30
    
    Write-Host "Success! Found $($response.total_cards) cards" -ForegroundColor Green
    
    if ($response.cards.Count -gt 0) {
        Write-Host "First 3 cards:" -ForegroundColor White
        for ($i = 0; $i -lt [Math]::Min(3, $response.cards.Count); $i++) {
            $card = $response.cards[$i]
            Write-Host "  $($i+1). $($card.name) (CMC: $($card.mana_cost))" -ForegroundColor White
        }
    }
}
catch {
    Write-Host "CMC sorting failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nBasic test completed!" -ForegroundColor Green
