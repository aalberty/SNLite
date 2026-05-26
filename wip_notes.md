# Authentication  
Two tokens required:  
**JSESSIONID** - this can be retrieved from browser dev tools in cookies  
**CSFR Token** - this can be retrieved via BG script (maybe only in scoped apps? The article says only available in private scope, but it's not clear what that means in the context of ServiceNow):

```
var sessionToken = gs.getSession().getSessionToken();
gs.info(sessionToken);
```


# Design notes  
## UI/UX  
Building as a TUI; this eliminates the need to build a new editor to bundle with it since you can just use your already installed and configured editor. The TUI offers an interface for interacting with the instance and viewing the data.

## Commands
- **search** (table, query, format{none, list, form})


rather than taking a 'commands in a repl' approach with commands being API calls, commands should interact with the UI primarily, and the API call should be a result of user interacting with the view in a way that *should* trigger api call (e.g. updating the query)

then your commands become:

- pinned.add(<record>)  
- pinned.remove(<record>)  
- results.sort(field, [a/de]scending)  
- current.setValue(field, val) <-- where current is the currently displayed form  
- list.addColumn(field, position)  
- list.groupBy(field)  
- list.setColumnWidth(field, width)    

# Scattered thoughts  
- 