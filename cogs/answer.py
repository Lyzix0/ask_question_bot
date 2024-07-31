import asyncio

import nextcord

import config
from cogs.base import BaseCog


class Answer(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.questions_data = {}

    def create_question_view(self):
        answer_button = nextcord.ui.Button(label="Ответить")
        answer_button.callback = self.answer_question_callback

        skip_button = nextcord.ui.Button(label="Пропустить")
        skip_button.callback = self.skip_callback

        view = nextcord.ui.View(timeout=None)
        view.add_item(answer_button)
        view.add_item(skip_button)
        return view

    async def skip_callback(self, interaction: nextcord.Interaction):
        original_embed = interaction.message.embeds[0]

        new_embed = nextcord.Embed(
            title="Вопрос пропущен",
            description=original_embed.description,
            color=nextcord.Color.red(),
        )

        await interaction.message.edit(embed=new_embed, view=None)
        await interaction.response.defer()

    async def answer_question_callback(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(
            "Пожалуйста, напишите свой ответ на вопрос.", ephemeral=True
        )

        def check(message):
            return (
                message.author == interaction.user
                and message.channel == interaction.channel
            )

        question = interaction.message.embeds[0].description
        try:
            response = await self.bot.wait_for("message", check=check, timeout=40)

        except asyncio.TimeoutError:
            await interaction.followup.send(
                "Вы не ответили на вопрос вовремя. Попробуйте еще раз", ephemeral=True
            )
            return

        user_answer = response.content
        self.questions_data[question] = user_answer

        cancel_button = nextcord.ui.Button(
            label="Отменить", style=nextcord.ButtonStyle.danger
        )
        cancel_button.callback = self.cancel_callback

        send_button = nextcord.ui.Button(
            label="Отправить", style=nextcord.ButtonStyle.green
        )
        send_button.callback = lambda q: self.send_question_answer(
            interaction, question
        )

        view = nextcord.ui.View()
        view.add_item(send_button)
        view.add_item(cancel_button)

        await interaction.followup.send(
            f"Ваш ответ: {user_answer}", ephemeral=True, view=view
        )

    async def cancel_callback(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(
            "Вы отменили ответ на вопрос.", ephemeral=True
        )
        await interaction.message.edit(view=None)

    async def send_question_answer(self, interaction: nextcord.Interaction, question):
        public_channel = self.bot.get_channel(config.PUBLIC_CHANNEL_ID)

        question_embed = nextcord.Embed(
            title="Анонимный вопрос",
            description=f"*{question}*",
            color=nextcord.Colour.from_rgb(43, 45, 49),
        )

        answer_embed = nextcord.Embed(
            title="Ответ от ХАОС",
            description=f"*{self.questions_data[question]}*",
            color=nextcord.Colour.blue(),
        )

        await public_channel.send(embed=question_embed)
        answer_message = await public_channel.send(embed=answer_embed)

        emoji = nextcord.PartialEmoji(name="emodziorvoteyes", id=1103737252909162506)
        await answer_message.add_reaction(emoji)


def setup(bot):
    bot.add_cog(Answer(bot))
