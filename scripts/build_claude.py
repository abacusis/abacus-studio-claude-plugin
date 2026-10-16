"""Thin Claude adapter over the shared source; no install or publication."""
import json


def render(root, sources):
    output = {source.relative_to(root).as_posix(): source.read_bytes() for source in sources}
    # The repository catalog selects plugins/claude; a standalone ZIP selects itself.
    catalog = json.loads(output['.claude-plugin/marketplace.json'])
    catalog['plugins'][0]['source'] = './'
    output['.claude-plugin/marketplace.json'] = (json.dumps(catalog, indent=2) + '\n').encode()
    return output
