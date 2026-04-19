# 🎵 自动音乐下载整理工具

一个基于 Python 和 yt-dlp 的自动化音乐库管理工具，支持 18 位艺人，采用简化设计理念。

## ✨ 核心特点

- 🤖 **智能艺人识别**: 支持 18 位艺人，包括多词艺人和别名映射
- 🔤 **多词艺人体测**: 自动识别 Taylor Swift、The Beatles、Stefanie Sun 等
- 🔡 **大小写不敏感**: taylor swift、TAYLOR SWIFT 都能正确识别
- 🎭 **别名映射**: A Yue→张震岳、JJ→林俊杰、Vae→许嵩 等
- 📁 **自动分类**: 按艺人名自动创建文件夹
- 🏷️ **精准标签**: ID3 标签完全按照你的输入设置
- ⚡ **断点续传**: 文件存在则跳过，不重复下载
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
# 搜索格式
艺人+歌曲

# URL格式（指定下载源）
艺人+歌曲+YouTube_URL
```

### 多词艺人示例

```txt
# 英文欧美艺人
Taylor Swift+Love Story
The Beatles+Hey Jude

# 华语艺人英文/罗马音名
Stefanie Sun+天黑黑
Wang Leehom+唯一
JJ Lin+江南
G.E.M.+泡沫

# 乐队
Sodagreen+小情歌
Mayday+温柔
```

### 别名映射示例

```txt
# 常用别名自动识别
A Yue+再见        → 自动识别为"张震岳"
Vae+庐州月        → 自动识别为"许嵩"
Eason+十年        → 自动识别为"陈奕迅"
```

### 大小写不敏感示例

```txt
# 以下写法全部正确
taylor swift+shake it off
TAYLOR SWIFT+Love Story
The Beatles+Hey Jude
THE BEATLES+Let It Be
```

### 中文艺人直接输入

```txt
# 直接使用中文歌手名
陶喆+蝴蝶
周杰伦+晴天
陈奕迅+十年
```

### URL 模式示例

```txt
# 从指定 URL 下载
周杰伦+晴天+https://www.youtube.com/watch?v=官方MV
Taylor Swift+Love Story+https://www.youtube.com/watch?v=HD版本
```

## 🎤 支持的艺人（18位）

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

### 智能下载模式
```python
# 统一逻辑：只要存在就跳过
"周杰伦+晴天"  → 已存在则跳过 ✅
"周杰伦+晴天+URL"  → 已存在则跳过 ✅

# 强制重新下载
python3 download_music.py -f
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


## 📝 更新日志

### v2.6 (当前版本)
- ✅ 统一逻辑：文件存在则跳过，不重复下载，音质不好的歌需要手动删除后使用url重新下载

### v2.5
- ✅ 简化格式：艺人+歌曲 或 艺人+歌曲+URL
- ✅ 移除 ytsearch1: 和 yturl: 前缀要求
- ✅ 向后兼容旧格式
- ✅ 更易编辑 txt 文件

### v2.4
- ✅ 新增 URL 下载格式
- ✅ URL 模式自动替换旧版本，无需手动删除
- ✅ 搜索模式跳过已存在文件

### v2.1
- ✅ 扩展支持 18位艺人
- ✅ 新增艺人别名映射系统（16个别名）
- ✅ 完善多词艺人识别
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
