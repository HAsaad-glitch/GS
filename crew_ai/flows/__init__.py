"""CrewAI Workflow Definitions.

This module contains flows that coordinate multiple crews into cohesive workflows.
"""

from GS.crew_ai.flows.data_analysis_flow import run_flow_analysis, plot_flow

__all__ = ["run_flow_analysis", "plot_flow"] 