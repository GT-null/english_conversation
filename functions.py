import streamlit as st
import os
import time
from pathlib import Path
import wave
import pyaudio
from pydub import AudioSegment
from audiorecorder import audiorecorder
import numpy as np
from scipy.io.wavfile import write
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import SystemMessage
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
import constants as ct

def record_audio(audio_input_file_path):
    """
    音声入力を受け取って音声ファイルを作成
    """

    audio = audiorecorder(
        start_prompt="発話開始",
        pause_prompt="やり直す",
        stop_prompt="発話終了",
        start_style={"color":"white", "background-color":"black"},
        pause_style={"color":"gray", "background-color":"white"},
        stop_style={"color":"white", "background-color":"black"}
    )

    if len(audio) > 0:
        audio.export(audio_input_file_path, format="wav")
    else:
        st.stop()

def transcribe_audio(audio_input_file_path):
    """
    音声入力ファイルから文字起こしテキストを取得
    Args:
        audio_input_file_path: 音声入力ファイルのパス
    """

    with open(audio_input_file_path, 'rb') as audio_input_file:
        transcript = st.session_state.openai_obj.audio.transcriptions.create(
            model="whisper-1",
            file=audio_input_file,
            language="en"
        )
    
    # 音声入力ファイルを削除
    os.remove(audio_input_file_path)

    return transcript

def save_to_wav(llm_response_audio, audio_output_file_path):
    """
    一旦mp3形式で音声ファイル作成後、wav形式に変換
    Args:
        llm_response_audio: LLMからの回答の音声データ
        audio_output_file_path: 出力先のファイルパス
    #GT: 戻り値はなく、音声をmp3からwavに変換して、それを指定のパスに保存する関数
    """

    temp_audio_output_filename = f"{ct.AUDIO_OUTPUT_DIR}/temp_audio_output_{int(time.time())}.mp3"
    with open(temp_audio_output_filename, "wb") as temp_audio_output_file:
        temp_audio_output_file.write(llm_response_audio)
    
    audio_mp3 = AudioSegment.from_file(temp_audio_output_filename, format="mp3")    #GT: pydubの関数"AudioSegment.from_file()"を使って、一時的に保存した mp3 を読み込んで「加工できる音声データ」に変換する処理
    audio_mp3.export(audio_output_file_path, format="wav")  #GT: pydubの関数"AudioSegment.export()"を使って、wav形式で音声ファイルを保存する処理

    # 音声出力用に一時的に作ったmp3ファイルを削除
    os.remove(temp_audio_output_filename)

def play_wav(audio_output_file_path, speed=1.0):
    """
    音声ファイルの読み上げ
    Args:
        audio_output_file_path: 音声ファイルのパス
        speed: 再生速度（1.0が通常速度、0.5で半分の速さ、2.0で倍速など）
    """

    # 音声ファイルの読み込み
    audio = AudioSegment.from_wav(audio_output_file_path)   #GT: pydubの関数"AudioSegment.from_wav()"を使って、指定されたwavファイルを読み込む処理
    
    # 速度を変更
    if speed != 1.0:
        # frame_rateを変更することで速度を調整
        modified_audio = audio._spawn(
            audio.raw_data, 
            overrides={"frame_rate": int(audio.frame_rate * speed)}
        )
        # 元のframe_rateに戻すことで正常再生させる（ピッチを保持したまま速度だけ変更）
        modified_audio = modified_audio.set_frame_rate(audio.frame_rate)

        modified_audio.export(audio_output_file_path, format="wav") #GT: pydubの関数"AudioSegment.export()"を使って、速度変更後の音声データを同じファイルパスに上書き保存する処理

    # PyAudioで再生
    with wave.open(audio_output_file_path, 'rb') as play_target_file:
        '''
        wave.open(file, mode)
            file: WAVファイルのパス（またはファイルオブジェクト）
            mode: 'rb' → read binary（読み込み・バイナリモード）
            戻り値は Wave_read オブジェクト（play_target_file に代入）
            このオブジェクトを通して WAV の中身（サンプリングレート、チャンネル数、サンプル幅など）にアクセスできる
        '''
        p = pyaudio.PyAudio()  
        stream = p.open(
            format=p.get_format_from_width(play_target_file.getsampwidth()),    
            channels=play_target_file.getnchannels(),
            rate=play_target_file.getframerate(),
            output=True
        )
        '''
            サンプル幅（sample width）=音声データ1サンプルを表現するのに使うバイト数, width=2は、2byte=16bit=CD音質=一般的なWAV, 音楽CD
            channels=1はモノラル、2はステレオ
            rate=サンプリングレート（sampling rate）=1秒間に何回音声データをサンプリングするかを表す値, 一般的なCD音質は44.1kHz
        '''
        data = play_target_file.readframes(1024)    
        '''
            1024フレームずつ音声データを読み込む （1024はバッファサイズ、一般的に小さすぎるとノイズ、大きすぎると遅延）
            フレーム (frame) = 1サンプルxチャンネル数。モノラルなら「1024サンプル」. ステレオなら「左1024+右1024サンプル」.
            戻り値は バイナリのbytes列（rawデータ）。
            readframes() が 楽譜の1小節をめくる係
        '''
        while data:
            stream.write(data)  #GT: PyAudioの出力バッファに書き込む（再生される）
            data = play_target_file.readframes(1024) #GT: 次の1024フレームを読み込む
        '''
            while data: で「読み込んだデータが空になるまで」ループ。
            stream.write(data) → これを呼ぶと実際にスピーカーから音が出る。
            ループを繰り返して ファイルの終わりまで再生。
            stream.write() が readframes() が 読み込んだ１小節を楽器に演奏させる係
        '''
        # PyAudioで音声再生が終わった後の「後片付け処理」
        stream.stop_stream()    #GT: いま動いている 再生ストリームを停止 する. データ送信を止めるだけで、まだストリーム自体は存在している状態。
        stream.close()      #GT: ストリームオブジェクトを閉じる。これで音声出力のためのリソース（バッファやデバイス接続）が解放される。
        p.terminate()       #GT: PyAudio全体を終了。サウンドデバイスとの接続を完全に切って、メモリも解放する。これを忘れると「デバイスがロックされたまま次の再生ができない」ことがある。
    # LLMからの回答の音声ファイルを削除
    os.remove(audio_output_file_path)

def create_chain(system_template):
    """
    LLMによる回答生成用のChain作成
    """

    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_template),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    chain = ConversationChain(
        llm=st.session_state.llm,
        memory=st.session_state.memory,
        prompt=prompt
    )

    return chain

def create_problem_and_play_audio():
    """
    問題生成と音声ファイルの再生（レベル別対応）
    Args:
        chain: 問題文生成用のChain
        speed: 再生速度（1.0が通常速度、0.5で半分の速さ、2.0で倍速など）
        openai_obj: OpenAIのオブジェクト
    """

    # 問題文を生成するChainを実行し、問題文を取得
    problem = st.session_state.chain_create_problem.predict(input="")

    # LLMからの回答を音声データに変換
    llm_response_audio = st.session_state.openai_obj.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=problem
    )

    # 音声ファイルの作成
    audio_output_file_path = f"{ct.AUDIO_OUTPUT_DIR}/audio_output_{int(time.time())}.wav"
    save_to_wav(llm_response_audio.content, audio_output_file_path) #GT: LLMからの回答の音声データをwav形式で保存する処理

    # 音声ファイルの読み上げ
    play_wav(audio_output_file_path, st.session_state.speed)    #GT: PyAudioで音声ファイルを再生する

    return problem, llm_response_audio

def create_evaluation():
    """
    ユーザー入力値の評価生成
    """

    llm_response_evaluation = st.session_state.chain_evaluation.predict(input="")       #GT: predictメソッドを実行し、評価結果を生成
                                                                                        #GT: ConversationChain.predict() は「ユーザーの発話を入力し、LLMの返答を返す」メソッド
    return llm_response_evaluation