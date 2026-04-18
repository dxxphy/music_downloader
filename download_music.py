#!/usr/bin/env python3
"""
本地音乐库自动化全能管家
直接使用用户输入的歌名，无需复杂清理
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
SONGS_FILE = os.path.expanduser("~/music_downloader/songs.txt")

def parse_search_query(line):
    """
    解析搜索查询，提取艺人和歌曲名
    格式: ytsearch1:艺人 歌曲名
    """
    line = line.strip()
    
    if not line.startswith("ytsearch1:"):
        return None, None
    
    # 去掉 ytsearch1: 前缀
    query = line.replace("ytsearch1:", "").strip()
    
    # 分割艺人和歌曲名（第一个空格处分割）
    parts = query.split(" ", 1)
    
    if len(parts) < 2:
        return None, None
    
    artist = parts[0].strip()
    song_name = parts[1].strip()
    
    return artist, song_name

def is_already_downloaded(artist, song_name):
    """
    检查歌曲是否已经下载
    """
    artist_dir = os.path.join(MUSIC_DIR, artist)
    
    if not os.path.exists(artist_dir):
        return False
    
    # 直接检查是否存在这个歌名的文件
    expected_file = os.path.join(artist_dir, f"{song_name}.mp3")
    
    if os.path.exists(expected_file):
        return True
    
    return False

def download_songs():
    """阶段一：读取 songs.txt 并下载歌曲"""
    if not os.path.exists(SONGS_FILE):
        print(f"⚠️ 找不到文件: {SONGS_FILE}")
        print("请确保 ~/music_downloader/songs.txt 文件存在并填好了歌曲列表")
        return
    
    with open(SONGS_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print("🚀 阶段一：开始下载歌曲...")
    
    downloaded_count = 0
    skipped_count = 0
    
    for line in lines:
        line = line.strip()
        if not line or not line.startswith("ytsearch1:"):
            continue
        
        artist, song_name = parse_search_query(line)
        
        if not artist or not song_name:
            print(f"⚠️ 跳过格式错误的行: {line}")
            continue
        
        # 检查是否已下载
        if is_already_downloaded(artist, song_name):
            print(f"⏭️  已下载: [{artist}] - [{song_name}]，跳过")
            skipped_count += 1
            continue
        
        print(f"\n📥 正在下载: [{artist}] - [{song_name}]")
        
        # 创建艺人文件夹
        artist_dir = os.path.join(MUSIC_DIR, artist)
        os.makedirs(artist_dir, exist_ok=True)
        
        # 构建 yt-dlp 输出路径
        output_template = os.path.join(artist_dir, "%(title)s.%(ext)s")
        
        # 构建 yt-dlp 命令
        command = [
            "yt-dlp",
            "-x",  # 只提取音频
            "--audio-format", "mp3",  # 转为 mp3
            "--add-metadata",  # 添加基础元数据
            "--embed-thumbnail",  # 嵌入封面图
            "--no-write-subs",  # 不下载字幕
            "-o", output_template,
            line
        ]
        
        # 执行下载
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode == 0:
                # 下载成功，重命名文件并设置标签
                success = rename_and_set_tags(artist_dir, artist, song_name)
                if success:
                    downloaded_count += 1
                    print(f"✅ 下载完成: [{artist}] - [{song_name}]")
                else:
                    print(f"⚠️ 下载成功但文件处理失败")
            else:
                print(f"❌ 下载失败: [{artist}] - [{song_name}]")
                if result.stderr:
                    print(f"   错误: {result.stderr[:200]}")
        
        except Exception as e:
            print(f"❌ 执行出错: {e}")
    
    print(f"\n📊 下载统计:")
    print(f"   新下载: {downloaded_count} 首")
    print(f"   已跳过: {skipped_count} 首")
    print(f"   总计: {downloaded_count + skipped_count} 首")

def rename_and_set_tags(artist_dir, artist, song_name):
    """
    重命名下载的文件并设置正确的标签
    """
    try:
        # 查找下载的 MP3 文件
        mp3_files = [f for f in os.listdir(artist_dir) if f.endswith('.mp3')]
        
        if not mp3_files:
            return False
        
        # 取最新的文件
        mp3_files.sort(key=lambda x: os.path.getmtime(os.path.join(artist_dir, x)))
        latest_file = mp3_files[-1]
        
        old_path = os.path.join(artist_dir, latest_file)
        new_path = os.path.join(artist_dir, f"{song_name}.mp3")
        
        # 重命名文件
        if old_path != new_path:
            os.rename(old_path, new_path)
        
        # 设置 ID3 标签
        try:
            audio = ID3(new_path)
        except ID3NoHeaderError:
            audio = ID3()
        
        # 设置标签
        audio.delall("TPE1")
        audio.delall("TIT2")
        audio.delall("TALB")
        
        audio.add(TPE1(encoding=3, text=artist))
        audio.add(TIT2(encoding=3, text=song_name))
        audio.add(TALB(encoding=3, text=f"{artist} 精选集"))
        
        audio.save(new_path)
        
        return True
    
    except Exception as e:
        print(f"   处理文件时出错: {e}")
        return False

def clean_extra_files():
    """阶段二：删除非 MP3 的垃圾文件"""
    print("\n🚀 阶段二：清理垃圾文件...")
    
    deleted_count = 0
    
    for root, dirs, files in os.walk(MUSIC_DIR):
        # 跳过隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for filename in files:
            if filename.endswith(('.webm', '.webp', '.m4a', '.temp')):
                filepath = os.path.join(root, filename)
                try:
                    os.remove(filepath)
                    deleted_count += 1
                except Exception as e:
                    print(f"   删除失败: {filename}")
    
    print(f"✅ 清理完成，删除了 {deleted_count} 个垃圾文件")

def main():
    print("🎵 本地音乐库自动化管家")
    print("=" * 50)
    print("特点：直接使用你输入的歌名，无需复杂处理")
    print("=" * 50 + "\n")
    
    download_songs()
    clean_extra_files()
    
    print("\n" + "=" * 50)
    print("🎶 全部任务完成！")
    print("💡 提示：请打开 Rhythmbox 并按 Ctrl+R 刷新库")
    print("=" * 50)

if __name__ == "__main__":
    main()
