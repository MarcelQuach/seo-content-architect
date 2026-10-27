# Project isolation, integrations and storage
This community skill is portable. It has no preconfigured personal Google Drive, company, shop, brand, account, API key or default client. Every user chooses their own storage and tools.

Suggested project structure: <project>/configuration, research, serp, clusters, briefs, drafts, qa, final, exports. Create only with explicit permission. Store private configuration and research outside the public skill repository. Do not commit client information, credentials or API responses containing secrets.

Prefer connected tools over manual CSV uploads when the user authorizes them and they are available. Check actual scopes and tool support; do not assume Ahrefs Standard includes specific API rights, or that GSC/Keyword Planner can be read through a particular connection. Respect API rate limits and budget. If automation is unavailable, explain the gap and provide a practical fallback. Record source timestamps and preserve reproducible evidence.
