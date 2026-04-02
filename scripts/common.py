import json
import os

MEMBERS = ["심은석", "이재성", "함범준"]

WEEKLY_SCOPE = {
    "1": "1장 전체",
    "2": "~ 2장. 진단 제지기",
    "3": "~ 2장. 디폴트 매개변수",
    "4": "~ 3장. 변경사항 모델링",
    "5": "~ 3장. Composition 생성하기",
    "6": "~ 4장. Compose UI 관점의 Subcomposition",
    "7": "~ 4장. 측정 정책",
}


def parse_issue_body(body):
    sections = {}
    current_section = None

    for line in body.split("\n"):
        line = line.strip()
        if line.startswith("### "):
            current_section = line[4:].strip()
            sections[current_section] = []
        elif current_section is not None and line:
            sections[current_section].append(line)

    return {k: "\n".join(v).strip() for k, v in sections.items()}


def load_links():
    try:
        with open("data/links.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {member: {} for member in MEMBERS}


def save_links(links):
    os.makedirs("data", exist_ok=True)
    with open("data/links.json", "w", encoding="utf-8") as f:
        json.dump(links, f, ensure_ascii=False, indent=2)


def generate_readme(links):
    lines = []
    lines.append("# 📖 Compose Internals Study")
    lines.append("")
    lines.append("> Jetpack Compose의 내부 동작 원리를 다루는 [Compose Internals](https://jorgecastillo.dev/book/) 책을 함께 읽고 정리하는 스터디입니다.")
    lines.append("")
    lines.append("## 스터디원")
    lines.append("")
    lines.append("| 심은석 | 이재성 | 함범준 |")
    lines.append("| :----: | :----: | :----: |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📎 주차별 노션 링크")
    lines.append("")
    lines.append("> 링크를 추가하려면 [Issue를 등록](../../issues/new/choose)해주세요.")
    lines.append("")
    lines.append("<!-- NOTION_LINKS_START -->")

    for member in MEMBERS:
        lines.append(f"### {member}")
        lines.append("")
        member_links = links.get(member, {})

        if member_links:
            lines.append("| 주차 | 범위 | 노션 링크 |")
            lines.append("| :--: | ---- | --------- |")
            sorted_weeks = sorted(member_links.keys(), key=lambda x: int(x))
            for week in sorted_weeks:
                url = member_links[week]
                scope = WEEKLY_SCOPE.get(week, "")
                lines.append(f"| {week}주차 | {scope} | [노션 링크]({url}) |")
        else:
            lines.append("_아직 등록된 링크가 없습니다._")

        lines.append("")

    lines.append("<!-- NOTION_LINKS_END -->")

    return "\n".join(lines) + "\n"


def set_github_env(key, value):
    github_env = os.environ.get("GITHUB_ENV")
    if github_env:
        with open(github_env, "a") as f:
            f.write(f"{key}={value}\n")


def set_github_output(key, value):
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"{key}={value}\n")
