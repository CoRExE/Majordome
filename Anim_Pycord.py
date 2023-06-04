import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from io import BytesIO
import datetime
from BotExtentions.addPack import jeton

# Importer la bibliothèque PyCord
import discord

# Définir les adresses IP
client_ip = '192.168.1.100'
server_ip = '10.0.0.2'

# Définir les ports
client_port = '8080'
server_port = '80'

# Créer un objet figure
fig, ax = plt.subplots()

# Définir les labels pour les ports et les adresses IP
labels = [f'{client_ip}:{client_port} (Client)', f'{server_ip}:{server_port} (Server)']

# Définir les positions des ports et des adresses IP sur l'axe X
x_pos = [0, 1]

# Dessiner les ports et les adresses IP sur le graphique
bar_plot = ax.bar(x_pos, [1, 1], align='center')
ax.set_xticks(x_pos)
ax.set_xticklabels(labels)
ax.set_ylabel('Port Forwarding')


# Fonction qui anime les barres du graphique
def animate(frame):
    # Déplacer la barre de gauche vers la droite
    bar_plot[0].set_height(0)
    bar_plot[1].set_height(1)
    bar_plot[0].set_x(frame / 100)
    bar_plot[1].set_x(frame / 100 + 1)
    return bar_plot


# Créer l'animation
animation = FuncAnimation(fig, animate, frames=100, repeat=True)

# Enregistrer l'animation sous forme d'image
buffer = BytesIO()
fig.savefig(buffer, format='png')
buffer.seek(0)

# Créer un bot Discord avec PyCord
bot = discord.Client()


# Définir une fonction pour envoyer l'image animée sur Discord
async def send_animation():
    # Ouvrir le buffer contenant l'image
    buffer.seek(0)
    # Créer un fichier Discord à partir de l'image
    file = discord.File(buffer, filename='animation.png')
    # Envoyer le fichier sur un canal Discord
    channel = await bot.fetch_channel("948675434428645446")
    await channel.send(file=file)


# Se connecter au bot Discord
@bot.event
async def on_ready():
    print('Bot connected.')
    # Envoyer l'animation toutes les 10 secondes
    while True:
        await send_animation()
        await discord.utils.sleep_until(datetime.datetime.now() + datetime.timedelta(seconds=10))


bot.run(jeton)
