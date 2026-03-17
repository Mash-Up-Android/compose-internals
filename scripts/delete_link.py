import os
import sys

from common import MEMBERS, generate_readme, load_links, parse_issue_body, save_links, set_github_env, set_github_output


def fail(message):
    print(f"Error: {message}")
    set_github_output("error_message", message)
    sys.exit(1)


def main():
    body = os.environ.get("ISSUE_BODY", "")
    parsed = parse_issue_body(body)

    member = parsed.get("👤 이름", "").strip()
    week = parsed.get("📅 삭제할 주차", "").strip()

    if not all([member, week]):
        fail("이름 또는 주차 정보가 누락되었습니다.")

    if member not in MEMBERS:
        fail(f"알 수 없는 이름입니다: {member}")

    try:
        week_num = int(week)
    except ValueError:
        fail(f"주차는 숫자로 입력해주세요. 입력값: {week}")

    links = load_links()

    if str(week_num) not in links.get(member, {}):
        fail(f"{member}의 {week_num}주차 링크가 존재하지 않습니다. 주차 번호를 다시 확인해주세요.")

    del links[member][str(week_num)]
    save_links(links)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(generate_readme(links))

    set_github_env("MEMBER", member)
    set_github_env("WEEK", week_num)

    print(f"Successfully deleted: {member} {week_num}주차")


if __name__ == "__main__":
    main()
