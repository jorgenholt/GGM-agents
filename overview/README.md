# overview

The project hub page: timeline and tasks, all sources mapped to the thesis structure, the
repository explained, and a place for the agents.

**Published at:** https://claude.ai/artifact/FqBcHUumqgnmVJMQ5Xevbh (private until shared from the
page's Share menu).

## How it stays in sync with the repo

The page shows nothing of its own. Everything it displays comes from `data/overview.json`, which
`build.py` generates from the repo:

| The page shows | It comes from |
|---|---|
| Sources, topics, chapters, reading list, the gap | `docs/literature-sources.md` |
| Timeline and milestones | the plan table in `docs/thesis-scope.md` |
| The argument, chapter list, decisions | `docs/project-thesis-structure.md` |
| Workflow steps and stage verdicts | `docs/workflow-task-inventory.md` |
| Questions for Thursday | `docs/questions-for-weekly-meeting.md` |
| Files, folders, recent commits | `git` |
| Agents | `agents/registry.json` (doesn't exist yet) |

So to change what the page says, change the docs. Then rebuild and republish:

```bash
python3 overview/build.py
```

Then ask Claude to republish `overview/index.html` with `data/overview.json` (same URL).

**This also happens automatically.** A cloud routine,
[GGM hub: sync and rebuild](https://claude.ai/code/routines/trig_01Wigzds8U52Zr9DqaZtaNrs), runs every
three hours. It clones `main` from GitHub, syncs hub writing into `thesis/`, runs the build, and
republishes only if the content fingerprint (`contentHash`) differs from the published copy. So only
changes merged into `main` on GitHub reach the page. Pause or delete it from the routine's page.

## Writing

The Writing tab is where the thesis is written. Its text lives in `thesis/` in the repo; the page
keeps drafts in its shared storage until the sync routine writes them to GitHub. How that works,
and what happens on a conflict: [`thesis/README.md`](../thesis/README.md).

## What is *not* in the repo

**Tasks**, **reading status** and **unsynced writing** are stored with the published page on
claude.ai, so everyone with access sees the same thing. Tasks and reading status are never written
back to git; writing is, at the next sync.

## Rules

- Nothing from `data_2023/` goes into the page. The build script only counts those files.
- "Related papers" has two kinds of link: *named in notes* (one entry mentions another) and
  *similar topic* (computed from the text). The second kind is a starting point, not a claim.
- The chapter-5 step for each source is matched from keywords, so check it before relying on it.
