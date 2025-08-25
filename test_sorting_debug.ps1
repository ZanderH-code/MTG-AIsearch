# Debug sorting functionality

$baseUrl = "https://mtg-ai-backend.onrender.com/api/search"

Write-Host "Debugging sorting functionality..." -ForegroundColor Green

# Test with a simple query to see if sorting works
$body = @{
    query = "lightning bolt"
    language = "en"
    sort = "edhrec"
    order = "desc"
} | ConvertTo-Json

Write-Host "Request body:" -ForegroundColor Yellow
Write-Host $body -ForegroundColor Gray

try {
    $response = Invoke-RestMethod -Uri $baseUrl -Method POST -Body $body -ContentType "application/json" -TimeoutSec 60
    
    Write-Host "`nResponse received:" -ForegroundColor Green
    Write-Host "Total cards: $($response.total_cards)" -ForegroundColor Cyan
    Write-Host "Scryfall query: $($response.scryfall_query)" -ForegroundColor Cyan
    
    if ($response.cards.Count -gt 0) {
        Write-Host "`nFirst 10 cards:" -ForegroundColor White
        for ($i = 0; $i -lt [Math]::Min(10, $response.cards.Count); $i++) {
            $card = $response.cards[$i]
            Write-Host "  $($i+1). $($card.name)" -ForegroundColor White
        }
        
        # Check if cards are actually different
        $firstCard = $response.cards[0].name
        $sameCards = ($response.cards | Where-Object { $_.name -eq $firstCard }).Count
        Write-Host "`nCards with same name as first: $sameCards" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nDebug completed!" -ForegroundColor Green
