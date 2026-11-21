"""The ``ontology-builder`` commands, on a workspace from the layered environment."""

from __future__ import annotations

import os
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Annotated, Any

import typer
import yaml

from ontology_builder import api, evaluation
from ontology_builder.workflows import (
    GovernanceRefusedError,
    IngestionFailedError,
    IngestionRefusedError,
    LlmError,
    OpenOntology,
    WorkflowRefusedError,
    Workspace,
    actor_of,
    create_ontology,
    open_ontology,
    workspace_from_env,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
"""Relative paths in the environment are relative to the repository root."""

REFUSALS = (
    WorkflowRefusedError,
    GovernanceRefusedError,
    IngestionRefusedError,
    IngestionFailedError,
    LlmError,
)

HELP = "Build leveled ontologies from Markdown corpora (spec 0002). Publishing is GUI-only."

User = Annotated[str, typer.Option("--user", help="Your handle (not a real name or email).")]


def _env_workspace() -> Workspace:
    return workspace_from_env(os.environ, REPO_ROOT)


@contextmanager
def _refusals() -> Iterator[None]:
    """A refusal of a use case is shown as a message and ends the command with exit code 1."""
    try:
        yield
    except REFUSALS as refused:
        typer.echo(f"refused: {refused}", err=True)
        raise typer.Exit(1) from None


def _commit_line(result: Any) -> str:
    if not result.ok:
        return f"not committed; the commit failed:\n{result.output}"
    return f"committed {result.sha}" if result.sha else "nothing to commit"


def _show_estimate(plan: Any) -> None:
    shown = plan.estimate
    cost = f"${shown.cost_usd:.2f}" if shown.cost_usd is not None else "unknown for this model"
    typer.echo(
        f"{shown.documents} documents, {shown.units} source units, model {plan.model}\n"
        f"estimated {shown.input_tokens} input tokens and up to {shown.output_tokens} "
        f"output tokens; estimated cost {cost}"
    )


def _show_eval_estimate(shown: Any) -> None:
    cost = f"${shown.cost_usd:.2f}" if shown.cost_usd is not None else "unknown for this model"
    typer.echo(
        f"evaluation: {shown.documents} documents, {shown.units} source units of the pet manuals\n"
        f"estimated {shown.input_tokens} input tokens and up to {shown.output_tokens} "
        f"output tokens; estimated cost {cost}"
    )


def _ingest(session: OpenOntology, user: str, folder: str, yes: bool) -> Any:
    plan = session.plan_ingestion(actor_of(user, "user"), folder)
    _show_estimate(plan)
    if not yes and not typer.confirm("Run it?", default=False):
        typer.echo("nothing was run")
        raise typer.Exit(1)
    return session.ingest(plan, confirm=True)


def make_app(workspace: Callable[[], Workspace] = _env_workspace) -> typer.Typer:
    """The command app; tests pass their own ``workspace``."""
    app = typer.Typer(no_args_is_help=True, add_completion=False, help=HELP)

    @app.command()
    def create(name: str, scope: Annotated[Path, typer.Option()], user: User) -> None:
        """Create an ontology with a scope record (YAML) as domain admin, and commit it."""
        with _refusals():
            record = yaml.safe_load(scope.read_text(encoding="utf-8")) or {}
            result = create_ontology(workspace(), name, record, actor_of(user, "domain_admin"))
        typer.echo(_commit_line(result))
        if not result.ok:
            raise typer.Exit(1)

    @app.command()
    def ingest(
        name: str,
        folder: str,
        user: User,
        yes: Annotated[bool, typer.Option("--yes", help="Skip the cost question.")] = False,
        resume: Annotated[str | None, typer.Option(help="Resume a failed run.")] = None,
    ) -> None:
        """Ingest a folder (under the sources root) as a new corpus; asks after the estimate."""
        with _refusals(), open_ontology(workspace(), name) as session:
            outcome = session.resume(resume) if resume else _ingest(session, user, folder, yes)
        typer.echo(f"run {outcome.run_id}: {outcome.status}; {_commit_line(outcome.commit)}")

    @app.command()
    def build(name: str) -> None:
        """Rebuild the raw release from the saved records (no commit)."""
        with _refusals(), open_ontology(workspace(), name) as session:
            typer.echo(f"raw release built in {session.build()}")

    @app.command()
    def serve(
        name: str,
        port: Annotated[int, typer.Option(envvar="ONTOLOGY_BUILDER_PORT")] = api.DEFAULT_PORT,
    ) -> None:
        """Serve the review GUI and its API on http://127.0.0.1:<port> (local only)."""
        with _refusals(), open_ontology(workspace(), name) as session:
            typer.echo(f"serving {name} on http://127.0.0.1:{port} (Ctrl+C stops)")
            api.serve(session, port)

    @app.command(name="eval")
    def evaluate(
        yes: Annotated[bool, typer.Option("--yes", help="Skip the cost question.")] = False,
        model: Annotated[str | None, typer.Option(help="Evaluate this model.")] = None,
        report_dir: Annotated[Path, typer.Option()] = evaluation.REPORTS_DIR,
    ) -> None:
        """Ingest the pet manuals live into a throw-away ontology and score it against the
        answer key; writes a dated report (costs money; not a gate)."""
        if model:
            os.environ["CLAUDE_MODEL"] = model  # read when the workspace makes its LLM client

        def confirm(estimate: Any) -> bool:
            _show_eval_estimate(estimate)
            return yes or typer.confirm("Run it?", default=False)

        with _refusals():
            result = evaluation.evaluate(workspace(), confirm, reports_dir=report_dir)
        if result is None:
            typer.echo("nothing was run")
            raise typer.Exit(1)
        for line in evaluation.summary_lines(result.scores):
            typer.echo(line)
        typer.echo(f"report: {result.report}")

    return app


def main() -> None:
    make_app()()
