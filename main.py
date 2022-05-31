from flask import Flask, request, jsonify, abort
from flask_cors import CORS, cross_origin
from rasa.core.agent import Agent
from rasa.core.utils import EndpointConfig
import asyncio
import json
import sys

agents = {}

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

action_endpoint = "http://localhost:5055/webhook"


def agent_get(orgid):
    agents_org = {"agent_one": './models/20220506-094845-few-consulate.tar.gz',
                  "agent_two": './models/20220506-104057-crispy-narrative.tar.gz',
                  "agent_three": './models/20220520-143613-leather-onion.tar.gz',
                  "agent_four": './models/20220520-114224-brass-mode.tar.gz'}
    agent = Agent.load(
        agents_org[orgid], action_endpoint=EndpointConfig(action_endpoint))
    # Guardamos agente cargado en memoria
    if agent:
        agents[orgid] = agent
    return agent


async def process(agent, msg):
    output = await agent.handle_text(msg)
    print(output)
    return output


@app.route("/")
def home():
    return 'Bot Running'


@app.route('/message', methods=['POST'])
@cross_origin(origin='*')
def new_message():
    if not request.json:
        abort(400)
    orgId = request.args.get('orgId')
    print("El id: {}".format(orgId))
    current_agent = agents[orgId] if orgId in agents else agent_get(orgId)
    print("El agente actual: {}".format(current_agent))
    user = request.json['sender']
    text = request.json['message']
    # res = (current_agent.handle_text(text_message=message, sender_id=user))
    message = asyncio.run(current_agent.handle_text(text_message=text, sender_id=user))
    # parse_message=asyncio.run(current_agent.parse_message(message_data=text))
    # handle_message=asyncio.run(current_agent.handle_message(message=text))
    predict_next_for_sender_id=asyncio.run(current_agent.predict_next_for_sender_id(sender_id=user))
    # log_message=asyncio.run(current_agent.log_message(text))
    # tracker = asyncio.run(current_agent.tracker_store.retrieve(user))
    # value = tracker.get_slot('specific_entity')
    # print("El tracker es {}".format(value))
    message = jsonify({"message":message,"predict_next_for_sender_id":predict_next_for_sender_id})
    return message


if __name__ == '__main__':
    app.run(host='localhost', port=9000, debug=True, use_reloader=False)
