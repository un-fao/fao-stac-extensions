## Summary

What this PR changes, in 1-3 bullet points.

-
-

## Linked issue

Closes #...

## Checklist

- [ ] `npm test` passes locally (schema validation + Markdown lint).
- [ ] `cd reference-implementation && pytest` passes locally.
- [ ] Every changed example still validates against its schema.
- [ ] Schema URLs were NOT bumped (or the bump is reflected everywhere
      consistently: schema `$id`, example `stac_extensions[]`,
      `package.json` `--schemaMap`, reference-implementation `SCHEMA_URI`,
      tests).
- [ ] CHANGELOG entries added under `[Unreleased]` for each affected
      extension and at the umbrella level.
- [ ] No AI/agent identifiers, personal paths, or `.claude/` references
      in the diff.
- [ ] No production hostnames or storage-bucket paths in committed
      examples (use `example.org` placeholders).
