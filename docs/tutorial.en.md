# Inbox Triage: from download to a repeatable workflow

English | [简体中文](tutorial.zh-CN.md) · [Project](../README.md)

This guide matches v0.2.1. Sort an exported inbox into a reply queue without connecting your mailbox. The helper uses message age, reply status, VIP senders, and your response target to explain what needs attention.

## 1. Download and verify

Open [v0.2.1](https://github.com/KarmenLoop/skill-inbox-triage/releases/tag/v0.2.1). Download `karmen-inbox-triage-v0.2.1.zip` and `karmen-inbox-triage-v0.2.1.zip.sha256` together. The ZIP contains source and a portable agent skill, not a desktop installer. Python 3.9+ is required; no third-party Python packages are needed.

On macOS, run `shasum -a 256 karmen-inbox-triage-v0.2.1.zip`; on Linux, use `sha256sum karmen-inbox-triage-v0.2.1.zip`. In Windows PowerShell, use `Get-FileHash .\karmen-inbox-triage-v0.2.1.zip -Algorithm SHA256`. Compare the full value with the downloaded checksum file before extracting. The expected hash must come from a trusted source.

Extract the archive and open a terminal in its top-level directory. On Windows, replace `python3` below with `py -3` or the Python command configured on your machine.

## 2. Check the first result

```sh
python3 scripts/run.py --version
python3 scripts/run.py --input examples/input.json
```

The version must be `karmen-inbox-triage 0.2.1`. The 50-hour-old message is overdue; the recent VIP message also enters reply_now, with a different reason. Compare the complete JSON with [examples/expected.json](../examples/expected.json). Exit 0 means the input was processed, not that the underlying task or reported findings passed.

## 3. Add the skill to an AI host

The local helper works without a host. To install instructions and references into the shared agent-skill directory:

```sh
python3 install.py --host agents
```

Other explicit choices are `--host codex`, `--host deepseek`, and `--host grok`. These select directory conventions, not verified support for every host version. For a host-specific location, use `python3 install.py --destination /path/to/a/new/karmen-inbox-triage` with your own path. The destination must be new and outside the source package.

Refresh the host’s skill discovery or start a new session. Confirm that it can read `karmen-inbox-triage/SKILL.md` and its references before relying on an invocation. Installation copies files; it does not grant tools, credentials, or account access.

## 4. Configure a real input

Copy `examples/input.json` to `my-input.json`, keep its JSON keys, and replace sample values. Set now and sla_hours for the review. Keep received_at timezone-aware, needs_reply Boolean, and status open, waiting, or closed; match VIP addresses exactly apart from case. The [input reference](INPUT.md) defines all fields and output keys.

Use UTF-8 JSON with an object at the top level. The input limit is 10 MiB. Duplicate keys, invalid JSON, and non-finite numbers are rejected. For records containing timestamps, include the UTC offset. Keep original observations and sources so someone else can check the result.

```sh
python3 scripts/run.py --input my-input.json --output my-result.json
```

The output path must not already exist. Read the result before passing it to another tool. No mailbox is read and no reply is sent. The result is only as current as the export and status values you provide.

## 5. Practice beyond the sample

Compare queues before and after marking a message waiting or closed. Change the response target to see which open items become overdue; do not treat an exported status as a live mailbox update.

Save the input, output, installed version, and any supporting evidence together. Compare outcomes after changing one relevant input at a time. If an AI prepares the JSON, inspect its records against the original material; fluent wording is not evidence that a fact or permission is correct.

You can pipe JSON through standard input with `--input -`. In PowerShell, use `Get-Content -Raw .\my-input.json | py -3 scripts/run.py --input -`. For automated workflows, check the exit code and inspect the domain result before taking any action.

## 6. Troubleshoot

- **Python cannot be found:** install Python 3.9+ and check the command with `python3 --version` or `py -3 --version`.
- **Input rejected / exit 2:** read stderr, validate the JSON, then compare required fields with [INPUT.md](INPUT.md).
- **Output already exists:** inspect or rename the earlier result, then choose a new output filename. A failed write may leave a partial new file; inspect it before retrying.
- **Host does not see the skill:** check the host’s configured skill root and refresh discovery. Run the helper directly to separate host setup from input problems.
- **Unexpected finding:** preserve the original input and output; report the version and a minimal synthetic reproduction through [Issues](https://github.com/KarmenLoop/skill-inbox-triage/issues). Remove private records first.

## 7. Update, roll back, or remove

Keep your inputs and outputs outside the installed skill folder. Verify a new release and install it into a fresh directory; the installer intentionally refuses replacement. Close active host sessions before moving directories. Keep the previous version as a backup, then select the intended directory using your host’s documented skill configuration. To roll back, restore that previous folder and refresh discovery.

To uninstall, remove only the exact skill directory created for `karmen-inbox-triage` after checking its path. No account, service, or scheduler is installed by this package.

## 8. Check or package a source change

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/check_docs.py
```

After committing a reviewed source change, build into a new directory outside the repository with `python3 scripts/package_release.py --output /path/to/new/release-dir`. The builder retains both languages, examples, tests, and legal notices and writes a checksum and commit receipt. Use the resulting asset’s version when updating documentation and example images.

[MIT license](../LICENSE) · [Project home](../README.md)
