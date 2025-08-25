# 测试排序功能的PowerShell脚本

$baseUrl = "https://mtg-ai-backend.onrender.com/api/search"

# 测试用例
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
    },
    @{
        name = "按法力值升序"
        sort = "cmc"
        order = "asc"
    },
    @{
        name = "按法力值降序"
        sort = "cmc"
        order = "desc"
    },
    @{
        name = "按力量降序"
        sort = "power"
        order = "desc"
    }
)

foreach ($testCase in $testCases) {
    Write-Host "`n测试: $($testCase.name)" -ForegroundColor Green
    Write-Host "排序参数: $($testCase.sort):$($testCase.order)" -ForegroundColor Yellow
    
    $body = @{
        query = "red creatures"
        language = "en"
        sort = $testCase.sort
        order = $testCase.order
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri $baseUrl -Method POST -Body $body -ContentType "application/json"
        
        Write-Host "✅ 成功 - 找到 $($response.total_cards) 张卡牌" -ForegroundColor Green
        Write-Host "Scryfall查询: $($response.scryfall_query)" -ForegroundColor Cyan
        
        if ($response.cards.Count -gt 0) {
            Write-Host "前3张卡牌:" -ForegroundColor White
            for ($i = 0; $i -lt [Math]::Min(3, $response.cards.Count); $i++) {
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
