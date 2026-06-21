import click
import asyncio
import os
import json
from rich.console import Console
from rich.table import Table
import asyncpg
from dotenv import load_dotenv

from scripts.simulate_ingestion import simulate_ingestion
from models import BaseAgent

load_dotenv()

console = Console()
DATABASE_URL = os.getenv("DATABASE_URL")

@click.group()
def cli():
    """AYUTHOS-AI: The 100-Agent Civilization Forecasting Engine"""
    pass

@cli.command()
@click.option('--files', '-f', multiple=True, help='Seed data files (PDF, MD, TXT, JSON).')
@click.option('--requirement', '-r', required=True, help='Natural language forecast query.')
@click.option('--platform', '-p', type=click.Choice(['parallel', 'twitter', 'reddit']), default='parallel', help='Simulation platform.')
@click.option('--max-rounds', '-m', type=int, default=100, help='Max simulation rounds.')
@click.option('--agents', '-a', type=int, default=100, help='Number of agents.')
@click.option('--json', 'json_output', is_flag=True, help='Machine-readable JSON output.')
@click.option('--no-cache', is_flag=True, help='Force fresh LLM calls.')
async def run(files, requirement, platform, max_rounds, agents, json_output, no_cache):
    """Launch a full 100-agent simulation."""
    console.print(f"[bold green]Launching simulation with requirement:[/bold green] {requirement}")
    console.print(f"Files: {files}, Platform: {platform}, Max Rounds: {max_rounds}, Agents: {agents}")
    console.print(f"JSON Output: {json_output}, No Cache: {no_cache}")
    console.print("[yellow]Simulation logic will be implemented in the Rust Orchestrator.[/yellow]")

@cli.command()
@click.option('--run-id', help='Specific run status.')
@click.option('--live', is_flag=True, help='Real-time dashboard.')
async def status(run_id, live):
    """Live dashboard of all agents, confidence scores, and emerging scenarios."""
    console.print(f"[bold blue]Checking status for run ID:[/bold blue] {run_id if run_id else 'latest'}")
    if live:
        console.print("[bold magenta]Displaying real-time dashboard...[/bold magenta]")
    console.print("[yellow]Status logic not yet fully implemented.[/yellow]")

@cli.command()
@click.option('--variable', '-v', required=True, help='Dynamically inject new variables mid-simulation.')
async def inject(variable):
    """Dynamically inject new variables mid-simulation."""
    console.print(f"[bold yellow]Injecting variable:[/bold yellow] {variable}")
    console.print("[yellow]Injection logic not yet implemented.[/yellow]")

@cli.command()
@click.option('--run-id', help='Export specific run.')
@click.option('--format', '-F', type=click.Choice(['json', 'md']), default='json', help='Output format.')
async def export(run_id, format):
    """Export simulation results."""
    console.print(f"[bold cyan]Exporting run ID:[/bold cyan] {run_id if run_id else 'latest'} in {format} format")
    console.print("[yellow]Export logic not yet implemented.[/yellow]")

@cli.group()
def agents():
    """Manage agent personas."""
    pass

@agents.command('list')
async def agents_list():
    """List all 100 agent personas."""
    console.print("[bold green]Listing all agent personas...[/bold green]")
    if not DATABASE_URL:
        console.print("[red]DATABASE_URL not found in .env. Cannot list agents.[/red]")
        return

    conn = None
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        rows = await conn.fetch("SELECT id, persona_name, background FROM agents ORDER BY id")
        
        if rows:
            table = Table(title="AYUTHOS-AI Agent Personas")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Persona Name", style="magenta")
            table.add_column("Background", style="green")

            for row in rows:
                table.add_row(str(row['id']), row['persona_name'], row['background'])
            console.print(table)
        else:
            console.print("[yellow]No agents found in the database. Run `python scripts/init_db.py` to generate them.[/yellow]")

    except Exception as e:
        console.print(f"[red]Error listing agents: {e}[/red]")
    finally:
        if conn:
            await conn.close()

@agents.command()
@click.option('--id', 'agent_id', required=True, help='Inspect specific agent.')
async def inspect(agent_id):
    """Inspect specific agent."""
    console.print(f"[bold blue]Inspecting agent ID:[/bold blue] {agent_id}[/bold blue]")
    if not DATABASE_URL:
        console.print("[red]DATABASE_URL not found in .env. Cannot inspect agent.[/red]")
        return

    conn = None
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        row = await conn.fetchrow("SELECT id, persona_name, background, personality_traits, memory FROM agents WHERE id = $1", int(agent_id))
        
        if row:
            table = Table(title=f"Agent Details: {row["persona_name"]}")
            table.add_column("Field", style="cyan")
            table.add_column("Value", style="magenta")

            table.add_row("ID", str(row["id"]))
            table.add_row("Persona Name", row["persona_name"])
            table.add_row("Background", row["background"])
            table.add_row("Personality Traits", json.dumps(row["personality_traits"], indent=2))
            table.add_row("Memory", json.dumps(row["memory"], indent=2))
            console.print(table)
        else:
            console.print(f"[red]Agent with ID {agent_id} not found.[/red]")

    except Exception as e:
        console.print(f"[red]Error inspecting agent: {e}[/red]")
    finally:
        if conn:
            await conn.close()

@agents.command()
@click.option('--id', 'agent_id', required=True, help='Modify agent personality.')
@click.option('--trait', required=True, help='Trait to modify.')
@click.option('--value', required=True, help='New value for the trait.')
async def modify(agent_id, trait, value):
    """Modify agent personality."""
    console.print(f"[bold yellow]Modifying agent ID:[/bold yellow] {agent_id}, Trait: {trait}, Value: {value}")
    if not DATABASE_URL:
        console.print("[red]DATABASE_URL not found in .env. Cannot modify agent.[/red]")
        return

    conn = None
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        row = await conn.fetchrow("SELECT personality_traits FROM agents WHERE id = $1", int(agent_id))
        
        if row:
            personality_traits = row["personality_traits"]
            personality_traits[trait] = json.loads(value) # Assuming value is JSON-serializable
            await conn.execute(
                "UPDATE agents SET personality_traits = $1 WHERE id = $2",
                json.dumps(personality_traits), int(agent_id)
            )
            console.print(f"[bold green]Successfully updated agent {agent_id}: set {trait} to {value}[/bold green]")
        else:
            console.print(f"[red]Agent with ID {agent_id} not found.[/red]")

    except json.JSONDecodeError:
        console.print(f"[red]Error: Value for trait '{trait}' is not valid JSON. Please provide a valid JSON string.[/red]")
    except Exception as e:
        console.print(f"[red]Error modifying agent: {e}[/red]")
    finally:
        if conn:
            await conn.close()

@click.group()
def ingest():
    """Manage data ingestion."""
    pass

@ingest.command()
@click.option('--simulate', is_flag=True, help='Simulate data ingestion from various sources.')
async def run(simulate):
    """Run data ingestion processes."""
    if simulate:
        await simulate_ingestion()
    else:
        click.echo("Please specify an ingestion method. Use --simulate for a simulated run.")

@cli.group()
def config():
    """Manage configuration."""
    pass

@config.command('show')
async def config_show():
    """Show current configuration."""
    console.print("[bold green]Showing current configuration...[/bold green]")
    console.print("[yellow]Config display logic not yet implemented.[/yellow]")

@config.command()
@click.option('--key', required=True, help='Configuration key.')
@click.option('--value', required=True, help='Configuration value.')
async def set(key, value):
    """Update configuration."""
    console.print(f"[bold yellow]Setting config key:[/bold yellow] {key} to {value}")
    console.print("[yellow]Config setting logic not yet implemented.[/yellow]")

if __name__ == '__main__':
    asyncio.run(cli())
