# Contributing

Thanks for wanting to help!

- **Found a bug?** Open an issue. Say what you ran, what you expected, and what happened.
- **Have an idea?** Open an issue first so we can talk about it.
- **Sending code?** Keep the change small. Add or update a test in `tests/`, and run `python -m unittest discover tests` before you open a pull request.

This repo is a thin wrapper. It depends on the lite packages and remounts their MCP tools. Fixes to how a tool works usually belong in that lite's repo:

- [json-repair-lite](https://github.com/tidybytetools/json-repair-lite)
- [json-shaper-lite](https://github.com/tidybytetools/json-shaper-lite)
- [base64-lite](https://github.com/tidybytetools/base64-lite)
- [hash-lite](https://github.com/tidybytetools/hash-lite)
- [md-chunk-lite](https://github.com/tidybytetools/md-chunk-lite)
- [doc2md-lite](https://github.com/tidybytetools/doc2md-lite)
- [pdf-table-pull-lite](https://github.com/tidybytetools/pdf-table-pull-lite)
- [link-check-lite](https://github.com/tidybytetools/link-check-lite)

Please be kind to everyone. By sending a change, you agree it is shared under the MIT license.
