from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import sys
import os

sys.path.append(os.path.abspath("./"))

from src.game_version_v1.tools.image_generation_tool import ImageGenerationTool 

@CrewBase
class GameVersionV1():
    """GameVersionV1 crew"""

    agents_config = '../config/agents.yaml'
    tasks_config = '../config/tasks.yaml'

    @agent
    def game_logic_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['game_logic_agent'],
            model=self.agents_config['game_logic_agent']['model'],
            verbose=False
        )

    @agent
    def ui_ux_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["ui_ux_agent"],
            model=self.agents_config["ui_ux_agent"]["model"],
            verbose=False
        )

    @agent
    def user_input_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["user_input_agent"],
            model=self.agents_config["user_input_agent"]["model"],
            verbose=False
        )

    @agent
    def code_integrator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["code_integrator_agent"],
            model=self.agents_config["code_integrator_agent"]["model"],
            verbose=False
        )

    @agent
    def tester_debugger_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["tester_debugger_agent"],
            model=self.agents_config["tester_debugger_agent"]["model"],
            verbose=False
        )

    @agent
    def image_asset_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["image_asset_agent"],
            model=self.agents_config["image_asset_agent"]["model"],
            tools=[ImageGenerationTool()],
            verbose=False
        )

    @agent
    def asset_integration_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["asset_integration_agent"],
            model=self.agents_config["asset_integration_agent"]["model"],
            verbose=False
        )

    @task
    def generate_game_logic(self) -> Task:
        return Task(
            config=self.tasks_config["generate_game_logic"],
        )

    @task
    def design_ui_ux(self) -> Task:
        return Task(
            config=self.tasks_config["design_ui_ux"],
        )
    
    @task
    def handle_input_controls(self) -> Task:
        return Task(
            config=self.tasks_config["handle_input_controls"],
        )

    @task
    def generate_visual_assets(self) -> Task:
        return Task(
            config=self.tasks_config["generate_visual_assets"],
        )

    @task
    def integrate_assets(self) -> Task:
        return Task(
            config=self.tasks_config["integrate_assets"],
        )
    
    @task
    def integrate_code_modules(self) -> Task:
        return Task(
            config=self.tasks_config["integrate_code_modules"],
        )
    
    @task
    def test_and_debug_game(self) -> Task:
        return Task(
            config=self.tasks_config["test_and_debug_game"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GameVersionV1 crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,    # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=False,
        )
