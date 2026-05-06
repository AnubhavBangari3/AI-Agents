from google.adk.agents import LoopAgent, SequentialAgent

from .subagents.post_generator.agent import initial_post_generator
from .subagents.post_refiner.agent import post_refiner
from .subagents.post_reviewer.agent import post_reviewer


refinement_loop = LoopAgent(
    name="PostRefinementLoop",
    max_iterations=5,
    sub_agents=[
        post_reviewer,
        post_refiner,
    ],
)


root_agent = SequentialAgent(
    name="LinkedInPostGenerationPipeline",
    sub_agents=[
        initial_post_generator,
        refinement_loop,
    ],
)