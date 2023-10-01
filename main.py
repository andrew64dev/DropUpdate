# Hi!
# This is DropUpdate, a Open-Source Discord bot, written in Python.
# It can be used to reply to a message, since i saw no bots with this!
# Its very useful for like linking websites to your FAQ channel, or for a FAQ channel with all the options of the FAQ.

# PLEASE DON'T STEAL THIS CODE.
# You are free of Self Hosting this bot for your server, but please mention me (andrew64dev) as the creator.

# This code is a mess. I spent days on this.

import discord, json, random, requests, asyncio

bot = discord.Bot()
config = json.load(open('config.json', 'r'))

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
] # Why this? It is for the embed image check. If i spam verify that a image exist, i may get blocked, but with different user agents, its more difficult.

class EditEmbedModal(discord.ui.Modal):
    def __init__(self, panelID, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.panelID = str(panelID)

        self.add_item(discord.ui.InputText(label="Embed Title"))
        self.add_item(discord.ui.InputText(label="Embed Description", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Embed Thumbnail URL", style=discord.InputTextStyle.long, placeholder="Please insert a direct URL.", required=False))

    async def callback(self, i: discord.Interaction):

        with open('database.json', 'r') as f:
            r = json.load(f)

        ch = await bot.fetch_channel(int(r[str(i.guild.id)]['panels'][str(self.panelID)]['channelID']))
        
        imgURL = None

        if not self.children[2].value == None:
            try:
                headers = {'User-Agent': random.choice(user_agents)}
                req = requests.get(url=self.children[2].value, headers=headers)

                print(req.status_code)

                if not req.status_code in (200, 201, 202):
                    pass
                else:
                    imgURL = self.children[2].value
            except requests.exceptions.MissingSchema:
                imgURL = None

        r[str(i.guild.id)]['panels'][self.panelID] = { 'embed': { 'title': self.children[0].value, 'desc': self.children[1].value, 'imgURL': imgURL } }

        embed = discord.Embed()
        embed.title = r[str(i.guild.id)]['panels'][str(self.panelID)]['embed']['title']
        embed.description = r[str(i.guild.id)]['panels'][str(self.panelID)]['embed']['desc']
        embed.color = discord.Color.random()
        embed.set_footer(text='PanelID: ' + str(self.panelID))
        if not r[str(i.guild.id)]['panels'][str(self.panelID)]['embed']['imgURL'] == None:
            embed.set_thumbnail(url=r[str(i.guild.id)]['panels'][str(self.panelID)]['embed']['imgURL'])

        async for msg in ch.history(limit=None):
            if msg.author.id == 1155949276791316511 or msg.author.id == "1155949276791316511":
                try:
                    if msg.id == int(r[str(i.guild.id)]['panels'][str(self.panelID)]['msgID']):
                        await msg.edit(embed=embed)
                except: pass

class ConfigModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Embed Title"))
        self.add_item(discord.ui.InputText(label="Embed Description", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Embed Thumbnail URL", style=discord.InputTextStyle.long, placeholder="Please insert a direct URL.", required=False))

    async def callback(self, i: discord.Interaction):
        embed = discord.Embed()
        embed.title = "Processing data..."
        embed.description = "Please wait while the data is being processed..."
        embed.color = discord.Color.brand_red()
        embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/1156589425552277565.gif?size=96&quality=lossless')
        embed.set_footer(text='DropUpdate - Processing data...')

        await i.response.defer()
    
        await i.followup.edit_message(message_id=i.message.id, content=None, embed=embed, view=None)

        with open('database.json', 'r') as f:
            r = json.load(f)
        
        panelID = str(random.randint(10000000000, 999999999999))

        imgURL = None

        if not self.children[2].value == None:
            try:
                headers = {'User-Agent': random.choice(user_agents)}
                req = requests.get(url=self.children[2].value, headers=headers)

                print(req.status_code)

                if not req.status_code in (200, 201, 202):
                    pass
                else:
                    imgURL = self.children[2].value
            except requests.exceptions.MissingSchema:
                imgURL = None
                embed.description += "\n\n**The selected image will not show due to a error.**"
                await i.followup.edit_message(message_id=i.message.id, content=None, embed=embed, view=None)


        r[str(i.guild.id)]['panels'][panelID] = { 'panelID': panelID, 'contents': [], 'inserted': 1, 'insideContents': "", 'embed': { 'title': self.children[0].value, 'desc': self.children[1].value, 'imgURL': imgURL } }

        with open('database.json', 'w') as f:
            r = json.dump(r, f, indent=5)

        await i.followup.edit_message(message_id=i.message.id, embed=i.message.embeds[0], view=PanelConfiguration2(panelID=str(panelID)))

class AddOptionModal(discord.ui.Modal):
    def __init__(self, panelID, other: bool, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.panelID = str(panelID)
        self.other = other


        self.add_item(discord.ui.InputText(label="Embed Name"))
        self.add_item(discord.ui.InputText(label="Embed Description", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Embed Thumbnail URL", style=discord.InputTextStyle.long, placeholder="Please insert a direct URL.", required=False))
        self.add_item(discord.ui.InputText(label="Option Name"))
        self.add_item(discord.ui.InputText(label="Option Description"))

    async def callback(self, i: discord.Interaction):
        embed = discord.Embed()
        embed.title = "Processing data..."
        embed.description = "Please wait while the data is being processed..."
        embed.color = discord.Color.brand_red()
        embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/1156589425552277565.gif?size=96&quality=lossless')
        embed.set_footer(text='DropUpdate - Processing data...')

        await i.response.defer()

        try:

            await i.followup.edit_message(message_id=i.message.id, content=None, embed=embed, view=None)

        except: pass

        with open('database.json', 'r') as f:
            r = json.load(f)

        imgURL = None

        if not self.children[2].value == None:
            try:
                headers = {'User-Agent': random.choice(user_agents)}
                req = requests.get(url=self.children[2].value, headers=headers)

                print(req.status_code)

                if not req.status_code in (200, 201, 202):
                    pass
                else:
                    imgURL = self.children[2].value
            except requests.exceptions.MissingSchema:
                imgURL = None
                embed.description += "\n\n**The selected image will not show due to a error.**"
                try:
                    await i.followup.edit_message(message_id=i.message.id, content=None, embed=embed, view=None)
                except: pass

        r[str(i.guild.id)]['panels'][str(self.panelID)]['contents'].append({
            'title': self.children[0].value,
            'desc': self.children[1].value,
            'imgURL': imgURL,
            'optionName': self.children[3].value,
            'optionDesc': self.children[4].value
        })

        r[str(i.guild.id)]['panels'][str(self.panelID)]['insideContents'] += "x"

        if len(r[str(i.guild.id)]['panels'][str(self.panelID)]['insideContents']) == 25:
            try:
                await i.followup.edit_message(message_id=i.message.id, content='Options are MAX!\nGoing back to menu in 5 seconds...', embed=None, view=None)
                await asyncio.sleep(5)
                await i.followup.edit_message(message_id=i.message.id, content=None, embed=i.message.embeds[0], view=PanelConfiguration2(panelID=str(self.panelID)))
            except: pass

            if self.other:
                return await i.response.send_message('Options are MAX!')

            return

        with open('database.json', 'w') as f:
            json.dump(r, f, indent=5)

        try:

            await i.followup.edit_message(message_id=i.message.id, embed=i.message.embeds[0], view=PanelConfiguration2(panelID=str(self.panelID)))
        
        except: pass

        if self.other:
          ch = await bot.fetch_channel(int(r[str(i.guild.id)]['panels'][str(self.panelID)]['channelID']))

          async for msg in ch.history(limit=None):
            if msg.author.id == 1155949276791316511 or msg.author.id == "1155949276791316511":
                  try:
                      if msg.id == int(r[str(i.guild.id)]['panels'][str(self.panelID)]['msgID']):
                        await msg.edit(view=OptionsHandler(guildID=i.guild.id, panelID=self.panelID))
                  except: pass
            
            


guildID2 = 1
panelID2 = 1

class OptionsHandler(discord.ui.View):

    def __init__(self, guildID = None, panelID = None):

        super().__init__(timeout=None)

        try:
            
            global guildID2, panelID2

            self.guildID = None       
            self.panelID = None     

            async def select_callback(i: discord.Interaction):
                global guildID2, panelID2
                guildID2 = i.guild.id
                panelID2 = str(i.message.embeds[0].footer.text).replace('PanelID: ', '')

                selected = panel.values[0]

                r = json.load(open('database.json', 'r'))

                result = None
                
                for item in r[str(guildID2)]['panels'][str(panelID2)]['contents']:
                    if str(item['optionName']) == str(selected):
                        result = item
                        break

                embed = discord.Embed()
                embed.title = result['title']
                embed.description = result['desc']
                if not result['imgURL'] == None: embed.set_thumbnail(url=result['imgURL'])
                embed.color = discord.Color.random()
                embed.set_footer(text='DropUpdate - Panel')

                await i.response.send_message(embed=embed, ephemeral=True)


            if self.guildID == None:
                guildID2 = guildID
            else:
                guildID2 = self.guildID

            if self.panelID == None:
                panelID2 = panelID
            else:
                panelID2 = self.panelID
            
            print(guildID2)

            panelID2 = json.load(open('database.json', 'r'))[str(guildID2)]['panels'][str(panelID2)]['panelID']

            self.panelID = panelID2

            options = []

            for x in json.load(open('database.json', 'r'))[str(guildID2)]['panels'][str(panelID2)]['contents']:
                name = x['optionName']
                dsc = x['optionDesc']
                options.append( discord.SelectOption(label=name, description=dsc) )

            panel = discord.ui.Select(
                placeholder="Select a option.",
                min_values=1,
                max_values=1,
                options=options,
                custom_id="panel"
            )

            panel.callback = select_callback

            OptionsHandler.add_item(self, item=panel)


        
        except TypeError as e:
            print('TypeError: ', e)

class PanelConfiguration2(discord.ui.View):
    def __init__(self, panelID):
        super().__init__(timeout=None)
        self.panelID = str(panelID)

    @discord.ui.button(label="Create message", custom_id="create-message", style=discord.ButtonStyle.blurple, emoji="<:eyes:1156310608204005506>", disabled=True)
    async def create_message_callback(self, button, i: discord.Interaction):

        await i.response.send_message('FAIL!', ephemeral=True)

    @discord.ui.button(label="Add a option", custom_id="add-option", style=discord.ButtonStyle.green, emoji="<:up:1156316069024243863>")
    async def add_option_callback(self, button, i: discord.Interaction):
        print(self.panelID)
        await i.response.send_modal(AddOptionModal(panelID=self.panelID, title='Add a option', other=False))

    @discord.ui.button(label="Send panel", custom_id="send-panel", style=discord.ButtonStyle.grey, emoji="<:sendmsg:1156631661610541147>")
    async def send_panel_callback(self, button, i: discord.Interaction):
        

        async def dropdowncallback(i2: discord.Interaction):

            with open('database.json', 'r') as f:
                r = json.load(f)

            embed2 = discord.Embed()
            embed2.title = "Processing data..."
            embed2.description = "Please wait while the data is being processed..."
            embed2.color = discord.Color.brand_red()
            embed2.set_thumbnail(url='https://cdn.discordapp.com/emojis/1156589425552277565.gif?size=96&quality=lossless')
            embed2.set_footer(text='DropUpdate - Processing data...')

            await i.followup.edit_message(message_id=i.message.id, content=None, embed=embed2, view=None)

            embed = discord.Embed()
            embed.title = r[str(i.guild.id)]['panels'][str(self.panelID)]['embed']['title']
            embed.description = r[str(i.guild.id)]['panels'][str(self.panelID)]['embed']['desc']
            embed.color = discord.Color.random()
            embed.set_footer(text='PanelID: ' + str(self.panelID))
            if not r[str(i.guild.id)]['panels'][str(self.panelID)]['embed']['imgURL'] == None:
                embed.set_thumbnail(url=r[str(i.guild.id)]['panels'][str(self.panelID)]['embed']['imgURL'])


            thing = dropdown.values[0]

            ch = await bot.fetch_channel(int(thing.id))

            msg = await ch.send(embed=embed, view=OptionsHandler(guildID=i.guild.id, panelID=self.panelID))   
            
            r[str(i.guild.id)]['panels'][str(self.panelID)]['msgID'] = str(msg.id)
            r[str(i.guild.id)]['panels'][str(self.panelID)]['channelID'] = str(ch.id)

          
            with open('database.json', 'w') as f:
                json.dump(r, f, indent=5)

            embed = discord.Embed()
            embed.title = "Panel created!"
            embed.description = "You just created a panel!\nYou can add more options by using /addoption.\nPanelID: " + str(self.panelID) + "\nYou can also see the panel ID directly from the embed footer."
            embed.color = discord.Color.brand_green()
            embed.set_footer(text="DropUpdate - Panel configuration")
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1155950681476309093.webp?size=96&quality=lossless")

            await i.followup.edit_message(message_id=i.message.id, content=None, embed=embed, view=None)


        with open('database.json', 'r') as f:
            r = json.load(f)
        
        if r[str(i.guild.id)]['panels'][str(self.panelID)]['insideContents'] == "":
            await i.followup.edit_message(message_id=i.message.id, content='No options!\nGoing back to menu in 5 seconds...', embed=None, view=None)
            await asyncio.sleep(5)
            await i.followup.edit_message(message_id=i.message.id, content=None, embed=i.message.embeds[0], view=PanelConfiguration2(panelID=str(self.panelID)))
            return

        embed = discord.Embed()
        embed.title = 'Send panel'
        embed.description = "Select a channel where to send the Panel that you just created."
        embed.color = discord.Color.yellow()
        embed.set_footer(text='DropUpdate - Panel configuration')
        embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/1156631661610541147.webp?size=96&quality=lossless')

        dropdown = discord.ui.Select(
            placeholder = "Select a channel",
            min_values=1,
            max_values=1,
            select_type=discord.ComponentType.channel_select,
            channel_types=[discord.ChannelType.text]
        )

        view = discord.ui.View()
        view.add_item(dropdown)
        dropdown.callback = dropdowncallback

        await i.response.edit_message(content=None, embed=embed, view=view)


class PanelConfiguration(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create message", custom_id="create-message", style=discord.ButtonStyle.blurple, emoji="<:eyes:1156310608204005506>")
    async def create_message_callback(self, button, i: discord.Interaction):

        await i.response.send_modal(ConfigModal(title='DropUpdate - Panel Configuration'))

    @discord.ui.button(label="Add a option", custom_id="add-option", style=discord.ButtonStyle.green, emoji="<:up:1156316069024243863>", disabled=True)
    async def add_option_callback(self, button, i: discord.Interaction):
        await i.response.send_message('FAIL!', ephemeral=True)
    
    @discord.ui.button(label="Send panel", custom_id="send-panel", style=discord.ButtonStyle.grey, emoji="<:sendmsg:1156631661610541147>", disabled=True)
    async def send_panel_callback(self, button, i: discord.Interaction):
        await i.response.send_message('FAIL!', ephemeral=True)

@bot.slash_command(description='Create a new panel.')
async def create(ctx: discord.ApplicationContext):

    if not ctx.author.guild_permissions.manage_guild:
        embed = discord.Embed()
        embed.title = "Missing Permissions"
        embed.description = "You are missing the Manage Server permission, so you cant create a new panel."
        embed.color = discord.Color.red()
        embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/1155950683598622891.webp?size=96&quality=lossless')
        return await ctx.respond(embed=embed, ephemeral=True)

    embed = discord.Embed()
    embed.title = "Create a new panel"
    embed.description = "Please create a new panel using the buttons below."
    embed.set_footer(text="DropUpdate - Panel Configuration")
    embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/1155951768044326933.webp?size=96&quality=lossless')
    embed.color = discord.Color.blurple()

    await ctx.respond(embed=embed, view=PanelConfiguration(), ephemeral=True)

@bot.slash_command(description='Add a option to a existing panel.')
async def add(ctx: discord.ApplicationContext, panelid: discord.Option(int, "The Panel ID.", required=True)):

    if not ctx.author.guild_permissions.manage_guild:
        embed = discord.Embed()
        embed.title = "Missing Permissions"
        embed.description = "You are missing the Manage Server permission, so you cant create a new panel."
        embed.color = discord.Color.red()
        embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/1155950683598622891.webp?size=96&quality=lossless')
        return await ctx.respond(embed=embed, ephemeral=True)

    await ctx.response.send_modal(AddOptionModal(title="Add a option", panelID=str(panelid), other=True))

@bot.slash_command(description='Remove a option from a existing panel.')
async def remove(ctx: discord.ApplicationContext, panelid: discord.Option(int, "The Panel ID.", required=True)):

    if not ctx.author.guild_permissions.manage_guild:
        embed = discord.Embed()
        embed.title = "Missing Permissions"
        embed.description = "You are missing the Manage Server permission, so you cant create a new panel."
        embed.color = discord.Color.red()
        embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/1155950683598622891.webp?size=96&quality=lossless')
        return await ctx.respond(embed=embed, ephemeral=True)

    with open('database.json', 'r') as f:
        r = json.load(f)

    async def selectcallback(i: discord.Interaction):

        option = select.values[0]

        embed = discord.Embed()
        embed.title = "Option dropped!"
        embed.description = "Option `" + str(option) + "` has been dropped from your panel!"
        embed.color = discord.Color.brand_red()
        embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/1155950683598622891.webp?size=96&quality=lossless')
        embed.set_footer(text="DropUpdate - Panel Configuration")
        
        for x in r[str(i.guild.id)]['panels'][str(panelid)]['contents']:
            print(x)
            if str(x['optionName']) == str(option):
                r[str(i.guild.id)]['panels'][str(panelid)]['contents'].remove(x)
                break
        r[str(i.guild.id)]['panels'][str(panelid)]['insideContents'][:-1]
      
        with open('database.json', 'w') as f:
            json.dump(r, f, indent=5)

        ch = await bot.fetch_channel(int(r[str(i.guild.id)]['panels'][str(panelid)]['channelID']))
      
        async for msg in ch.history(limit=None):
            if msg.author.id == 1155949276791316511 or msg.author.id == "1155949276791316511":
                  try:
                      if msg.id == int(r[str(i.guild.id)]['panels'][str(panelid)]['msgID']):
                        await msg.edit(view=OptionsHandler(guildID=i.guild.id, panelID=panelid))
                  except: pass
      
        await i.response.edit_message(embed=embed, view=None)
    
    options = [ discord.SelectOption( label=x['optionName'], description=x['optionDesc'] ) for x in r[str(ctx.guild.id)]['panels'][str(panelid)]['contents'] ] # alr MAYBE this time i made it difficult :) sorry i like one line stuff

    select = discord.ui.Select(
        placeholder = "Select a option to drop...",
        min_values=1,
        max_values=1,
        options = options
    )

    select.callback = selectcallback

    view = discord.ui.View()
    view.add_item(select)

    await ctx.respond(view=view, ephemeral=True)

@bot.slash_command(description="Edit a Panel Embed")
async def editpanel(ctx: discord.ApplicationContext, panelid: discord.Option(int, 'The Panel ID.', required=True)):

    if not ctx.author.guild_permissions.manage_guild:
        embed = discord.Embed()
        embed.title = "Missing Permissions"
        embed.description = "You are missing the Manage Server permission, so you cant create a new panel."
        embed.color = discord.Color.red()
        embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/1155950683598622891.webp?size=96&quality=lossless')
        return await ctx.respond(embed=embed, ephemeral=True)

    await ctx.response.send_message(EditEmbedModal(panelID=panelid))

@bot.event
async def on_guild_join(guild: discord.Guild):
    with open('database.json', 'r') as f:
        r = json.load(f)
    
    r[str(guild.id)] = { 'panels': { }, 'serverID': str(guild.id) }

    with open('database.json', 'w') as f:
        json.dump(r, f, indent=5)

@bot.event
async def on_ready():
    bot.add_view(PanelConfiguration())
    bot.add_view(PanelConfiguration2(panelID=None))
    bot.add_view(OptionsHandler(guildID=1, panelID=1))
    print('OK')
    await bot.change_presence(activity=discord.Game(name='Updating your messages!'))
    while True:
      await bot.change_presence(activity=discord.Game(name='Updating your messages!'))
      await asyncio.sleep(5)
      await bot.change_presence(activity=discord.Game(name='Keeping track of your panels!'))

bot.run(config['token'])