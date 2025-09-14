from pathlib import Path
from typing import Any, List
from bs4 import BeautifulSoup
from bs4.element import Tag
from operator import itemgetter
import markdown, shutil

from config import config

def prepare_dist(path: Path) -> Path:
    template = path.joinpath("template")
    output = path.joinpath("dist")
    output.mkdir(exist_ok=True, parents=True)
    output.joinpath("pages").mkdir(exist_ok=True)

    shutil.copyfile(template.joinpath("style.css"), output.joinpath("style.css"))
    shutil.copytree(template.joinpath("assets"), output.joinpath("assets"), dirs_exist_ok=True)

    return output

def template_read(path: Path) -> str:
    index = path.joinpath("template/index.html")

    if index.exists():
        return index.read_text()

    exit(0x02)

def appunti_read(path: Path) -> List:
    appunti_path = path.joinpath("appunti")
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

def appunti_summary(template: BeautifulSoup, tag: Tag, appunti: List):
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

def write_home(path: Path, template_str: str, appunti: List):
    template = BeautifulSoup(template_str, features="html.parser")
    content = BeautifulSoup(markdown.markdown(config["home"]["content"]), features="html.parser")

    content_el = template.find(id="content")
    if isinstance(content_el, Tag):
        content_el.append(content)

    summary = template.find(id="summary")
    if isinstance(summary, Tag):
        appunti_summary(template, summary, appunti)

    path.joinpath("index.html").write_text(str(template.prettify()))

def write_page(path: Path, template: BeautifulSoup, page: dict[str, Any]):
    page_file = path.joinpath(page["id"] + ".html")
    appunti = BeautifulSoup(markdown.markdown(page["file"].read_text(), extensions=['tables']), features="html.parser")

    content_el = template.find(id="content")
    if isinstance(content_el, Tag):
        content_el.clear()
        content_el.append(appunti)

    page_file.write_text(str(template.prettify()))

def write_pages(path: Path, template_str: str, appunti: List):
    pages = path.joinpath("pages")
    template = BeautifulSoup(template_str, features="html.parser")
    header = BeautifulSoup(config["overrides"]["header"], features="html.parser")

    summary = template.find(id="summary")
    if isinstance(summary, Tag):
        appunti_summary(template, summary, appunti)

    header_el = template.find("head")
    if isinstance(header_el, Tag):
        header_el.append(header)

    for topic in appunti:
        topic_path = pages.joinpath(topic["id"])
        topic_path.mkdir(exist_ok=True)

        for page in topic["list"]:
            write_page(topic_path, template, page)

def generate(path: Path):
    output = prepare_dist(path)
    template = template_read(path)
    appunti = appunti_read(path)

    write_home(output, template, appunti)
    write_pages(output, template, appunti)
