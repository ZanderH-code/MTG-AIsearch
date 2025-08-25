# 简单测试EDHRec数据

$baseUrl = "https://api.scryfall.com/cards/search"

Write-Host "检查Scryfall API中的EDHRec数据..." -ForegroundColor Green

try {
    $params = @{
        q = '"Sol Ring"'
        unique = "cards"
    }
    
    $headers = @{
        "User-Agent" = "MTG-AI-Search/1.0"
        "Accept" = "application/json"
    }
    
    $response = Invoke-RestMethod -Uri $baseUrl -Method GET -Body $params -Headers $headers -TimeoutSec 30
    
    if ($response.data.Count -gt 0) {
        $card = $response.data[0]
        Write-Host "`n卡牌: $($card.name)" -ForegroundColor Cyan
        Write-Host "所有字段: $($card.PSObject.Properties.Name -join ', ')" -ForegroundColor Gray
        
        # 检查EDHRec字段
        $edhrecFields = $card.PSObject.Properties.Name | Where-Object { $_ -like "*edhrec*" }
        if ($edhrecFields) {
            Write-Host "✅ 找到EDHRec字段: $($edhrecFields -join ', ')" -ForegroundColor Green
        } else {
            Write-Host "❌ 没有找到EDHRec字段" -ForegroundColor Red
        }
        
        # 检查评分字段
        $ratingFields = $card.PSObject.Properties.Name | Where-Object { $_ -like "*rating*" -or $_ -like "*score*" }
        if ($ratingFields) {
            Write-Host "📊 找到评分字段: $($ratingFields -join ', ')" -ForegroundColor Yellow
        }
    }
}
catch {
    Write-Host "❌ 测试失败: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n测试完成!" -ForegroundColor Green
