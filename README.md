# 🎵 自动音乐下载整理工具

一个基于 Python 和 yt-dlp 的自动化音乐库管理工具，可以一键下载、清理、去重和整理你的音乐收藏。

## ✨ 功能特点

- 🎯 **智能下载**: 从 YouTube 自动搜索并下载 MP3 格式音乐
- 🏷️ **自动标签**: 修复 ID3 标签（艺人、标题、专辑）
- 📁 **智能分类**: 按艺人名自动创建文件夹分类存储
- 🧹 **深度清理**: 自动去除文件名中的多余信息（官方版、MV、歌词等）
- 🔍 **智能去重**: 自动识别并删除重复和低质量版本
- 🌏 **多语言支持**: 智能识别中英文艺人名（支持大小写不敏感）
- ⚡ **断点续传**: 自动跳过已下载的歌曲

## 📋 系统要求

- Linux/macOS
- Python 3.6+
- 网络连接

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装 yt-dlp（核心下载工具）
pip3 install yt-dlp

# 安装 Python 依赖
pip3 install mutagen

# 验证安装
yt-dlp --version
python3 -c "import mutagen; print('mutagen installed')"
```

### 2. 下载项目

```bash
# 克隆或下载项目到本地
git clone <https://github.com/dxxphy/music_downloader.git>
cd music-manager

# 或者直接下载 download_music.py
wget <https://github.com/dxxphy/music_downloader.git>/download_music.py
```

### 3. 配置快捷命令（可选）

```bash
# 添加到 ~/.bashrc
echo 'alias music-dl="python3 ~/<your folder>/download_music.py"' >> ~/.bashrc
source ~/.bashrc

# 现在可以直接使用
music-dl
```

## 📝 使用方法

### 基本用法

```bash
# 1. 编辑歌曲列表
nano ~/<your folder>/songs.txt

# 2. 添加歌曲（每行一首）
ytsearch1:周杰伦 晴天
ytsearch1:Taylor Swift Love Story
ytsearch1:The Beatles Hey Jude

# 3. 运行下载脚本
python3 ~/<your folder>/download_music.py

# 或者使用快捷命令
music-dl
```

### 歌曲列表格式

```txt
# 搜索格式（推荐）
ytsearch1:艺人 歌曲名

# 直接使用 YouTube URL
https://www.youtube.com/watch?v=xxxxxxxxx
```

### 支持的搜索格式

```txt
# 中文歌曲
ytsearch1:周杰伦 晴天
ytsearch1:陈奕迅 十年

# 英文歌曲
ytsearch1:Taylor Swift Love Story
ytsearch1:The Beatles Hey Jude

# 多词艺人名（自动识别）
ytsearch1:The Beatles Yesterday
ytsearch1:Wang Leehom 唯一

# 大小写不敏感
ytsearch1:the beatles hey jude
ytsearch1:TAYLOR SWIFT love story
```

## 🎤 支持的艺人

脚本已优化支持以下艺人的名称清理：

### 华语歌手
- 🇨🇳 **周杰伦** / Jay Chou
- 🇨🇳 **陈奕迅** / Eason Chan
- 🇨🇳 **孙燕姿** / Stefanie Sun / Sun Yan Zi
- 🇨🇳 **王力宏** / Wang Leehom
- 🇨🇳 **陶喆** / David Tao
- 🇨🇳 **方大同** / Khalil Fong
- 🇨🇳 **许嵩** / Vae
- 🇨🇳 **邓紫棋** / G.E.M. / Deng Ziqi
- 🇨🇳 **曹格** / Gary Chaw
- 🇨🇳 **蔡健雅**
- 🇨🇳 **张震岳**

### 欧美歌手
- 🇺🇸 **Taylor Swift**
- 🇬🇧 **The Beatles** / Beatles

> 💡 **提示**: 如果你常用的艺人不在列表中，可以在脚本中添加他们的英文名别名。

## 📂 文件结构

```
~/music_downloader/
├── download_music.py    # 主脚本
├── songs.txt            # 歌曲列表
├── README.md            # 说明文档
│
├── artist_1/              # 按艺人分类的文件夹
│   ├── song1.mp3
│   ├── song2.mp3
│   └── ...
│
├── artist_2/
    ├── song3.mp3
    ├── song4.mp3
    └── ...

```

## ⚙️ 工作流程

```
📝 编辑 songs.txt
    ↓
🔍 智能搜索 YouTube
    ↓
📥 下载 MP3 文件
    ↓
🗑️ 删除垃圾文件（webm, webp等）
    ↓
🔀 智能去重（保留高质量版本）
    ↓
🏷️ 修复 ID3 标签
    ↓
✏️ 清理文件名
    ↓
✅ 完成！
```

## 🎯 核心功能说明

### 1. 智能艺人名识别

```python
# 自动识别多词艺人名
"The Beatles Hey Jude"  → 艺人: "The Beatles"
"Wang Leehom 唯一"        → 艺人: "Wang Leehom"
"Taylor Swift Love Story" → 艺人: "Taylor Swift"

# 大小写不敏感
"the beatles hey jude"   → 艺人: "The Beatles"
"TAYLOR SWIFT love story" → 艺人: "Taylor Swift"
```

### 2. 文件名自动清理

```python
# 原始文件名
"周杰伦 - 晴天 Official Music Video.mp3"

# 清理后
"晴天.mp3"
```

### 3. 智能去重

```python
# 自动识别重复歌曲
# 保留文件大小更大的版本（通常音质更好）
# 删除重复和低质量版本
```

### 4. ID3 标签修复

```python
# 自动设置正确的标签
艺人: "周杰伦"
标题: "晴天"
专辑: "周杰伦 精选集"
```

## 🛠️ 配置和自定义

### 添加新的艺人别名

编辑 `download_music.py`，找到以下部分：

```python
# 添加艺人英文名
artist_aliases = [
    'Your Artist Name', '艺人名',
    # ...
]

# 添加多词艺人名
known_multi_word_artists = [
    "Your Artist Name",
    # ...
]
```

### 修改音乐库路径

```python
# 在 download_music.py 中修改
MUSIC_DIR = os.path.expanduser("~/Music")
```

## 🎵 使用示例

### 下载单个艺人的歌曲

```txt
ytsearch1:周杰伦 晴天
ytsearch1:周杰伦 七里香
ytsearch1:周杰伦 稻香
```

### 批量下载多首歌曲

```txt
ytsearch1:周杰伦 晴天
ytsearch1:陈奕迅 十年
ytsearch1:Taylor Swift Love Story
ytsearch1:The Beatles Hey Jude
ytsearch1:孙燕姿 天黑黑
```

### 使用直接 URL

```txt
https://www.youtube.com/watch?v=xxxxxxxxx
https://www.youtube.com/watch?v=yyyyyyyyyyy
```

## 🎶 刷新音乐播放器

下载完成后，在音乐播放器中刷新库：

### Rhythmbox
```bash
# 启动 Rhythmbox
rhythmbox

# 按 Ctrl+R 刷新音乐库
```

### 其他播放器
- **Clementine**: 工具 → 导入音乐库
- **Audacious**: 文件 → 添加音乐
- ** VLC**: 媒体 → 打开文件夹

## ⚠️ 故障排除

### 1. yt-dlp 未安装

```bash
错误: yt-dlp: command not found
解决: pip3 install yt-dlp
```

### 2. mutagen 未安装

```bash
错误: No module named 'mutagen'
解决: pip3 install mutagen
```

### 3. 下载失败

```bash
# 检查网络连接
ping youtube.com

# 更新 yt-dlp
pip3 install --upgrade yt-dlp

# 尝试使用直接 URL 而非搜索
```

### 4. 标签显示"未知艺人"

```bash
# 在 Rhythmbox 中按 Ctrl+R 刷新
# 或重启音乐播放器
```

### 5. 文件名清理不干净

```bash
# 在脚本中添加特定艺人的英文名
# 参见"配置和自定义"部分
```

## 📊 性能和限制

### 优势
- ✅ 自动化程度高，无需手动整理
- ✅ 智能识别，减少重复下载
- ✅ 批量处理，效率高
- ✅ 支持多种艺人名格式

### 限制
- ⚠️ 依赖 YouTube 可用性
- ⚠️ 音质受 YouTube 源文件限制（通常 128-192kbps）
- ⚠️ 搜索准确性取决于 YouTube 算法

## 🔧 高级用法

### 定时任务

```bash
# 添加到 crontab
crontab -e

# 每天凌晨 3 点检查新歌曲
0 3 * * * python3 ~/music_downloader/download_music.py
```

### 日志记录

```bash
# 保存下载日志
python3 ~/music_downloader/download_music.py > ~/music_downloader/download.log 2>&1
```

### 与其他工具集成

```bash
# 下载后自动备份
rsync -av ~/music_downloader/ /backup/music/

# 下载后自动同步到云存储
rclone sync ~/music_downloader/ remote:music/
```

## 📝 更新日志

### v1.0.0 (当前版本)
- ✅ 基础下载和清理功能
- ✅ 智能艺人名识别
- ✅ 多词艺人名支持
- ✅ 大小写不敏感匹配
- ✅ 自动去重和标签修复

## 🤝 贡献

欢迎提交问题报告和改进建议！

## 📄 许可证

MIT License

## 🙏 致谢

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - 强大的视频下载工具
- [Mutagen](https://github.com/quodlibet/mutagen) - 音频元数据处理库

## 📮 联系方式

- 项目地址: [GitHub](<https://github.com/dxxphy/music_downloader.git>)
- 问题反馈: [Issues](<https://github.com/dxxphy/music_downloader.git>/issues)

---

**享受你的自动化音乐下载体验！** 🎶
