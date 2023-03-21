"""
[WEB版VOICEVOX API（高速）](https://voicevox.su-shiki.com/su-shikiapis/)
[WEB版VOICEVOX API（低速）](https://voicevox.su-shiki.com/su-shikiapis/ttsquest/)
fast=Trueオプションで高速URLを使用します。
ただし、API消費に限りがありますのでご注意ください。

消費ポイントの計算式　1500+100*(UTF-8文字数)
初期のポイント: 1,000,000ポイント

確認の仕方はcheck_point()
"""
import os
import sys
from io import BytesIO
import json
from enum import IntEnum, auto
import argparse
import requests
# from pydub import AudioSegment
# from pydub.playback import play

apikey = os.getenv("VOICEVOX_API_KEY")
url = "https://api.tts.quest/v1"
fast_url = "https://api.su-shiki.com/v2"
local_url = "http://localhost:50021"


class BidirectionalEnum(IntEnum):
    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value == value:
                return member
        return super()._missing_(value)


class CV(BidirectionalEnum):
    """VOICEVOX Characters Voice IDs

    $ curl -fsSL 'https://api.su-shiki.com/v2/voicevox/speakers?key={API_KEY}' | jq
    [
      {
        "supported_features": {
          "permitted_synthesis_morphing": "SELF_ONLY"
        },
        "name": "四国めたん",
        "speaker_uuid": "7ffcb7ce-00ec-4bdc-82cd-45a8889e43ff",
        "styles": [
          {
            "name": "ノーマル",
            "id": 2
          },
          {
            "name": "あまあま",
            "id": 0
          },
          {
            "name": "ツンツン",
            "id": 6
          },
          {
            "name": "セクシー",
            "id": 4
          },
          {
            "name": "ささやき",
            "id": 36
          },
          {
            "name": "ヒソヒソ",
            "id": 37
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "SELF_ONLY"
        },
        "name": "ずんだもん",
        "speaker_uuid": "388f246b-8c41-4ac1-8e2d-5d79f3ff56d9",
        "styles": [
          {
            "name": "ノーマル",
            "id": 3
          },
          {
            "name": "あまあま",
            "id": 1
          },
          {
            "name": "ツンツン",
            "id": 7
          },
          {
            "name": "セクシー",
            "id": 5
          },
          {
            "name": "ささやき",
            "id": 22
          },
          {
            "name": "ヒソヒソ",
            "id": 38
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "ALL"
        },
        "name": "春日部つむぎ",
        "speaker_uuid": "35b2c544-660e-401e-b503-0e14c635303a",
        "styles": [
          {
            "name": "ノーマル",
            "id": 8
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "ALL"
        },
        "name": "雨晴はう",
        "speaker_uuid": "3474ee95-c274-47f9-aa1a-8322163d96f1",
        "styles": [
          {
            "name": "ノーマル",
            "id": 10
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "ALL"
        },
        "name": "波音リツ",
        "speaker_uuid": "b1a81618-b27b-40d2-b0ea-27a9ad408c4b",
        "styles": [
          {
            "name": "ノーマル",
            "id": 9
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "ALL"
        },
        "name": "玄野武宏",
        "speaker_uuid": "c30dc15a-0992-4f8d-8bb8-ad3b314e6a6f",
        "styles": [
          {
            "name": "ノーマル",
            "id": 11
          },
          {
            "name": "喜び",
            "id": 39
          },
          {
            "name": "ツンギレ",
            "id": 40
          },
          {
            "name": "悲しみ",
            "id": 41
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "ALL"
        },
        "name": "白上虎太郎",
        "speaker_uuid": "e5020595-5c5d-4e87-b849-270a518d0dcf",
        "styles": [
          {
            "name": "ふつう",
            "id": 12
          },
          {
            "name": "わーい",
            "id": 32
          },
          {
            "name": "びくびく",
            "id": 33
          },
          {
            "name": "おこ",
            "id": 34
          },
          {
            "name": "びえーん",
            "id": 35
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "ALL"
        },
        "name": "青山龍星",
        "speaker_uuid": "4f51116a-d9ee-4516-925d-21f183e2afad",
        "styles": [
          {
            "name": "ノーマル",
            "id": 13
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "ALL"
        },
        "name": "冥鳴ひまり",
        "speaker_uuid": "8eaad775-3119-417e-8cf4-2a10bfd592c8",
        "styles": [
          {
            "name": "ノーマル",
            "id": 14
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "SELF_ONLY"
        },
        "name": "九州そら",
        "speaker_uuid": "481fb609-6446-4870-9f46-90c4dd623403",
        "styles": [
          {
            "name": "ノーマル",
            "id": 16
          },
          {
            "name": "あまあま",
            "id": 15
          },
          {
            "name": "ツンツン",
            "id": 18
          },
          {
            "name": "セクシー",
            "id": 17
          },
          {
            "name": "ささやき",
            "id": 19
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "SELF_ONLY"
        },
        "name": "もち子さん",
        "speaker_uuid": "9f3ee141-26ad-437e-97bd-d22298d02ad2",
        "styles": [
          {
            "name": "ノーマル",
            "id": 20
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "ALL"
        },
        "name": "剣崎雌雄",
        "speaker_uuid": "1a17ca16-7ee5-4ea5-b191-2f02ace24d21",
        "styles": [
          {
            "name": "ノーマル",
            "id": 21
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "ALL"
        },
        "name": "WhiteCUL",
        "speaker_uuid": "67d5d8da-acd7-4207-bb10-b5542d3a663b",
        "styles": [
          {
            "name": "ノーマル",
            "id": 23
          },
          {
            "name": "たのしい",
            "id": 24
          },
          {
            "name": "かなしい",
            "id": 25
          },
          {
            "name": "びえーん",
            "id": 26
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "ALL"
        },
        "name": "後鬼",
        "speaker_uuid": "0f56c2f2-644c-49c9-8989-94e11f7129d0",
        "styles": [
          {
            "name": "人間ver.",
            "id": 27
          },
          {
            "name": "ぬいぐるみver.",
            "id": 28
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "ALL"
        },
        "name": "No.7",
        "speaker_uuid": "044830d2-f23b-44d6-ac0d-b5d733caa900",
        "styles": [
          {
            "name": "ノーマル",
            "id": 29
          },
          {
            "name": "アナウンス",
            "id": 30
          },
          {
            "name": "読み聞かせ",
            "id": 31
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "ALL"
        },
        "name": "ちび式じい",
        "speaker_uuid": "468b8e94-9da4-4f7a-8715-a22a48844f9e",
        "styles": [
          {
            "name": "ノーマル",
            "id": 42
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "ALL"
        },
        "name": "櫻歌ミコ",
        "speaker_uuid": "0693554c-338e-4790-8982-b9c6d476dc69",
        "styles": [
          {
            "name": "ノーマル",
            "id": 43
          },
          {
            "name": "第二形態",
            "id": 44
          },
          {
            "name": "ロリ",
            "id": 45
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "ALL"
        },
        "name": "小夜/SAYO",
        "speaker_uuid": "a8cc6d22-aad0-4ab8-bf1e-2f843924164a",
        "styles": [
          {
            "name": "ノーマル",
            "id": 46
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "ALL"
        },
        "name": "ナースロボ＿タイプＴ",
        "speaker_uuid": "882a636f-3bac-431a-966d-c5e6bba9f949",
        "styles": [
          {
            "name": "ノーマル",
            "id": 47
          },
          {
            "name": "楽々",
            "id": 48
          },
          {
            "name": "恐怖",
            "id": 49
          },
          {
            "name": "内緒話",
            "id": 50
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "ALL"
        },
        "name": "†聖騎士 紅桜†",
        "speaker_uuid": "471e39d2-fb11-4c8c-8d89-4b322d2498e0",
        "styles": [
          {
            "name": "ノーマル",
            "id": 51
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "ALL"
        },
        "name": "雀松朱司",
        "speaker_uuid": "0acebdee-a4a5-4e12-a695-e19609728e30",
        "styles": [
          {
            "name": "ノーマル",
            "id": 52
          }
        ],
        "version": "0.14.2"
      },
      {
        "supported_features": {
          "permitted_synthesis_morphing": "ALL"
        },
        "name": "麒ヶ島宗麟",
        "speaker_uuid": "7d1e7ba7-f957-40e5-a3fc-da49f769ab65",
        "styles": [
          {
            "name": "ノーマル",
            "id": 53
          }
        ],
        "version": "0.14.2"
      }
    ]

    Python用に整形
    $ curl -fsSL 'https://api.su-shiki.com/v2/voicevox/speakers?key={API_KEY}' |
        jq '.[] | "\(.name)\(.styles[].name) = \(.styles[].id)"'

    参考: https://docs.python.org/ja/3/library/enum.html#enum.Enum._missing_
    """

    四国めたんあまあま = 0
    四国めたんノーマル = 2
    四国めたんセクシー = 4
    四国めたんツンツン = 6
    四国めたんささやき = 36
    四国めたんヒソヒソ = 37

    ずんだもんノーマル = 3
    ずんだもんあまあま = 1
    ずんだもんツンツン = 7
    ずんだもんセクシー = 5
    ずんだもんささやき = 22
    ずんだもんヒソヒソ = 38

    春日部つむぎノーマル = 8
    雨晴はうノーマル = 10
    波音リツノーマル = 9

    玄野武宏ノーマル = 11
    玄野武宏喜び = 39
    玄野武宏ツンギレ = 40
    玄野武宏悲しみ = 41

    白上虎太郎ふつう = 12
    白上虎太郎わーい = 32
    白上虎太郎びくびく = 33
    白上虎太郎おこ = 34
    白上虎太郎びえーん = 35

    青山龍星ノーマル = 13
    冥鳴ひまりノーマル = 14
    九州そらノーマル = 16
    九州そらあまあま = 15
    九州そらツンツン = 18
    九州そらセクシー = 17
    九州そらささやき = 19

    もち子さんノーマル = 20
    剣崎雌雄ノーマル = 21

    WhiteCULノーマル = 23
    WhiteCULたのしい = 24
    WhiteCULかなしい = 25
    WhiteCULびえーん = 26

    後鬼人間ver = 27
    後鬼ぬいぐるみver = 28

    No7ノーマル = 29
    No7アナウンス = 30
    No7読み聞かせ = 31

    ちび式じいノーマル = 42

    櫻歌ミコノーマル = 43
    櫻歌ミコ第二形態 = 44
    櫻歌ミコロリ = 45

    小夜SAYOノーマル = 46

    ナースロボ＿タイプＴノーマル = 47
    ナースロボ＿タイプＴ楽々 = 48
    ナースロボ＿タイプＴ恐怖 = 49
    ナースロボ＿タイプＴ内緒話 = 50

    聖騎士紅桜ノーマル = 51
    雀松朱司ノーマル = 52
    麒ヶ島宗麟ノーマル = 53

    def __str__(self):
        """
        >>> CV.四国めたんノーマル
        四国めたんノーマル
        """
        return self.name

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_string(cls, value):
        """
        >>> CV(2)
        四国めたんノーマル
        """
        return cls[value].name


class Mode(IntEnum):
    """VOICEVOX mode"""
    SLOW = auto()
    FAST = auto()
    LOCAL = auto()


def check_point() -> dict:
    """ API残数確認
    注意: APIポイント確認だけでも1500ポイント消費する
    """
    return requests.get(f"{fast_url}/api", params={"key": apikey}).text


def audio_query(text: str, speaker: int = 0) -> requests.Response:
    """音声の合成用クエリの作成"""
    headers = {"accept": "application/json"}
    params = {"text": text, "speaker": speaker}
    return requests.post(f"{local_url}/audio_query",
                         headers=headers,
                         params=params)


def synthesis(data, speaker: int = 0) -> requests.Response:
    """音声合成するAPI"""
    headers = {"accept": "audio/wav", "Content-Type": "application/json"}
    params = {"speaker": speaker}
    return requests.post(f"{local_url}/synthesis",
                         headers=headers,
                         data=json.dumps(data),
                         params=params)


def get_voice(text,
              speaker: int = 0,
              mode: Mode = Mode.SLOW) -> requests.Response:
    """VOICEVOX web apiへアクセスしてaudioレスポンスを得る"""
    if mode == 3:
        body = audio_query(text, speaker=speaker).json()
        print(body)
        response = synthesis(body, speaker=speaker)
        return response
    elif mode == 2:
        params = {"key": apikey, "speaker": speaker, "text": text}
        response = requests.get(f"{fast_url}/voicevox/audio", params)
        return response
    # else mode == 1:
    wav_api = requests.get(
        f"{url}/voicevox",  # 末尾のスラッシュがないとエラー
        params={
            "speaker": speaker,
            "text": text
        })
    if wav_api.status_code != 200:
        print("Warnig: Use fast mode")
        raise requests.HTTPError(wav_api.status_code)
    wav_url = wav_api.json()["wavDownloadUrl"]
    response = requests.get(wav_url)
    return response


def build_audio(binary, wav_file=""):
    """audioバイナリを作成
    ファイルパス wav_fileが渡されたらそのファイルにwavを保存する。
    """
    if wav_file:
        with open(wav_file, "wb") as f:
            f.write(binary)
    else:
        wav_file = BytesIO(binary)
    return AudioSegment.from_wav(wav_file)


if __name__ == "__main__":
    argparse.add("--character", "-c", )
    text = sys.argv[-1]
    # リクエスト過多の429エラーが出たときには
    # fastバージョンを使う
    # try:
    #     resp = get_voice(text)
    # except requests.HTTPError:
    #     resp = get_voice(text, mode=Mode.FAST)
    resp = get_voice(text, mode=Mode.LOCAL)
    audio = build_audio(resp.content, wav_file="sample.wav")
    play(audio)
