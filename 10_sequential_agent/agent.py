from google.adk.agents import SequentialAgent

from .subagents.validator.agent import lead_validator_agent
from .subagents.scorer.agent import lead_scorer_agent
from .subagents.recommender.agent import action_recommender_agent


root_agent = SequentialAgent(
    name="LeadQualificationPipeline",
    sub_agents=[
        lead_validator_agent,
        lead_scorer_agent,
        action_recommender_agent,
    ],
    description="Pipeline that validates, scores and recommends actions for leads",
)