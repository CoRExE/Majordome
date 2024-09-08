#  Copyright (c) 2024.
#  Ceci est une propriété de CoRExE, vous êtes autorisés à l'intégration de ce produit.
#  Il est formellement interdit de monétiser ce contenu.
#  Toute infraction aux règles précédemment citée pourra engager des poursuites.

import requests
import base64

# Define the URL and the payload to send.
webui_server_url = "http://127.0.0.1:7860"


def txt2img(prompt):
    url = f"{webui_server_url}/sdapi/v1/txt2img"
    payload = {
        "prompt": prompt,
        "negative_prompt": "ugly, blurry, low quality",
        "seed": -1,
        "steps": 20,
        "sampler_index": "Euler",
        "scheduler": "simple",
        "n_iter": 1,
        "batch_size": 1,
        "cfg_scale": 1,
        "distilled_cfg_scale": 3.5,
    }
    try:
        response = requests.post(url, json=payload)  # Envoyez directement le dictionnaire
        # response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
        r = response.json()
        if 'images' in r and r['images']:
            image_data = base64.b64decode(r['images'][0])
            return image_data
        else:
            print("Aucune image n'a été générée.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'appel à l'API : {e}")
        return None
