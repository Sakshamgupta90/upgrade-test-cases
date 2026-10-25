# Upgrade Test Cases

Small, deliberately outdated projects for testing whether an AI agent can work out
what's wrong with old code and write the right fix. Each folder pins old versions
of its framework and libraries and uses APIs that later versions changed or removed.

Each case has:

- 1–2 code files written the old way
- the dependency manifest with old versions pinned (`requirements.txt`, `package.json`, `pom.xml`, ...)
- `TASK.md`: the instruction to give the agent

The answer key is in [`EXPECTED_FIXES.md`](EXPECTED_FIXES.md). **Don't let the agent
read it**: point the agent at one case folder at a time, or delete the file from the
copy the agent works on.

## Cases

| Folder | Stack | Pinned | Kind |
|---|---|---|---|
| `python-pydantic` | Python, pydantic | 1.10.13 | Major-version migration |
| `python-flask` | Python, Flask | 1.1.4 | Migration + vulnerable versions |
| `python-django` | Python, Django | 3.2.25 | Migration |
| `python-pandas` | Python, pandas | 1.5.3 | Migration |
| `node-express` | Node.js, Express | 4.17.1 | Migration + vulnerable versions |
| `node-security` | Node.js, lodash, axios | 4.17.15, 0.21.0 | Security (CVEs) |
| `typescript` | TypeScript | 4.9.5 | Compiler config migration |
| `react` | React, Create React App | 17.0.2 | Migration |
| `nextjs` | Next.js | 12.3.4 | Migration |
| `vue` | Vue, Vue Router | 2.6.14, 3.5.3 | Migration |
| `angular` | Angular | 12.2.17 | Migration |
| `java-spring-boot` | Java, Spring Boot | 2.7.18 | Migration |
| `java-log4j` | Java, Log4j | 2.14.1 | Security (Log4Shell) |
| `go` | Go, jwt-go | go 1.15 | Deprecations + security |
| `ruby-rails` | Ruby, Rails | 6.1.7 | Migration |
| `php-laravel` | PHP, Laravel | 8.x | Migration |

## How to use a case

1. Give the agent one folder and the instruction in its `TASK.md`.
2. Compare its changes with that case's section in `EXPECTED_FIXES.md`.
3. Score it on: did it find every issue, did it change the versions correctly, and did it
   avoid inventing APIs that don't exist?

## Tests

These 8 cases have behaviour tests that pass on the old code **and** after a correct upgrade
to the latest version, so a tool like PatchForge can verify its fix:

| Case | Run with | Notes |
|---|---|---|
| `python-pydantic` | `pytest` | |
| `python-flask` | `pytest` | old pins need Python 3.9 (`.python-version`) |
| `python-django` | `pytest` | Python 3.9; a correct upgrade to Django 6 must raise it to 3.12 |
| `python-pandas` | `pytest` | Python 3.10; a correct upgrade to pandas 3 must raise it to 3.11 |
| `node-express` | `npm test` | |
| `node-security` | `npm test` | |
| `typescript` | `npm test` | compiles the project; TypeScript 7 rejects the old settings |
| `react` | `npm test` | renders the app to HTML; the old `react-scripts` install is slow |

The tests check behaviour, not which API is used, so they don't give the answer away.
The other cases have no tests yet. Some cases are fragments of a larger app (for example
`python-django` has no `settings.py`; its tests configure Django themselves).
