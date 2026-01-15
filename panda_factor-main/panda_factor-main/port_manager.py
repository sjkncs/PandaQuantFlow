#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
端口管理工具 - 检查和清理端口占用
"""

import subprocess
import sys
import re

def check_port(port):
    """检查端口是否被占用"""
    try:
        # Windows命令
        result = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True,
            text=True,
            encoding='gbk'
        )
        
        # 查找端口占用
        lines = result.stdout.split('\n')
        occupied = []
        
        for line in lines:
            if f':{port}' in line and 'LISTENING' in line:
                # 提取PID
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    occupied.append({
                        'line': line.strip(),
                        'pid': pid
                    })
        
        return occupied
        
    except Exception as e:
        print(f"❌ 检查端口失败: {e}")
        return []

def get_process_name(pid):
    """获取进程名称"""
    try:
        result = subprocess.run(
            ['tasklist', '/FI', f'PID eq {pid}', '/FO', 'CSV', '/NH'],
            capture_output=True,
            text=True,
            encoding='gbk'
        )
        
        if result.stdout:
            # 解析CSV输出
            parts = result.stdout.strip().split(',')
            if len(parts) > 0:
                return parts[0].strip('"')
        
        return "未知进程"
        
    except Exception as e:
        return f"错误: {e}"

def kill_process(pid):
    """结束进程"""
    try:
        result = subprocess.run(
            ['taskkill', '/PID', pid, '/F'],
            capture_output=True,
            text=True,
            encoding='gbk'
        )
        
        if result.returncode == 0:
            return True, "成功"
        else:
            return False, result.stderr
            
    except Exception as e:
        return False, str(e)

def main():
    """主函数"""
    print("=" * 70)
    print("🔧 Panda 端口管理工具")
    print("=" * 70)
    print()
    
    # 检查常用端口
    ports_to_check = [8111, 27017, 8000, 8080]
    
    print("📊 检查端口占用情况...")
    print()
    
    all_clear = True
    occupied_info = {}
    
    for port in ports_to_check:
        occupied = check_port(port)
        
        if occupied:
            all_clear = False
            occupied_info[port] = occupied
            
            print(f"⚠️  端口 {port} 被占用:")
            for info in occupied:
                pid = info['pid']
                process_name = get_process_name(pid)
                print(f"   PID: {pid}")
                print(f"   进程: {process_name}")
                print(f"   详情: {info['line']}")
                print()
        else:
            print(f"✅ 端口 {port} 可用")
    
    print()
    print("=" * 70)
    
    if all_clear:
        print("🎉 所有端口都可用！")
        print()
        print("您可以直接运行:")
        print("  py start_server_fixed.py")
        print()
    else:
        print("⚠️  发现端口占用")
        print()
        print("选项:")
        print("  1. 自动清理所有占用的端口")
        print("  2. 手动选择要清理的端口")
        print("  3. 退出（不做任何操作）")
        print()
        
        choice = input("请选择 (1/2/3): ").strip()
        
        if choice == '1':
            print()
            print("🔄 正在清理所有占用的端口...")
            print()
            
            for port, infos in occupied_info.items():
                print(f"清理端口 {port}...")
                for info in infos:
                    pid = info['pid']
                    process_name = get_process_name(pid)
                    
                    success, message = kill_process(pid)
                    if success:
                        print(f"  ✅ 已结束进程 {process_name} (PID: {pid})")
                    else:
                        print(f"  ❌ 无法结束进程 {process_name} (PID: {pid}): {message}")
            
            print()
            print("✅ 清理完成！")
            print()
            print("现在可以运行:")
            print("  py start_server_fixed.py")
            
        elif choice == '2':
            print()
            print("📋 可清理的端口:")
            port_list = list(occupied_info.keys())
            
            for i, port in enumerate(port_list, 1):
                print(f"  {i}. 端口 {port}")
            
            print()
            selections = input("请输入要清理的端口编号（用逗号分隔，如: 1,2）: ").strip()
            
            try:
                indices = [int(x.strip()) - 1 for x in selections.split(',')]
                
                print()
                for idx in indices:
                    if 0 <= idx < len(port_list):
                        port = port_list[idx]
                        print(f"清理端口 {port}...")
                        
                        for info in occupied_info[port]:
                            pid = info['pid']
                            process_name = get_process_name(pid)
                            
                            success, message = kill_process(pid)
                            if success:
                                print(f"  ✅ 已结束进程 {process_name} (PID: {pid})")
                            else:
                                print(f"  ❌ 无法结束进程 {process_name} (PID: {pid}): {message}")
                
                print()
                print("✅ 清理完成！")
                
            except Exception as e:
                print(f"❌ 输入错误: {e}")
        
        else:
            print()
            print("👋 已退出，未做任何更改")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 已取消")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
