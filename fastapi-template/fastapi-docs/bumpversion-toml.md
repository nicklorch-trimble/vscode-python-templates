# Version Management (.bumpversion.toml)

Documentation for the version bumping configuration.

```toml
[tool.bumpversion]
current_version = "0.0.1"
commit = true
commit_args = "--no-verify"
tag = true
tag_name = "v{new_version}"
allow_dirty = true
parse = "(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)(\\.(?P<dev>post)\\d+\\.dev\\d+)?"
serialize = [
    "{major}.{minor}.{patch}.{dev}.dev{distance_to_latest_tag}",
    "{major}.{minor}.{patch}"
]
message = "Version updated from {current_version} to {new_version}"

[[tool.bumpversion.files]]
filename = "pyproject.toml"
search = "version = \"{current_version}\""
replace = "version = \"{new_version}\""
```