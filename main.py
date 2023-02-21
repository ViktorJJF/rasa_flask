from flask import Flask, request, jsonify, abort
from flask_cors import CORS, cross_origin
from rasa.core.agent import Agent, load_agent

# from rasa.core.tracker_store import retrieve,TrackerStore
from rasa.utils.endpoints import EndpointConfig
from rasa.model_training import train
from rasa.shared.core.events import SlotSet
import asyncio
import json
import sys
import shutil
import os

agents = {}

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

action_endpoint = "http://localhost:5055/webhook"


def get_agent(bot_id):
    agent = Agent.load(
        f"./models/{bot_id}.tar.gz", action_endpoint=EndpointConfig(url=action_endpoint)
    )
    # agent=load_agent(model_server="https://chatbotsqa.s3.amazonaws.com/333.tar.gz")
    # print(f"El agent: {agent}")
    # agent=Agent()
    # Guardamos agente cargado en memoria
    if agent:
        agents[bot_id] = agent
    return agent


async def process(agent, msg):
    output = await agent.handle_text(msg)
    print(output)
    return output


@app.route("/train", methods=["POST"])
def trainModel():
    bot_id = request.json["bot_id"]
    train(
        f"./bots/{bot_id}/domain.yml",
        f"./config.yml",
        f"./bots/{bot_id}/data",
        "./models",
        fixed_model_name=f"{bot_id}",
    )
    agent = get_agent(bot_id)
    # print("El resultado del training {}".format(trainingResult))
    print("Hecho!")
    return jsonify({"ok": True, "msg": f"Bot {bot_id} entrenado"})


@app.route("/base-skill", methods=["POST"])
def createBaseSkill():
    business_type = request.json["business_type"]
    bot_id = request.json["bot_id"]
    base = "./bots/base/"
    target = f"./bots/{bot_id}"
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copytree(base, target)
    return jsonify({"ok": True, "msg": f"Bot skill base para bot: {bot_id} creado"})


@app.route("/base-skill-trained", methods=["POST"])
def createBaseSkillTrained():
    business_type = request.json["business_type"]
    bot_id = request.json["bot_id"]
    base = "./bots/base/"
    target = f"./bots/{bot_id}"
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copytree(base, target)
    train(
        f"./bots/{bot_id}/domain.yml",
        f"./config.yml",
        f"./bots/{bot_id}/data",
        "./models",
        fixed_model_name=f"{bot_id}",
    )
    # load agent
    get_agent(bot_id)
    return jsonify(
        {"ok": True, "msg": f"Bot skill base para bot: {bot_id} creado y entrenado"}
    )


@app.route("/intents", methods=["GET"])
def listIntents():
    bot_id = request.json["bot_id"]
    train(
        f"./bots/{bot_id}/domain.yml",
        f"./config.yml",
        f"./bots/{bot_id}/data",
        "./models",
        fixed_model_name=f"{bot_id}",
    )
    # print("El resultado del training {}".format(trainingResult))
    print("Hecho!")
    return jsonify({"ok": True, "msg": f"Bot {bot_id} trainning"})


@app.route("/intents", methods=["POST"])
def createIntent():
    bot_id = request.json["bot_id"]
    train(
        f"./bots/{bot_id}/domain.yml",
        f"./config.yml",
        f"./bots/{bot_id}/data",
        "./models",
        fixed_model_name=f"{bot_id}",
    )
    # print("El resultado del training {}".format(trainingResult))
    print("Hecho!")
    return jsonify({"ok": True, "msg": f"Bot {bot_id} trainning"})


@app.route("/intents", methods=["PUT"])
def updateIntent():
    bot_id = request.json["bot_id"]
    train(
        f"./bots/{bot_id}/domain.yml",
        f"./config.yml",
        f"./bots/{bot_id}/data",
        "./models",
        fixed_model_name=f"{bot_id}",
    )
    # print("El resultado del training {}".format(trainingResult))
    print("Hecho!")
    return jsonify({"ok": True, "msg": f"Bot {bot_id} trainning"})


@app.route("/intents", methods=["DELETE"])
def deleteIntent():
    bot_id = request.json["bot_id"]
    train(
        f"./bots/{bot_id}/domain.yml",
        f"./config.yml",
        f"./bots/{bot_id}/data",
        "./models",
        fixed_model_name=f"{bot_id}",
    )
    # print("El resultado del training {}".format(trainingResult))
    print("Hecho!")
    return jsonify({"ok": True, "msg": f"Bot {bot_id} trainning"})


@app.route("/")
def home():
    return "Bot Running"


@app.route("/message", methods=["POST"])
@cross_origin(origin="*")
def new_message():
    if not request.json:
        abort(400)
    agent = request.json["bot_id"]
    print("El id: {}".format(agent))
    current_agent = agents[agent] if agent in agents else get_agent(agent)
    sender_id = request.json["sender_id"]
    tracker_store = current_agent.tracker_store
    tracker_state = tracker_store.get_or_create_tracker(sender_id)
    # print("El tracker store: {}".format(tracker_store))
    # print("El tracker state: {}".format(tracker_state))
    # ss = SlotSet('first_name', 'Alex')
    # print(f"El ss: {ss}")
    input = request.json["message"]
    # tracker_state.update(ss)
    # tracker_store.save(tracker_state)
    # res = (current_agent.handle_text(text_message=message, sender_id=user))
    message = asyncio.run(
        current_agent.handle_text(text_message=input, sender_id=sender_id)
    )
    parse_message = asyncio.run(current_agent.parse_message(input))
    # handle_message=asyncio.run(current_agent.handle_message(message=text))
    predict_next_for_sender_id = asyncio.run(
        current_agent.predict_next_for_sender_id(sender_id=sender_id)
    )
    # predict_next_with_tracker = current_agent.predict_next_with_tracker(
    #     tracker=tracker_state
    # )
    # log_message=asyncio.run(current_agent.log_message(input))
    # tracker=retrieve(sender_id)
    # print(f"tracker encontrado: {tracker}")
    # tracker = asyncio.run(current_agent.tracker_store.retrieve(user))
    # value = tracker.get_slot('specific_entity')
    # print("El tracker es {}".format(value))
    message = jsonify(
        {
            "message": message,
            # "predict_next_for_sender_id": predict_next_for_sender_id,
            "parse_message": parse_message,
            # "predict_next_with_tracker": predict_next_with_tracker,
        }
    )
    return message


if __name__ == "__main__":
    app.run(host="localhost", port=9000, debug=True, use_reloader=False)
