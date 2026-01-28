# Restore Original Learning Graph Files

## Manual Restoration Required

Due to git lock file issues, the learning graph files need to be manually restored.

## Steps to Restore

Run these commands from `/Users/camgross/Projects/claude-skills`:

```bash
# Restore original learning graph CSV and JSON
git checkout '36c8c06d^' -- docs/learning-graph/learning-graph.csv
git checkout '36c8c06d^' -- docs/learning-graph/learning-graph.json

# If these files were modified, restore them too
git checkout '36c8c06d^' -- docs/learning-graph/quality-metrics.md
git checkout '36c8c06d^' -- docs/learning-graph/taxonomy-distribution.md
```

## Files Already Deleted

The following GED-specific files have been deleted:
- `docs/learning-graph/list-concepts.md` (GED Science concept list)
- `docs/learning-graph/course-description.md` (GED Science course description)

These should not be restored as they were GED-specific additions.

## Verification

After restoration, verify:
- `docs/learning-graph/learning-graph.csv` starts with "Artificial Intelligence" (not "Scientific Reasoning")
- `docs/learning-graph/learning-graph.json` contains original concepts (not GED Science concepts)
