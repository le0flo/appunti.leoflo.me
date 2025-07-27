from pathlib import Path
from typing import Any, List
from bs4 import BeautifulSoup
from bs4.element import Tag
from operator import itemgetter
import argparse, tomllib, markdown, shutil

def readConfig(path: Path) -> dict[str, Any]:
    config = path.joinpath("config.toml")

    if config.exists():
        return tomllib.loads(config.read_text())

    exit(0x01)

def readTemplate(path: Path) -> str:
    index = path.joinpath("index.html")

    if index.exists():
        return index.read_text()

    exit(0x02)

def findAppunti(path: Path, config: dict[str, Any]) -> List:
    appunti_path = path.joinpath(config["content_dir"])
    appunti = []

    for folder in appunti_path.iterdir():
        if folder.is_dir():
            files = []

            for file in folder.iterdir():
                if file.is_file() and file.suffix == ".md":
                    files.append({
                        "name": file.stem[4:],
                        "id": file.stem.lower().replace(". ", "-").replace(" ", "-"),
                        "file": file,
                    })

            
            appunti.append({
                "name": folder.suffix[2:],
                "id": folder.name.lower().replace(". ", "-").replace(" ", "-"),
                "list": sorted(files, key=itemgetter("id")),
            })

    return sorted(appunti, key=itemgetter("id"))

def prepareOutputFolder(path: Path, config: dict[str, Any]) -> Path:
    assets = path.joinpath("assets")
    output = path.joinpath(config["output_dir"])
    output.mkdir(exist_ok=True, parents=True)

    output.joinpath("pages").mkdir(exist_ok=True)
    shutil.copyfile(root_path.joinpath("style.css"), output.joinpath("style.css"))
    shutil.copytree(assets, output.joinpath("assets"), dirs_exist_ok=True)

    return output

def generateSummary(template: BeautifulSoup, tag: Tag, appunti: List):
    for topic in appunti:
        topic_el = template.new_tag("li")
        topic_list = template.new_tag("ol")

        for page in topic["list"]:
            link = template.new_tag("a")
            link.string = page["name"]
            link["href"] = "/pages/" + topic["id"] + "/" + page["id"] + ".html"

            page_el = template.new_tag("li")
            page_el.append(link)
            topic_list.append(page_el)

        topic_el.string = topic["name"]
        topic_el.append(topic_list)
        tag.append(topic_el)

def writeHome(path: Path, config: dict[str, Any], template_str: str, appunti: List):
    template = BeautifulSoup(template_str, features="html.parser")
    content = BeautifulSoup(markdown.markdown(config["home"]["content"]), features="html.parser")

    content_el = template.find(id="content")
    if isinstance(content_el, Tag):
        content_el.append(content)

    summary = template.find(id="summary")
    if isinstance(summary, Tag):
        generateSummary(template, summary, appunti)

    path.joinpath("index.html").write_text(str(template.prettify()))

def writePage(path: Path, template: BeautifulSoup, page: dict[str, Any]):
    page_file = path.joinpath(page["id"] + ".html")
    appunti = BeautifulSoup(markdown.markdown(page["file"].read_text(), extensions=['tables']), features="html.parser")

    content_el = template.find(id="content")
    if isinstance(content_el, Tag):
        content_el.clear()
        content_el.append(appunti)

    page_file.write_text(str(template.prettify()))

def writePages(path: Path, config: dict[str, Any], template_str: str, appunti: List):
    pages = path.joinpath("pages")
    template = BeautifulSoup(template_str, features="html.parser")
    header = BeautifulSoup(config["pages"]["header"], features="html.parser")

    summary = template.find(id="summary")
    if isinstance(summary, Tag):
        generateSummary(template, summary, appunti)

    header_el = template.find("head")
    if isinstance(header_el, Tag):
        header_el.append(header)

    for topic in appunti:
        topic_path = pages.joinpath(topic["id"])
        topic_path.mkdir(exist_ok=True)

        for page in topic["list"]:
            writePage(topic_path, template, page)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="python generate.py", usage="%(prog)s [options] path")
    parser.add_argument("path", type=Path, help="The location of the \"index.html\" and \"assets/appunti\" folder.")
    args = parser.parse_args()

    root_path = Path(args.path)

    config = readConfig(root_path)
    template = readTemplate(root_path)
    appunti_list = findAppunti(root_path, config)

    output_path = prepareOutputFolder(root_path, config)
    writeHome(output_path, config, template, appunti_list)
    writePages(output_path, config, template, appunti_list)
