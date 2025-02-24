import os

import yaml
from mdutils import MdUtils

# root = "./data"
root = "."

mdFile = MdUtils(file_name="README.md", title="Nkululeko database repository")
mdFile.create_md_file()
mdFile.new_header(level=1, title="Data")
mdFile.new_paragraph(
    "This is the default top directory for Nkululeko data import. "
    "Each database should be in its own subfolder "
    "(you can also use `ln -sf` to soft link original database "
    "path to these subfolders) "
    "and contain a README how to import the data to Nkululeko CSV or audformat."
)
mdFile.new_header(level=2, title="Accessibility")
mdFile.new_paragraph(
    "The column `access` in the table below indicates "
    "the database's accessability. The following values are used:"
)
mdFile.new_list(
    [
        "`public`: the database is publicly available in the internet "
        "and can be downloaded directly without any restrictions.",
        "`restricted`: the database is publicly available on the internet "
        "but requires registration or other restrictions to download.",
        "`private`: the database is not publicly available on the internet "
        "and requires the private information of the owner of the dataset.",
    ]
)
mdFile.new_paragraph(
    "To support open science and reproducible research, "
    "we encourage to submit PR and recipes for public dataset for "
    "now on."
)

# read all lines in yaml file
with open(os.path.join(root, "descr.yml")) as stream:
    descr = yaml.safe_load(stream)

table_list = ["Name", "Target", "Description", "Access"]
db_num = 0

for dataset_name in descr.keys():
    # print(dataset_name)
    table_list.extend(
        [
            descr[dataset_name][0]["name"],
            descr[dataset_name][1]["target"],
            descr[dataset_name][2]["descr"],
            descr[dataset_name][3]["access"],
        ]
    )
    db_num += 1

mdFile.new_table(columns=4, rows=db_num + 1, text=table_list, text_align="left")

# add information about number of datasets
mdFile.new_paragraph(f"This recipe contains information about {db_num} datasets.")

mdFile.new_header(level=2, title="Performance")
mdFile.new_line(
    mdFile.new_inline_image(
        text="Nkululeko performance", path="../meta/images/nkululeko_ser_20240719.png"
    )
)
mdFile.new_line()
mdFile.create_md_file()
