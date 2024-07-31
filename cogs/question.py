import nextcord

import config
from cogs.base import BaseCog


class QuestionCog(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

    @nextcord.slash_command(
        name="вопрос",
        description="Задать анонимный вопрос",
        guild_ids=[config.GUILD_ID],
    )
    async def question_command(self, interaction: nextcord.Interaction):
        form = nextcord.ui.Modal(title="Задайте ваш вопрос")
        form.add_item(
            nextcord.ui.TextInput(
                label="Спросите то, что вас интересует",
                placeholder="Ваш текст...",
            )
        )
        form.callback = self._get_question_callback

        await interaction.response.send_modal(form)

    async def _get_question_callback(self, interaction: nextcord.Interaction):
        response = interaction.data["components"][0]["components"][0]["value"]

        channel: nextcord.TextChannel = self.bot.get_channel(config.PRIVATE_CHANNEL_ID)

        embed = nextcord.Embed(
            title="Новый анонимный вопрос",
            color=nextcord.Color.yellow(),
            description=response,
        )

        answer_cog = self.bot.get_cog("Answer")
        view = answer_cog.create_question_view()

        await interaction.send(
            content="Вопрос успешно отправлен! Ответ будет опубликован тут <#1267777121066029089>.\n"
            "*Ваш вопрос может быть пропущен, если он нарушал правила публикации или правила сервера.*",
            delete_after=10,
            ephemeral=True,
        )
        await channel.send(embed=embed, view=view)


def setup(bot):
    bot.add_cog(QuestionCog(bot))
