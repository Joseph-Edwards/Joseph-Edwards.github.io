import requests
import json

AUTHOR_REPOS = [
    "libsemigroups/libsemigroups",
    "libsemigroups/libsemigroups_pybind11",
]

MAINTAINER_REPOS = [
    "semigroups/Semigroups",
    "digraphs/Digraphs",
]

CONTRIBUTOR_REPOS = [
    "gap-system/gap",
    "libsemigroups/Semigroups.jl",
    "libsemigroups/HPCombi",
    "github/docs",
    "gap-actions/run-pkg-tests",
    "graph-algorithms/edge-addition-planarity-suite",
]


def process_languages(language_to_bytes: dict) -> list:
    total_bytes = sum(language_to_bytes.values())

    # Convert byte count to percentage
    percentages = {
        language: num_bytes * 100 / total_bytes
        for language, num_bytes in language_to_bytes.items()
    }

    # Select only the significant languages, and convert to a list of dicts so
    # Hugo doesn't sort by keys
    percentages = [
        {"name": lang, "percent": perc}
        for lang, perc in percentages.items()
        if round(perc, 1) > 0
    ]

    return sorted(percentages, key=lambda x: x["percent"], reverse=True)


def process_repos(repos: list, output_file_name: str) -> None:
    out = []
    for repo in repos:
        print(f"Fetching {repo} . . . ", end="")
        # fetch repo info
        repo_url = f"https://api.github.com/repos/{repo}"
        r = requests.get(repo_url)
        data = r.json()

        # fetch language breakdown
        language_url = requests.get(repo_url + "/languages")
        languages = process_languages(language_url.json())

        repo_name = data.get("name")
        org = data.get("full_name")[: -(len(repo_name) + 1)]

        out.append(
            {
                "name": repo_name,
                "org": org,
                "description": data.get("description"),
                "stars": data.get("stargazers_count"),
                "forks": data.get("forks_count"),
                "languages": languages,
                "url": data.get("html_url"),
            }
        )
        print("done")

    with open(output_file_name, "w") as f:
        json.dump(out, f, indent=2)


process_repos(AUTHOR_REPOS, "data/github/author.json")
process_repos(MAINTAINER_REPOS, "data/github/maintainer.json")
process_repos(CONTRIBUTOR_REPOS, "data/github/contributor.json")
