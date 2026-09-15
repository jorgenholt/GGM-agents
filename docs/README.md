# docs

Working documents for the project thesis. Start here.

## Read in this order

| File | What it is | When you want it |
|---|---|---|
| [`thesis-scope.md`](thesis-scope.md) | The two-phase structure — project thesis now, master's in spring | Orienting, or when someone proposes building something |
| [`project-thesis-structure.md`](project-thesis-structure.md) | Proposed chapter structure, related work, open decisions | Discussing structure with supervisors. **Short version is at the top** |
| [`workflow-task-inventory.md`](workflow-task-inventory.md) | The analysis: four input layers, eleven workflow stages, what is code vs agent vs human | Working on the core chapter. This is the analytical heart |
| [`how-it-would-work.md`](how-it-would-work.md) | One scenario walked end to end, today versus with agents | Explaining the idea to someone concretely |
| [`ggm-model.md`](ggm-model.md) | Model reference — sets, variables, constraints, parameters, calibration, with PDF page pointers | Looking up how GGM actually works |
| [`questions-for-weekly-meeting.md`](questions-for-weekly-meeting.md) | Things needing a human answer, and answers already resolved | Before each weekly meeting |
| [`ggm-documentation-v3.0.pdf`](ggm-documentation-v3.0.pdf) | Egging & Holz (2019), DIW Data Documentation 100 | The source of truth for GGM |

## Which file does a new finding go in?

Per the convention in the root `CLAUDE.md`:

- **How GGM works** → `ggm-model.md`, with a source line or PDF page that proves it
- **What is automatable and why** → `workflow-task-inventory.md`
- **Needs a human answer** → `questions-for-weekly-meeting.md`
- **Thesis framing or chapter structure** → `project-thesis-structure.md`
- **Phase, scope, deadlines** → `thesis-scope.md`

Keep the analysis in one place and link to it rather than restating — the task classification lives
in `workflow-task-inventory.md`, and everything else points there.

## Conventions

- **PDF page references are PDF page numbers**, not the printed footer number, which runs 2 lower.
  PDF p. 48 shows "46" at the bottom.
- Distinguish **verified** from **assumed**. Most of the workflow analysis is inferred from
  documentation, not observed — it is marked as such and needs checking with Franziska and Lukas.
- Resolved questions move to the **Resolved** section of the questions file with their answer, rather
  than being deleted.
