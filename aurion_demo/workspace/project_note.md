# Project Note — Demo Workspace

This is a small, included sample file. The bounded governed mission reads **only** this file (inside the
bundled demo workspace) and extracts action items from it. Nothing here is sensitive; it ships with the
public Demo Public Alpha package.

## Context

We are preparing the public Demo Public Alpha runtime. A few follow-ups came up while reviewing the
governed mission spine. The mission's job is to pull out the first three action items below and save
them — without touching the internet.

## Candidate action items

- [ ] Document the bounded PermissionGraph contract (read-in-workspace, write-in-generated, deny network).
- [ ] Add a clear terminal summary that distinguishes allowed vs blocked steps.
- [ ] Ship a cross-platform CI matrix (Linux, Windows, macOS) that runs the mission with no secrets.
- [ ] (extra) Explore optional local-model integration later — explicitly out of scope for now.

## Notes

The runtime must stay offline and deterministic. The external-research step is expected to be **denied**
by the PermissionGraph because no network permission is granted in this bounded package.
