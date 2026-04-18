# 🎵 自动音乐下载整理工具

一个基于 Python 和 yt-dlp 的自动化音乐库管理工具，支持 30+ 位艺人，采用简化设计理念。

## ✨ 核心特点

- 🎯 **极简设计**: 直接使用你输入的歌名，不做任何复杂处理
- 🤖 **智能艺人识别**: 支持 30+ 位艺人，包括多词艺人和别名映射
- 🔤 **多词艺人体测**: 自动识别 Taylor Swift、The Beatles、Stefanie Sun 等
- 🔡 **大小写不敏感**: taylor swift、TAYLOR SWIFT 都能正确识别
- 🎭 **别名映射**: A Yue→张震岳、JJ→林俊杰、Vae→许嵩 等
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

### 基本格式

```txt
# 标准格式
ytsearch1:艺人 歌曲名
```

### 多词艺人示例

```txt
# 英文欧美艺人
ytsearch1:Taylor Swift Love Story
ytsearch1:The Beatles Hey Jude

# 华语艺人英文/罗马音名
ytsearch1:Stefanie Sun 天黑黑
ytsearch1:Wang Leehom 唯一
ytsearch1:JJ Lin 江南
ytsearch1:G.E.M. 泡沫

# 乐队
ytsearch1:Sodagreen 小情歌
ytsearch1:Mayday 温柔
```

### 别名映射示例

```txt
# 常用别名自动识别
ytsearch1:A Yue 再见        → 自动识别为"张震岳"
ytsearch1:Vae 庐州月        → 自动识别为"许嵩"
ytsearch1:Eason 十年        → 自动识别为"陈奕迅"
ytsearch1:JJ 江南           → 自动识别为"林俊杰"
ytsearch1:Fish 勇气         → 自动识别为"梁静茹"
```

### 大小写不敏感示例

```txt
# 以下写法全部正确
ytsearch1:taylor swift shake it off
ytsearch1:TAYLOR SWIFT Love Story
ytsearch1:The Beatles Hey Jude
ytsearch1:THE BEATLES Let It Be
ytsearch1:stefanie sun 天黑黑
ytsearch1:STEFANIE SUN 开始懂了
```

### 中文艺人直接输入

```txt
# 直接使用中文歌手名
ytsearch1:周杰伦 晴天
ytsearch1:陈奕迅 十年
ytsearch1:陶喆 蝴蝶
ytsearch1:许嵩 素颜
ytsearch1:方大同 Love Song
ytsearch1:张震岳 再见
ytsearch1:林俊杰 江南
ytsearch1:邓紫棋 泡沫
```

## 🎤 支持的艺人（30+ 位）

### ✨ 新增艺人别名支持

**智能识别功能**：
- 🔤 **多词艺人识别**：自动识别 Taylor Swift、The Beatles、Stefanie Sun 等
- 🔡 **大小写不敏感**：taylor swift、TAYLOR SWIFT 都能正确识别
- 🎭 **别名映射系统**：A Yue→张震岳、JJ→林俊杰、Vae→许嵩 等 16 个别名
- 🌏 **中英文混合**：支持华语歌手英文/罗马音名（JJ Lin、Stefanie Sun、David Tao）

### 📋 完整艺人列表

**欧美艺人**
- 🇺🇸 Taylor Swift
- 🇬🇧 The Beatles

**华语艺人英文/罗马音名**
- 🇨🇳 Stefanie Sun (孙燕姿)
- 🇨🇳 Wang Leehom / Leehom Wang (王力宏)
- 🇨🇳 David Tao (陶喆)
- 🇨🇳 Jay Chou (周杰伦)
- 🇨🇳 Khalil Fong (方大同)
- 🇨🇳 Eason Chan (陈奕迅)
- 🇨🇳 Gary Chaw (曹格)
- 🇨🇳 G.E.M. / Deng Ziqi (邓紫棋)
- 🇨🇳 JJ Lin (林俊杰)
- 🇨🇳 Fish Leong (梁静茹)
- 🇨🇳 Karen Mok (莫文蔚)
- 🇨🇳 Joker Xue (薛之谦)
- 🇨🇳 Tanya Chua (蔡健雅)
- 🇨🇳 Li Ronghao (李荣浩)

**乐队**
- 🇹🇼 Sodagreen (苏打绿)
- 🇹🇼 Mayday (五月天)


## ⚙️ 核心设计理念

### "所见即所得"
```python
用户输入:  "ytsearch1:許嵩 南山憶"
文件名:    "南山憶.mp3"  ✅ 保留用户输入
```

### 智能识别

```python
# 多词艺人识别（大小写不敏感）
"taylor swift"     → "Taylor Swift" ✅
"TAYLOR SWIFT"     → "Taylor Swift" ✅
"stefanie sun"     → "Stefanie Sun" ✅
"THE BEATLES"      → "The Beatles" ✅

# 别名映射
"A Yue"            → "张震岳"      ✅
"Vae"              → "许嵩"        ✅
"JJ"               → "林俊杰"      ✅
"Eason"            → "陈奕迅"      ✅
"Fish"             → "梁静茹"      ✅

# 罗马音/英文名识别
"Stefanie Sun"     → "孙燕姿"      ✅（文件夹名）
"Wang Leehom"      → "王力宏"      ✅（文件夹名）
"JJ Lin"           → "林俊杰"      ✅（文件夹名）
```

## 🎶 刷新音乐播放器

```bash
rhythmbox
# 按 Ctrl+R 刷新
```

## 📝 更新日志

### v2.1 (当前版本)
- ✅ 扩展支持 30+ 位艺人
- ✅ 新增艺人别名映射系统（16个别名）
- ✅ 完善多词艺人识别（20位艺人）
- ✅ 修复下载统计显示bug
- ✅ 增强华语歌手英文/罗马音名支持
- ✅ 新增乐队支持（苏打绿、五月天）

### v2.0
- ✅ 简化设计，直接使用用户输入
- ✅ 支持多词艺人识别
- ✅ 大小写不敏感匹配
- ✅ 下载前智能检查

### v1.0 (已废弃)
- 旧版本包含复杂的文件名清理逻辑
- 代码复杂，容易出现清理错误

## 📄 许可证

MIT License

---

**享受简单、可控的音乐下载体验！** 🎶
