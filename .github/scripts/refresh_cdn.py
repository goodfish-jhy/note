#!/usr/bin/env python3
"""
腾讯云CDN缓存刷新脚本
用于在GitHub Actions中自动刷新修改文件的CDN缓存
支持批量处理、错误重试和详细日志
"""

import json
import os
import sys
import time
from typing import List, Dict, Any
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cdn.v20180606 import cdn_client, models


class CDNRefresher:
    """CDN缓存刷新器"""
    
    def __init__(self):
        self.secret_id = os.environ.get('TENCENT_SECRET_ID')
        self.secret_key = os.environ.get('TENCENT_SECRET_KEY')
        self.region = os.environ.get('TENCENT_REGION')
        self.cdn_domain = os.environ.get('CDN_DOMAIN')
        self.changed_files = os.environ.get('CHANGED')
        
        # 腾讯云CDN API限制
        self.max_urls_per_batch = 1000  # 每批最多1000个URL
        self.max_retries = 3  # 最大重试次数
        self.retry_delay = 2  # 重试延迟（秒）
        
        self.client = None
        self._validate_config()
        self._init_client()
    
    def _validate_config(self):
        """验证配置参数"""
        required_vars = {
            'TENCENT_SECRET_ID': self.secret_id,
            'TENCENT_SECRET_KEY': self.secret_key,
            'TENCENT_REGION': self.region,
            'CDN_DOMAIN': self.cdn_domain
        }
        
        missing_vars = [name for name, value in required_vars.items() if not value]
        
        if missing_vars:
            print("错误: 缺少必要的环境变量")
            for name in missing_vars:
                print(f"  {name}: 未设置")
            print("\n请在GitHub Secrets中设置这些变量")
            sys.exit(1)
        
        print("✓ 配置验证通过")
        print(f"  地域: {self.region}")
        print(f"  CDN域名: {self.cdn_domain}")
    
    def _init_client(self):
        """初始化腾讯云客户端"""
        try:
            cred = credential.Credential(self.secret_id, self.secret_key)
            self.client = cdn_client.CdnClient(cred, self.region)
            print("✓ 腾讯云客户端初始化成功")
        except Exception as e:
            print(f"✗ 腾讯云客户端初始化失败: {e}")
            sys.exit(1)
    
    def decode_octal_path(octal_path: Union[str, bytes]) -> str:
        """转义UTF-8格式中文目录"""
        if isinstance(octal_path, bytes):
            s = octal_path.decode('latin-1')
        else:
            s = octal_path
        
        oct_pat = re.compile(r'\\([0-7]{1,3})')

        def replace_octal(match: re.Match) -> str:
            oct_val = match.group(1)
            byte_val = int(oct_val, 8) & 0xFF
            return chr(byte_val)

        s_bytes_like = oct_pat.sub(replace_octal, s)

        raw_bytes = s_bytes_like.encode('latin-1')
        try:
            decoded = raw_bytes.decode('utf-8')
        except UnicodeDecodeError as e:
            raise UnicodeDecodeError(
                "utf-8",
                raw_bytes,
                e.start,
                e.end,
                f"Invalid UTF‑8 sequence while decoding the path: {e.reason}"
            ) from None

        return decoded
    
    def _build_urls(self) -> List[str]:
        """构建需要刷新的URL列表
        通过环境变量 MAP_MD_TO_HTML 控制是否将 .md 转换为 .html（默认转换）。
        当工作流监听 gh-pages 分支时，应设置 MAP_MD_TO_HTML=false。
        """
        if not self.changed_files:
            return []
        
        urls = []
        map_md_to_html = os.environ.get('MAP_MD_TO_HTML', 'true').lower() == 'true'
        for file_path in self.changed_files.strip().split(' '):
            # 去除 file_path 中可能存在的引号
            file_path = file_path.strip('\'"')
            if ('\\' in file_path):
                file_path = self.decode_octal_path(file_path)
            if file_path:
                if file_path.endswith('.md') and map_md_to_html:
                    # Markdown文件转换为HTML URL（仅当启用时）
                    html_file = file_path[:-3] + '.html'
                    url = f'https://{self.cdn_domain}/{html_file}'
                    urls.append(url)
                    print(f"  {file_path} → {url}")
                else:
                    # 其他文件直接使用
                    url = f'https://{self.cdn_domain}/{file_path}'
                    urls.append(url)
                    print(f"  {file_path} → {url}")
        
        return urls
    
    def _split_urls_into_batches(self, urls: List[str]) -> List[List[str]]:
        """将URL列表分割成批次"""
        batches = []
        for i in range(0, len(urls), self.max_urls_per_batch):
            batch = urls[i:i + self.max_urls_per_batch]
            batches.append(batch)
        return batches
    
    def _refresh_batch(self, urls: List[str], batch_num: int, total_batches: int) -> Dict[str, Any]:
        """刷新一批URL"""
        print(f"\n正在处理第 {batch_num}/{total_batches} 批...")
        print(f"本批包含 {len(urls)} 个URL")
        
        for attempt in range(self.max_retries):
            try:
                req = models.PurgeUrlsCacheRequest()
                req.Urls = urls
                req.Area = 'mainland'  # 刷新中国境内加速节点
                
                print(f"  尝试 {attempt + 1}/{self.max_retries}: 调用腾讯云API...")
                resp = self.client.PurgeUrlsCache(req)
                
                print(f"  ✓ 第 {batch_num} 批刷新成功")
                print(f"    任务ID: {resp.TaskId}")
                print(f"    请求ID: {resp.RequestId}")
                
                return {
                    'success': True,
                    'task_id': resp.TaskId,
                    'request_id': resp.RequestId,
                    'urls_count': len(urls)
                }
                
            except TencentCloudSDKException as e:
                print(f"  ✗ 第 {attempt + 1} 次尝试失败: {e}")
                if attempt < self.max_retries - 1:
                    print(f"    等待 {self.retry_delay} 秒后重试...")
                    time.sleep(self.retry_delay)
                else:
                    print(f"  ✗ 第 {batch_num} 批刷新失败，已达到最大重试次数")
                    return {
                        'success': False,
                        'error': str(e),
                        'urls_count': len(urls)
                    }
            
            except Exception as e:
                print(f"  ✗ 第 {attempt + 1} 次尝试发生未知错误: {e}")
                if attempt < self.max_retries - 1:
                    print(f"    等待 {self.retry_delay} 秒后重试...")
                    time.sleep(self.retry_delay)
                else:
                    print(f"  ✗ 第 {batch_num} 批刷新失败，已达到最大重试次数")
                    return {
                        'success': False,
                        'error': str(e),
                        'urls_count': len(urls)
                    }
    
    def refresh_cache(self):
        """主刷新函数"""
        print("开始CDN缓存刷新流程...")
        
        # 构建URL列表
        urls = self._build_urls()
        if not urls:
            print("没有需要刷新的URL，跳过CDN刷新")
            return
        
        print(f"\n总共需要刷新 {len(urls)} 个URL")
        
        # 分割成批次
        batches = self._split_urls_into_batches(urls)
        print(f"将分 {len(batches)} 批处理")
        
        # 处理每个批次
        results = []
        for i, batch in enumerate(batches, 1):
            result = self._refresh_batch(batch, i, len(batches))
            results.append(result)
        
        # 统计结果
        self._print_summary(results)
        
        # 检查是否有失败的批次
        failed_batches = [r for r in results if not r['success']]
        if failed_batches:
            print("\n⚠️  有批次刷新失败，请检查日志")
            sys.exit(1)
        else:
            print("\n🎉 所有批次刷新成功！")
    
    def _print_summary(self, results: List[Dict[str, Any]]):
        """打印刷新结果摘要"""
        print("\n" + "="*50)
        print("刷新结果摘要")
        print("="*50)
        
        total_urls = sum(r['urls_count'] for r in results)
        successful_batches = sum(1 for r in results if r['success'])
        failed_batches = len(results) - successful_batches
        
        print(f"总批次数: {len(results)}")
        print(f"成功批次数: {successful_batches}")
        print(f"失败批次数: {failed_batches}")
        print(f"总URL数: {total_urls}")
        
        if successful_batches > 0:
            print(f"\n成功刷新的任务ID:")
            for i, result in enumerate(results, 1):
                if result['success']:
                    print(f"  批次 {i}: {result['task_id']}")


def main():
    """主函数"""
    try:
        refresher = CDNRefresher()
        refresher.refresh_cache()
    except KeyboardInterrupt:
        print("\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n发生未预期的错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
