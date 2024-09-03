from jigsawstack import JigsawStack, JigsawStackError as err
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('JIGSAW_STACK_API_KEY')
jigsawstack = JigsawStack(api_key)

def jss_create_prompt(prompt):
    res = jigsawstack.prompt_engine.create(prompt)
    prompt_engine_id = res["prompt_engine_id"]
    
    return prompt_engine_id

def jss_delete_prompts():
    prompt_dict = jigsawstack.prompt_engine.list()
    prompts = prompt_dict["prompt_engines"]
    for p in prompts:
        jigsawstack.prompt_engine.delete(p["id"])

def jss_create_params(context, init_value, return_prompt):
    params = {
    "prompt": "Use this interview " + context  + "to answer questions {about}" ,
    "inputs": [
        {
            "key": "about",
            "optional": False,
            "initial_value": init_value,
        },
    ],
    "return_prompt": return_prompt,
    }

    return params

def jss_run_prompt(prompt):
    completion = jigsawstack.prompt_engine.run(prompt)

    return completion

def set_prompt(prompt_id, input):
    prompt = {
        "id": prompt_id,
        "input_values": {
            "about": input,
        }
    }
    
    return prompt


    