# NPM-Downloader使用说明

NPM-Downloader是一个Python脚本，可以从NCBI获取蛋白质和对应mRNA碱基序列数据，并以FASTA格式保存到本地文件中。

### 安装要求

- Python 3.7或更高版本
- requests库

### 运行方法

- 将NPM-Downloader.py文件保存到您的电脑上
- 打开命令行，切换到文件所在的目录
- 输入以下命令运行脚本：

```bash
python NPM-Downloader.py
```

- 根据提示输入一个基因名称，例如BRCA1，按回车键确认
- 等待脚本搜索NCBI Gene数据库，并下载RefSeqs序列
- 在文件所在的目录中查看生成的FASTA文件，文件名的格式为RefSeq编号_类型.fasta，例如NP_009225.1_protein.fasta

### 注意事项

- 请确保您的网络连接正常，否则可能无法访问NCBI
- 请尊重NCBI的API使用规范，不要发送过多或过频的请求
- 请合理使用NCBI的数据，遵守数据使用政策