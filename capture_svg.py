#!/usr/bin/env python3
"""
SVG to GIF Converter
Captures SVG animation and converts it to GIF
"""

import time
import os
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

def capture_svg_animation():
    """Capture SVG animation and save as GIF"""
    
    # SVG URL
    svg_url = "https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=26&pause=1500&color=6366F1&center=true&vCenter=true&width=600&lines=Hey%2C+I'm+Biaoo+%F0%9F%91%8B; Passionate+about+AI+%26+Sustainability"
    
    print("正在捕获SVG动画...")
    
    # 创建assets目录
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    # 创建打字机效果GIF
    print("\n创建打字机效果GIF...")
    create_typing_gif()


def create_typing_gif():
    """创建真正的打字机效果GIF"""
    
    # 创建assets目录
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    # 文本内容
    text_lines = [
        "Hey, I'm Biaoo",
        "Passionate about AI & Sustainability"
    ]
    
    # 创建图片参数
    width, height = 1000, 260  # 增加分辨率
    background_color = (0, 0, 0, 0)  # 透明背景
    text_color = '#6366F1'  # Indigo color
    
    # 尝试加载字体
    font_size = 36  # 增加字体大小
    font = None
    
    # 尝试多个字体路径，优先使用Fira Code
    font_paths = [
        "/System/Library/Fonts/Monaco.ttf",  # macOS等宽字体
        "/System/Library/Fonts/SF-Mono-Regular.otf",  # macOS系统等宽字体
        "/System/Library/Fonts/SF-Mono-Bold.otf",
        "/System/Library/Fonts/Menlo.ttc",  # macOS等宽字体
        "/Library/Fonts/FiraCode-Regular.ttf",  # 如果安装了Fira Code
        "/Library/Fonts/FiraCode-Bold.ttf",
        "/System/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SF-Pro-Display-Regular.otf",
        "/System/Library/Fonts/NewYork.ttf",
        "/Library/Fonts/Arial.ttf",
        "/Library/Fonts/Helvetica.ttc"
    ]
    
    for font_path in font_paths:
        try:
            font = ImageFont.truetype(font_path, font_size)
            print(f"✅ 使用字体: {font_path}")
            break
        except:
            continue
    
    if font is None:
        print("⚠️ 无法加载系统字体，使用默认字体")
        font = ImageFont.load_default()
    
    images = []
    
    # 创建基础空白帧（只创建一次）
    base_blank_frame = Image.new('RGBA', (width, height), color=background_color)
    
    # 第一行文字 - 打字机效果
    current_text = ""
    for char in text_lines[0]:
        current_text += char
        # 基于空白帧创建新图片，确保一致性
        img = base_blank_frame.copy()
        draw = ImageDraw.Draw(img)
        
        # 计算文字位置使其居中
        bbox = draw.textbbox((0, 0), current_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        draw.text((x, y), current_text, fill=text_color, font=font)
        images.append(img)
    
    # 添加第一行完成后的停顿帧
    for _ in range(8):  # 增加停顿帧数，让第一行更容易看到
        # 创建完整的最后一帧副本
        last_frame = images[-1].copy()
        images.append(last_frame)
    
    # 添加空白停顿帧（使用相同的空白帧对象）
    for _ in range(3):  # 减少空白停顿帧
        images.append(base_blank_frame.copy())
    
    # 第二行文字 - 打字机效果
    current_text = ""
    for char in text_lines[1]:
        current_text += char
        # 基于空白帧创建新图片，确保一致性
        img = base_blank_frame.copy()
        draw = ImageDraw.Draw(img)
        
        # 计算文字位置使其居中
        bbox = draw.textbbox((0, 0), current_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        draw.text((x, y), current_text, fill=text_color, font=font)
        images.append(img)
    
    # 添加最终停顿帧
    for _ in range(30):  # 增加最终停顿帧，让第二行更容易看到
        # 创建完整的最后一帧副本
        last_frame = images[-1].copy()
        images.append(last_frame)
    
    # 保存GIF
    if images:
        print(f"准备保存 {len(images)} 帧到GIF...")
        
        # 确保所有图片都是RGBA模式
        for i, img in enumerate(images):
            if img.mode != 'RGBA':
                images[i] = img.convert('RGBA')
        
        # 使用更直接的方法保存GIF
        try:
            # 创建新的GIF
            first_frame = images[0]
            remaining_frames = images[1:]
            
            first_frame.save(
                'assets/typing.gif',
                format='GIF',
                save_all=True,
                append_images=remaining_frames,
                duration=150,
                loop=0,
                optimize=True,  # 启用优化以减少文件大小
                disposal=2,  # 保持disposal=2，清除上一帧
                background=(0, 0, 0, 0)  # 设置透明背景
            )
            print("✅ 打字机效果GIF已保存到 assets/typing.gif")
        except Exception as e:
            print(f"保存失败: {e}")
            # 尝试最简单的保存方法
            try:
                images[0].save('assets/typing.gif', save_all=True, append_images=images[1:], duration=150, loop=0)
                print("✅ 使用简单方法保存GIF成功")
            except Exception as e2:
                print(f"简单方法也失败: {e2}")
        
        print(f"📊 总共创建了 {len(images)} 帧")
    else:
        print("❌ 无法创建GIF")

if __name__ == "__main__":
    print("🚀 开始创建打字机效果GIF...")
    print("=" * 50)
    
    capture_svg_animation()

    
    print("\n" + "=" * 50)
    print("✅ 转换完成！")
    print("📁 文件保存在 assets/ 目录中")
    print("📝 在README.md中使用: ![Typing Animation](./assets/typing.gif)") 