# shirase

shiraseは、定刻に日経新聞(radiko)をDiscordサーバまで取ってきてくれます。

## 機能

特定のチャンネルにradikoのURLを定時投稿します。  
その際役職にメンションを飛ばします。

## 使い方

discord.pyとjpholidayに依存するため、pipでインストールしてください。  
親ディレクトリにdata_shirase.pyを作成し、トークン、チャンネルID、役職IDを記述します。

```python
def token():
  return ""
def channel_id():
  return 
def role_id():
  return 
```
