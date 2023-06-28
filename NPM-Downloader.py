import requests
import os


def get_gene_data(gene_name):
    """
    The function is used to get protein sequence and mRNA sequence of a gene from NCBI.
    :param gene_name: the name of a gene, for example, BRCA1[human]
    :return: protein sequence and mRNA sequence of the gene
    :example: get_gene_data("BRCA1[human]")
    """
    esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    esearch_params = {
        "db": "gene",
        "term": gene_name,
        "retmode": "json"
    }
    esearch_response = requests.get(esearch_url, params=esearch_params)
    esearch_data = esearch_response.json()
    gene_id = esearch_data["esearchresult"]["idlist"][0]
    # By elink, get protein ID and mRNA ID of the gene
    elink_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
    elink_params = {
        "dbfrom": "gene",
        "id": gene_id,
        "db": "protein,nuccore",
        "retmode": "json"
    }
    elink_response = requests.get(elink_url, params=elink_params)
    elink_data = elink_response.json()
    protein_id = elink_data["linksets"][0]["linksetdbs"][0]["links"][0]
    mrna_id = elink_data["linksets"][0]["linksetdbs"][1]["links"][0]
    # by efetch, get protein sequence and mRNA sequence of the gene
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

    return protein_seq, mrna_seq


def save_gene_data(gene_name, gene_data):
    """
    The function is used to save gene data in fasta format.
    :param gene_name: the name of a gene, for example, BRCA1[human]
    :param gene_data: the data of a gene, including protein sequence and mRNA sequence
    :return: None
    :example: save_gene_data("BRCA1[human]", gene_data)
    """
    output_dir = os.path.join(os.getcwd(), "output")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    fasta_file = os.path.join(output_dir, gene_name + ".fasta")
    with open(fasta_file, "w") as f:
        f.write(gene_data)

print("Welcome to NPM-Downloader! The program is used to download protein sequence and mRNA sequence of a gene from NCBI.")
print('Author: Shibo Li')
print('MiQroEra Digital Technology Co., Ltd.')
gene_name = input("请输入基因名称：")
protein_seq, mrna_seq = get_gene_data(gene_name)
if protein_seq and mrna_seq:
    gene_data = protein_seq + mrna_seq
    save_gene_data(gene_name, gene_data)
    print("基因数据已保存在output目录下的" + gene_name + ".fasta文件中。")
else:
    print("获取基因数据失败，错误信息为：" + protein_seq)
