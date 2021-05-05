# shirase

shirase は Discord Bot です。定刻に日経電子版NEWSの URL を Discord サーバまで取ってきてくれます。  
shirase は discord.py と jpholiday に依存します。

## 機能

特定のチャンネルに radiko の URL を定時投稿します。  
その際、ロールに対してメンションを飛ばします。

## 使い方

1. 以下のリンクを参考に、`discord.py` と `jpholiday` をインストールします。
   - <https://github.com/Rapptz/discord.py>
   - <https://github.com/Lalcs/jpholiday>

2. `./data_shirase.py` を作成し、以下を返す関数を定義します。:トークン, チャンネルID, ロールID。

```python
def token():
  return "token"
def channel_id():
  return 123456789
def role_id():
  return 987654321
```
