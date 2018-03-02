ruser is a user account manager for PRAW.

## Usage:

Run ruser as its own script to manage accounts. 

To import ruser into your script, put the following.

```python
import ruser

ruser.setUser('USERNAME') # must be exactly as put into ruser script.

reddit = ruser.configure()
```

Run the script. This will replace ruser.configure() with the appropriate lines.

If you want to more tightly pack your package, you can run ruser and enter the command "exp" to export to ruser_min.

The same concepts apply, but you need to import `ruser_min` instead.

