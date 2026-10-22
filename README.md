# Inbox Triage

English | [简体中文](README.zh-CN.md)

Sort an exported inbox into a reply queue without connecting your mailbox. The helper uses message age, reply status, VIP senders, and your response target to explain what needs attention.

[Download v0.2.1](https://github.com/KarmenLoop/skill-inbox-triage/releases/tag/v0.2.1) · [Tutorial](docs/tutorial.en.md) · [Input reference](docs/INPUT.md) · [Report an issue](https://github.com/KarmenLoop/skill-inbox-triage/issues)

## What it does

The 50-hour-old message is overdue; the recent VIP message also enters reply_now, with a different reason.

No mailbox is read and no reply is sent. The result is only as current as the export and status values you provide.

![Inbox Triage sample JSON output from version 0.2.1](docs/images/example-output-v0.2.1.svg)

*Actual local output from v0.2.1, rendered as an image. [Complete result](examples/expected.json) · [Image provenance](docs/images/provenance.json).*

## Start here

Download `karmen-inbox-triage-v0.2.1.zip` and its `.sha256` file from the release, verify the hash, then extract the ZIP. In the extracted directory, use Python 3.9 or later:

```sh
python3 scripts/run.py --version
python3 scripts/run.py --input examples/input.json
```

Expected version: `karmen-inbox-triage 0.2.1`. The 50-hour-old message is overdue; the recent VIP message also enters reply_now, with a different reason.

To install the complete skill into a host that reads `~/.agents/skills`:

```sh
python3 install.py --host agents
```

The installer refuses an existing destination. Host discovery and invocation vary; see the [full setup and practice guide](docs/tutorial.en.md). You can run the helper directly without an AI host.

## Use it with your own work

Set now and sla_hours for the review. Keep received_at timezone-aware, needs_reply Boolean, and status open, waiting, or closed; match VIP addresses exactly apart from case.

Compare queues before and after marking a message waiting or closed. Change the response target to see which open items become overdue; do not treat an exported status as a live mailbox update.

Read the [field contract](docs/INPUT.md) before preparing a new input. The helper runs locally with the Python standard library; it needs no model account, API key, or network connection. An AI host has its own data and permission settings.

## Questions

**Do I need Gmail or Microsoft credentials?** No credentials are used by this helper. If you export mail with another tool, review that tool’s access separately.

**Where does the result go?** JSON is printed to stdout unless you request a new file with `--output`. Existing output files are preserved. The helper reads only the submitted records and any local paths documented in its input contract.

## Documentation and support

- [Download, install, configure, practice, upgrade, and remove](docs/tutorial.en.md)
- [Input/output contract](docs/INPUT.md) and [compatibility](docs/COMPATIBILITY.md)
- [Changelog](CHANGELOG.md), [contributing](CONTRIBUTING.md), [support](SUPPORT.md), and [security reports](SECURITY.md)

## License

[MIT](LICENSE). Keep the license and [notice](NOTICE.md) with redistributed copies. Maintained by [KarmenLoop](https://karmenloop.com).
