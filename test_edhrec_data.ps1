# 检查Scryfall API中的EDHRec数据

$baseUrl = "https://api.scryfall.com/cards/search"

# 测试一些知名的EDH卡牌
$testCards = @(
    "Sol Ring",
    "Cyclonic Rift", 
    "Swords to Plowshares",
    "Counterspell",
    "Lightning Bolt"
)

Write-Host "检查Scryfall API中的EDHRec数据..." -ForegroundColor Green
Write-Host ("=" * 50) -ForegroundColor Yellow

foreach ($cardName in $testCards) {
    Write-Host "`n卡牌: $cardName" -ForegroundColor Cyan
    
    try {
        $params = @{
            q = "`"$cardName`""
            unique = "cards"
        }
        
        $headers = @{
            "User-Agent" = "MTG-AI-Search/1.0"
            "Accept" = "application/json"
        }
        
        $response = Invoke-RestMethod -Uri $baseUrl -Method GET -Body $params -Headers $headers -TimeoutSec 30
        
        if ($response.data.Count -gt 0) {
            $card = $response.data[0]
            Write-Host "  所有字段: $($card.PSObject.Properties.Name -join ', ')" -ForegroundColor Gray
            
            # 检查是否有EDHRec相关字段
            $edhrecFields = $card.PSObject.Properties.Name | Where-Object { $_ -like "*edhrec*" }
            if ($edhrecFields) {
                Write-Host "  ✅ 找到EDHRec相关字段: $($edhrecFields -join ', ')" -ForegroundColor Green
                foreach ($field in $edhrecFields) {
                    Write-Host "    $field`: $($card.$field)" -ForegroundColor White
                }
            } else {
                Write-Host "  ❌ 没有找到EDHRec相关字段" -ForegroundColor Red
            }
            
            # 检查其他可能的评分字段
            $ratingFields = $card.PSObject.Properties.Name | Where-Object { $_ -like "*rating*" -or $_ -like "*score*" }
            if ($ratingFields) {
                Write-Host "  📊 找到评分相关字段: $($ratingFields -join ', ')" -ForegroundColor Yellow
                foreach ($field in $ratingFields) {
                    Write-Host "    $field`: $($card.$field)" -ForegroundColor White
                }
            }
            
            # 显示一些重要字段的值
            $importantFields = @('name', 'cmc', 'power', 'toughness', 'rarity', 'set_name')
            Write-Host "  重要字段:" -ForegroundColor Magenta
            foreach ($field in $importantFields) {
                if ($card.PSObject.Properties.Name -contains $field) {
                    Write-Host "    $field`: $($card.$field)" -ForegroundColor White
                }
            }
        }
    }
    catch {
        Write-Host "❌ 获取 $cardName 失败: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n检查完成!" -ForegroundColor Green
