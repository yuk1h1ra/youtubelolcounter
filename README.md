# youtubelolcounter

YouTubeのLiveアーカイブにてコメントされたものを抽出し、LOL,LMAOなどをカウントする

## Requirements

### poetry

poetryはbundler, composer, npm, cargo, yarnのような、Pythonのパッケージマネージャ。  
Manjaro Linux(Arch系)では、以下のようにインストールする。

```bash
sudo pacman -S python-poetry
```

## Setup

リポジトリをクローンし、pythonパッケージのインストールを行う。

```bash
git clone https://github.com/yuk1h1ra/youtubelolcounter.git
cd youtubelolcounter
poetry install
```

## Execute

### YouTube Live Chat Replay Crawler

以下のコマンドで実行し、YouTubeのLiveアーカイブのURLが求められるので入力する。  
ライブチャットの取得、書き出しには時間がかかり、長時間のアーカイブではそれに比例して長くなる。  
2時間程度のアーカイブで、5分~10分程度かかる。  

```bash
$ poetry run python src/youtube_livechat_replay_crawler.py
Input YouTube URL: <Target URL>
```

取得したチャットは `dest/YYYY-MM-DD_<VIDEOID>/all_livechat.txt` に保存される
