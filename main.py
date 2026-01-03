import os
import sys
import time

# Attempt to import Rich for UI
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.markdown import Markdown
    from rich.prompt import Prompt, Confirm
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Rich library not found. Falling back to basic UI.")

from src.engine import TRIZEngine
from src.models import IdealityFactor, EngineeringParameter

# --- Resource Path Handling (PyInstaller Support) ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# Initialize Console
if RICH_AVAILABLE:
    console = Console()
else:
    class MockConsole:
        def print(self, *args, **kwargs):
            print(*args)
        def rule(self, title=""):
            print(f"--- {title} ---")
    console = MockConsole()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header():
    if RICH_AVAILABLE:
        title = """
[bold cyan]AI-Assisted TRIZ Engineering Solver[/bold cyan]
[dim]Advanced Problem Solving Engine v2.0[/dim]
"""
        console.print(Panel(title.strip(), border_style="cyan"))
        console.print("[yellow]System Ready. Loading Knowledge Base...[/yellow]")
    else:
        print("=== AI-Assisted TRIZ Solver v2.0 ===")

def print_step_header(step_num, title):
    if RICH_AVAILABLE:
        console.print(f"\n[bold green on black] STEP {step_num} [/bold green on black] [bold white]{title}[/bold white]")
        console.rule(style="green")
    else:
        print(f"\n--- STEP {step_num}: {title} ---")

def simulate_thinking(text="Analyzing input..."):
    if RICH_AVAILABLE:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            progress.add_task(description=text, total=None)
            time.sleep(1.0) # Fake delay for UX
    else:
        print(f"[{text}]")
        time.sleep(0.5)

def resolve_parameter(engine: TRIZEngine, step_name: str, prompt_text: str) -> EngineeringParameter:
    while True:
        console.print(f"\n[bold]{prompt_text}[/bold]")
        if RICH_AVAILABLE:
            user_input = Prompt.ask("[cyan]User Input[/cyan]")
        else:
            user_input = input("User Input: ")
        
        simulate_thinking("AI is interpreting your input (Parsing Keywords)...")
        
        match, logs = engine.normalize_input_to_parameter(user_input)
        
        # Transparency: Show AI Logic
        if RICH_AVAILABLE:
            log_text = "\n".join([f"- {l}" for l in logs])
            console.print(Panel(log_text, title="[dim]AI Internal Reasoning[/dim]", border_style="dim", expand=False))
        else:
            print("--- AI Reasoning ---")
            for l in logs: print(f"- {l}")
        
        if match:
            console.print(f"\n[bold green]✅ Identified Parameter #{match.id}:[/bold green] [white]{match.name}[/white]")
            
            if RICH_AVAILABLE:
                confirm = Confirm.ask("Is this interpretation correct?")
            else:
                confirm = input("Is this correct? (y/n): ").lower() == 'y'

            if confirm:
                return match
            else:
                console.print("[yellow]Let's try again. Please try standard terms (e.g., 'Weight', 'Speed', 'Force').[/yellow]")
        else:
            console.print("[bold red]❌ Could not confidently identify a parameter.[/bold red]")
            console.print("Please try using clearer keywords (e.g., 'Moving object weight', 'Strength', 'Power').")

def main():
    data_dir = resource_path(os.path.join('src', 'data'))
    engine = TRIZEngine(data_dir=data_dir)

    clear_screen()
    show_header()

    # Phase 1: Context
    print_step_header(1, "Define Engineering System (系統定義)")
    if RICH_AVAILABLE:
        sys_name = Prompt.ask("System Name (e.g., 'Robot Arm')")
    else:
        sys_name = input("System Name: ")

    # Phase 2: Improving
    print_step_header(2, "Identify Improving Parameter (改善參數)")
    console.print(f"[dim]Describe what you want to improve in the [bold]{sys_name}[/bold].[/dim]")
    improving_param = resolve_parameter(engine, "Improving", "What do you want to IMPROVE? (e.g. 'I want it to be faster / 速度')")

    # Phase 3: Worsening
    print_step_header(3, "Identify Worsening Parameter (惡化參數)")
    console.print("[dim]When you improve that, what gets worse? This creates the technical contradiction.[/dim]")
    worsening_param = resolve_parameter(engine, "Worsening", f"When '{improving_param.name}' improves, what gets WORSE? (e.g. 'Structure gets weak / 結構變弱')")

    # Phase 4: Solution
    print_step_header(4, "TRIZ S.O.L.V.E.R Results (解決方案報告)")
    
    simulate_thinking("Querying Altshuller Matrix & Generating Report...")
    
    try:
        report = engine.solve_contradiction(improving_param.id, worsening_param.id)
        
        # Display Logic Log
        if RICH_AVAILABLE:
             log_text = "\n".join([f"> {l}" for l in report.execution_log])
             console.print(Panel(log_text, title="[bold blue]Matrix Lookup Trace[/bold blue]", border_style="blue"))
        
        console.print(f"\n[bold underline]Strategy Detected:[/bold underline] {report.strategy_note}\n")
        
        if RICH_AVAILABLE:
            table = Table(title=f"Suggested Inventive Principles for {sys_name}", box=box.ROUNDED)
            table.add_column("ID", justify="center", style="cyan", no_wrap=True)
            table.add_column("Principle Name (發明原則)", style="magenta")
            table.add_column("Description & Examples (說明與範例)")

            for p in report.suggested_principles:
                desc_md = f"{p.description}\n\n[dim]Example: {', '.join(p.examples)}[/dim]"
                table.add_row(str(p.id), p.name, desc_md)
            
            console.print(table)
        else:
            for p in report.suggested_principles:
                print(f"#{p.id} - {p.name}")
                print(f"   {p.description}")

    except Exception as e:
        console.print(f"[bold red]Error in calculation:[/bold red] {e}")

    # Phase 5: Ideality
    print_step_header(5, "Ideality Audit (理想度評估 - Optional)")
    if RICH_AVAILABLE:
        do_audit = Confirm.ask("Calculate Ideality Score?")
    else:
        do_audit = input("Calculate Ideality Score? (y/n): ").lower() == 'y'

    if do_audit:
        benefits = []
        costs_harms = []
        
        console.print("[cyan]Adding Benefits... (Value 1-10)[/cyan]")
        while True:
             if RICH_AVAILABLE:
                 name = Prompt.ask("Benefit Name (or enter to stop)")
             else:
                 name = input("Benefit Name (or enter to stop): ")
             
             if not name: break
             val = float(input("Value (1-10): "))
             benefits.append(IdealityFactor(name=name, weight=val))
        
        console.print("[magenta]Adding Costs/Harms... (Value 1-10)[/magenta]")
        while True:
             if RICH_AVAILABLE:
                 name = Prompt.ask("Cost/Harm Name (or enter to stop)")
             else:
                 name = input("Cost/Harm Name (or enter to stop): ")
             
             if not name: break
             val = float(input("Value (1-10): "))
             costs_harms.append(IdealityFactor(name=name, weight=val))
        
        score = engine.calculate_ideality(benefits, costs_harms, [])
        console.print(Panel(f"[bold green]Final Ideality Score: {score}[/bold green]", title="Ideality Result"))

if __name__ == "__main__":
    main()