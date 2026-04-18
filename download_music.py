#!/usr/bin/env python3
"""
本地音乐库自动化全能管家 - 简化版
特点：直接使用用户输入的歌名，支持多词艺人和大小写不敏感
"""
import os
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
    支持多词艺人（Taylor Swift、The Beatles等）和大小写不敏感
    """
    line = line.strip()
    
    if not line.startswith("ytsearch1:"):
        return None, None
    
    query = line.replace("ytsearch1:", "").strip()
    
    # 多词艺人列表（按长度排序，避免短词被误匹配）
    multi_word_artists = [
        "Stefanie Sun", "Taylor Swift", "Wang Leehom", "Leehom Wang",
        "David Tao", "Jay Chou", "Khalil Fong", "Eason Chan",
        "Gary Chaw", "The Beatles", "G.E.M.", "Deng Ziqi",
        "JJ Lin", "Fish Leong", "Karen Mok", "Joker Xue",
        "Sodagreen", "Mayday", "Tanya Chua", "Li Ronghao"
    ]
    
    # 艺人别名映射（别名 -> 标准中文名）
    artist_mapping = {
        # 英文/其他名 -> 中文名
        "A Yue": "张震岳",
        "Vae": "许嵩",
        "Eason": "陈奕迅",
        "Yanzi": "孙燕姿",
        "Stefanie": "孙燕姿",
        "Leehom": "王力宏",
        "Khalil": "方大同",
        "G.E.M.": "邓紫棋",
        "JJ": "林俊杰",
        "A-Mei": "张惠妹",
        "Hebe": "田馥甄",
        "Joker": "薛之谦",
        "Fish": "梁静茹",
        "Karen": "莫文蔚",
        "Dave": "王杰",
        "Gary": "曹格",
        "Tanya": "蔡健雅",
    }
    
    # 检查是否匹配多词艺人（大小写不敏感）
    query_lower = query.lower()
    for artist in multi_word_artists:
        if query_lower.startswith(artist.lower() + " "):
            # 使用原始查询提取歌名，保持用户输入的大小写
            song_name = query[len(artist):].strip()
            return artist, song_name
    
    # 检查特殊映射
    for alias, standard_name in artist_mapping.items():
        if query_lower.startswith(alias.lower() + " "):
            song_name = query[len(alias):].strip()
            return standard_name, song_name
    
    # 默认：第一个空格分割
    parts = query.split(" ", 1)
    if len(parts) >= 2:
        return parts[0].strip(), parts[1].strip()
    
    return None, None

def is_already_downloaded(artist, song_name):
    """检查歌曲是否已经下载"""
    artist_dir = os.path.join(MUSIC_DIR, artist)
    
    if not os.path.exists(artist_dir):
        return False
    
    expected_file = os.path.join(artist_dir, f"{song_name}.mp3")
    return os.path.exists(expected_file)

def download_songs():
    """阶段一：读取 songs.txt 并下载歌曲"""
    if not os.path.exists(SONGS_FILE):
        print(f"⚠️ 找不到文件: {SONGS_FILE}")
        print("请确保 ~/music_downloader/songs.txt 文件存在并填好了歌曲列表")
        return
    
    with open(SONGS_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print("🚀 阶段一：开始下载歌曲...")
    print("💡 特点：直接使用你输入的歌名，支持多词艺人\n")
    
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
            print(f"⏭️  已存在: [{artist}] - [{song_name}]")
            skipped_count += 1
            continue
        
        print(f"📥 正在下载: [{artist}] - [{song_name}]")
        
        # 创建艺人文件夹
        artist_dir = os.path.join(MUSIC_DIR, artist)
        os.makedirs(artist_dir, exist_ok=True)
        
        # 构建 yt-dlp 输出路径
        output_template = os.path.join(artist_dir, "%(title)s.%(ext)s")
        
        # 构建 yt-dlp 命令
        command = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "--add-metadata",
            "--embed-thumbnail",
            "--no-write-subs",
            "-o", output_template,
            line
        ]
        
        # 执行下载
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode == 0:
                success = rename_and_set_tags(artist_dir, artist, song_name)
                if success:
                    downloaded_count += 1
                    print(f"✅ 完成: [{artist}] - [{song_name}]\n")
                else:
                    print(f"⚠️ 下载成功但文件处理失败\n")
            else:
                print(f"❌ 失败: [{artist}] - [{song_name}]")
                if result.stderr:
                    error_msg = result.stderr[:200].replace('\n', ' ')
                    print(f"   错误: {error_msg}")
                print()
        
        except Exception as e:
            print(f"❌ 执行出错: {e}\n")
    
    print(f"📊 下载统计:")
    print(f"   新下载: {downloaded_count} 首")
    print(f"   已跳过: {skipped_count} 首")
    print(f"   总计: {downloaded_count + skipped_count} 首")

def rename_and_set_tags(artist_dir, artist, song_name):
    """重命名下载的文件并设置正确的标签"""
    try:
        import glob
        mp3_files = glob.glob(os.path.join(artist_dir, "*.mp3"))
        
        if not mp3_files:
            return False
        
        # 取最新的文件
        mp3_files.sort(key=lambda x: os.path.getmtime(x))
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
    print("🚀 阶段二：清理垃圾文件...")
    
    import os
    deleted_count = 0
    
    for root, dirs, files in os.walk(MUSIC_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for filename in files:
            if filename.endswith(('.webm', '.webp', '.m4a', '.temp')):
                filepath = os.path.join(root, filename)
                try:
                    os.remove(filepath)
                    deleted_count += 1
                except Exception:
                    pass
    
    print(f"✅ 清理完成，删除了 {deleted_count} 个垃圾文件\n")

def main():
    print("🎵 本地音乐库自动化管家（简化版 v2.1）")
    print("=" * 60)
    print("✨ 新特性：支持更多艺人别名和映射")
    print("=" * 60 + "\n")
    
    download_songs()
    clean_extra_files()
    
    print("=" * 60)
    print("🎶 全部任务完成！")
    print("💡 提示：请打开 Rhythmbox 并按 Ctrl+R 刷新库")
    print("=" * 60)

if __name__ == "__main__":
    main()
