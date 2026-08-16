import discord
from discord.ext import commands
from discord.ui import Button, View

# Configuração de intenções
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Lista em memória para armazenar as pessoas que clicaram no botão
lista_participantes = set()


def tem_permissao(ctx):
    # Verifica se o usuário tem permissão de Administrador
    return ctx.author.guild_permissions.administrator


# Classe da Interface com o Botão
class EventoView(View):

    def __init__(self):
        super().__init__(timeout=None)  # O botão não expira automaticamente

    @discord.ui.button(
        label="Participar do Evento",
        style=discord.ButtonStyle.green,
        custom_id="btn_event_join",
    )
    async def entrar_evento(
        self, interaction: discord.Interaction, button: Button
    ):
        usuario = interaction.user

        if usuario.id in lista_participantes:
            await interaction.response.send_message(
                "Você já está na lista!", ephemeral=True
            )
        else:
            lista_participantes.add(usuario.id)
            await interaction.response.send_message(
                f"✅ {usuario.mention}, você entrou no evento!",
                ephemeral=True,
            )


@bot.event
async def on_ready():
    print(f"✅ Bot conectado com sucesso como: {bot.user.name}")


# Comando para abrir a inscrição do evento
@bot.command(name="eventjoin")
async def event_join(ctx):
    if not tem_permissao(ctx):
        await ctx.send("❌ Você não tem permissão para usar este comando.")
        return

    view = EventoView()
    await ctx.send(
        "📢 **Inscrições Abertas para o Evento!**\nClique no botão abaixo para garantir sua vaga:",
        view=view,
    )


# Comando para listar quem clicou no botão
@bot.command(name="eventlist")
async def event_list(ctx):
    if not tem_permissao(ctx):
        await ctx.send("❌ Você não tem permissão para usar este comando.")
        return

    if not lista_participantes:
        await ctx.send("📋 A lista do evento está vazia no momento.")
        return

    membros_mencionados = [f"<@{user_id}>" for user_id in lista_participantes]
    lista_str = "\n".join(membros_mencionados)

    embed = discord.Embed(
        title="📋 Lista de Participantes do Evento",
        description=lista_str,
        color=discord.Color.blue(),
    )
    embed.set_footer(text=f"Total: {len(lista_participantes)} participantes")

    await ctx.send(embed=embed)


TOKEN = "MTUzODU1ODIyNjkxMDU1MjE0NA.GveyyO.gqPVghxRWxwCBuJoZaSBmcmOHb48OQUCpD4l3g"

bot.run(TOKEN)