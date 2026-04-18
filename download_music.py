#!/usr/bin/env python3
"""
本地音乐库自动化全能管家
一键完成：下载 → 清理 → 标签修复 → 文件重命名
"""
import os
import glob
import re
import subprocess
try:
    from mutagen.id3 import ID3, TPE1, TIT2, TALB, ID3NoHeaderError
except ImportError:
    print("❌ 请先在终端执行: pip3 install mutagen")
    exit(1)

# 设定音乐库路径
MUSIC_DIR = os.path.expanduser("~/Music")
SONGS_FILE = os.path.join(MUSIC_DIR, "songs.txt")

def clean_title(raw_title, artist_name=""):
    """
    深度清理文件名，提取纯净的歌曲标题
    支持：中英文歌手、官方MV、歌词版、动态字幕等各种杂乱格式
    """
    clean_t = raw_title

    # 去除各种括号及内容（包括中文括号）
    clean_t = re.sub(r'\(.*?\)|\[.*?\]|【.*?】|（.*?）|「.*?」', '', clean_t)

    # 去除引号和书名号
    for char in ['"', '"', '"', '"', ''', ''', '《', '》']:
        clean_t = clean_t.replace(char, '')

    # 去除常见垃圾后缀（持续更新中）
    remove_words = [
        'Official Music Video', 'official music video', 'official video', 'official audio',
        'MV', 'mv', 'lyric', 'lyrics', '歌词版', '歌詞版', '官方', 'Official', 'official',
        'HD', '4K', '高清', '動態歌詞Lyrics', '动态歌词', '抖音',
        'Sun Yan Zi', 'Sun Yan-Zi', 'Cloudy Day', 'Green Light', 'Encounter', 'I Am Fine',
        'Karaoke', 'VEA', 'Leehom Wang', '陳奕迅', '孫燕姿', '何曼婷',
        '独留我赏烟花飞满天，摇曳后就随风飘远', '太多的伤 难诉衷肠',
        'FEAR AND DREAMS 世界巡迴演唱會 澳門站｜第六場 10 AUG 2025 ENCORE｜',
        '[Official MV]', '(Official', '(official', 'Video Karaoke', '歌詞', 'UltraHD'
    ]
    for word in remove_words:
        # 使用 str.replace 避免正则表达式特殊字符问题
        clean_t = clean_t.replace(word, '')

    # 去除分隔符和多余符号
    clean_t = re.sub(r'\s*[-—–——⧸／｜]\s*', ' ', clean_t)

    # 智能清理掉标题里的歌手名字，保留纯歌名
    if artist_name:
        clean_t = clean_t.replace(artist_name, "")

    # 清理常见英艺文名和别名（支持你的常听歌手）
    artist_aliases = [
        'Khalil Fong', '方大同',
        'Jay Chou', '周杰伦',
        'David Tao', '陶喆',
        'G.E.M.', 'Deng Ziqi', '邓紫棋',
        'Vae', '许嵩',
        'Eason Chan', 'Eason', '陈奕迅', '陳奕迅',
        'Stefanie Sun', 'Yanzi', '孙燕姿', '孫燕姿',
        'Wang Leehom', 'Leehom Wang', '王力宏',
        'Taylor Swift', 'Taylor',
        'Gary Chaw', '曹格',
        'The Beatles', 'Beatles', '披头士'
    ]
    for alias in artist_aliases:
        clean_t = clean_t.replace(alias, "")

    # 去除多余空格和特殊字符
    clean_t = ' '.join(clean_t.split())
    clean_t = clean_t.strip(' .,;:!?\'"()[]{}《》「」')

    return clean_t

def download_songs():
    """阶段一：读取 songs.txt 并调用 yt-dlp 智能分类下载歌曲"""
    if not os.path.exists(SONGS_FILE):
        print(f"⚠️ 找不到文件: {SONGS_FILE}")
        print("请确保 ~/Music/songs.txt 文件存在并填好了歌曲列表，否则将跳过下载阶段。")
        return

    with open(SONGS_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print("🚀 阶段一：开始执行智能分类下载...")
    for line in lines:
        line = line.strip()
        if not line:
            continue  # 跳过空行

        # 解析歌手名字，用于建立分类文件夹
        if line.startswith("ytsearch1:"):
            query_text = line.replace("ytsearch1:", "").strip()

            # 智能解析艺人名：支持多词艺名（如 The Beatles、Wang Leehom 等）
            known_multi_word_artists = [
                "The Beatles", "Taylor Swift", "Wang Leehom", "Leehom Wang", "David Tao",
                "Stefanie Sun", "Jay Chou", "Khalil Fong", "Eason Chan", "Gary Chaw"
            ]

            artist = query_text.split(" ")[0]  # 默认取第一个词

            # 检查是否匹配已知的多词艺名（不区分大小写）
            query_text_lower = query_text.lower()
            for known_artist in known_multi_word_artists:
                if query_text_lower.startswith(known_artist.lower() + " "):
                    artist = known_artist  # 使用标准格式的艺名
                    break

            # 预测清理后的最终文件名
            expected_title = clean_title(query_text, artist)
            expected_file = os.path.join(MUSIC_DIR, artist, f"{expected_title}.mp3")

            # 检查该文件是否已经下载且修复过
            if os.path.exists(expected_file):
                print(f"⏩ 发现已下载: [{artist}] - [{expected_title}]，自动跳过！")
                continue

        else:
            artist = "其他"

        print(f"\n======================================")
        print(f"🎵 正在处理: {line}")
        print(f"📁 目标文件夹: {artist}")
        print(f"======================================\n")

        # 构建 yt-dlp 的输出路径： ~/Music/歌手名/歌曲标题.后缀
        output_template = os.path.join(MUSIC_DIR, artist, "%(title)s.%(ext)s")

        # 组合 yt-dlp 命令
        command = [
            "yt-dlp",
            "-x", # 只提取音频
            "--audio-format", "mp3", # 转为 mp3
            "--add-metadata", # 添加基础元数据（歌手、标题）
            "--embed-thumbnail", # 嵌入封面图
            "--no-write-subs", # 明确禁止下载字幕/歌词文件
            "-o", output_template,
            line
        ]

        # 执行下载命令
        subprocess.run(command)

    print("\n✅ 下载阶段全部完成！\n")

def fix_mp3_tags():
    """阶段二：深度清理所有 MP3 文件（去重、删除垃圾文件、修复标签、重命名）"""
    mp3_files = glob.glob(os.path.join(MUSIC_DIR, "**", "*.mp3"), recursive=True)

    if not mp3_files:
        print("⚠️ 未找到任何 MP3 文件，无需修复标签。")
        return

    print("🚀 阶段二：开始深度清理和修复...\n")
    print("📋 正在删除非 MP3 垃圾文件...")

    # 删除所有非 MP3 文件（webm, webp, m4a等）
    for root, dirs, files in os.walk(MUSIC_DIR):
        # 跳过隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for filename in files:
            if filename.endswith(('.webm', '.webp', '.m4a', '.temp')):
                filepath = os.path.join(root, filename)
                try:
                    os.remove(filepath)
                    print(f"  🗑️ 删除: {filename}")
                except Exception as e:
                    print(f"  ⚠️ 无法删除 {filename}: {e}")

    print("\n📋 开始去重和修复 MP3 文件...")

    # 按艺人文件夹分组处理
    artist_folders = {}
    for mp3_path in mp3_files:
        dir_name = os.path.dirname(mp3_path)
        artist_name = os.path.basename(dir_name)

        if artist_name == "Music" or not artist_name:
            continue

        if artist_name not in artist_folders:
            artist_folders[artist_name] = []
        artist_folders[artist_name].append(mp3_path)

    total_fixed = 0
    total_duplicates = 0

    # 处理每个艺人的文件夹
    for artist_name, files in artist_folders.items():
        print(f"\n🎤 处理 {artist_name} 的歌曲...")

        # 去重：使用标题作为唯一标识
        seen_titles = {}
        files_to_delete = []

        for mp3_path in files:
            filename = os.path.basename(mp3_path)
            raw_title = os.path.splitext(filename)[0]
            pure_title = clean_title(raw_title, artist_name)

            if not pure_title:
                continue

            # 如果这个标题已经存在，比较文件大小，保留较大的
            if pure_title in seen_titles:
                existing_file = seen_titles[pure_title]
                existing_size = os.path.getsize(existing_file)
                current_size = os.path.getsize(mp3_path)

                if current_size > existing_size:
                    files_to_delete.append(existing_file)
                    seen_titles[pure_title] = mp3_path
                    print(f"  🔄 替换低质量版本: {pure_title}")
                else:
                    files_to_delete.append(mp3_path)
                    print(f"  🗑️ 删除重复/低质量: {pure_title}")
                total_duplicates += 1
            else:
                seen_titles[pure_title] = mp3_path

        # 删除重复文件
        for filepath in files_to_delete:
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"  ⚠️ 无法删除重复文件: {e}")

        # 处理剩余的唯一文件
        for mp3_path in seen_titles.values():
            dir_name, filename = os.path.split(mp3_path)
            raw_title = os.path.splitext(filename)[0]
            pure_title = clean_title(raw_title, artist_name)

            try:
                # 读取 MP3 标签
                try:
                    audio = ID3(mp3_path)
                except ID3NoHeaderError:
                    audio = ID3()

                # 清空旧标签
                audio.delall("TPE1")
                audio.delall("TIT2")
                audio.delall("TALB")

                # 设置新标签
                audio.add(TPE1(encoding=3, text=artist_name))
                audio.add(TIT2(encoding=3, text=pure_title))
                audio.add(TALB(encoding=3, text=f"{artist_name} 精选集"))

                # 保存修改
                audio.save(mp3_path)

                # 重命名文件
                new_filename = f"{pure_title}.mp3"
                new_mp3_path = os.path.join(dir_name, new_filename)

                if mp3_path != new_mp3_path:
                    print(f"  ✏️ {os.path.basename(filename)} -> {new_filename}")
                    os.rename(mp3_path, new_mp3_path)

                total_fixed += 1

            except Exception as e:
                print(f"  ❌ 处理 {filename} 时出错: {e}")

    print(f"\n🎉 完美！成功整理了 {total_fixed} 首歌曲，删除了 {total_duplicates} 个重复文件。")

def main():
    print("🌟 本地音乐库自动化全能管家 🌟")
    print("=" * 50)
    print("功能：一键下载 → 清理 → 修复标签 → 重命名")
    print("=" * 50 + "\n")

    download_songs()
    fix_mp3_tags()

    print("\n" + "=" * 50)
    print("🎶 全部任务已完成！")
    print("💡 提示：请打开 Rhythmbox 并按 Ctrl+R 刷新音乐库")
    print("=" * 50)

if __name__ == "__main__":
    main()
