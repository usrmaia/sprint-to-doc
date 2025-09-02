import src.config.logger
import logging

from agno.app.fastapi import FastAPIApp
from agents import task_agent, file_agent

api = FastAPIApp(agents=[task_agent, file_agent])
api.serve(app=api.get_app())
