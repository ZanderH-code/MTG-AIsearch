import re
import json
import os
from typing import Dict, List, Any

class MTGPreprocessor:
    """MTG术语预处理器，用于将中文/俚语转换为标准英文术语"""
    
    def __init__(self, glossary_path: str = "mtg_glossary.json"):
        """初始化预处理器
        
        Args:
            glossary_path: 术语词典文件路径
        """
        self.glossary_path = glossary_path
        self.glossary = self._load_glossary()
        
    def _load_glossary(self) -> Dict[str, Any]:
        """加载术语词典"""
        try:
            # 获取当前文件所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            glossary_file = os.path.join(current_dir, "..", self.glossary_path)
            
            with open(glossary_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"加载术语词典失败: {e}")
            return {"terms": {}, "regex_rules": []}
    
    def preprocess_input(self, user_input: str, language: str = "zh") -> str:
        """预处理用户输入
        
        Args:
            user_input: 用户输入的自然语言查询
            language: 输入语言 ("zh" 或 "en")
            
        Returns:
            预处理后的文本
        """
        text = user_input
        
        if language == "zh":
            # 中文输入：术语替换 + 正则表达式
            # 1. 正则表达式替换（处理模糊/俚语表达）
            for rule in self.glossary.get("regex_rules", []):
                try:
                    pattern = rule["pattern"]
                    replacement = rule["replacement"]
                    text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
                except Exception as e:
                    print(f"正则替换失败 {pattern}: {e}")
                    continue
            
            # 2. 术语替换（处理一一对应的术语）
            for term, replacement in self.glossary.get("terms", {}).items():
                try:
                    text = text.replace(term, replacement)
                except Exception as e:
                    print(f"术语替换失败 {term}: {e}")
                    continue
                    
        elif language == "en":
            # 英文输入：标准化MTG俚语和术语
            # 1. 处理常见的MTG俚语
            english_slang_mapping = {
                "hate bears": "2/2 creatures with disruptive abilities",
                "bolt test": "creatures that can be killed by Lightning Bolt",
                "dies to removal": "creatures easily removed",
                "dork": "small utility creatures",
                "fatty": "large expensive creatures",
                "evasion": "flying, menace, or unblockable",
                "removal": "destroy or exile effects",
                "cantrip": "spells that draw a card",
                "wrath": "destroy all creatures",
                "burn": "direct damage spells",
                "engine": "cards that generate card advantage",
                "value": "card advantage effects",
                "curve": "mana curve considerations",
                "tempo": "time advantage strategies",
                "aggro": "aggressive low-cost strategies",
                "control": "defensive control strategies",
                "combo": "combination strategies",
                "midrange": "medium-cost strategies",
                "finisher": "game-winning cards",
                "staple": "commonly used cards"
            }
            
            # 2. 应用英文俚语替换
            for slang, standard in english_slang_mapping.items():
                text = text.replace(slang, standard)
            
            # 3. 处理常见的MTG术语缩写
            abbreviation_mapping = {
                "cmc": "mana value",
                "mv": "mana value",
                "pow": "power",
                "tou": "toughness",
                "pt": "power and toughness",
                "loy": "loyalty",
                "kw": "keyword",
                "o:": "oracle text:",
                "c:": "color:",
                "t:": "type:",
                "r:": "rarity:",
                "is:": "special:"
            }
            
            # 4. 应用缩写替换
            for abbrev, full in abbreviation_mapping.items():
                text = text.replace(abbrev, full)
        
        return text
    
    def get_processed_examples(self) -> Dict[str, List[str]]:
        """获取预处理示例"""
        examples = {
            "zh": [
                "帮我找个地落套牌的强力终端",
                "控制套牌的清场法术",
                "具有飞行能力的生物",
                "艾斯波控制套牌的法术",
                "仇恨熊",
                "组合技的引擎卡",
                "红色烧牌",
                "穿透生物"
            ],
            "en": [
                "hate bears for control deck",
                "bolt test creatures",
                "aggro deck dorks",
                "combo engine cards",
                "evasion creatures",
                "removal spells",
                "burn spells",
                "wrath effects"
            ]
        }
        
        # 预处理中文示例
        processed_zh = []
        for example in examples["zh"]:
            processed = self.preprocess_input(example, "zh")
            processed_zh.append(f"{example} → {processed}")
        
        # 预处理英文示例
        processed_en = []
        for example in examples["en"]:
            processed = self.preprocess_input(example, "en")
            processed_en.append(f"{example} → {processed}")
        
        return {
            "zh": processed_zh,
            "en": processed_en
        }

# 创建全局预处理器实例
mtg_preprocessor = MTGPreprocessor()

def preprocess_mtg_query(user_input: str, language: str = "zh") -> str:
    """便捷函数：预处理MTG查询
    
    Args:
        user_input: 用户输入
        language: 语言 ("zh" 或 "en")
        
    Returns:
        预处理后的文本
    """
    return mtg_preprocessor.preprocess_input(user_input, language)
