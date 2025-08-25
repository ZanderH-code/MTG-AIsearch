# 通过我们的API测试EDHRec排序

$baseUrl = "https://mtg-ai-backend.onrender.com/api/search"

Write-Host "测试EDHRec排序功能..." -ForegroundColor Green

$body = @{
    query = "Sol Ring"
    language = "en"
    sort = "edhrec"
    order = "desc"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri $baseUrl -Method POST -Body $body -ContentType "application/json" -TimeoutSec 60
    
    Write-Host "✅ API调用成功" -ForegroundColor Green
    Write-Host "找到 $($response.total_cards) 张卡牌" -ForegroundColor Cyan
    
    if ($response.cards.Count -gt 0) {
        Write-Host "`n前5张卡牌:" -ForegroundColor Yellow
        for ($i = 0; $i -lt [Math]::Min(5, $response.cards.Count); $i++) {
            $card = $response.cards[$i]
            Write-Host "  $($i+1). $($card.name)" -ForegroundColor White
        }
        
        Write-Host "`n注意: 如果EDHRec排序没有生效，前几张卡牌应该都是相同的" -ForegroundColor Red
    }
}
catch {
    Write-Host "❌ 测试失败: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n测试完成!" -ForegroundColor Green
