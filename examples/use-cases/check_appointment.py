import asyncio
import os

import dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, SecretStr

from browser_use.agent.service import Agent
from browser_use.controller.service import Controller

dotenv.load_dotenv()


controller = Controller()


class WebpageInfo(BaseModel):
	link: str = 'https://appointment.mfa.gr/en/reservations/aero/ireland-grcon-dub/'


@controller.action('Go to the webpage', param_model=WebpageInfo)
def go_to_webpage(webpage_info: WebpageInfo):
	return webpage_info.link


async def main():
	task = (
		'Go to the Greece MFA webpage via the link I provided you.'
		'Check the visa appointment dates. If there is no available date in this month, check the next month.'
		'If there is no available date in both months, tell me there is no available date.'
	)
	print(os.getenv('DEEPSEEK_API_KEY', ''))
	model = ChatOpenAI(base_url='https://api.deepseek.com/v1', model="deepseek-reasoner", api_key=SecretStr(os.getenv('DEEPSEEK_API_KEY', '')))
	agent = Agent(task, model, controller=controller, use_vision=False)

	try:
		result = await agent.run()
	except Exception as e:
		print(f"An error occurred: {e}")
		return


if __name__ == '__main__':
	asyncio.run(main())
