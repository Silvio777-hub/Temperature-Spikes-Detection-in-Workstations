import sys
import os
from src.cli.parser import create_parser
from src.cli.commands import handle_status, handle_train, handle_diagnose

# Re-import monitor from original logic or updated modular one
# For now, we'll keep the monitor function here or move to a dedicated module

def run_monitor(args):
    # This will be the main entry point for the dashboard
    # Importing it here avoids circular dependencies
    from src.ui.terminal_display import TerminalDisplay
    # (Existing monitor logic from previous main.py)
    pass

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    if args.command == "status":
        handle_status()
    elif args.command == "train":
        handle_train(args)
    elif args.command == "diagnose":
        handle_diagnose()
    elif args.command == "monitor":
        from src.monitor import run_monitoring_loop
        run_monitoring_loop(use_ml=args.use_ml)
    elif args.command == "stress":
        from src.stress import run_stress
        run_stress(args.duration, args.cores)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
