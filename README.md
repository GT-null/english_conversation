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

## ２０２５年８月２０日 修正内容

### 修正点

#### 1. functions.py - Whisper音声認識の精度向上

**transcribe_audio() 関数の改善（行41-74）**

音声認識の精度を向上させるため、以下の機能を追加：

1. **モード別コンテキストプロンプト**
   - 日常会話モード: "English conversation practice session"
   - シャドーイングモード: "shadowing exercise"
   - ディクテーションモード: "dictation exercise"

2. **temperature パラメータの追加**
   - `temperature=0.2` を設定し、より決定的で一貫性のある認識結果を実現

3. **自動モード判定**
   - `st.session_state` のフラグから現在のモードを自動判定
   - 適切なコンテキストプロンプトを自動選択

```python
# 実装例
context_prompts = {
    "conversation": "This is an English conversation practice session...",
    "shadowing": "This is a shadowing exercise...",
    "dictation": "This is a dictation exercise..."
}

transcript = st.session_state.openai_obj.audio.transcriptions.create(
    model="whisper-1",
    file=audio_input_file,
    language="en",
    prompt=context_prompts[current_mode],  # コンテキスト追加
    temperature=0.2  # 精度向上のため低温度設定
)
```

### 改善効果

1. **音声認識精度の向上**: コンテキストを提供することで、Whisperがより適切な文字起こしを実行
2. **モード特化の最適化**: 各学習モードに応じた認識パラメータで、誤認識を削減
3. **一貫性のある結果**: temperature設定により、同じ音声入力に対して安定した認識結果