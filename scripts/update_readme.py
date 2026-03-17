import os
import sys

from common import MEMBERS, generate_readme, load_links, parse_issue_body, save_links, set_github_env


def main():
    body = os.environ.get("ISSUE_BODY", "")
    parsed = parse_issue_body(body)

    member = parsed.get("👤 이름", "").strip()
    week = parsed.get("📅 주차", "").strip()
    url = parsed.get("🔗 Notion URL", "").strip()

    if not all([member, week, url]):
        print(f"Error: Missing required fields. Parsed: {parsed}")
        sys.exit(1)

    if member not in MEMBERS:
        print(f"Error: Unknown member: {member}")
        sys.exit(1)

    try:
        week_num = int(week)
    except ValueError:
        print(f"Error: Week must be a number, got: {week}")
        sys.exit(1)

    links = load_links()
    links[member][str(week_num)] = url
    save_links(links)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(generate_readme(links))

    set_github_env("MEMBER", member)
    set_github_env("WEEK", week_num)

    print(f"Successfully updated: {member} {week_num}주차")


if __name__ == "__main__":
    main()
