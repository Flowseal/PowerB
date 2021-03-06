# PowerB - The most customizable Discord bot
> ## **Advantages**
> - One code style (*snake-case*)
> - Slash commands API
> - Easy to use
> - Easy to customize
> - Easy to add functions
> - Unique and convenient system of functions
> - Demo-files and ready-to-use functions
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
@slash.slash(name="help",
             description="Print list of commands in pm")
async def help (ctx):
    # your function
    pass
```
**Where:**
> name =

Command to trigger fuinction

> .. pass

Your function structure

**Example:**

```python
@slash.slash(name="hello",
             description="Hello World!")
async def hello (ctx):
    await ctx.send('World!')
```
When user types */hello* (/ - prefix for slash commands) bot will reply with message *World!*

Also you can use **checks for admin** (*tools/checks.py*):
```python
if not is_admin(user):
    #..
    pass

# or with notify (only async)

if not await is_admin_notify(ctx):
    #..
    pass
```
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
> - on_member_join
> - on_voice_state_update
