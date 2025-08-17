# English Conversation App

## ２０２５年８月１７日 修正内容

### 修正点

#### 1. constants.py の改善

**日常英会話プロンプトの強化 (SYSTEM_TEMPLATE_BASIC_CONVERSATION)**
- 構造化された指導原則を追加
- 段階的なエラー修正戦略（エコー修正）を導入
- 会話技術とレスポンスガイドラインを明確化

**レベル別問題生成プロンプトの追加**
- `SYSTEM_TEMPLATE_CREATE_PROBLEM_BEGINNER`: 初級者用（8-12語）
- `SYSTEM_TEMPLATE_CREATE_PROBLEM_INTERMEDIATE`: 中級者用（12-16語）  
- `SYSTEM_TEMPLATE_CREATE_PROBLEM_ADVANCED`: 上級者用（15-20語）
- 各レベルに適した語彙、文法、トピックを定義

#### 2. main.py の改善

**レベル別プロンプト自動選択機能**
- シャドーイングモード（MODE_2）でユーザーの英語レベルに応じたプロンプトを自動選択
- ディクテーションモード（MODE_3）でユーザーの英語レベルに応じたプロンプトを自動選択

```python
# 実装箇所: 行137-143, 行236-242
if st.session_state.englv == "初級者":
    problem_template = ct.SYSTEM_TEMPLATE_CREATE_PROBLEM_BEGINNER
elif st.session_state.englv == "中級者":
    problem_template = ct.SYSTEM_TEMPLATE_CREATE_PROBLEM_INTERMEDIATE
else:  # 上級者
    problem_template = ct.SYSTEM_TEMPLATE_CREATE_PROBLEM_ADVANCED
```

#### 3. functions.py の改善

**create_problem_and_play_audio() 関数**
- docstringを「レベル別対応」に更新（行166）

### 改善効果

1. **学習効果の向上**: ユーザーのレベルに最適化された問題が自動生成される
2. **自然な会話**: より洗練されたプロンプトにより、AIの応答が自然で教育的に
3. **段階的な学習**: 初級者から上級者まで、適切な難易度で練習可能