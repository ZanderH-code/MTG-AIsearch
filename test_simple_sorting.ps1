# 简单测试排序功能

$baseUrl = "https://mtg-ai-backend.onrender.com/api/search"

Write-Host "测试排序功能..." -ForegroundColor Green

# 测试按名称升序和降序
$testCases = @(
    @{
        name = "按名称升序"
        sort = "name"
        order = "asc"
    },
    @{
        name = "按名称降序"
        sort = "name"
        order = "desc"
    }
)

foreach ($testCase in $testCases) {
    Write-Host "`n测试: $($testCase.name)" -ForegroundColor Yellow
    
    $body = @{
        query = "red creatures"
        language = "en"
        sort = $testCase.sort
        order = $testCase.order
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri $baseUrl -Method POST -Body $body -ContentType "application/json" -TimeoutSec 60
        
        Write-Host "✅ 成功 - 找到 $($response.total_cards) 张卡牌" -ForegroundColor Green
        
        if ($response.cards.Count -gt 0) {
            Write-Host "前5张卡牌:" -ForegroundColor White
            for ($i = 0; $i -lt [Math]::Min(5, $response.cards.Count); $i++) {
                $card = $response.cards[$i]
                Write-Host "  $($i+1). $($card.name)" -ForegroundColor White
            }
        }
    }
    catch {
        Write-Host "❌ 失败: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n测试完成!" -ForegroundColor Green
