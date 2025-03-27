#!/usr/bin/env python
"""
Command-line interface for CrewAI flows visualization.
"""

import argparse
import os
from GS.crew_ai.flows import plot_flow

def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(description='CrewAI flow visualization tools')
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Visualization command
    visualize_parser = subparsers.add_parser('visualize', help='Generate a visualization of a flow')
    visualize_parser.add_argument('--flow', choices=['analysis'], default='analysis',
                                help='The flow to visualize')
    visualize_parser.add_argument('--output', type=str, default=None,
                                help='Output file name (without extension)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'visualize':
        output_file = args.output or f"{args.flow}_flow"
        
        if args.flow == 'analysis':
            # Generate the visualization
            path = plot_flow(output_file=output_file)
            print(f"Flow visualization created at: {path}")
            
            # Try to open the visualization in a browser if it's a local file
            if path and os.path.exists(path) and path.endswith('.html'):
                try:
                    import webbrowser
                    print("Opening visualization in web browser...")
                    webbrowser.open(f"file://{os.path.abspath(path)}")
                except Exception as e:
                    print(f"Could not open the browser: {e}")
            else:
                print(f"Looking for visualization at current directory: {os.path.abspath('.')}")
                default_path = f"{output_file}.html"
                if os.path.exists(default_path):
                    try:
                        import webbrowser
                        print(f"Found at {default_path}. Opening in web browser...")
                        webbrowser.open(f"file://{os.path.abspath(default_path)}")
                    except Exception as e:
                        print(f"Could not open the browser: {e}")
                else:
                    print(f"Could not locate the visualization file.")
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 