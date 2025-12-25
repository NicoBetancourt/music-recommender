from pydantic_ai import Agent, AgentRunResult
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from src.agents.prompts import system_prompt
from src.core.config import settings
from src.domain.schemas.song import SongFeatures


class SongFeaturesAgent:
    def __init__(self):
        provider = GoogleProvider(api_key=settings.GOOGLE_API_KEY)
        model = GoogleModel(settings.MODEL, provider=provider)
        self.agent = Agent(
            system_prompt=system_prompt,
            model=model,
            output_type=SongFeatures,
        )

    async def __call__(
        self,
        input: str,
    ) -> AgentRunResult[SongFeatures]:
        answer: SongFeatures = await self.agent.run(input)
        return answer.output
