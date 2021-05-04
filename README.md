# PowerB - The most customizable Discord bot
> ## **Advantages**
> - One code style (*snake-case*)
> - Easy to use
> - Easy to customize
> - Easy to add functions
> - Unique and convenient system of functions
> - Demo-files and first functions
> 
> *and some more..*

<br><br>

## **How to start**
1) Clone repository into your folder using
- > git clone https://github.com/Flowseal/PowerB
2) Install required modules using
- > pip install -r requirements.txt
3) Change the **token** and **id** in file *config/setting.py*
4) Start the bot using file ***start.py***
<br><br>

## **How to customize functions**

* To add function create a .py file in *custom/* folder. **There is demo file (*demo.py*), that might help you with creating a function**
* Each file in *custom/* folder - group of functions (or one function)
* You dont need to import each function in custom folder, ***it will be imported automatically***
  <br><br>
## <a name="funcstruct"></a>**Function structure**
```python
@client.command(aliases = ['trigger'])
async def __trigger (ctx):
    # your function
    pass
```
**Where:**
> aliases =

List of commands to trigger function (in that case - *trigger*)

> pass

Your function structure

**Example:**

```python
@client.command(aliases = ['hello'])
async def __hello (ctx):
    await ctx.send('World!')
```
When user types *!hello* (! - prefix in config) bot will reply with message *World!*
<br><br>

## **How to add command in !help list**
**The bot provided with 2 in-build commands:**
- *!help* - user commands list
- *!ahelp* - admin commands list

**To add a command in each list follow this code:**

Add user command:
> settings.commands['Fun']['hello'] = 'Print hello world!'

Add admin command:
> settings.admin_commands['Fun']['set_hello'] = 'Set the greeting message'

*'Fun'* - the category, that will contain provided command

*'hello'* *'set_hello'* - command

= '..' - command description (will be printed with *command*_help)
<br><br>

## **How to add event in function**
To add event just create a default python function with event name

**Example:**
```python
# ping-pong reply (on_message - discord.py event name)
async def on_message(message):
    if (message.content == 'ping'):
        await message.channel.send('pong!')
```

**Supported events:**
> - on_ready
> - on_message
> - on_command_error
