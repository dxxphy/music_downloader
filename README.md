# 🎵 自动音乐下载整理工具

一个基于 Python 和 yt-dlp 的自动化音乐库管理工具，采用简化设计理念。

## ✨ 核心特点

- 🎯 **极简设计**: 直接使用你输入的歌名，不做任何复杂处理
- 🔤 **智能艺人识别**: 支持多词艺人（Taylor Swift、The Beatles等）
- 🔡 **大小写不敏感**: taylor swift、TAYLOR SWIFT 都能正确识别
- 📁 **自动分类**: 按艺人名自动创建文件夹
- 🏷️ **精准标签**: ID3 标签完全按照你的输入设置
- ⚡ **断点续传**: 下载前检查，自动跳过已下载的歌曲
- 🗑️ **自动清理**: 删除下载过程中的垃圾文件

## 🚀 快速开始

```bash
# 安装依赖
pip3 install yt-dlp mutagen

# 配置快捷命令
echo 'alias music-dl="python3 ~/music_downloader/download_music.py"' >> ~/.bashrc
source ~/.bashrc

# 使用
music-dl
```

## 📝 使用方法

```txt
# 标准格式
ytsearch1:艺人 歌曲名

# 多词艺人（自动识别）
ytsearch1:Taylor Swift Love Story
ytsearch1:The Beatles Hey Jude

# 大小写不敏感
ytsearch1:taylor swift shake it off
ytsearch1:THE BEATLES LET IT BE
ytsearch1:a yue 再见  → 自动识别为 张震岳
```

## 🎤 支持的艺人

### 多词艺人
- Taylor Swift、The Beatles、Wang Leehom、David Tao、Stefanie Sun

### 单词艺人
- 周杰伦、陈奕迅、许嵩、方大同、张震岳、蔡健雅、李荣浩、李健、曹格、王杰

## ⚙️ 核心设计理念

### "所见即所得"
```python
用户输入:  "ytsearch1:許嵩 南山憶"
文件名:    "南山憶.mp3"  ✅ 保留用户输入
```

### 智能识别
```python
"taylor swift"  → "Taylor Swift" ✅
"the beatles"   → "The Beatles" ✅
"A Yue"         → "张震岳"      ✅
```

## 🎶 刷新音乐播放器

```bash
rhythmbox
# 按 Ctrl+R 刷新
```

## 📝 更新日志

### v2.0 (当前版本)
- ✅ 简化设计，直接使用用户输入
- ✅ 支持多词艺人识别
- ✅ 大小写不敏感匹配
- ✅ 下载前智能检查

## 📄 许可证

MIT License

---

**享受简单、可控的音乐下载体验！** 🎶
