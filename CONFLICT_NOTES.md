# Merge Conflict Notes

## What happened
Both branches changed the same line of `README.md` (line 3, the `Status:` line) starting from the same parent commit (`d757a35`):

| Branch | Commit | New text of line 3 |
|--------|--------|--------------------|
| `proposal` | "README: mark proposal as complete" | `Status: Proposal complete, see proposal.md (awaiting merge into main).` |
| `main` | "README: mark data as prepared" | `Status: Data prepared, analysis not started.` |

Git cannot choose between two different edits of one line, so merging `main` into `proposal` stopped with:

```
CONFLICT (content): Merge conflict in README.md
Automatic merge failed; fix conflicts and then commit the result.
```

GitHub reported the same conflict on the pull request from `proposal` into `main`.

## How the conflict looked
```
<<<<<<< HEAD
Status: Proposal complete, see proposal.md (awaiting merge into main).
=======
Status: Data prepared, analysis not started.
>>>>>>> main
```

## How I resolved it
1. Ran `git merge main` while on the `proposal` branch to bring `main`'s change in and resolve the conflict there, so `main` stays clean until the pull request is merged.
2. Opened `README.md` and read both versions. Neither was wrong: they describe two different true facts (data is ready, proposal is written).
3. Replaced the whole conflict block, including the `<<<<<<<`, `=======` and `>>>>>>>` markers, with one line that keeps both facts:
   `Status: Data prepared and proposal complete (see proposal.md); analysis not started.`
4. Checked that no conflict markers remained in the file (`grep` for `<<<<<<<`, `=======`, `>>>>>>>` found none).
5. Ran `git add README.md` and `git commit` to complete the merge, then pushed `proposal`.
6. The pull request became mergeable and was merged into `main`.

## Lesson
Resolving the conflict means deciding what the line should say, not picking a side. Keeping `Status:` to a single short line makes this kind of clash more likely, so a longer status section would make future conflicts easier to resolve.
