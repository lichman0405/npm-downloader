# 导入所需的模块
import requests
import os

# 定义一个函数，输入基因名称，返回基因对应的蛋白质序列和mRNA序列数据
def get_gene_data(gene_name):
    # 使用NCBI的esearch接口，根据基因名称查询对应的基因ID
    esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    esearch_params = {
        "db": "gene",
        "term": gene_name,
        "retmode": "json"
    }
    esearch_response = requests.get(esearch_url, params=esearch_params)
    esearch_data = esearch_response.json()
    # 如果查询成功，获取第一个基因ID
    if esearch_data.get("header", {}).get("status", "ERROR") == "OK": # 使用get()方法避免KeyError
        gene_id = esearch_data["esearchresult"]["idlist"][0]
        # 使用NCBI的elink接口，根据基因ID查询对应的蛋白质ID和mRNA ID
        elink_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
        elink_params = {
            "dbfrom": "gene",
            "id": gene_id,
            "db": "protein,nuccore",
            "retmode": "json"
        }
        elink_response = requests.get(elink_url, params=elink_params)
        elink_data = elink_response.json()
        # 如果查询成功，获取第一个蛋白质ID和第一个mRNA ID
        if elink_data.get("header", {}).get("status", "ERROR") == "OK": # 使用get()方法避免KeyError
            protein_id = elink_data["linksets"][0]["linksetdbs"][0]["links"][0]
            mrna_id = elink_data["linksets"][0]["linksetdbs"][1]["links"][0]
            # 使用NCBI的efetch接口，根据蛋白质ID和mRNA ID查询对应的序列数据
            efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
            efetch_params = {
                "db": "protein",
                "id": protein_id,
                "rettype": "fasta",
                "retmode": "text"
            }
            efetch_response = requests.get(efetch_url, params=efetch_params)
            protein_seq = efetch_response.text
            efetch_params["db"] = "nuccore"
            efetch_params["id"] = mrna_id
            efetch_response = requests.get(efetch_url, params=efetch_params)
            mrna_seq = efetch_response.text
            # 返回蛋白质序列和mRNA序列数据
            return protein_seq, mrna_seq
        else:
            # 如果查询失败，返回错误信息
            return elink_data.get("header", {}).get("status", "ERROR"), None # 使用get()方法避免KeyError
    else:
        # 如果查询失败，返回错误信息
        return esearch_data.get("header", {}).get("status", "ERROR"), None # 使用get()方法避免KeyError

# 定义一个函数，输入基因名称和序列数据，将其保存在fasta格式的文件中
def save_gene_data(gene_name, gene_data):
    # 检查是否存在output目录，如果不存在则创建
    output_dir = os.path.join(os.getcwd(), "output")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    # 生成fasta文件名，使用基因名称作为文件名
    fasta_file = os.path.join(output_dir, gene_name + ".fasta")
    # 打开文件，写入序列数据
    with open(fasta_file, "w") as f:
        f.write(gene_data)

# 测试代码，输入一个基因名称，例如BRCA1[human]
gene_name = input("请输入基因名称：")
# 调用get_gene_data函数，获取基因对应的蛋白质序列和mRNA序列数据
protein_seq, mrna_seq = get_gene_data(gene_name)
# 如果获取成功，调用save_gene_data函数，将序列数据保存在fasta格式的文件中
if protein_seq and mrna_seq:
    gene_data = protein_seq + mrna_seq
    save_gene_data(gene_name, gene_data)
    print("基因数据已保存在output目录下的" + gene_name + ".fasta文件中。")
# 如果获取失败，打印错误信息
else:
    print("获取基因数据失败，错误信息为：" + protein_seq)
