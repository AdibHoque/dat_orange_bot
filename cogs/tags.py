from discord.ext import commands


class Tags:
    def __init__(self, bot):
        self.bot = bot

    async def get_all_tags(self, author: int):
        return await self.bot.r.table('tags') \
            .get(str(author)) \
            .without('id') \
            .default({}) \
            .run(self.bot.connection)

    async def get_tag(self, author: int, tag: str):
        return (await self.get_all_tags(author)).get(tag, None)

    async def create_tag(self, author: int, tag_name: str, tag_content: str):
        await self.bot.r.table('tags') \
            .insert({'id': str(author), tag_name: tag_content}, conflict='update') \
            .run(self.bot.connection)

    async def delete_tag(self, author: int, tag_name: str):
        tags = await self.get_all_tags(author)
        tags.pop(tag_name)
        tags.update({'id': str(author)})

        await self.bot.r.table('tags') \
            .insert(tags, conflict='update') \
            .run(self.bot.connection)

    @commands.group(aliases=['tags'], invoke_without_command=True)
    async def tag(self, ctx, *, tag_name: str=None):
        """ Create tags unique to you
        Specify tag_name to view a tag
        """
        if not ctx.invoked_subcommand and not tag_name:
            _help = await self.bot.formatter.format_help_for(ctx, ctx.command)

            for page in _help:
                await ctx.send(page)
        elif tag_name:
            tag = await self.get_tag(ctx.author.id, tag_name)

            if not tag:
                return await ctx.send('No tags created by you found matching that name.')
            else:
                await ctx.send(tag)

    @tag.command()
    async def create(self, ctx, tag_name: str, *, tag_content: commands.clean_content(fix_channel_mentions=True)):
        """ Create a tag """
        tag = await self.get_tag(ctx.author.id, tag_name)

        if tag:
            return await ctx.send('Cannot overwrite tags. Use the `edit` command to modify existing tags.')

        if tag_name == 'id':
            return await ctx.send('Tags cannot be named `id` as it is a reserved name.')

        await self.create_tag(ctx.author.id, tag_name, tag_content)
        await ctx.send('Tag created successfully!')

    @tag.command()
    async def edit(self, ctx, tag_name: str, *, tag_content: commands.clean_content(fix_channel_mentions=True)):
        """ Edits an existing tag """
        tag = await self.get_tag(ctx.author.id, tag_name)

        if not tag:
            return await ctx.send('No tags found matching that name. Create tags with the `create` command.')

        await self.delete_tag(ctx.author.id, tag_name)
        await self.create_tag(ctx.author.id, tag_name, tag_content)
        await ctx.send('Tag edited successfully!')

    @tag.command()
    async def remove(self, ctx, *, tag_name: str):
        """ Removes a tag you created """
        tag = await self.get_tag(ctx.author.id, tag_name)

        if not tag:
            return await ctx.send('No tags found matching that name.')

        await self.delete_tag(ctx.author.id, tag_name)
        await ctx.send('Tag removed successfully!')

    @tag.command(name='list')
    async def list_tags(self, ctx):
        """ Lists all tags created by you """
        tags = await self.get_all_tags(ctx.author.id)

        if not tags:
            return await ctx.send('You don\'t have any tags')

        names = sorted(list(tags.keys()), key=str.lower)
        names = ', '.join(names)
        await ctx.send(f'**{len(tags)} tags**\n```\n{names}```')


def setup(bot):
  bot.add_cog(Tags(bot))
