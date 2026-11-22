// The outcome of a write: the commit it made (by its short SHA), that there was nothing to
// commit, or the output of the git hook that refused it, in which case nothing was committed
// (FR-27).
import type { CommitOut } from "../api";

export function CommitLine({ commit, done }: { commit: CommitOut; done: string }) {
  if (!commit.ok) {
    return (
      <>
        <p className="problem" role="alert">
          A git hook failed, so nothing was committed. Fix the cause and try again.
        </p>
        <pre className="hook-output">{commit.output}</pre>
      </>
    );
  }
  if (commit.sha === null)
    return <p>{commit.output === "" ? "Nothing to commit." : commit.output}</p>;
  return (
    <p>
      {done} as commit <code>{commit.sha.slice(0, 7)}</code>. Nothing was pushed.
    </p>
  );
}
